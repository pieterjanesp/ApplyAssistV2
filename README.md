# ApplyAssistV2

Job application assistant platform — generate, adapt, and optimize CVs and cover letters with AI.

## Tech Stack

- **Frontend**: React + TypeScript (Vite) + Tailwind CSS
- **Backend**: FastAPI (Python) + Pydantic
- **Database & Auth**: Supabase
- **AI**: Abstracted LLM layer (Claude + OpenAI)

## Architecture

Domain-based design with 4 core domains:

| Domain | Purpose |
|---|---|
| **Profile** | User's professional identity — foundation data |
| **Documents** | CV and cover letter generation, adaptation, optimization |
| **Jobs** | Job catalog, search, and matching |
| **Applications** | Apply flow orchestration and status tracking |

## Project Structure

```
Apply Assist/
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + Python
├── .env.example       # Environment variable template
├── Makefile           # Unified dev commands
└── CLAUDE.md          # Claude Code instructions
```

## Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- A Supabase project

### 1. Environment Variables

```bash
cp .env.example .env
# Fill in your Supabase and AI provider credentials
```

### 2. Install Dependencies

```bash
make install
```

Or manually:

```bash
cd frontend && npm install
cd backend && pip install -e ".[dev]"
```

### 3. Run Development Servers

```bash
make dev
```

Or separately:

```bash
# Frontend (port 5173)
cd frontend && npm run dev

# Backend (port 8000)
cd backend && uvicorn app.main:app --reload
```

### 4. Verify

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs (Swagger UI)
- Health check: http://localhost:8000/health

## Development Commands

```bash
make install        # Install all dependencies
make dev            # Run both frontend and backend
make dev-frontend   # Run frontend only
make dev-backend    # Run backend only
make lint           # Lint both stacks
make format         # Format both stacks
make test           # Run backend tests
```
