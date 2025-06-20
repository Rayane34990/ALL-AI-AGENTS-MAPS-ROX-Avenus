import requests
import os
from db.models import Agent, SessionLocal, init_db

GITHUB_API = "https://api.github.com/search/repositories"

# You can set a GitHub token for higher rate limits
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

HEADERS = {'Accept': 'application/vnd.github+json'}
if GITHUB_TOKEN:
    HEADERS['Authorization'] = f'token {GITHUB_TOKEN}'

def parse_repo(repo):
    return {
        'name': repo['name'],
        'description': repo.get('description', ''),
        'source': 'GitHub',
        'type': '',  # To be improved: infer from topics/readme
        'tags': ','.join(repo.get('topics', [])),
        'deployment': '',  # To be improved: infer from readme/dockerfile
        'license': repo['license']['spdx_id'] if repo.get('license') else '',
        'repo_link': repo['html_url'],
        'demo_link': '',  # To be improved: infer from repo homepage
        'paper_link': '',
        'last_updated': repo['updated_at'],
        'related': '',
        'rating': str({'stars': repo['stargazers_count'], 'activity': 'high' if repo['forks_count'] > 10 else 'low'}),
        'install': ''  # To be improved: infer from readme
    }

def insert_agent(agent):
    db = SessionLocal()
    db_agent = Agent(**agent)
    db.merge(db_agent)
    db.commit()
    db.close()

def ingest_github(topic="ai-agent", max_pages=1):
    print(f"Fetching GitHub repos for topic: {topic}")
    for page in range(1, max_pages+1):
        params = {'q': f'topic:{topic}', 'sort': 'stars', 'order': 'desc', 'per_page': 30, 'page': page}
        resp = requests.get(GITHUB_API, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"GitHub API error: {resp.status_code}", resp.text)
            break
        data = resp.json()
        for repo in data.get('items', []):
            agent = parse_repo(repo)
            insert_agent(agent)
        if 'items' not in data or len(data['items']) < 30:
            break
    print("GitHub ingestion complete.")

if __name__ == "__main__":
    init_db()
    ingest_github()
