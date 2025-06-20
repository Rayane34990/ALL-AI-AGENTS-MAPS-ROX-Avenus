from fastapi import APIRouter, Query, HTTPException
from db.models import Agent, get_all_agents, search_agents, SessionLocal
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/agents")
def list_agents(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    try:
        db = SessionLocal()
        total = db.query(Agent).count()
        agents = db.query(Agent).order_by(Agent.id.desc()).offset((page-1)*limit).limit(limit).all()
        db.close()
        return {
            "results": [a.__dict__ for a in agents],
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/agents/{agent_id}")
def get_agent(agent_id: int):
    db = SessionLocal()
    agent = db.query(Agent).filter_by(id=agent_id).first()
    db.close()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.__dict__

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
    db = SessionLocal()
    query = db.query(Agent)
    if q:
        query = query.filter(
            Agent.name.ilike(f'%{q}%') |
            Agent.description.ilike(f'%{q}%') |
            Agent.tags.ilike(f'%{q}%') |
            Agent.type.ilike(f'%{q}%') |
            Agent.source.ilike(f'%{q}%') |
            Agent.license.ilike(f'%{q}%')
        )
    if type:
        query = query.filter(Agent.type == type)
    if tag:
        query = query.filter(Agent.tags.ilike(f'%{tag}%'))
    if license:
        query = query.filter(Agent.license == license)
    if source:
        query = query.filter(Agent.source == source)
    total = query.count()
    agents = query.order_by(Agent.id.desc()).offset((page-1)*limit).limit(limit).all()
    db.close()
    return {
        "results": [a.__dict__ for a in agents],
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
