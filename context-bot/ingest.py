import json
from util import build_doc_store
from haystack.nodes import PreProcessor
from os import listdir
from os.path import isfile, join

import urllib3
urllib3.disable_warnings()


def read_json(basepath):
    """Process already formatted JSON"""
    files = [join(basepath, f) for f in listdir(basepath) if isfile(join(basepath, f))]
    data = []
    for file in files:
        print(f"Ingesting: {file}")
        with open(file, 'r') as f:
            data.extend(json.load(f))
    return data


def format_doc(doc):
    """Normalize doc to haystack format"""
    content = doc.pop('content')
    return {
      'content': content, 
      'meta': {**doc}
    }


def normalize_doc_list(document_list):
    return [ format_doc(doc) for doc in document_list]


def preprocess_data(data, preprocessor):
    return preprocessor.process(data)


def preprocessor_builder(split_length, split_overlap):
    return PreProcessor (
        clean_empty_lines=True, 
        split_by='word',
        split_respect_sentence_boundary=True,
        split_length=split_length,
        split_overlap=split_overlap
    )


def index_docs(docs):
    """Push docs to docstore"""
    docstore = build_doc_store()
    docstore.write_documents(docs)


def ingest_docs(split_length=250, split_overlap=30, basepath="data"):
    """Read and normalize doc json before writing them to OpenSearch"""
    raw_docs = read_json(basepath)
    normalized = normalize_doc_list(raw_docs)
    preprocessed = preprocess_data(
                        normalized, 
                        preprocessor_builder(
                            split_length, 
                            split_overlap))
    
    index_docs(preprocessed)


if __name__=="__main__":
    ingest_docs(split_length=150, split_overlap=20)