import os

import requests

def run_task(system: str, user: str) -> str:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": user}
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]