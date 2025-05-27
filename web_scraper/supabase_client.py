from dotenv import dotenv_values
from supabase import create_client, Client
import re
from pprint import pprint

config = dotenv_values(".env")

supabase: Client = create_client(
    config["SUPABASE_URL"],
    config["SUPABASE_KEY"],
)

def get_name(name):
    # Extract first, middle, and last name using regex
    # This handles: 
    # 1. First MI. Last (e.g., "John A. Smith")
    # 2. First Middle Another-Middle Last (e.g., "John Alan Smith-Jones")
    # 3. First Last (e.g., "John Smith")

    # New pattern that captures middle part as group 2
    name_pattern = re.compile(r'^(\w+)\s+(.*)\s+(\S+)$')
    match = name_pattern.search(name)
    
    first_name = ""
    middle_name_initial = ""
    last_name = ""
    
    if match and match.group(2):  # If there's a middle part
        first_name = match.group(1)
        middle_name_initial = match.group(2)
        last_name = match.group(3)
    else:
        # Try simpler pattern for just first and last name
        simple_pattern = re.compile(r'^(\w+)\s+(\S+)$')
        simple_match = simple_pattern.search(name)
        if simple_match:
            first_name = simple_match.group(1)
            last_name = simple_match.group(2)
        else:
            # Fallback: just use the full name
            first_name = name
            last_name = ""

    return first_name, middle_name_initial, last_name

def insert_professor(school: str, name: str, email: str, href: str):
    """
    Insert a professor into the database if they don't already exist.
    """

    first_name, middle_name_initial, last_name = get_name(name)
    
    # Check if professor already exists with same name components
    response = supabase.table("professors").select("*").eq("first_name", first_name)
    
    if middle_name_initial:
        response = response.eq("middle_name_initial", middle_name_initial)
    
    response = response.eq("last_name", last_name).execute()
    
    # Only insert if no match was found
    if len(response.data) == 0:
        response = supabase.table("professors").insert({
            "university": school,
            "first_name": first_name,
            "middle_name_initial": middle_name_initial,
            "last_name": last_name,
            "serves": 0,
            "email": email,
            "gs_link": href,
        }).execute()
        print(f"[Supabase Client] Response for insert_professor:")
        pprint(response)
        if len(response.data) != 0:
            print(f"[Supabase Client] Inserted professor: {name}")
        else:
            print(f"[Supabase Client] Error Inserting Data for {name}")
    else:
        print(f"[Supabase Client] Professor already exists: {name}")

def insert_embedding_text(school, name, embedding_text):
    first_name, middle_name_initial, last_name = get_name(name)
    response = supabase.table("professors").update({
        "embedding_text": embedding_text
    }).match({
        "first_name": first_name,
        "middle_name_initial": middle_name_initial,
        "last_name": last_name,
        "university": school
    }).execute()
    print(f"[Supabase Client] Response for insert_embedding_text:") 
    pprint(response)
    if len(response.data) != 0:
        print(f"[Supabase Client] Updated professor: {name}'s info")
        return response.data[0]["id"]
    else:
        print(f"[Supabase Client] Error Updating Data for {name}")
        return ""

def get_missing_professors():
    # response = supabase.table("professors").select("*").is_("description", "null").eq("added_to_pinecone", False).not_.is_("university", "null").not_.is_("first_name", "null").not_.is_("last_name", "null").not_.is_("email", "null").not_.is_("gs_link", "null").not_.is_("embedding_text", "null").execute()

    # for testing purposes, will not include embedding_text requirement
    response = supabase.table("professors").select("*").is_("description", "null").eq("added_to_pinecone", False).not_.is_("university", "null").not_.is_("first_name", "null").not_.is_("last_name", "null").not_.is_("email", "null").not_.is_("gs_link", "null").execute()
    print(f"[Supabase Client] Response for get_missing_professors:")
    print(len(response.data))
    if len(response.data) != 0:
        print(f"[Supabase Client] Found {len(response.data)} missing professors")
    else:
        print(f"[Supabase Client] No missing professors found")
    return response.data

def update_description(uuid, description):
    response = supabase.table("professors").update({
        "description": description
    }).match({
        "id": uuid
    }).execute()
    print(f"[Supabase Client] Response for update_description:")
    print(len(response.data))
    if len(response.data) != 0:
        print(f"[Supabase Client] Updated description for professor: {uuid}")
    else:
        print(f"[Supabase Client] Error Updating Description for {uuid}")

def add_to_pinecone(uuid):
    response = supabase.table("professors").update({
        "added_to_pinecone": True
    }).match({
        "id": uuid
    }).execute()
    print(f"[Supabase Client] Response for add_to_pinecone:")
    print(len(response.data))
    if len(response.data) != 0:
        print(f"[Supabase Client] Added professor to pinecone: {uuid}")
    else:
        print(f"[Supabase Client] Error Adding Professor to Pinecone: {uuid}")