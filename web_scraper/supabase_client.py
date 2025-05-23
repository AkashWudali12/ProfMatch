from dotenv import dotenv_values
from supabase import create_client, Client
import re

config = dotenv_values(".env")

supabase: Client = create_client(
    config["SUPABASE_URL"],
    config["SUPABASE_KEY"],
)

def insert_professor(school: str, name: str, email: str, href: str):
    """
    Insert a professor into the database if they don't already exist.
    """
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
    
    # Check if professor already exists with same name components
    response = supabase.table("professors").select("*").eq("first_name", first_name)
    
    if middle_name_initial:
        response = response.eq("middle_name_initial", middle_name_initial)
    
    response = response.eq("last_name", last_name).execute()
    
    # Only insert if no match was found
    if len(response.data) == 0:
        supabase.table("professors").insert({
            "university": school,
            "first_name": first_name,
            "middle_name_initial": middle_name_initial,
            "last_name": last_name,
            "serves": 0,
            "email": email,
            "gs_link": href,
        }).execute()
        print(f"Inserted professor: {name}")
    else:
        print(f"Professor already exists: {name}")
