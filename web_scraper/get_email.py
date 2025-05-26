import requests
from dotenv import dotenv_values
import re

config = dotenv_values(".env")

url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": f"Bearer {config['PERPLEXITY_API_KEY']}"}

def get_email(name, affiliation):
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Look for the email of researchers in faculty directories for universities. Find actual emails, not placeholders."},
            {"role": "user", "content": f"Find the email of {name} at {affiliation}. If you can't find their exact email, respond with 'Email not found'."},
        ],
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30).json()
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            # Extract email address with regex
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.edu', content)
            if email_match:
                return True, email_match.group(0)  # Return just the matched email
            else:
                return False, "No .edu email found in response"
        else:
            print(f"Unexpected response: {response}")
            return False, "Error: Invalid API response"
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, "Error: API request failed"