import os
from haystack.nodes import BM25Retriever
from haystack import Pipeline
from haystack.nodes import PromptNode, PromptTemplate, PromptModel
from util import build_doc_store
from time import time
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPEN_API_KEY')

def query_model(query, model_name="google/flan-t5-large"):
    lfqa_prompt = PromptTemplate(
        """Synthesize a comprehensive answer from the following text for the given question. 
        Provide a clear and concise response that summarizes the 
        key points and information presented in the text. 
        Your answer should be in your own words.
        \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    )

    document_store=build_doc_store()    
    if model_name=="gpt-3.5-turbo":
        retriever = BM25Retriever(document_store=document_store, top_k=5)
        prompt_open_ai = PromptModel(model_name_or_path="gpt-3.5-turbo", api_key=openai_api_key, model_kwargs={"max_tokens": 2048})
        prompt_node = PromptNode(prompt_open_ai, default_prompt_template=lfqa_prompt)
    else:
        retriever = BM25Retriever(document_store=document_store, top_k=2)
        prompt_node = PromptNode(model_name_or_path=model_name, default_prompt_template=lfqa_prompt, model_kwargs={"model_max_length" : 1512})

    pipeline = Pipeline()
    pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipeline.add_node(component=prompt_node, name="Prompt", inputs=["Retriever"])

    output = pipeline.run(query=query)

    return output['results'][0]

if __name__=="__main__":
    query = "How do I enable segment replication"
    start = time()
    print(f"\n\nResults: \n{query_model(query)}")
    end = time()
    print(f"Time Taken: {end - start}")