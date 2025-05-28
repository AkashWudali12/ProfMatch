from fastapi import FastAPI
from pydantic import BaseModel
from models import Response, PromptRequest
from utils import vector_search, rerank_professors
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "http://localhost:4173"   # Production preview (Docker)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_professors")
def get_professors(request: PromptRequest):
    start_time = time.time()    
    prompt = request.prompt
    school = request.school
    previous_professors = request.previous_professors
    logger.info(f"Prompt: {prompt}, School: {school}")
    embedding = request.resume_embedding
    professors = vector_search(prompt, school, embedding, previous_professors)  # returns list of uuids
    professors = rerank_professors(professors)
    end_time = time.time()
    logger.info(f"Time taken: {end_time - start_time} seconds")
    
    return Response(
        professors=professors
    )