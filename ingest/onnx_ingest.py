# ONNX Model Zoo Ingestion Stub
# API: https://github.com/onnx/models or scraping

import requests
import sqlite3
import os

ONNX_MODELS_URL = "https://api.github.com/repos/onnx/models/contents/"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

# Helper to parse ONNX model metadata from GitHub API

def parse_model(item):
    name = item.get('name', '')
    url = item.get('html_url', '')
    return {
        'name': name,
        'description': '',  # Could be improved by fetching README
        'source': 'ONNX Model Zoo',
        'type': '',
        'tags': 'onnx',
        'deployment': 'ONNX',
        'license': '',
        'repo_link': url,
        'demo_link': '',
        'paper_link': '',
        'last_updated': '',
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
