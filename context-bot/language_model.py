from haystack.nodes import BM25Retriever
from haystack import Pipeline, Document
from haystack.nodes import PromptNode, PromptTemplate
from haystack.nodes import TransformersSummarizer
from util import build_doc_store


def query_model(query):
    lfqa_prompt = PromptTemplate(
        name="lfqa",
        prompt_text="""Synthesize a comprehensive answer from the following text for the given question. 
                                Provide a clear and concise response that summarizes the key points and information presented in the text. 
                                Your answer should be in your own words and be no longer than 50 words. 
                                \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    )

    document_store=build_doc_store()
    retriever = BM25Retriever(document_store=document_store)
    prompt_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=lfqa_prompt, model_kwargs={"model_max_length" : 1024})

    docs =retriever.retrieve(query=query)
    #summary = summarizer.predict(documents=docs)
    #small_docs = [Document(content=doc.meta["summary"]) for doc in summary]
    output = prompt_node(query=query, documents=docs, debug=False)

    return output[0]

if __name__=="__main__":
    query = "How do I enable segment replication"
    print(f"\n\nResults: \n{query_model(query)}")