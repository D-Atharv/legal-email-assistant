# Architecture Documentation

## System Overview

The Legal Email Assistant is a full-stack web application that uses AI to analyze legal emails and generate professional replies. The system follows a client-server architecture with clear separation between frontend presentation, backend business logic, and AI processing.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Next.js    │  │   React 19   │  │  TypeScript  │      │
│  │  App Router  │  │  Components  │  │    + Hooks   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                   │             │
│         └──────────────────┼───────────────────┘             │
│                            │                                 │
│                     ┌──────▼──────┐                          │
│                     │   API Client │                         │
│                     └──────┬──────┘                          │
└────────────────────────────┼────────────────────────────────┘
                             │
                    HTTPS / REST API
                             │
┌────────────────────────────▼────────────────────────────────┐
│                         Server Layer                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI    │  │   Pydantic   │  │   Uvicorn    │      │
│  │   Routing    │  │  Validation  │  │  ASGI Server │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘      │
│         │                  │                                 │
│         └──────────────────┼─────────────────┐               │
│                            │                 │               │
│                     ┌──────▼──────┐   ┌──────▼──────┐       │
│                     │   Services   │   │   Models    │       │
│                     └──────┬───────┘   └─────────────┘       │
│                            │                                 │
│                     ┌──────▼──────┐                          │
│                     │   Modules    │                         │
│                     │  (Business   │                         │
│                     │    Logic)    │                         │
│                     └──────┬───────┘                          │
└────────────────────────────┼────────────────────────────────┘
                             │
                      Google Gemini API
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      AI Processing Layer                    │
│                                                               │
│             ┌────────────────────────────┐                   │
│             │   Google Gemini 2.5 Flash  │                   │
│             │   - Email Analysis          │                   │
│             │   - Draft Generation        │                   │
│             └────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Components

```
client/
├── app/                        # Next.js App Router
│   ├── layout.tsx              # Root layout with theme
│   ├── page.tsx                # Landing page
│   └── assistant/
│       └── page.tsx            # Main assistant interface
│
├── components/                 # React components
│   ├── ui/                     # Shadcn UI primitives
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   │
│   ├── EmailInput.tsx          # Email text input
│   ├── ContractInput.tsx       # Contract clauses input
│   ├── JsonViewer.tsx          # JSON visualization
│   ├── DraftPreview.tsx        # Draft output display
│   └── AuditLogPreview.tsx     # Audit log viewer
│
└── lib/                        # Utilities
    ├── api.ts                  # Backend API client
    ├── json_converter.ts       # JSON parsing
    └── utils.ts                # Helper functions
```

### Backend Components

```
server/
├── main.py                     # Application entry point
│   └── create_app()            # FastAPI app factory
│
├── core/                       # Core configuration
│   └── config.py               # Settings management
│
├── routes/                     # API endpoints
│   ├── analyze.py              # POST /analyze/
│   └── draft.py                # POST /draft/
│
├── services/                   # Service layer
│   ├── analyzer_service.py     # Analysis orchestration
│   ├── drafting_service.py     # Drafting orchestration
│   └── audit_service.py        # Audit logging
│
├── modules/                    # Core business logic
│   ├── analyzer.py             # Email analysis engine
│   ├── drafter.py              # Reply generation engine
│   ├── parser.py               # Email parsing utilities
│   └── contract_store.py       # Contract clause management
│
├── models/                     # Data models
│   ├── analysis_schema.py      # Analysis output schema
│   └── request_models.py       # API request schemas
│
└── utils/                      # Utility functions
    ├── text_utils.py           # Text processing
    ├── date_utils.py           # Date parsing
    └── clause_utils.py         # Clause extraction
```

## Data Flow

### 1. Email Analysis Flow

```
User Input (Email Text)
        │
        ▼
┌───────────────────┐
│  EmailInput.tsx   │  Frontend: Capture email text
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  api.ts           │  API Client: POST /analyze/
│  analyzeEmail()   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  analyze.py       │  Route: Receive request
│  router.post()    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  analyzer_        │  Service: Orchestrate analysis
│  service.py       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  analyzer.py      │  Module: Core analysis logic
│  analyze_email()  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Google Gemini    │  AI: Extract structured data
│  API               │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  AnalysisSchema   │  Model: Validate response
│  (Pydantic)       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  audit_service.py │  Service: Log operation
└────────┬──────────┘
         │
         ▼
JSON Response to Client
```

### 2. Draft Generation Flow

```
User Input (Email + Analysis + Contract)
        │
        ▼
┌───────────────────┐
│  ContractInput    │  Frontend: Capture inputs
│  .tsx             │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  api.ts           │  API Client: POST /draft/
│  draftReply()     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  draft.py         │  Route: Receive request
│  router.post()    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  drafting_        │  Service: Orchestrate drafting
│  service.py       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  contract_store   │  Module: Extract clauses
│  .py              │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  drafter.py       │  Module: Generate draft
│  generate_draft_  │
│  reply()          │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Google Gemini    │  AI: Generate reply text
│  API               │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  audit_service.py │  Service: Log operation
└────────┬──────────┘
         │
         ▼
Draft Response to Client
```

## Technology Stack Details

### Frontend Technologies

| Technology           | Version | Purpose                      |
| -------------------- | ------- | ---------------------------- |
| Next.js              | 16.x    | React framework with SSR/SSG |
| React                | 19.x    | UI component library         |
| TypeScript           | 5.x     | Type safety                  |
| Tailwind CSS         | 4.x     | Utility-first CSS            |
| Shadcn UI            | Latest  | Component library            |
| Lucide React         | Latest  | Icon library                 |
| React JSON View Lite | 2.x     | JSON visualization           |

### Backend Technologies

| Technology      | Version   | Purpose                        |
| --------------- | --------- | ------------------------------ |
| FastAPI         | 0.121.x   | High-performance web framework |
| Python          | 3.11+     | Programming language           |
| Pydantic        | 2.x       | Data validation                |
| Uvicorn         | Latest    | ASGI server                    |
| Google Gemini   | 2.5-flash | LLM for AI processing          |
| LangChain       | Latest    | AI workflow framework          |
| LangGraph       | Latest    | Graph-based AI workflows       |
| Python-dateutil | 2.9.x     | Date parsing                   |
| Jinja2          | Latest    | Template engine                |

## Design Patterns

### 1. Layered Architecture

The system uses a layered architecture for separation of concerns:

```
Presentation Layer (Frontend)
    ↓
API Layer (REST)
    ↓
Service Layer (Business logic orchestration)
    ↓
Module Layer (Core business logic)
    ↓
External Services (AI APIs)
```

**Benefits:**

- Clear separation of concerns
- Easy to test individual layers
- Flexible to replace implementations
- Maintainable and scalable

### 2. Repository Pattern

Contract clauses are managed through a repository-like pattern in `contract_store.py`:

```python
class ContractStore:
    def __init__(self):
        self.clauses = {}

    def add_clause(self, id: str, text: str):
        self.clauses[id] = text

    def get_clause(self, id: str) -> str:
        return self.clauses.get(id)

    def get_all_clauses(self) -> dict:
        return self.clauses
```

### 3. Service Layer Pattern

Services orchestrate complex operations:

```python
# analyzer_service.py
async def analyze_email_service(email_text: str):
    # Orchestrates:
    # 1. Text cleaning
    # 2. AI analysis
    # 3. Validation
    # 4. Audit logging
    result = analyze_email(email_text)
    await audit_service.log_analysis(result)
    return result
```

### 4. Factory Pattern

FastAPI app is created using factory pattern:

```python
def create_app() -> FastAPI:
    app = FastAPI(...)
    app.add_middleware(CORSMiddleware, ...)
    app.include_router(analyze.router, ...)
    app.include_router(draft.router, ...)
    return app

app = create_app()
```

### 5. Strategy Pattern

Different text processing strategies in `text_utils.py`:

```python
def clean_text(text: str) -> str:
    # Strategy: Remove extra whitespace
    return " ".join(text.split())

def normalize_text(text: str) -> str:
    # Strategy: Lowercase and normalize
    return text.lower().strip()
```

## Data Models

### AnalysisSchema

Defines the structure of analyzed email data:

```python
class AnalysisSchema(BaseModel):
    intent: str
    primary_topic: str
    parties: PartiesModel
    agreement_reference: AgreementReferenceModel
    questions: List[str]
    requested_due_date: Optional[str]
    urgency_level: str
```

**Validation:**

- All dates must be in ISO format (YYYY-MM-DD)
- Urgency level must be: "low", "medium", or "high"
- Parties and agreement fields can be null

### Request Models

```python
class AnalyzeRequest(BaseModel):
    email_text: str

class DraftRequest(BaseModel):
    email_text: str
    analysis: dict  # AnalysisSchema as dict
    contract_text: str
```

## Security Architecture

### 1. Environment Variables

- Sensitive data stored in `.env` files
- Not committed to version control
- Loaded via `pydantic-settings`

### 2. CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],  # Specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Input Validation

- All inputs validated with Pydantic
- Type checking on frontend with TypeScript
- SQL injection not applicable (no database)
- XSS prevention via React's automatic escaping

### 4. API Key Management

- Gemini API key stored in environment variable
- Never exposed to frontend
- Loaded once at startup

## Scalability Considerations

### Current Architecture

**Stateless Design:**

- No session management
- Each request is independent
- Easy to scale horizontally

**Performance Characteristics:**

- Analysis: 2-5 seconds per request
- Drafting: 3-6 seconds per request
- Bottleneck: Google Gemini API rate limits

### Scaling Strategies

**1. Horizontal Scaling:**

```
          Load Balancer
               │
     ┌─────────┼─────────┐
     │         │         │
  Server 1  Server 2  Server 3
```

**2. Caching Layer:**

```python
# Add Redis for caching common analyses
from redis import Redis

cache = Redis(host='localhost', port=6379)

def analyze_email_cached(email_text: str):
    cache_key = hash(email_text)
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    result = analyze_email(email_text)
    cache.set(cache_key, json.dumps(result), ex=3600)
    return result
```

**3. Rate Limiting:**

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze/")
@limiter.limit("10/minute")
async def analyze_endpoint():
    ...
```

**4. Queue System:**

For long-running operations:

```python
# Add Celery for background tasks
from celery import Celery

celery_app = Celery('legal-assistant')

@celery_app.task
def analyze_email_async(email_text: str):
    return analyze_email(email_text)
```

## Error Handling Strategy

### Frontend Error Handling

```typescript
try {
  const result = await analyzeEmail(emailText);
  // Success path
} catch (error) {
  if (error instanceof TypeError) {
    // Network error
    setError("Cannot connect to server");
  } else {
    // API error
    setError(error.message);
  }
}
```

### Backend Error Handling

```python
@router.post("/")
async def analyze_endpoint(payload: AnalyzeRequest):
    try:
        result = await analyze_email_service(payload.email_text)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Log error
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
```

## Monitoring and Observability

### Audit Logging

All operations are logged to `static/audit_logs/`:

```python
def log_operation(operation_type: str, data: dict):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    filename = f"audit-{timestamp}.json"

    with open(f"static/audit_logs/{filename}", "w") as f:
        json.dump({
            "timestamp": timestamp,
            "operation": operation_type,
            "data": data
        }, f, indent=2)
```

### Recommended Additions

**1. Structured Logging:**

```python
import logging
import structlog

logger = structlog.get_logger()

logger.info("email_analyzed",
    email_length=len(email_text),
    processing_time=elapsed_time)
```

**2. Health Checks:**

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "gemini_api": check_gemini_connection()
    }
```

**3. Metrics:**

```python
from prometheus_client import Counter, Histogram

analysis_counter = Counter('analysis_total', 'Total analyses')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis duration')

@analysis_duration.time()
def analyze_email(email_text: str):
    analysis_counter.inc()
    # ... analysis logic
```

## Future Enhancements

### 1. Database Integration

Add PostgreSQL for persistent storage:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True)
    email_text = Column(Text)
    result = Column(JSON)
    created_at = Column(DateTime)
```

### 2. Authentication

Add user authentication:

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/analyze/")
async def analyze(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    # ... proceed with analysis
```

### 3. WebSocket Support

Real-time updates for long operations:

```python
from fastapi import WebSocket

@app.websocket("/ws/analyze")
async def analyze_ws(websocket: WebSocket):
    await websocket.accept()
    # Stream analysis progress
    async for chunk in analyze_stream(email_text):
        await websocket.send_json(chunk)
```

### 4. Multi-Model Support

Support multiple AI providers:

```python
class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, text: str) -> dict:
        pass

class GeminiProvider(LLMProvider):
    def analyze(self, text: str) -> dict:
        # Gemini implementation
        pass

class OpenAIProvider(LLMProvider):
    def analyze(self, text: str) -> dict:
        # OpenAI implementation
        pass
```

## Deployment Architecture

### Production Setup

```
                    Internet
                       │
                       ▼
              ┌────────────────┐
              │  Load Balancer │
              │    (Nginx)     │
              └────────┬───────┘
                       │
           ┌───────────┴───────────┐
           │                       │
           ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │   Frontend   │        │   Backend    │
    │  (Vercel)    │        │  (Render)    │
    └──────────────┘        └──────┬───────┘
                                    │
                                    ▼
                           ┌────────────────┐
                           │  Google Gemini │
                           │      API       │
                           └────────────────┘
```

### Recommended Infrastructure

**Small Scale (< 1000 users):**

- Frontend: Vercel Free Tier
- Backend: Render.com Free Tier or Railway
- No database needed

**Medium Scale (< 10,000 users):**

- Frontend: Vercel Pro
- Backend: AWS EC2 t3.medium or equivalent
- Cache: Redis Cloud
- Database: PostgreSQL (if needed)

**Large Scale (> 10,000 users):**

- Frontend: Vercel Enterprise or Cloudflare Pages
- Backend: Kubernetes cluster on AWS/GCP
- Cache: Redis Cluster
- Database: PostgreSQL with read replicas
- Message Queue: RabbitMQ or AWS SQS
- Monitoring: DataDog or New Relic

---

**Last Updated:** November 19, 2025
