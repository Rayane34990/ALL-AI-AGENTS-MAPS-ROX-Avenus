# ONNX Model Zoo Ingestion Stub
# API: https://github.com/onnx/models or scraping

import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal  # noqa: E402, F401, F403

ONNX_MODELS_URL = "https://api.github.com/repos/onnx/models/contents/"

# Helper to parse ONNX model metadata from GitHub API

def parse_model(item):
    name = item.get('name', '')
    url = item.get('html_url', '')
    return Agent(
        name=name,
        description='',  # Could be improved by fetching README
        source='ONNX Model Zoo',
        type='',
        tags='onnx',
        deployment='ONNX',
        license='',
        repo_link=url,
        demo_link='',
        paper_link='',
        last_updated='',
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

def ingest_onnx():
    print("Fetching ONNX Model Zoo models...")
    resp = requests.get(ONNX_MODELS_URL)
    if resp.status_code != 200:
        print(f"ONNX Model Zoo API error: {resp.status_code}", resp.text)
        return
    data = resp.json()
    for item in data:
        if item['type'] == 'dir':
            agent = parse_model(item)
            insert_agent(agent)
    print(f"ONNX Model Zoo ingestion complete. Total models: {len([i for i in data if i['type']=='dir'])}")

if __name__ == "__main__":
    ingest_onnx()
