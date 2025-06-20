import requests
import xml.etree.ElementTree as ET
from db.models import Agent, SessionLocal, init_db

ARXIV_API = "http://export.arxiv.org/api/query"

def parse_entry(entry):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
    summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
    link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
    updated = entry.find('{http://www.w3.org/2005/Atom}updated').text.strip()
    categories = ','.join([c.attrib['term'] for c in entry.findall('{http://www.w3.org/2005/Atom}category')])
    return {
        'name': title,
        'description': summary,
        'source': 'arXiv',
        'type': '',  # To be improved: infer from categories
        'tags': categories,
        'deployment': '',
        'license': '',
        'repo_link': '',
        'demo_link': '',
        'paper_link': link,
        'last_updated': updated,
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

def ingest_arxiv(query="artificial intelligence", max_results=20):
    print(f"Fetching arXiv papers for query: {query}")
    params = {'search_query': query, 'start': 0, 'max_results': max_results}
    resp = requests.get(ARXIV_API, params=params)
    if resp.status_code != 200:
        print(f"arXiv API error: {resp.status_code}", resp.text)
        return
    root = ET.fromstring(resp.text)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        agent = parse_entry(entry)
        insert_agent(agent)
    print("arXiv ingestion complete.")

if __name__ == "__main__":
    init_db()
    ingest_arxiv()
