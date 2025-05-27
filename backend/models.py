from pydantic import BaseModel

class Professor(BaseModel):
    id: int
    uuid: str
    name: str
    school: str
    description: str
    gscholar: str
    email_subject: str | None
    email_body: str | None
    email_address: str | None

class Response(BaseModel):
    professors: list[Professor]

class PromptRequest(BaseModel):
    prompt: str
    school: str
    resume_embedding: list[float]
    previous_professors: list[str] # list of uuids

class RerunRequest(BaseModel):
    prompt_embedding: list[float]
    previous_professors: list[str] # list of uuids
    school: str
    resume_embedding: list[float]