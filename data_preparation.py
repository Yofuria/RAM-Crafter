import os
import argparse
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import chromadb


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--vectordb_name', type=str, default=None, help="the name of vectordb")

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()
    embeddings = SentenceTransformerEmbeddings(
        model_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model/all-MiniLM-L6-v2'),
        model_kwargs={"device": "cuda"})
    chroma = chromadb.PersistentClient(
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database/', args.vectordb_name))

    collection = chroma.create_collection("crafter")
