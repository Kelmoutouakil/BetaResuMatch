import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Define index name
index_name = "job-matching"

# Check if the index exists, and create it if it doesn't
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Adjust the dimension based on your embeddings
        metric="cosine",  # Adjust the metric as needed
        spec=ServerlessSpec(
            cloud="aws",  # or "aws" if you prefer
            region="us-east-1"  # Adjust the region as needed
        )
    )
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")

# Connect to the index
index = pc.Index(index_name)

# Initialize the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # This is the embedding model

# Your existing code for processing and embedding data goes here