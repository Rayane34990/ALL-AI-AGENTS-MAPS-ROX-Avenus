# AI Agent Discovery Engine

Open-source platform to map and search every AI agent, model, or tool across GitHub, papers, APIs, and directories.

## Features
- Unified, queryable knowledge base
- Modular ingestion (GitHub, arXiv, APIs, etc.)
- Deduplication and classification
- Minimal REST API and web UI
- Free/low-cost hosting support

## Quickstart
1. `pip install -r requirements.txt`
2. `python -c "from db.models import init_db; init_db()"`
3. `uvicorn main:app --reload`

## Contributing
See `docs/CONTRIBUTING.md` for guidelines.
