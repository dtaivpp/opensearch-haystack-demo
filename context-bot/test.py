from ingest import ingest_docs
from language_model import query_model

tests = [
  #3.7142857142857144
  {
    "ingestion": {
      "split_length": 100,
      "split_overlap": 20
    }
  },
  # 3.4285714285714284
  {
    "ingestion": {
      "split_length": 100,
      "split_overlap": 40
    }
  }, 
  # 3.2
  {
    "ingestion": {
      "split_length": 200,
      "split_overlap": 20
    }
  },
  #3.1
  {
    "ingestion": {
      "split_length": 200,
      "split_overlap": 40
    }
  }
]


def query_set(query_function):
  questions = [
    "How can I enable segment replication?",
    "What is OpenSearch?",
    "Why should I use OpenSearch?",
    "Is OpenSearch open source?",
    "What is the relationship between OpenSearch and Elasticsearch?",
    "Which endpoint is used to ingest into OpenSearch",
    "What is the default port for Dashboards?"
  ]

  results = {"raw_results": []}
  agg_score = 0
  for query in questions:
    answer = query_function(query)
    rating = int(input(f"""On a 1-5 scale where 5 is completely answers the question
            \nand a 1 is does not answer the question
            \nrate this response to the question:
            \nQuestion: {query}
            \nResponse: {answer}
            """))
    results["raw_results"].append({
      "question": query, 
      "answer": answer, 
      "rating": rating
    })
    agg_score += rating
  
  results.update({"score": agg_score / len(questions)})
  return results


def bayesian_optomize():
  final = []
  for test in tests:
    ingest_docs(**test['ingestion'])
    results = query_set(query_model)
    print(f"Test Score: {results['score']}")
    test.update(**results)
    final.append(test)


if __name__=="__main__":
  bayesian_optomize()