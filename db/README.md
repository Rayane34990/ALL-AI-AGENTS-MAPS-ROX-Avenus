This directory contains the database models and migration logic for the AI Agent Discovery project.

# PostgreSQL Cloud-Native Setup

- The project now uses PostgreSQL for persistent, scalable storage via SQLAlchemy ORM.
- Set the `DATABASE_URL` environment variable to your PostgreSQL connection string (e.g., `postgresql://user:password@host:port/dbname`).
- The legacy SQLite setup is no longer used.
- See the main README for setup instructions.
