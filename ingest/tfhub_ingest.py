import requests
import os
import sys
import xml.etree.ElementTree as ET
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal

TFHUB_SITEMAP = "https://tfhub.dev/sitemap.xml"

def parse_model_url(url):
    name = url.split('/')[-1]
    return Agent(
        name=name,
        description='',  # Could be improved by scraping model page
        source='TensorFlow Hub',
        type='',
        tags='',
        deployment='TensorFlow',
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
