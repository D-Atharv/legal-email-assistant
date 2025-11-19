# Backend Documentation

## Overview

The Legal Email Assistant backend is a FastAPI-based REST API that provides email analysis and draft generation capabilities using Google Gemini AI. It follows a layered architecture with clear separation between routes, services, and business logic.

## Project Structure

```
server/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── test_main.http             # HTTP test requests
│
├── core/                       # Core configuration
│   ├── config.py              # Settings management
│   └── __pycache__/
│
├── graph/                      # LangGraph workflows (optional)
│   └── email_graph.py         # Graph-based workflows
│
├── models/                     # Pydantic data models
│   ├── analysis_schema.py     # Analysis output schema
│   ├── request_models.py      # API request schemas
│   └── __pycache__/
│
├── modules/                    # Core business logic
│   ├── analyzer.py            # Email analysis engine
│   ├── drafter.py             # Reply generation engine
│   ├── parser.py              # Email parsing utilities
│   ├── contract_store.py      # Contract clause management
│   └── __pycache__/
│
├── routes/                     # API endpoints
│   ├── analyze.py             # POST /analyze/ endpoint
│   ├── draft.py               # POST /draft/ endpoint
│   └── __pycache__/
│
├── services/                   # Service layer (orchestration)
│   ├── analyzer_service.py    # Analysis orchestration
│   ├── audit_service.py       # Audit logging
│   ├── drafting_service.py    # Drafting orchestration
│   └── __pycache__/
│
├── static/                     # Static files
│   └── audit_logs/            # JSON audit logs
│
└── utils/                      # Utility functions
    ├── clause_utils.py        # Clause extraction
    ├── date_utils.py          # Date parsing
    ├── text_utils.py          # Text processing
    └── __pycache__/
```

## Core Components

### 1. Application Entry Point (`main.py`)

The main application file that initializes FastAPI and configures middleware.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routes import analyze, draft

def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="Legal Email Assistant",
        description="Analyze legal emails + draft replies using LLM",
        version="1.0.0"
    )

    # CORS middleware
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
```

**Key Features:**

- Application factory pattern for testability
- Automatic API documentation at `/docs`
- CORS configured for specific origin
- Modular router structure

### 2. Configuration (`core/config.py`)

Centralized configuration management using Pydantic Settings.

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Legal Email Assistant - Backend"
    LOG_LEVEL: str = "INFO"

    # CORS
    FRONTEND_ORIGIN: str | None = Field(default="http://localhost:3000")

    # LLM Provider
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")

    # Audit Logs
    AUDIT_LOG_DIR: str = Field(default="static/audit_logs")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

**Usage:**

```python
from core.config import settings

api_key = settings.GEMINI_API_KEY
model = settings.GEMINI_MODEL
```

### 3. Data Models

#### Analysis Schema (`models/analysis_schema.py`)

Defines the structure of the analysis output.

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PartiesModel(BaseModel):
    client: Optional[str] = Field(default=None)
    counterparty: Optional[str] = Field(default=None)

class AgreementReferenceModel(BaseModel):
    type: Optional[str] = Field(default=None)
    date: Optional[str] = Field(default=None)

class AnalysisSchema(BaseModel):
    intent: str
    primary_topic: str
    parties: PartiesModel
    agreement_reference: AgreementReferenceModel
    questions: List[str] = Field(default_factory=list)
    requested_due_date: Optional[str] = Field(default=None)
    urgency_level: str

    class Config:
        extra = "ignore"
```

#### Request Models (`models/request_models.py`)

```python
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    email_text: str

class DraftRequest(BaseModel):
    email_text: str
    analysis: dict  # AnalysisSchema as dict
    contract_text: str
```

## API Routes

### Analyze Route (`routes/analyze.py`)

Handles email analysis requests.

```python
from fastapi import APIRouter, HTTPException
from models.request_models import AnalyzeRequest
from services.analyzer_service import analyze_email_service

router = APIRouter()

@router.post("/", summary="Analyze legal email")
async def analyze_email_endpoint(payload: AnalyzeRequest):
    """
    POST /analyze

    Analyzes a legal email and returns structured JSON.
    """
    try:
        result = await analyze_email_service(payload.email_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Draft Route (`routes/draft.py`)

Handles draft generation requests.

```python
from fastapi import APIRouter, HTTPException
from models.request_models import DraftRequest
from services.drafting_service import draft_reply_service

router = APIRouter()

@router.post("/", summary="Draft legal reply")
async def draft_email_endpoint(payload: DraftRequest):
    """
    POST /draft

    Generates a legal reply based on analysis and contract clauses.
    """
    try:
        draft_text = await draft_reply_service(
            email_text=payload.email_text,
            analysis=payload.analysis,
            contract_text=payload.contract_text
        )
        return {"draft": draft_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Core Business Logic

### Analyzer Module (`modules/analyzer.py`)

Pure LLM-based email analysis engine.

```python
import json
from typing import Dict, Any
from google import genai
from core.config import settings
from models.analysis_schema import AnalysisSchema
from utils.text_utils import clean_text

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def analyze_email(email_text: str) -> Dict[str, Any]:
    """
    Analyze email using Gemini AI.

    Args:
        email_text: Raw email text to analyze

    Returns:
        Validated analysis dictionary
    """
    email_text = clean_text(email_text)

    prompt = f"""
You are a legal email analysis engine.

Extract structured information from the email below.
Return ONLY valid JSON in this schema:
{{
  "intent": "string",
  "primary_topic": "string",
  "parties": {{
    "client": "string or null",
    "counterparty": "string or null"
  }},
  "agreement_reference": {{
    "type": "string or null",
    "date": "ISO date string (YYYY-MM-DD) or null"
  }},
  "questions": ["list of legal questions"],
  "requested_due_date": "ISO date string or null",
  "urgency_level": "low | medium | high"
}}

RULES:
- Convert all dates to ISO format (YYYY-MM-DD)
- Extract ALL legal questions
- Do NOT hallucinate
- Output ONLY JSON

Email:
{email_text}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt
    )

    raw = response.text.strip()

    # Parse JSON
    try:
        data = json.loads(raw)
    except:
        # Extract JSON from surrounding text
        start = raw.index("{")
        end = raw.rindex("}") + 1
        data = json.loads(raw[start:end])

    # Validate with Pydantic
    validated = AnalysisSchema(**data)
    return validated.model_dump()
```

**Key Features:**

- Pure LLM approach (no regex)
- Structured JSON output
- Pydantic validation
- Error handling for JSON extraction

### Drafter Module (`modules/drafter.py`)

Legal reply generation engine.

```python
import json
from google import genai
from core.config import settings
from utils.text_utils import clean_text

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_draft_reply(analysis: dict, clauses: dict, original_email: str) -> str:
    """
    Generate professional legal reply.

    Args:
        analysis: Structured analysis from analyzer
        clauses: Dictionary of contract clauses {id: text}
        original_email: Original email text

    Returns:
        Drafted reply email text
    """
    clause_block = "\n".join([f"{cid}: {text}" for cid, text in clauses.items()])

    prompt = f"""
You are a senior commercial contracts lawyer.

Produce a reply that:
- Uses professional legal tone
- Addresses sender by name
- Answers ALL questions from analysis
- Uses ONLY these clauses:
  {clause_block}
- If clause not in list, write:
  "Based on the provided excerpt, this clause is not included, so we cannot confirm."
- NEVER invent clauses

ORIGINAL EMAIL:
{original_email}

STRUCTURED ANALYSIS:
{json.dumps(analysis, indent=2)}

--- DRAFT THE EMAIL BELOW THIS LINE ONLY ---
"""

    resp = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[prompt]
    )

    return clean_text(resp.text)
```

## Service Layer

Services orchestrate business logic and handle cross-cutting concerns.

### Analyzer Service (`services/analyzer_service.py`)

```python
from modules.analyzer import analyze_email

async def analyze_email_service(email_text: str):
    """
    Service layer for email analysis.

    Allows both FastAPI routes and LangGraph nodes to reuse logic.
    """
    return analyze_email(email_text)
```

### Drafting Service (`services/drafting_service.py`)

```python
from modules.drafter import generate_draft_reply
from modules.contract_store import extract_clauses

async def draft_reply_service(email_text: str, analysis: dict, contract_text: str) -> str:
    """
    Service layer for draft generation.

    Args:
        email_text: Original email
        analysis: Structured analysis
        contract_text: Raw contract clauses

    Returns:
        Drafted reply email
    """
    clauses = extract_clauses(contract_text)
    draft = generate_draft_reply(analysis, clauses, email_text)
    return draft
```

### Audit Service (`services/audit_service.py`)

```python
import json
from datetime import datetime
from pathlib import Path
from core.config import settings

def log_operation(operation_type: str, data: dict):
    """
    Log operation to audit file.

    Args:
        operation_type: Type of operation (analysis, draft)
        data: Data to log
    """
    audit_dir = Path(settings.AUDIT_LOG_DIR)
    audit_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    filename = f"audit-{timestamp}.json"

    log_data = {
        "timestamp": timestamp,
        "operation": operation_type,
        "data": data
    }

    with open(audit_dir / filename, "w") as f:
        json.dump(log_data, f, indent=2)
```

## Utilities

### Text Utils (`utils/text_utils.py`)

```python
def clean_text(text: str) -> str:
    """Remove extra whitespace from text."""
    return " ".join(text.split())

def normalize_text(text: str) -> str:
    """Normalize text to lowercase."""
    return text.lower().strip()
```

### Date Utils (`utils/date_utils.py`)

```python
from datetime import datetime
import dateparser

def parse_date(date_string: str) -> str | None:
    """
    Parse date string to ISO format.

    Args:
        date_string: Date in any format

    Returns:
        ISO format date (YYYY-MM-DD) or None
    """
    try:
        dt = dateparser.parse(date_string)
        if dt:
            return dt.strftime("%Y-%m-%d")
    except:
        pass
    return None
```

### Clause Utils (`utils/clause_utils.py`)

```python
import re

def extract_clauses(contract_text: str) -> dict:
    """
    Extract clauses from contract text.

    Args:
        contract_text: Raw contract text with clauses

    Returns:
        Dictionary of {clause_id: clause_text}
    """
    clauses = {}

    # Match patterns like "Clause 9.1:" or "Section 5.2:"
    pattern = r"(Clause|Section)\s+([\d.]+):\s*(.+?)(?=(?:Clause|Section)\s+[\d.]+:|$)"
    matches = re.finditer(pattern, contract_text, re.IGNORECASE | re.DOTALL)

    for match in matches:
        clause_id = f"{match.group(1)} {match.group(2)}"
        clause_text = match.group(3).strip()
        clauses[clause_id] = clause_text

    return clauses
```

## Running the Server

### Development Mode

```bash
cd server
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

**Features:**

- Auto-reload on code changes
- Debug mode enabled
- Accessible at http://localhost:8000
- API docs at http://localhost:8000/docs

### Production Mode

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Configuration:**

- 4 worker processes
- Uvicorn worker class
- Binds to all interfaces

## Testing

### Running Tests

```bash
cd server
pytest
pytest -v  # Verbose
pytest -s  # Show print statements
pytest test_analyzer.py  # Specific file
pytest -k "test_analyze"  # Pattern matching
```

### Writing Tests

```python
# test_analyzer.py
import pytest
from modules.analyzer import analyze_email

def test_analyze_email():
    """Test basic email analysis."""
    email_text = """
    Dear Team,

    Regarding the MSA dated 2024-03-15 between ABC Corp and XYZ Ltd.
    Can you clarify the payment terms?

    Please respond by 2024-03-20.
    """

    result = analyze_email(email_text)

    assert result["intent"]
    assert result["primary_topic"]
    assert "ABC Corp" in [result["parties"]["client"], result["parties"]["counterparty"]]
    assert result["agreement_reference"]["date"] == "2024-03-15"
    assert len(result["questions"]) > 0
    assert result["requested_due_date"] == "2024-03-20"

@pytest.mark.asyncio
async def test_analyzer_service():
    """Test analyzer service."""
    from services.analyzer_service import analyze_email_service
    result = await analyze_email_service("Test email")
    assert result is not None
```

## Error Handling

### Standard Error Response

```python
{
  "detail": "Error message"
}
```

### Custom Exception Handler

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## Logging

### Basic Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Dependencies

### Core Dependencies

```
fastapi~=0.121.2          # Web framework
uvicorn[standard]         # ASGI server
pydantic~=2.12.4         # Data validation
pydantic-settings~=2.12.0 # Settings management
python-multipart          # Form data support
```

### AI Dependencies

```
google-genai             # Google Gemini SDK
langgraph               # Graph-based workflows
langchain               # AI framework
langchain-core          # Core abstractions
langchain-community     # Community integrations
```

### Utility Dependencies

```
python-dateutil~=2.9.0  # Date parsing
dateparser              # Natural language dates
jinja2                  # Template engine
rich                    # Terminal formatting
```

### Development Dependencies

```
pytest                  # Testing framework
pytest-asyncio         # Async testing
httpx                  # HTTP client for tests
```

## Performance Considerations

### Response Times

- Analysis: 2-5 seconds
- Drafting: 3-6 seconds
- Bottleneck: Gemini API latency

### Optimization Strategies

1. **Caching** - Cache common analyses
2. **Connection Pooling** - Reuse HTTP connections
3. **Rate Limiting** - Prevent abuse
4. **Async Operations** - Use async/await properly

## Security Best Practices

1. **Environment Variables** - Never commit `.env`
2. **API Keys** - Rotate regularly
3. **CORS** - Restrict to specific origins
4. **Input Validation** - Use Pydantic models
5. **Error Messages** - Don't expose internal details

---

**Last Updated:** November 19, 2025
