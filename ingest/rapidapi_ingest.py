import requests
import sqlite3
import os

RAPIDAPI_URL = "https://api.rapidapi.com/hub/apis"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

# Note: This is a placeholder; RapidAPI may require scraping or an API key for full access.
def parse_api(api):
    return {
        'name': api.get('name', ''),
        'description': api.get('description', ''),
        'source': 'RapidAPI',
        'type': '',
        'tags': ','.join(api.get('categories', [])),
        'deployment': '',
        'license': '',
        'repo_link': api.get('website', ''),
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

def ingest_rapidapi():
    print("Fetching RapidAPI APIs...")
    # This is a placeholder; actual implementation may require scraping or an API key.
    resp = requests.get(RAPIDAPI_URL)
    if resp.status_code != 200:
        print(f"RapidAPI error: {resp.status_code}", resp.text)
        return
    data = resp.json()
    for api in data.get('apis', []):
        agent = parse_api(api)
        insert_agent(agent)
    print(f"RapidAPI ingestion complete. Total APIs: {len(data.get('apis', []))}")

if __name__ == "__main__":
    ingest_rapidapi()
