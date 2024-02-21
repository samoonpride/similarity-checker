import os
import asyncio
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}


async def perform_inference(data):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)  # Serialize data to JSON
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def send_request_to_get_score(text_target, all_texts):
    data = {
        "inputs": {
            "source_sentence": text_target,
            "sentences": all_texts
        }
    }
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(perform_inference(data))
    return results
