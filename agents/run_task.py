import os
import time
import requests

def run_task(system: str, user: str, max_retries: int = 3) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openrouter/free", 
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ]
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            # If successful and 'choices' exists, return the content
            if response.status_code == 200 and "choices" in response_data:
                return response_data["choices"][0]["message"]["content"]
            
            # Extract the specific OpenRouter error message
            error_msg = response_data.get("error", {}).get("message", "Unknown API Error")
            print(f"API Error (Attempt {attempt + 1}/{max_retries}): Status {response.status_code} - {error_msg}")
            
        except Exception as e:
            print(f"Request failed (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            error_msg = str(e)
            
        # If it's the last attempt, raise the exception so the node fails gracefully
        if attempt == max_retries - 1:
            raise Exception(f"run_task failed after {max_retries} attempts. Last error: {error_msg}")
        
        # Exponential backoff: Wait 2s, then 4s before retrying
        time.sleep(2 ** (attempt + 1))