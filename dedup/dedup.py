import hashlib
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from models import Agent, SessionLocal

try:
    from sentence_transformers import SentenceTransformer, util
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    MODEL = None

# Hash-based deduplication

def agent_hash(agent):
    key = (agent.name + (agent.description or '') + (agent.repo_link or '') + (agent.paper_link or '')).lower()
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def fetch_agents():
    db = SessionLocal()
    agents = db.query(Agent).all()
    db.close()
    return agents

def remove_duplicates():
    agents = fetch_agents()
    seen = set()
    to_remove = []
    for agent in agents:
        h = agent_hash(agent)
        if h in seen:
            to_remove.append(agent.id)
        else:
            seen.add(h)
    if to_remove:
        db = SessionLocal()
        db.query(Agent).filter(Agent.id.in_(to_remove)).delete(synchronize_session=False)
        db.commit()
        db.close()
    print(f"Removed {len(to_remove)} exact duplicates.")

# Semantic similarity deduplication (optional, requires sentence-transformers)
def semantic_dedup(threshold=0.92):
    if not MODEL:
        print("sentence-transformers not installed; skipping semantic dedup.")
        return
    agents = fetch_agents()
    texts = [a.name + ' ' + (a.description or '') for a in agents]
    embeddings = MODEL.encode(texts, convert_to_tensor=True)
    to_remove = set()
    for i in range(len(agents)):
        if agents[i].id in to_remove:
            continue
        for j in range(i+1, len(agents)):
            if agents[j].id in to_remove:
                continue
            sim = float(util.pytorch_cos_sim(embeddings[i], embeddings[j]))
            if sim > threshold:
                to_remove.add(agents[j].id)
    if to_remove:
        db = SessionLocal()
        db.query(Agent).filter(Agent.id.in_(to_remove)).delete(synchronize_session=False)
        db.commit()
        db.close()
    print(f"Removed {len(to_remove)} semantically similar duplicates.")

def infer_type(description, tags):
    desc = (description or '').lower() + ' ' + (tags or '').lower()
    if 'chat' in desc or 'dialog' in desc:
        return 'chatbot'
    if 'vision' in desc or 'image' in desc:
        return 'vision model'
    if 'retrieval' in desc or 'rag' in desc:
        return 'retrieval tool'
    if 'planning' in desc:
        return 'planning agent'
    if 'summarization' in desc:
        return 'summarization'
    if 'diffusion' in desc:
        return 'diffusion model'
    if 'reinforcement' in desc or 'rlhf' in desc:
        return 'RL agent'
    return 'other'

def auto_tag(description):
    desc = (description or '').lower()
    tags = set()
    for kw in ['llm', 'chatbot', 'rag', 'summarization', 'diffusion', 'vision', 'planning', 'retrieval', 'rlhf', 'api', 'docker', 'pytorch', 'tensorflow']:
        if kw in desc:
            tags.add(kw)
    return ','.join(sorted(tags))

def classify_agents():
    db = SessionLocal()
    agents = db.query(Agent).all()
    for agent in agents:
        new_type = infer_type(agent.description, agent.tags)
        new_tags = auto_tag(agent.description)
        # Merge with existing tags
        merged_tags = ','.join(sorted(set((agent.tags or '').split(',') + new_tags.split(','))))
        agent.type = new_type
        agent.tags = merged_tags
    db.commit()
    db.close()
    print(f"Classified {len(agents)} agents with type and tags.")

def deduplicate_agents():
    remove_duplicates()
    semantic_dedup()
    classify_agents()

if __name__ == "__main__":
    deduplicate_agents()
