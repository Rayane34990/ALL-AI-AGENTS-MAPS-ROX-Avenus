# There’s An AI For That Ingestion Stub
# Website: https://theresanaiforthat.com/ (scraping)

import requests
import os
import sys
from bs4 import BeautifulSoup
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal  # noqa: E402, F401, F403

SITE_URL = "https://theresanaiforthat.com/"


def insert_agent(agent):
    db = SessionLocal()
    exists = db.query(Agent).filter_by(name=agent.name, source=agent.source).first()
    if not exists:
        db.add(agent)
        db.commit()
    db.close()

def ingest_thereisnai():
    print("Scraping 'There’s An AI For That'...")
    try:
        resp = requests.get(SITE_URL)
        if resp.status_code != 200:
            print(f"Error: {resp.status_code}", resp.text)
            return
        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.select('a.tool-card')
        for card in cards:
            name = card.select_one('.tool-card-title').get_text(strip=True)
            description = card.select_one('.tool-card-description').get_text(strip=True)
            tags = ','.join([t.get_text(strip=True) for t in card.select('.tool-card-tag')])
            link = SITE_URL.rstrip('/') + card['href']
            agent = Agent(
                name=name,
                description=description,
                source="There’s An AI For That",
                type='',
                tags=tags,
                deployment='web',
                license='',
                repo_link=link,
                demo_link='',
                paper_link='',
                last_updated='',
                related='',
                rating='',
                install=''
            )
            insert_agent(agent)
            time.sleep(0.1)  # Be polite to the server
        print(f"Scraped {len(cards)} tools from There’s An AI For That.")
    except Exception as e:
        print(f"Scraping failed: {e}")

if __name__ == "__main__":
    ingest_thereisnai()
