# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

ApplyAssistV2 — job application assistant platform with React frontend and FastAPI backend.

## Tech Stack

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS v4
- **Backend**: FastAPI + Python 3.11+ + Pydantic v2
- **Database & Auth**: Supabase (supabase-py + @supabase/supabase-js)
- **AI**: Abstracted LLM layer supporting Claude (Anthropic) and OpenAI
- **State**: Zustand (frontend), Pydantic Settings (backend)

## Architecture

Domain-based design — 4 core domains, each owning its routes, services, schemas, and models:

1. **Profile** — user's professional identity (WRITE owner)
2. **Documents** — CV and cover letter creation/adaptation (reads Profile)
3. **Jobs** — job catalog, search, matching (reads Profile)
4. **Applications** — orchestrates apply flow (reads all, WRITE own records)

Cross-cutting: Auth (Supabase), AI abstraction layer.

## Key Patterns

- Domain folders contain all related code together (not split by file type)
- CV is structured data (sections, items, ordering) — not flat text
- AI layer uses Abstract Base Class + Factory pattern
- Frontend mirrors backend domains in `src/domains/`
- One service file per domain in `src/services/`
- Auth is frontend-only (Supabase direct), not a backend domain

## Common Commands

```bash
make dev              # Run both frontend + backend
make lint             # Lint both stacks
make test             # Run backend tests (pytest)
cd frontend && npm run dev      # Frontend dev server (port 5173)
cd backend && uvicorn app.main:app --reload  # Backend dev server (port 8000)
```

## Backend Specifics

- Entry point: `backend/app/main.py`
- Config: `backend/app/config.py` (pydantic-settings, reads .env)
- API prefix: `/api/v1/`
- Linting: `ruff check .` + `ruff format .`
- Type checking: `mypy app`

## Frontend Specifics

- Entry point: `frontend/src/main.tsx`
- Router: react-router-dom v7 in `frontend/src/App.tsx`
- API client: `frontend/src/lib/api.ts` (axios with JWT interceptor)
- Linting: ESLint + Prettier
- Tailwind v4 via `@tailwindcss/vite` plugin
