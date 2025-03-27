import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import json

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))


index_name = "job-matching"


if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  
        metric="cosine",  
        spec=ServerlessSpec(
            cloud="aws",  
            region="us-east-1"  
        )
    )
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")


index = pc.Index(index_name)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  
