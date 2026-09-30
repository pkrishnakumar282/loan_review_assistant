import requests

from config import (
    OLLAMA_URL,
    OLLAMA_MODEL
)


def generate_answer(prompt):

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        )

    except requests.exceptions.ConnectionError:

        return (
            "ERROR: Ollama is not running. "
            "Start Ollama and try again."
        )

    except Exception as e:

        return f"ERROR: {str(e)}"