import sys

sys.path.append('...')
sys.path.append('..')
root = '../root/'
import warnings

warnings.filterwarnings("ignore")
import os
import json
from time import time
import openai
import argparse
from util import summarize_react_trial
from agents import ReactReflectAgent, ReactAgent, ReflexionStrategy, Memory_update
import logging


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--result_path', type=str, default=None, help="result save path")
    parser.add_argument('--model_path', type=str, default=None, help="the model path")
    parser.add_argument('--vectordb_name', type=str, default=None, help="the name of the vectordb")
    parser.add_argument('--method', type=str, default=None, help="RAM or R3")

    return parser.parse_args(args)


def RAM(task_name, args, n=3):
    agents = [agent_cls(logger, args, task_name)]
    trial, steps = 0, 0
    correct, incorrect, halted = 0, 0, 0
    for i in range(n):
        if trial == 0:
            exp = True
        else:
            exp = False
        for agent in [a for a in agents if not a.if_task_finished()]:
            if strategy != ReflexionStrategy.NONE:
                obs, fd, pred, step, previous_action, previous_observation, achieve_subgoal = agent.run(reset_exp=exp, reflect_strategy=strategy)
            else:
                obs, fd, pred, step, previous_action, previous_observation, achieve_subgoal = agent.run()

        trial += 1
        steps += step
        c, ic, h = summarize_react_trial(agents)
        correct, incorrect, halted = correct + len(c), incorrect + len(ic), halted + len(h)
        logger.info(f'-----------Finished Trial {trial}, Correct: {correct}, Incorrect: {incorrect}, Halted: {halted}')

        if len(c) > 0 and args.method == 'RAM':
            Memory_update(logger, args, task_name, agent.wrap_env.subgoal, obs, fd, previous_action, previous_observation, achieve_subgoal).add_memory()
            return pred, trial, '', steps, fd

    if args.method == 'RAM':
        Memory_update(logger, args, task_name, agents[0].wrap_env.subgoal, obs, fd, previous_action, previous_observation, achieve_subgoal).add_memory()
        return pred, trial, '', steps, fd


def Task(task_name, args):
    logger.info('\n' + '~~~~~~~~~~' + 'Task: ' + task_name)
    answer[task_name] = {}
    # answer[ID]['Q'] = q
    # answer[ID]['A'] = a
    # answer[ID]['P'], answer[ID]['Time'], answer[ID]['R'], answer[ID]['Eval'] = [], [], [], []
    # answer[ID]['Turn'], answer[ID]['Step'], answer[ID]['Feedback'] = '', '', ''

    time_1 = time()

    prediction, turns, title, step, feedback = RAM(task_name=task_name, args=args, n=3)

    time_2 = time()
    timecost = round(time_2 - time_1, 3)
    while True:
        if '\n' in prediction:
            prediction = prediction.strip().replace('\n', '')
        else:
            break
    print('\n')
    # tag = GPT_assis(q, a, prediction)
    # print(tag)
    # answer[ID]['Eval'].append(tag)
    answer[task_name]['P'] = prediction
    answer[task_name]['Time'] = timecost
    answer[task_name]['Turn'] = turns
    answer[task_name]['Step'] = step
    # answer[ID]['R'].append(title)
    answer[task_name]['Feedback'] = feedback


if __name__ == '__main__':
    args = parse_args()

    strategy: ReflexionStrategy = ReflexionStrategy.REFLEXION
    agent_cls = ReactReflectAgent if strategy != ReflexionStrategy.NONE else ReactAgent

    logger = logging.getLogger()
    logger.setLevel('INFO')
    formatter = logging.Formatter()
    chlr = logging.StreamHandler()
    chlr.setFormatter(formatter)
    chlr.setLevel('INFO')
    if not os.path.exists('./log'):
        os.makedirs('./log')
    fhlr = logging.FileHandler('./log/' + 'Crafter_32K_' + args.method + '.log')
    fhlr.setFormatter(formatter)
    logger.addHandler(chlr)
    logger.addHandler(fhlr)

    #
    task_list = ['collect_coal', 'collect_diamond', 'collect_drink', 'collect_iron', 'collect_sapling', 'collect_stone',
                 'collect_wood', 'make_iron_pickaxe', 'make_iron_sword',
                 'make_stone_pickaxe', 'make_stone_sword', 'make_wood_pickaxe', 'make_wood_sword', 'place_furnace',
                 'place_plant', 'place_stone', 'place_table']

    path = args.result_path

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    try:
        with open(path, 'r') as f:
            answer = json.loads(f.read())
    except:
        answer = {}

    for task in task_list:
        Task(task, args)
        with open(path, 'w') as g:
            g.write(json.dumps(answer))
