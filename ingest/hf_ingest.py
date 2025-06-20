import requests
import sqlite3
import os
import time

HF_API = "https://huggingface.co/api/models"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

# Helper to parse model metadata

def parse_model(model):
    card_data = model.get('cardData', {})
    return {
        'name': model.get('modelId', ''),
        'description': model.get('description', card_data.get('summary', '')),
        'source': 'HuggingFace',
        'type': '',  # To be inferred/classified
        'tags': ','.join(model.get('tags', [])),
        'deployment': ','.join(card_data.get('library_name', [])) if card_data.get('library_name') else '',
        'license': model.get('license', card_data.get('license', '')),
        'repo_link': f"https://huggingface.co/{model.get('modelId', '')}",
        'demo_link': card_data.get('demo', ''),
        'paper_link': card_data.get('paper', ''),
        'last_updated': model.get('lastModified', ''),
        'related': ','.join(card_data.get('related_models', [])) if card_data.get('related_models') else '',
        'rating': '',
        'install': card_data.get('pip', '')
    }

def insert_agent(agent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO agents (name, description, source, type, tags, deployment, license, repo_link, demo_link, paper_link, last_updated, related, rating, install)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (agent['name'], agent['description'], agent['source'], agent['type'], agent['tags'], agent['deployment'], agent['license'], agent['repo_link'], agent['demo_link'], agent['paper_link'], agent['last_updated'], agent['related'], agent['rating'], agent['install']))
    conn.commit()
    conn.close()

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
