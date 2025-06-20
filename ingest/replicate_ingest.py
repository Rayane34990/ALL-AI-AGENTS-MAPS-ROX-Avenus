# Replicate.com Ingestion Stub
# API: https://replicate.com/api/models (unofficial/public scraping)

import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal  # noqa: E402, F401, F403

REPLICATE_API = "https://replicate.com/api/models"

def parse_model(model):
    return Agent(
        name=model.get('name', ''),
        description=model.get('description', ''),
        source='Replicate',
        type='',
        tags=','.join(model.get('tags', [])),
        deployment='',
        license=model.get('license', ''),
        repo_link=f"https://replicate.com{model.get('url', '')}",
        demo_link='',
        paper_link='',
        last_updated=model.get('updated_at', ''),
        related='',
        rating='',
        install=''
    )

def insert_agent(agent):
    db = SessionLocal()
    exists = db.query(Agent).filter_by(name=agent.name, source=agent.source).first()
    if not exists:
        db.add(agent)
        db.commit()
    db.close()

def ingest_replicate():
    print("Fetching Replicate.com models...")
    resp = requests.get(REPLICATE_API)
    if resp.status_code != 200:
        print(f"Replicate API error: {resp.status_code}", resp.text)
        return
    data = resp.json()
    for model in data.get('results', []):
        agent = parse_model(model)
        insert_agent(agent)
    print(f"Replicate.com ingestion complete. Total models: {len(data.get('results', []))}")

if __name__ == "__main__":
    ingest_replicate()
