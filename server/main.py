"""
FastAPI application entrypoint.

- Initializes API routes
- Sets up CORS
- No MCP integration anymore
- LangGraph is used only inside workflow endpoints (if added)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routes import analyze, draft

def create_app() -> FastAPI:
    app = FastAPI(
        title="Legal Email Assistant",
        description="Analyze legal emails + draft replies using LLM + MCP",
        version="1.0.0"
    )

    # CORS: Allow your frontend domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(analyze.router, prefix="/analyze", tags=["analysis"])
    app.include_router(draft.router, prefix="/draft", tags=["drafting"])


    return app

app = create_app()
