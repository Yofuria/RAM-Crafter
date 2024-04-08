from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma
import chromadb
from torch import cuda, bfloat16
import transformers
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
import os
import openai




class AnyOpenAILLM:
    def __init__(self, *args, **kwargs):
        # Determine model type from the kwargs
        model_name = kwargs.get('model_name', 'gpt-3.5-turbo')
        if model_name.split('-')[0] == 'text':
            self.model = OpenAI(*args, **kwargs)
            self.model_type = 'completion'
        # else:
        #     self.model = ChatOpenAI(*args, **kwargs)
        #     self.model_type = 'chat'

    def __call__(self, prompt: str):
        prompt = str(prompt)
        prompt = prompt.replace('"', '^')
        while True:
            if '\n' in prompt:
                prompt = prompt.strip().replace('\n', ' ')
            else:
                break
        args = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=args,
            max_tokens=100
        )

        return response.choices[0].message.content


def get_model(df_new_token, model):
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=bfloat16
    )

    model_config = AutoConfig.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(
        model,
        trust_remote_code=True,
        config=model_config,
        # load_in_8bit=True
        quantization_config=bnb_config,
    )  # .half().to(device)
    query_pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        repetition_penalty=1.1,
        max_new_tokens=df_new_token,
        # torch_dtype=torch.float16,
        device_map="auto")
    llm = HuggingFacePipeline(pipeline=query_pipeline)
    return llm


def get_similarity_encoder(
        encode_model=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model/bert-base-nli-mean-tokens')):
    encoder = SentenceTransformer(encode_model)
    return encoder


def get_vectordb(re_no=1, df_collection_name="crafter",
                 df_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database',
                                      'chroma_db'),
                 df_model_name=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model/all-MiniLM-L6-v2')):
    embeddings = SentenceTransformerEmbeddings(model_name=df_model_name)
    chroma = chromadb.PersistentClient(path=df_path)
    collection = chroma.get_collection(df_collection_name)
    vectordb = Chroma(
        client=chroma,
        collection_name=df_collection_name,
        embedding_function=embeddings,
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": re_no, "filter": {
        'source': {'$nin': ['shortmem']}}})  # search_type="similarity_score_threshold", "score_threshold": 1.3,
    return retriever, collection, vectordb
