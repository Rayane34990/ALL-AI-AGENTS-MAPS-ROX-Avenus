import requests
import sqlite3
import os
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO agents (name, description, source, type, tags, deployment, license, repo_link, demo_link, paper_link, last_updated, related, rating, install)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (agent['name'], agent['description'], agent['source'], agent['type'], agent['tags'], agent['deployment'], agent['license'], agent['repo_link'], agent['demo_link'], agent['paper_link'], agent['last_updated'], agent['related'], agent['rating'], agent['install']))
    conn.commit()
    conn.close()

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
    ingest_arxiv()
