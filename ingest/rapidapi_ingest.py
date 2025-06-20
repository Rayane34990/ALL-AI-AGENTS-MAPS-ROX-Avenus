import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal  # noqa: E402, F401, F403

RAPIDAPI_URL = "https://api.rapidapi.com/hub/apis"

# Note: This is a placeholder; RapidAPI may require scraping or an API key for full access.
def parse_api(api):
    return Agent(
        name=api.get('name', ''),
        description=api.get('description', ''),
        source='RapidAPI',
        type='',
        tags=','.join(api.get('categories', [])),
        deployment='',
        license='',
        repo_link=api.get('website', ''),
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
