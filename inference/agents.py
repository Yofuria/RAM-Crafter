import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gym
from typing import List
from enum import Enum
import tiktoken
from langchain.prompts import PromptTemplate
from llm import AnyOpenAILLM, get_similarity_encoder, get_vectordb, get_model
from prompts import reflect_prompt, react_agent_prompt, feedback_agent_prompt, react_reflect_agent_prompt
from prompts import REFLECTION_HEADER, LAST_TRIAL_HEADER, REFLECTION_AFTER_LAST_TRIAL_HEADER
from fewshots import CRAFTER_SAMPLE, CRAFTER_REFLECTIONS, CRAFTER_FEEDBACK
import openai
import logging
import argparse
from craft import craft_env



class ReflexionStrategy(Enum):
    """
    NONE: No reflection
    LAST_ATTEMPT: Use last reasoning trace in context
    REFLEXION: Apply inference to the next reasoning trace
    LAST_ATTEMPT_AND_REFLEXION: Use last reasoning trace in context and apply inference to the next reasoning trace
    """
    NONE = 'base'
    LAST_ATTEMPT = 'last_trial'
    REFLEXION = 'inference'
    LAST_ATTEMPT_AND_REFLEXION = 'last_trial_and_reflexion'


class Memory_update:
    def __init__(self,
                 logger: logging.Logger,
                 args: argparse.Namespace,
                 task: str,
                 subgoals: list,
                 observation: list,
                 hfeedback: str,
                 pre_action: list,
                 pre_observation: list,
                 ach_subgoal: list,
                 llm: AnyOpenAILLM = AnyOpenAILLM(
                     temperature=0,
                     max_tokens=100,
                     model_name="gpt-3.5-turbo",
                     model_kwargs={"stop": "\n"},
                     # openai_api_key=os.environ['OPENAI_API_KEY']
                 ),
                 sim_encoder=get_similarity_encoder(),
                 ) -> None:
        self.logger = logger
        self.args = args
        self.task = task
        self.subgoals = subgoals
        self.pre_action = pre_action
        self.pre_observation = pre_observation
        self.ach_subgoal = ach_subgoal
        self.llm = llm
        self.retriever = get_vectordb(df_collection_name='crafter',
                                      df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           'database',
                                                           args.vectordb_name))[0]
        self.collection = get_vectordb(df_collection_name='crafter',
                                       df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            'database',
                                                            args.vectordb_name))[1]
        self.vectordb = get_vectordb(df_collection_name='crafter',
                                     df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                          'database',
                                                          args.vectordb_name))[2]
        self.observe = observation
        self.hfeedback = hfeedback
        self.mem = ''
        self.enc = tiktoken.encoding_for_model("text-davinci-003")
        self.sim_encoder = sim_encoder

    def add_memory(self):
        print('--------------------------Mem upd----------------------------')
        self.mem = 'The sequence of {} is '.format(self.task)
        for action in self.subgoals:
            self.mem += 'do {} times to {}, '.format(str(action[1]), action[0])
        self.collection.add(
            documents=[self.mem],
            metadatas=[{"source": "crafter"}],
            ids=["id_" + self.task])

        if len(self.pre_action) == len(self.pre_observation) and len(self.pre_observation) == len(self.ach_subgoal):
            for i in range(len(self.pre_action)):
                mem_achieve_subgoaol = ''
                mem_achieve_subgoaol += 'Based on the observation \'{}\', the sequence of actions to complete \'{}\' is '.format(
                    self.pre_observation[i], self.ach_subgoal[i])
                for act in self.pre_action[i]:
                    mem_achieve_subgoaol += '{}, '.format(act)

                print(mem_achieve_subgoaol)
                self.collection.add(
                    documents=[mem_achieve_subgoaol],
                    metadatas=[{"source": "crafter"}],
                    ids=["id_" + self.ach_subgoal[i] + self.pre_observation[i]])


class ReactAgent:
    def __init__(self,
                 logger: logging.Logger,
                 args: argparse.Namespace,
                 task: str,
                 max_steps: int = 3,
                 agent_prompt: PromptTemplate = react_agent_prompt,
                 feedback_prompt: PromptTemplate = feedback_agent_prompt,
                 interact_llm: AnyOpenAILLM = AnyOpenAILLM(
                     temperature=0,
                     max_tokens=100,
                     model_name="gpt-4",
                     model_kwargs={"stop": "\n"},
                     # openai_api_key=os.environ['OPENAI_API_KEY']
                 ),
                 sim_encoder=get_similarity_encoder()
                 ) -> None:
        self.logger = logger
        self.args = args
        self.task = task
        env = gym.make("smartplay:Crafter-v0")
        self.wrap_env = craft_env.WrapEnv(env)
        self.answer = ''
        self.max_steps = max_steps
        self.agent_prompt = agent_prompt
        self.react_examples = CRAFTER_SAMPLE
        self.feedback_examples = CRAFTER_FEEDBACK
        self.interact_llm = interact_llm
        self.feedback_prompt = feedback_prompt
        self.llm = get_model(df_new_token=8000, model=args.model_path)
        self.enc = tiktoken.encoding_for_model("text-davinci-003")
        self.retriever = get_vectordb(df_collection_name='crafter',
                                      df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           'database',
                                                           args.vectordb_name))[0]
        self.collection = get_vectordb(df_collection_name='crafter',
                                       df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            'database',
                                                            args.vectordb_name))[1]
        self.sim_encoder = sim_encoder
        self.__reset_agent()
        self.__reset_temporal_mem()
        self.wrap_env.set_task(self.task)
        self.previous_action = []
        self.previous_observation = []
        self.achieve_subgoal = []

    def run(self, reset_exp, reset_agent=True) -> None:
        if reset_agent:
            self.__reset_agent()
        if reset_exp:
            self.__reset_temporal_mem()

        while not self.is_halted() and not self.is_finished():
            self.step()

    def step(self) -> None:
        # Note previous action
        if not self.wrap_env.previous_action:
            self.wrap_env.previous_observation = str(self.wrap_env.steps(['0.Noop'])[-1])

        no = str(self.step_n)

        # Think
        if self.scratchpad == '':
            self.scratchpad += str(self.wrap_env.steps(['0.Noop'])[-1])

        self.scratchpad += f'\nThought {self.step_n}:'
        raw_thought = self.prompt_agent().split('Action ' + no + ':')[0]
        self.scratchpad += ' ' + raw_thought
        self.logger.info(self.scratchpad.split('\n')[-1])

        # Retrieval
        try:
            relevant_subgoal = self.retriever.get_relevant_documents(self.task)
            doc_details = relevant_subgoal[0].to_json()['kwargs']
            text = doc_details['page_content']

            if len(self.enc.encode(text)) > 3000:
                relevant_subgoal[0].page_content = text[:3000]

            self.scratchpad += relevant_subgoal[0].page_content
        except Exception as e:
            self.logger.info(e)

        # Act
        self.scratchpad += f'\nAction {self.step_n}:'
        raw_action = self.prompt_agent().split(']')[0] + ']'
        self.scratchpad += ' ' + raw_action
        try:
            action = raw_action.split('[')
            print('action: ', action)
            action_type, argument = action[0], action[1].strip(']')
        except:
            action_type, argument = 'Act', raw_action
        self.logger.info(self.scratchpad.split('\n')[-1])

        # Observe
        self.scratchpad += f'\nObservation {self.step_n}: '
        if action_type == 'Finish':
            self.answer = argument

            signal = self.if_task_finished()

            if signal:
                self.scratchpad += ' Task is completed.'
            else:
                self.scratchpad += ' Task is not completed.'

            self.finished = True
            self.step_n += 1
            return

        if action_type == 'Act':
            try:
                executable_actions = {0: 'Noop', 1: 'Move West', 2: 'Move East', 3: 'Move North', 4: 'Move South',
                                      5: 'Do',
                                      6: 'Sleep', 7: 'Place Stone',
                                      8: 'Place Table', 9: 'Place Furnace', 10: 'Place Plant', 11: 'Make Wood Pickaxe',
                                      12: 'Make Stone Pickaxe', 13: 'Make Iron Pickaxe', 14: 'Make Wood Sword',
                                      15: 'Make Stone Sword',
                                      16: 'Make Iron Sword'}

                argument = argument.split(', ')
                print(argument)

                if len(argument) != 3 or not all(
                        items in executable_actions.items() for items in {int(argument[1]): argument[0]}.items()):
                    self.scratchpad += 'Invalid Act format. Vaild format is <action, number, times>.'
                else:
                    action_list = []
                    for _ in range(int(argument[2])):
                        action_list.append(argument[1] + '.' + argument[0])

                    achievement = self.wrap_env.achievements

                    obs = str(self.wrap_env.steps(actions_list=action_list)[-1])

                    for key in achievement.keys():  # if two subgoal achieve together?
                        if self.wrap_env.achievements[key] != achievement[key]:
                            self.achieve_subgoal.append(key)
                            self.previous_action.append(self.wrap_env.previous_action)
                            self.previous_observation.append(self.wrap_env.previous_observation)
                            self.wrap_env.previous_action = []
                            self.wrap_env.previous_observation = ''
                            break

                    if self.args.method == 'RAM':
                        if obs in self.observe:
                            feedback = self.get_feedback(observation=obs)  # when to get feedback
                            self.hfeedback += feedback
                            self.scratchpad += format_step(feedback)
                            self.answer = feedback
                        else:
                            self.observe.append(obs)
                            self.scratchpad += format_step(obs)
                            self.answer = obs

                    signal = self.if_task_finished()

                    if signal:
                        self.scratchpad += ' Task is completed.'
                        self.finished = True
                        self.step_n += 1

            except Exception as e:
                self.logger.info(e)
                self.scratchpad += f'Could not execute this action, please try again.'

        else:
            self.scratchpad += 'Invalid Action. Valid Actions are Act[<action>] and Finish[<answer>].'

        self.logger.info(self.scratchpad.split('\n')[-1])

        self.step_n += 1

    def prompt_agent(self) -> str:
        return format_step(self.llm(self._build_agent_prompt()))
        # prompt = [{"role": "user", "content": self._build_agent_prompt()}]
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=prompt,
        #     max_tokens=100
        # )
        #
        # return format_step(response.choices[0].message.content)

    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
            examples=self.react_examples,
            task=self.task,
            get_observation=self.scratchpad)

    def is_finished(self) -> bool:  # if llm finished
        return self.finished

    def if_task_finished(self):  # how to get the progress if task finished
        return self.wrap_env.done

    def is_halted(self) -> bool:  ## exceed max try/ exceed context wind + not finish
        return ((self.step_n > self.max_steps) or (
                len(self.enc.encode(self._build_agent_prompt())) > 3896)) and not self.finished

    def __reset_agent(self) -> None:
        self.step_n = 1
        self.finished = False
        self.scratchpad: str = ''

    def __reset_temporal_mem(self) -> None:
        self.observe: list = []
        self.hfeedback: str = ''

    def get_feedback(self, observation) -> str:
        fdo = format_step(self.interact_llm(self._build_feedback_prompt(observation=observation)))
        self.logger.info('***********original feedback:' + fdo)
        # fd = exempt_label(fdo, self.key, self.sim_encoder)
        fd = fdo
        self.logger.info('***********feedback:' + fd)
        self.logger.info('***********subgoals:' + str(self.wrap_env.achievements) + '\n')

        return fd

    def _build_feedback_prompt(self, observation) -> str:
        subgoals = ''
        for goal in self.wrap_env.subgoal:
            subgoals += 'Subgoal: {}, the number of times Student need to complete: {}, the number of times Student have already completed: {}'.format(
                goal[0], str(goal[1]), str(self.wrap_env.achievements[goal[0]]))
        return self.feedback_prompt.format(
            examples=self.feedback_examples,
            task=self.task,
            subgoals=subgoals,
            scratchpad=self.scratchpad,
            observation=observation)


class ReactReflectAgent(ReactAgent):
    def __init__(self,
                 logger: logging.Logger,
                 args: argparse.Namespace,
                 task: str,
                 max_steps: int = 3,
                 agent_prompt: PromptTemplate = react_reflect_agent_prompt,
                 feedback_prompt: PromptTemplate = feedback_agent_prompt,
                 reflect_prompt: PromptTemplate = reflect_prompt,
                 interact_llm: AnyOpenAILLM = AnyOpenAILLM(
                     temperature=0,
                     max_tokens=100,
                     model_name="gpt-4",
                     model_kwargs={"stop": "\n"},
                     # openai_api_key=os.environ['OPENAI_API_KEY']
                     ),
                 sim_encoder=get_similarity_encoder()
                 ) -> None:

        super().__init__(logger, args, task, max_steps, agent_prompt, feedback_prompt, interact_llm,
                         sim_encoder)
        self.reflect_llm = get_model(df_new_token=100, model=args.model_path)
        self.reflect_prompt = reflect_prompt
        self.reflect_examples = CRAFTER_REFLECTIONS
        self.reflections: List[str] = []
        self.reflections_str: str = ''

    def run(self, reset_exp, reset_agent=True,
            reflect_strategy: ReflexionStrategy = ReflexionStrategy.REFLEXION) -> None:

        if self.is_finished() or self.is_halted():
            self.reflect(reflect_strategy)

        ReactAgent.run(self, reset_exp, reset_agent)

        return self.observe, self.hfeedback, self.answer, self.step_n, self.previous_action, self.previous_observation, self.achieve_subgoal

    def reflect(self, strategy: ReflexionStrategy) -> None:
        self.logger.info('-----------Reflecting-----------')
        if strategy == ReflexionStrategy.LAST_ATTEMPT:
            self.reflections = [self.scratchpad]
            self.reflections_str = format_last_attempt(self.task, self.reflections[0])
        elif strategy == ReflexionStrategy.REFLEXION:
            self.reflections += [self.prompt_reflection()]
            self.reflections_str = format_reflections(self.reflections)
        elif strategy == ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION:
            self.reflections_str = format_last_attempt(self.task, self.scratchpad)
            self.reflections = [self.prompt_reflection()]
            self.reflections_str += format_reflections(self.reflections, header=REFLECTION_AFTER_LAST_TRIAL_HEADER)
        else:
            raise NotImplementedError(f'Unknown reflection strategy: {strategy}')
        self.logger.info(self.reflections_str)

    def prompt_reflection(self) -> str:
        return format_step(self.reflect_llm(self._build_reflection_prompt()))
        # prompt = [{"role": "user", "content": self._build_reflection_prompt()}]
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=prompt,
        #     max_tokens=100
        # )
        #
        # return format_step(response.choices[0].message.content)

    def _build_reflection_prompt(self) -> str:
        return self.reflect_prompt.format(
            examples=self.reflect_examples,
            task=self.task,
            scratchpad=truncate_scratchpad(self.scratchpad, tokenizer=self.enc))

    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
            examples=self.react_examples,
            task=self.task,
            reflections=self.reflections_str,
            get_observation=self.scratchpad)


### String Stuff ###
gpt2_enc = tiktoken.encoding_for_model("text-davinci-003")


def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n\n', ' ').replace('\n', ' ').replace('\'', '')


def format_reflections(reflections: List[str], header: str = REFLECTION_HEADER) -> str:
    if reflections == []:
        return ''
    else:
        return header + 'Reflections:\n- ' + '\n- '.join([r.strip() for r in reflections])


def format_last_attempt(task: str,
                        scratchpad: str,
                        header: str = LAST_TRIAL_HEADER):
    return header + f'Task: {task}\n' + truncate_scratchpad(scratchpad, tokenizer=gpt2_enc).strip(
        '\n').strip() + '\n(END PREVIOUS TRIAL)\n'


def truncate_scratchpad(scratchpad: str, n_tokens: int = 1600, tokenizer=gpt2_enc) -> str:
    lines = scratchpad.split('\n')
    observations = filter(lambda x: x.startswith('Observation'), lines)
    observations_by_tokens = sorted(observations, key=lambda x: len(tokenizer.encode(x)))
    while len(gpt2_enc.encode('\n'.join(lines))) > n_tokens:
        largest_observation = observations_by_tokens.pop(-1)
        ind = lines.index(largest_observation)
        lines[ind] = largest_observation.split(':')[0] + ': [truncated wikipedia excerpt]'
    return '\n'.join(lines)
