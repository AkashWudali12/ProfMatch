import requests
from dotenv import dotenv_values
import re
config = dotenv_values(".env")

url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": f"Bearer {config['PERPLEXITY_API_KEY']}"}

def generate_description(name, affiliation):
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": """Generate a short description of the professor 
             based on information about his most recent research. 
             Be concise and to the point. Do not include any other information. 
             Make sure information is accurate."""},
            {
                "role": "user", 
                "content": f"""Generate a short description of {name}, 
                a researcher at {affiliation} based on information about 
                his most recent research. Be concise and to the point. 
                Make sure information is accurate. 
                Make sure the description is compelling and interesting."""
            },
        ],
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30).json()
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            # Remove citation numbers like [1], [2], etc from the content
            content = re.sub(r'\[\d+\]', '', content)
            content = content.replace("**", "")
            return content
        else:
            print(f"Unexpected response: {response}")
            return False, "Error: Invalid API response"
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, "Error: API request failed"