from pinecone import Pinecone
from dotenv import dotenv_values

config = dotenv_values(".env")

pc = Pinecone(api_key=config["PINECONE_API_KEY"])
index = pc.Index(config["PINECONE_INDEX"])

def upsert_professor(vectors, namespace):

    """
    Upsert professor data to Pinecone with vector embedding and metadata.
    
    Args:
        vectors: List of dictionaries with structure: {id=uuid, values=embedding, metadata=metadata}
        embedding: List of floats representing the professor's embedding
        namespace: Namespace to store the data in
        metadata: Dictionary containing professor metadata
        uuid: Unique identifier for the professor
    """
    print(f"[Pinecone Client] Inserting {len(vectors)} vectors into {namespace}")
    try:
        index.upsert(
            vectors=vectors,
            namespace=namespace
        )
        print(f"[Pinecone Client] Success")
    except Exception as e:
        print(f"[Pinecone Client] Failed with Exception: {str(e)}")

def search_professor(query):
    return index.query(query)