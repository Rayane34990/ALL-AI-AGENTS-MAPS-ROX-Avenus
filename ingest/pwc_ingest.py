import requests
from db.models import Agent, SessionLocal, init_db
import os

PWC_API = "https://paperswithcode.com/api/v1/papers/"
PWC_TOKEN = os.environ.get('PWC_TOKEN')
HEADERS = {'Authorization': f'Token {PWC_TOKEN}'} if PWC_TOKEN else {}

def parse_paper(paper):
    return {
        'name': paper.get('title', ''),
        'description': paper.get('abstract', ''),
        'source': 'PapersWithCode',
        'type': '',  # To be improved: infer from tasks/models
        'tags': ','.join([t['name'] for t in paper.get('tasks', [])]),
        'deployment': '',
        'license': '',
        'repo_link': paper.get('repository', {}).get('url', ''),
        'demo_link': '',
        'paper_link': paper.get('url_abs', ''),
        'last_updated': paper.get('date', ''),
        'related': '',
        'rating': '',
        'install': ''
    }

def insert_agent(agent):
    db = SessionLocal()
    db_agent = Agent(**agent)
    db.merge(db_agent)
    db.commit()
    db.close()

def ingest_pwc(query="artificial intelligence", page=1):
    print(f"Fetching Papers With Code papers for query: {query}")
    params = {'q': query, 'page': page}
    resp = requests.get(PWC_API, headers=HEADERS, params=params)
    if resp.status_code != 200:
        print(f"Papers With Code API error: {resp.status_code}", resp.text)
        return
    data = resp.json()
    for paper in data.get('results', []):
        agent = parse_paper(paper)
        insert_agent(agent)
    print("Papers With Code ingestion complete.")

if __name__ == "__main__":
    init_db()
    ingest_pwc()
