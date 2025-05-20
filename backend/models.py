from pydantic import BaseModel

class Professor(BaseModel):
    id: int
    uuid: str
    name: str
    school: str
    description: str
    gscholar: str
    email_subject: str
    email_body: str
    email_address: str

class Response(BaseModel):
    professors: list[Professor]

class PromptRequest(BaseModel):
    prompt: str
    school: str
    resume_embedding: list[float]

class RerunRequest(BaseModel):
    prompt_embedding: list[float]
    previous_professors: list[str] # list of uuids
    school: str
    resume_embedding: list[float]