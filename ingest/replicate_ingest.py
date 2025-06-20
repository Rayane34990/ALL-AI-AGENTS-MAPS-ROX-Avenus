# Replicate.com Ingestion Stub
# API: https://replicate.com/api/models (unofficial/public scraping)

import requests
import sqlite3
import os

REPLICATE_API = "https://replicate.com/api/models"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

def parse_model(model):
    return {
        'name': model.get('name', ''),
        'description': model.get('description', ''),
        'source': 'Replicate',
        'type': '',
        'tags': ','.join(model.get('tags', [])),
        'deployment': '',
        'license': model.get('license', ''),
        'repo_link': f"https://replicate.com{model.get('url', '')}",
        'demo_link': '',
        'paper_link': '',
        'last_updated': model.get('updated_at', ''),
        'related': '',
        'rating': '',
        'install': ''
    }

def insert_agent(agent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO agents (name, description, source, type, tags, deployment, license, repo_link, demo_link, paper_link, last_updated, related, rating, install)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (agent['name'], agent['description'], agent['source'], agent['type'], agent['tags'], agent['deployment'], agent['license'], agent['repo_link'], agent['demo_link'], agent['paper_link'], agent['last_updated'], agent['related'], agent['rating'], agent['install']))
    conn.commit()
    conn.close()

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
