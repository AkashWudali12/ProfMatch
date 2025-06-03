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
    # Get all matching professors and order by serves count
    # response = supabase.table("professors").select("*").in_("id", uuids).order("serves").execute()

    response = supabase.table("professors").select("*").in_("id", uuids).execute()
    print("Response: ", response)
    
    # Take only the first 10 least served professors
    professors_to_use = response.data[:10]
    to_ret = []
    
    for i, prof in enumerate(professors_to_use):
        to_add = Professor(id=i, 
                        uuid=prof["id"], 
                        name=f"Dr. {prof['first_name']} {prof['middle_name_initial']} {prof['last_name']}", 
                        school=prof["university"], 
                        description=prof["description"], 
                        gscholar=prof["gs_link"], 
                        email_subject=prof["subject_template"], 
                        email_body=prof["body"], 
                        email_address=prof["email"])
        to_ret.append(to_add)
        
        # Increment serves count only for the selected professors
        supabase.table("professors").update({"serves": prof["serves"] + 1}).eq("id", prof["id"]).execute()
    
    print(f"[Supabase Client] Found {len(to_ret)} professors from a pool of {len(response.data)}")
    return to_ret