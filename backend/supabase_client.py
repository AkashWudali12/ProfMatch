from supabase import create_client, Client
import re
from pprint import pprint
from models import Professor
import os
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

def get_professors(uuids: list[str]) -> list[Professor]:
    response = supabase.table("professors").select("*").in_("id", uuids).execute()  
    to_ret = [Professor(id=i, 
                        uuid=prof["id"], 
                        name=f"Dr. {prof['first_name']} {prof['middle_name_initial']} {prof['last_name']}", 
                        school=prof["university"], 
                        description=prof["description"], 
                        gscholar=prof["gs_link"], 
                        email_subject=prof["subject_template"], 
                        email_body=prof["body"], 
                        email_address=prof["email"]) for i, prof in enumerate(response.data)]
    print(f"[Supabase Client] Found {len(to_ret)} professors")
    return to_ret