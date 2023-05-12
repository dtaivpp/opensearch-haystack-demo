import argparse
from language_model import query_model
from ingest import ingest_docs

def main(args):
    if args.ingest: 
        ingest_docs()
    
    query_models = {
        'gpt': 'gpt-3.5-turbo', 
        'flan': 'google/flan-t5-large'
    }
    
    if args.question: 
        response = query_model(model_name=query_models.get(args.model), query=args.question)
        print(response)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', 
        '--ingest',
        action='store_true',
        help="Use this to ingest documents from ./data/<documents>.json into OpenSearch")
    

    parser.add_argument(
        '-m', 
        '--model', 
        choices=['flan', 'gpt'], 
        help="Which model to query with")

    parser.add_argument(
        '-q', 
        '--question', 
        type=str, 
        help="What you'd like to ask")
    
    args = parser.parse_args()
    main(args)