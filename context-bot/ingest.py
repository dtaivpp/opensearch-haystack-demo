import json
from util import build_doc_store
from haystack.nodes import PreProcessor
from os import listdir
from os.path import isfile, join

import urllib3
urllib3.disable_warnings()

def read_json(basepath="data"):
    files = [join(basepath, f) for f in listdir(basepath) if isfile(join(basepath, f))]
    data = []
    for file in files:
        print(f"Ingesting: {file}")
        with open(file, 'r') as f:
            data.extend(json.load(f))
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
    docstore = build_doc_store()
    docstore.write_documents(docs)


if __name__=="__main__":
    raw_docs = read_json()
    normalized = normalize_docs(raw_docs)
    preprocessed = preprocess_data(normalized)
    ingest_docs(preprocessed)