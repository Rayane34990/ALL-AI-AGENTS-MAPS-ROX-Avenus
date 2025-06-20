import requests
import sqlite3
import os
import xml.etree.ElementTree as ET

TFHUB_SITEMAP = "https://tfhub.dev/sitemap.xml"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))

def parse_model_url(url):
    name = url.split('/')[-1]
    return {
        'name': name,
        'description': '',  # Could be improved by scraping model page
        'source': 'TensorFlow Hub',
        'type': '',
        'tags': '',
        'deployment': 'TensorFlow',
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

def ingest_tfhub():
    print("Fetching TensorFlow Hub models...")
    resp = requests.get(TFHUB_SITEMAP)
    if resp.status_code != 200:
        print(f"TFHub sitemap error: {resp.status_code}", resp.text)
        return
    root = ET.fromstring(resp.text)
    urls = [loc.text for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if '/google/' not in loc.text]
    for url in urls:
        agent = parse_model_url(url)
        insert_agent(agent)
    print(f"TensorFlow Hub ingestion complete. Total models: {len(urls)}")

if __name__ == "__main__":
    ingest_tfhub()
