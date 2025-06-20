from fastapi import APIRouter, Query, HTTPException
from db.models import Agent, get_all_agents, search_agents
from fastapi.responses import JSONResponse
import sqlite3
import os

router = APIRouter()

@router.get("/agents")
def list_agents(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    try:
        agents = get_all_agents()
        start = (page - 1) * limit
        end = start + limit
        return {
            "results": agents[start:end],
            "total": len(agents),
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/agents/{agent_id}")
def get_agent(agent_id: int):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    agent = conn.execute('SELECT * FROM agents WHERE id=?', (agent_id,)).fetchone()
    conn.close()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return dict(agent)

@router.get("/search")
def search(q: str):
    return search_agents(q)

@router.get("/search/advanced")
def advanced_search(
    q: str = '',
    type: str = '',
    tag: str = '',
    license: str = '',
    source: str = '',
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/agents.db'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    query = 'SELECT * FROM agents WHERE 1=1'
    params = []
    if q:
        query += ' AND (name LIKE ? OR description LIKE ? OR tags LIKE ? OR type LIKE ? OR source LIKE ? OR license LIKE ?)' 
        for _ in range(6):
            params.append(f'%{q}%')
    if type:
        query += ' AND type=?'
        params.append(type)
    if tag:
        query += ' AND tags LIKE ?'
        params.append(f'%{tag}%')
    if license:
        query += ' AND license=?'
        params.append(license)
    if source:
        query += ' AND source=?'
        params.append(source)
    query += ' ORDER BY id DESC LIMIT ? OFFSET ?'
    params.extend([limit, (page-1)*limit])
    agents = conn.execute(query, params).fetchall()
    total = conn.execute('SELECT COUNT(*) FROM agents').fetchone()[0]
    conn.close()
    return {
        "results": [dict(a) for a in agents],
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/export")
def export_agents():
    try:
        agents = get_all_agents()
        return JSONResponse(content={"results": agents, "total": len(agents)}, media_type="application/json")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
