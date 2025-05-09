from fastapi import FastAPI
from pydantic import BaseModel
from models import Response, PromptRequest
from utils import vector_search, rerank_professors
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_professors")
def get_professors(request: PromptRequest):
    prompt = request.prompt
    school = request.school
    time.sleep(1.5)
    professors = vector_search(prompt, school)
    professors = rerank_professors(professors)
    
    return Response(
        professors=professors
    )