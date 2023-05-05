from haystack.document_stores import OpenSearchDocumentStore

import urllib3
urllib3.disable_warnings()

def _opensearch_kwargs():
  return {
      'host': "localhost",
      'port': 9200,
      'verify_certs': False,
      'scheme': "https",
      'username': "admin",
      'password': "admin",
  }


def build_doc_store() -> OpenSearchDocumentStore:
  return OpenSearchDocumentStore(
      **_opensearch_kwargs()
    )

