<h1 align="center">RAM with Crafter</h1>

## ✏️ Table of Contents

- [⚙ **Installation**](#-installation)
- [🚀 **Quick Start**](#-quick-start)
    - [**Step 1: Prerequisites**](#step-1-prerequisites)
    - [**Step 2: Inference**](#step-2-inference)

## ⚙ Installation

```bash
# clone RAM
git clone https://github.com/Yofuria/RAM-Crafter.git
cd RAM-Crafter_main

#create conda env
conda create -n RAM
conda activate RAM

# install package
pip install -r requirements.txt

# export openai key
export OPENAI_API_KEY="[your_openai_api_key]"
```

## 🚀 Quick Start

### Step 1: Prerequisites

In this work, we use **all-MinLM-L6-v2** to construct database, and use **bert-base-nli-mean-tokens** to calculate the
semantic similarity of feedback and ground truth.

You can download these two models from [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
and [bert-base-nli-mean-tokens](https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens). You should put
all-MiniLM-L6-v2 and bert-base-nli-mean-tokens at the path inference/.

If you want to use other models, you can change them at line 81 and line 88 in inference/llm.py.

### Step 2: Inference

We test LLMs using Python codes under the path inference/ with four methods in our work. We select the method for
evaluation via --method and the specific dataset via --dataset. Let's take FreshQA as an example:

For RAM:

```
python inference/RAM.py --dataset freshqa --result_path ./result/freshqa_ram.json --method RAM --vectordb_name chroma_db --model_path ./model/Llama-2-7b-chat-hf 
```

Open-source models can be downloaded and loaded from models/ by default, you can change the path via --model_path. You
can download
the [LlaMa-2-7B](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf), [LlaMa-2-13B](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf)
and [Vicuna-7B](https://huggingface.co/lmsys/vicuna-7b-v1.5) from Hugginig Face. For Vicuna-7B, you should modify prompt
according to instruct tuning. You can also determine the output result through --result_path.

The implementation parameters of models and metrics are in default settings. All the experiments can be run on 1 A100
each with 80G GPU