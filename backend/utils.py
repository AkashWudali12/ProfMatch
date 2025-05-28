from models import Professor
import logging
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from universities import NAME_TO_ABBR
from pprint import pprint
from supabase_client import get_professors

import os 
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

model = SentenceTransformer("all-MiniLM-L6-v2")

TOP_K = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

def embed_text(text: str) -> list[float]:
    # add noise to text embeddings 
    embedding = model.encode(text)
    return embedding.tolist()  # Convert numpy array to Python list

def vector_search(query: str, school: str, resume_embedding: list[float], previous_professors: list[str]) -> list[Professor]:
    query_vector = embed_text(query)

    logger.info(f"Query: {query}")
    logger.info(f"School: {school}")
    logger.info(f"Query vector: {query_vector}")
    logger.info(f"Namespace: {NAME_TO_ABBR[school]}")
    logger.info(f"Previous professors: {previous_professors}")

    # use resume embedding to rerank professors
    response = index.query(
        namespace=NAME_TO_ABBR[school],
        top_k=TOP_K,
        include_metadata=True,
        vector=query_vector,
        filter={"uuid": {"$nin": previous_professors}}  # Exclude previous professors by UUID
    )

    logger.info("Response: ")
    pprint(response)

    # get uuids from response
    uuids = [hit["id"] for hit in response["matches"]]

    logger.info(f"Found {len(uuids)} professors")
    logger.info(f"UUIDs: {uuids}")

    # list of uuids of professors
    return uuids

def rerank_professors(professor_ids: list[str]) -> list[Professor]:
    print("Got professor ids: ", professor_ids)

    return get_professors(professor_ids)