import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": f"Bearer {config['PERPLEXITY_API_KEY']}"}

def valid_researcher(name, affiliation):
    print(f"Verifying {name} with affiliation {affiliation}")
    researcher_query = f"Is {name} currently a researcher, meaning is {name} primarily publishing research papers?"
    retired_query = f"Is {name}, researcher at {affiliation}, not retired, and not a professor emeritus?"
    affiliation_query = f"Is {name} a researcher affiliated with {affiliation}?"
    celebrity_query = f"Is {name}, researcher at {affiliation}, not a celebrity researcher. Only say No if they are extremely well known by the general public."
    willingness_query = f"Would {name}, researcher at {affiliation}, be potentially willing to mentor or work with undergraduate students?"

    for query in [researcher_query, retired_query, willingness_query, celebrity_query, affiliation_query]:
        payload = { 
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Be precise and concise. Only respond with Yes or No."},
                {"role": "user", "content": query},
            ],
            "response_format": {
                "type": "regex",
                "regex": {"regex": r"Yes|No"},
            },
        }
        response = requests.post(url, headers=headers, json=payload).json()
        # print("--------------------------------")   
        # print("Raw response:")
        # print(response)
        # print("--------------------------------")
        if "error" in response:
            print(f"Error: {response['error']}")
            return False
        result = response["choices"][0]["message"]["content"]
        print("--------------------------------")
        print(f"Query: {query}")
        print(f"Result: {result}")
        print("--------------------------------")
        if result == "No":
            return False
    return True