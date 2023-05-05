import json
from util import build_doc_store
from haystack.nodes import PreProcessor

import urllib3
urllib3.disable_warnings()

def read_json(filename="data/opensearch-docs-and-blogs.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def format_doc(doc):
    content = doc.pop('content')
    return {
      'content': content, 
      'meta': {**doc}
    }


def normalize_docs(document_list):
    return [ format_doc(doc) for doc in document_list]


def preprocess_data(data):
    preprocessor = preprocessor_builder()
    return preprocessor.process(data)


def preprocessor_builder():
    return PreProcessor (
        clean_empty_lines=True, 
        split_by='word',
        split_respect_sentence_boundary=True,
        split_length=300,
        split_overlap=20
    )


def ingest_docs(docs):
    docstore = build_doc_store('1028')
    docstore.write_documents(docs)


if __name__=="__main__":
    raw_docs = read_json()
    normalized = normalize_docs(raw_docs)
    preprocessed = preprocess_data(normalized)
    ingest_docs(preprocessed)