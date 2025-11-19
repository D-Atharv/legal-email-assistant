# Quick Reference Guide

A quick reference for common tasks and commands in the Legal Email Assistant project.

## 📋 Table of Contents

- [Development Setup](#development-setup)
- [Running the Application](#running-the-application)
- [Common Commands](#common-commands)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Useful Code Snippets](#useful-code-snippets)

---

## Development Setup

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/legal-email-assistant.git
cd legal-email-assistant

# Backend setup
cd server
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Create .env with GEMINI_API_KEY
uvicorn main:app --reload

# Frontend setup (new terminal)
cd client
npm install
# Create .env.local with NEXT_PUBLIC_BACKEND_URL
npm run dev
```

### Prerequisites

- Node.js 20+
- Python 3.11+
- Google Gemini API Key

---

## Running the Application

### Backend

```bash
# Development
cd server
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Access:**

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend

```bash
# Development
cd client
npm run dev

# Production
npm run build
npm start
```

**Access:**

- App: http://localhost:3000
- Assistant: http://localhost:3000/assistant

### Docker

```bash
# Build and run both services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Common Commands

### Backend Commands

```bash
# Activate virtual environment
source venv/bin/activate        # Linux/Mac
.\venv\Scripts\Activate.ps1     # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000

# Run tests
pytest
pytest -v                       # Verbose
pytest -s                       # Show print output
pytest test_file.py            # Specific file
pytest -k "test_name"          # Pattern match

# Code formatting
black .
isort .

# Check code quality
flake8
mypy .
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Type check
npx tsc --noEmit

# Clear cache
rm -rf .next
rm -rf node_modules
npm install
```

### Git Commands

```bash
# Create feature branch
git checkout -b feature/your-feature

# Stage changes
git add .

# Commit changes
git commit -m "Type: Description"

# Push branch
git push origin feature/your-feature

# Update from main
git fetch upstream
git rebase upstream/main

# Check status
git status
git diff
git log --oneline
```

---

## API Endpoints

### POST /analyze/

Analyze a legal email.

```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Your email here..."}'
```

**Response:** Analysis JSON with intent, parties, questions, etc.

### POST /draft/

Generate a reply draft.

```bash
curl -X POST "http://localhost:8000/draft/" \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Original email...",
    "analysis": {...},
    "contract_text": "Clause 9.1: ..."
  }'
```

**Response:** `{"draft": "Reply email text..."}`

---

## Environment Variables

### Backend (.env)

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
GEMINI_MODEL=gemini-2.5-flash
FRONTEND_ORIGIN=http://localhost:3000
AUDIT_LOG_DIR=static/audit_logs
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## Troubleshooting

### Backend Issues

**Port already in use:**

```bash
# Find process
netstat -ano | findstr :8000     # Windows
lsof -ti:8000                    # Linux/Mac

# Kill process
taskkill /PID <pid> /F           # Windows
kill -9 <pid>                    # Linux/Mac
```

**Module not found:**

```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Gemini API error:**

- Check API key in `.env`
- Verify API key is valid
- Check quota limits

### Frontend Issues

**Cannot connect to backend:**

- Verify backend is running
- Check `NEXT_PUBLIC_BACKEND_URL`
- Check CORS settings

**Build errors:**

```bash
rm -rf .next node_modules
npm install
npm run build
```

**Type errors:**

```bash
npx tsc --noEmit
# Fix reported errors
```

### Common Errors

**CORS Error:**

- Ensure `FRONTEND_ORIGIN` matches frontend URL exactly
- Include protocol (http:// or https://)

**JSON Parse Error:**

- Check response from Gemini API
- Ensure proper JSON format in prompts

**Import Error:**

- Check file paths are correct
- Ensure all dependencies are installed

---

## Useful Code Snippets

### Backend: Add New Endpoint

```python
# routes/new_route.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def new_endpoint(data: dict):
    # Your logic here
    return {"result": "success"}

# main.py
from routes import new_route
app.include_router(new_route.router, prefix="/new", tags=["new"])
```

### Frontend: Add New Component

```tsx
// components/NewComponent.tsx
interface NewComponentProps {
  data: string;
}

export function NewComponent({ data }: NewComponentProps) {
  return <div>{data}</div>;
}

// Usage
import { NewComponent } from "@/components/NewComponent";
<NewComponent data="test" />;
```

### API Call

```typescript
// lib/api.ts
export async function newApiCall(param: string): Promise<Response> {
  const res = await fetch(`${BACKEND_URL}/endpoint/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ param }),
  });

  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return await res.json();
}
```

### Error Handling

```python
# Backend
try:
    result = process_data(data)
    return result
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal error")
```

```typescript
// Frontend
try {
  const result = await apiCall(data);
  setSuccess(result);
} catch (error) {
  setError(error instanceof Error ? error.message : "Unknown error");
} finally {
  setLoading(false);
}
```

### Testing

```python
# test_example.py
import pytest

def test_function():
    result = my_function("test")
    assert result == expected
    assert "key" in result

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

---

## File Locations

```
Project Root
├── server/                 Backend code
│   ├── main.py            Entry point
│   ├── .env               Environment variables
│   ├── routes/            API endpoints
│   ├── services/          Business logic
│   └── tests/             Test files
│
├── client/                Frontend code
│   ├── app/               Pages
│   ├── components/        React components
│   ├── lib/               Utilities
│   └── .env.local         Environment variables
│
└── docs/                  Documentation
    ├── API.md             API reference
    ├── SETUP.md           Setup guide
    └── ARCHITECTURE.md    Architecture docs
```

---

## Port Configuration

| Service  | Default Port | Environment Variable |
| -------- | ------------ | -------------------- |
| Backend  | 8000         | -                    |
| Frontend | 3000         | -                    |

To change ports:

**Backend:**

```bash
uvicorn main:app --port 8001
```

**Frontend:**

```bash
npm run dev -- --port 3001
```

---

## Keyboard Shortcuts (Development)

**VS Code:**

- `Ctrl/Cmd + P` - Quick file open
- `Ctrl/Cmd + Shift + P` - Command palette
- `Ctrl/Cmd + `` - Toggle terminal
- `F5` - Start debugging
- `Ctrl/Cmd + /` - Toggle comment

**Browser:**

- `F12` - Open dev tools
- `Ctrl/Cmd + Shift + R` - Hard refresh
- `Ctrl/Cmd + Shift + C` - Inspect element

---

## Resource Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Google Gemini API](https://ai.google.dev/)

---

## Support

**Documentation:**

- [Full README](../README.md)
- [API Documentation](./API.md)
- [Setup Guide](./SETUP.md)

**Getting Help:**

1. Check documentation
2. Search existing issues
3. Create new issue
4. Contact maintainers

---

**Last Updated:** November 19, 2025
