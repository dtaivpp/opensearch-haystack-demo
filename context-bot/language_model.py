import os
from haystack.nodes import BM25Retriever, EmbeddingRetriever, JoinDocuments
from haystack.nodes import PromptNode, PromptTemplate, PromptModel
from haystack import Pipeline
from util import build_doc_store
from time import time
from dotenv import load_dotenv

LFQA_PROMPT = PromptTemplate(
        """Synthesize a comprehensive answer from the following text for the given question. 
        Provide a clear and concise response that summarizes the 
        key points and information presented in the text. 
        Your answer should be in your own words.
        \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    )


load_dotenv()
openai_api_key = os.getenv('OPEN_API_KEY')

config = {
    "model_configs": {
        "gpt-3.5-turbo": {
            "pipeline":
                PromptNode(
                    PromptModel(model_name_or_path="gpt-3.5-turbo", 
                                api_key=openai_api_key, 
                                model_kwargs={"max_tokens": 2048}), 
                    default_prompt_template=LFQA_PROMPT),
            "params": 
                {"top_k": 5}
        },
        "google/flan-t5-large": {
            "pipeline":
                PromptNode(model_name_or_path="google/flan-t5-large", 
                           model_kwargs={"model_max_length" : 1512}, 
                           default_prompt_template=LFQA_PROMPT),
            "params": 
                {"top_k": 2}
        }
    },
    "retreiver_configs":{
        "bm25": [lambda document_store: BM25Retriever(document_store=document_store, top_k=5)],
        "vector": [lambda document_store: EmbeddingRetriever(document_store=document_store, top_k=5)],
        "all": [lambda document_store: BM25Retriever(document_store=document_store, top_k=5),
                lambda document_store: EmbeddingRetriever(document_store=document_store, top_k=5)]
    }
}


def pipeline_run(query, model_name="google/flan-t5-large", retreiver_type="all"):
    pipeline = Pipeline()
    document_store = build_doc_store()
    retreiver_list = config["retreiver_configs"][retreiver_type]
    model = config["model_configs"][model_name]

    join_documents = JoinDocuments(
        join_mode="reciprocal_rank_fusion",
        top_k_join=model["params"]["top_k"]
    )

    # Add retriever/s to pipeline
    index_names = []
    for index, retreiver in enumerate(retreiver_list):
        doc_store = retreiver(document_store)
        pipeline.add_node(component=doc_store, name=str(index), inputs=["Query"])
        index_names.append(str(index))

    # Run join to combine retrieved documents
    pipeline.add_node(component=join_documents, name="JoinDocuments",
              inputs=index_names)

    pipeline.add_node(component=model["pipeline"], name="Prompt", inputs=["JoinDocuments"])
    results = pipeline.run(query=query)
    
    # Run and return results
    return results["results"][0]

if __name__=="__main__":
    query = "What is SSFO and why should I use it"
    start = time()
    print(f"\n\nResults: \n{pipeline_run(query=query, retreiver_type='bm25')}")
    end = time()
    print(f"Time Taken: {end - start}")