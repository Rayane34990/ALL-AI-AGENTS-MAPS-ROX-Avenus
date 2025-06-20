import requests
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal

HF_API = "https://huggingface.co/api/models"

# Helper to parse model metadata

def parse_model(model):
    card_data = model.get('cardData', {})
    return Agent(
        name=model.get('modelId', ''),
        description=model.get('description', card_data.get('summary', '')),
        source='HuggingFace',
        type='',  # To be inferred/classified
        tags=','.join(model.get('tags', [])),
        deployment=','.join(card_data.get('library_name', [])) if card_data.get('library_name') else '',
        license=model.get('license', card_data.get('license', '')),
        repo_link=f"https://huggingface.co/{model.get('modelId', '')}",
        demo_link=card_data.get('demo', ''),
        paper_link=card_data.get('paper', ''),
        last_updated=model.get('lastModified', ''),
        related=','.join(card_data.get('related_models', [])) if card_data.get('related_models') else '',
        rating='',
        install=card_data.get('pip', '')
    )

def insert_agent(agent):
    db = SessionLocal()
    exists = db.query(Agent).filter_by(name=agent.name, source=agent.source).first()
    if not exists:
        db.add(agent)
        db.commit()
    db.close()

def ingest_hf(query="ai", limit=100, max_pages=5, delay=1):
    print(f"Fetching Hugging Face models for query: {query}")
    page = 0
    total = 0
    while page < max_pages:
        params = {'search': query, 'limit': limit, 'full': 'true', 'skip': page * limit}
        resp = requests.get(HF_API, params=params)
        if resp.status_code != 200:
            print(f"Hugging Face API error: {resp.status_code}", resp.text)
            break
        data = resp.json()
        if not data:
            break
        for model in data:
            agent = parse_model(model)
            insert_agent(agent)
            total += 1
        print(f"Page {page+1}: {len(data)} models ingested.")
        if len(data) < limit:
            break
        page += 1
        time.sleep(delay)
    print(f"Hugging Face ingestion complete. Total models: {total}")

if __name__ == "__main__":
    ingest_hf()
