# Legal Email Assistant

A sophisticated AI-powered legal email analysis and drafting assistant built with FastAPI, Next.js, and Google Gemini AI. This system analyzes legal emails, extracts structured information, and generates professional legal reply drafts based on contract clauses.

## 🎯 Overview

The Legal Email Assistant is a full-stack application that streamlines the legal email workflow:

1. **Email Analysis** - Parses incoming legal emails and extracts structured information including intent, parties, questions, and urgency
2. **JSON Review** - Allows users to review and edit the extracted analysis in both JSON and visual formats
3. **Contract Integration** - Accepts relevant contract clauses to inform the response
4. **Draft Generation** - Automatically generates professional legal reply emails based on the analysis and contract clauses

## ✨ Features

- **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash for intelligent email parsing
- **Structured Data Extraction**: Extracts intent, parties, agreement references, questions, dates, and urgency levels
- **Interactive Workflow**: Step-by-step UI for reviewing and editing analysis before drafting
- **Contract-Aware Responses**: Generates replies strictly based on provided contract clauses
- **Audit Logging**: Comprehensive logging system for tracking all analysis and drafting operations
- **Modern UI**: Dark-themed, responsive interface with smooth animations
- **Type-Safe**: Full TypeScript support on frontend and Pydantic validation on backend

## 🏗️ Architecture

```
legal-email-assistant/
├── client/                 # Next.js 16 frontend
│   ├── app/               # Next.js app router
│   │   ├── assistant/     # Main assistant page
│   │   └── ...
│   ├── components/        # React components
│   │   ├── ui/           # Shadcn UI components
│   │   └── ...
│   └── lib/              # Frontend utilities and API client
│
└── server/               # FastAPI backend
    ├── core/            # Configuration management
    ├── models/          # Pydantic data models
    ├── modules/         # Core business logic (analyzer, drafter)
    ├── routes/          # API endpoints
    ├── services/        # Service layer
    ├── utils/           # Utility functions
    └── static/          # Audit logs storage
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ and npm
- **Python** 3.11+
- **Google Gemini API Key** (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Backend Setup

1. **Navigate to server directory:**

   ```bash
   cd server
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**

   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   FRONTEND_ORIGIN=http://localhost:3000
   AUDIT_LOG_DIR=static/audit_logs
   ```

5. **Run the server:**

   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to client directory:**

   ```bash
   cd client
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Create `.env.local` file:**

   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

4. **Run the development server:**

   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

## 📖 Usage

1. **Access the application** at `http://localhost:3000/assistant`

2. **Step 1 - Analyze Email:**

   - Paste the legal email text
   - Click "Analyze Email"
   - The AI will extract structured information

3. **Step 2 - Review Analysis:**

   - View and edit the JSON analysis
   - Review the pretty-printed visualization
   - Click "Confirm & Continue"

4. **Step 3 - Provide Contract:**

   - Enter relevant contract clauses
   - Click "Generate Draft Reply"

5. **Step 4 - View Draft:**
   - Review the generated legal reply
   - Copy and use in your email client

## 🔧 API Documentation

### POST `/analyze/`

Analyzes a legal email and returns structured JSON.

**Request:**

```json
{
  "email_text": "Dear Team, regarding the MSA dated 2024-03-15..."
}
```

**Response:**

```json
{
  "intent": "seek clarification",
  "primary_topic": "payment terms",
  "parties": {
    "client": "Company A",
    "counterparty": "Company B"
  },
  "agreement_reference": {
    "type": "Master Service Agreement",
    "date": "2024-03-15"
  },
  "questions": ["What is the payment schedule?", "Are late fees applicable?"],
  "requested_due_date": "2024-03-20",
  "urgency_level": "high"
}
```

### POST `/draft/`

Generates a legal reply email based on analysis and contract clauses.

**Request:**

```json
{
  "email_text": "original email text...",
  "analysis": {
    /* analysis JSON from /analyze */
  },
  "contract_text": "Clause 9.1: Payment terms... Clause 9.2: Late fees..."
}
```

**Response:**

```json
{
  "draft": "Dear Ms. Sharma,\n\nThank you for your email regarding..."
}
```

## 🗂️ Data Models

### AnalysisSchema

```python
{
  "intent": str,                    # e.g., "seek clarification"
  "primary_topic": str,             # e.g., "payment terms"
  "parties": {
    "client": Optional[str],
    "counterparty": Optional[str]
  },
  "agreement_reference": {
    "type": Optional[str],          # e.g., "MSA"
    "date": Optional[str]           # ISO format: YYYY-MM-DD
  },
  "questions": List[str],           # Extracted questions
  "requested_due_date": Optional[str],  # ISO format
  "urgency_level": str              # "low" | "medium" | "high"
}
```

## 🎨 Tech Stack

### Frontend

- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **Shadcn UI** - Component library
- **Lucide React** - Icons
- **React JSON View Lite** - JSON visualization

### Backend

- **FastAPI** - High-performance API framework
- **Pydantic 2** - Data validation
- **Google Gemini AI** - LLM for analysis and drafting
- **LangChain & LangGraph** - AI workflow orchestration
- **Python-dateutil** - Date parsing
- **Jinja2** - Template engine
- **Uvicorn** - ASGI server

## 📝 Environment Variables

### Backend (`.env`)

| Variable          | Description              | Default                 |
| ----------------- | ------------------------ | ----------------------- |
| `GEMINI_API_KEY`  | Google Gemini API key    | Required                |
| `GEMINI_MODEL`    | Gemini model to use      | `gemini-2.5-flash`      |
| `FRONTEND_ORIGIN` | CORS allowed origin      | `http://localhost:3000` |
| `AUDIT_LOG_DIR`   | Directory for audit logs | `static/audit_logs`     |

### Frontend (`.env.local`)

| Variable                  | Description     | Default                 |
| ------------------------- | --------------- | ----------------------- |
| `NEXT_PUBLIC_BACKEND_URL` | Backend API URL | `http://localhost:8000` |

## 🧪 Testing

### Backend Tests

```bash
cd server
pytest
```

### API Testing

Use the provided `test_main.http` file with REST Client extension in VS Code:

```http
### Test analyze endpoint
POST http://localhost:8000/analyze/
Content-Type: application/json

{
  "email_text": "Your test email..."
}
```

## 📊 Audit Logs

All analysis and drafting operations are logged to `server/static/audit_logs/` with timestamps. Each log contains:

- Timestamp
- Operation type (analysis or draft)
- Input data
- Output results
- Processing metadata

## 🔒 Security Considerations

- API keys are stored in environment variables
- CORS is configured for specific origins
- Input validation using Pydantic
- No sensitive data is logged in audit files (configurable)

## 🛠️ Development

### Code Structure

**Backend Modules:**

- `analyzer.py` - Pure LLM-based email analysis
- `drafter.py` - Legal reply generation
- `analyzer_service.py` - Service layer for analysis
- `drafting_service.py` - Service layer for drafting
- `audit_service.py` - Audit logging functionality

**Frontend Components:**

- `EmailInput.tsx` - Email text input
- `ContractInput.tsx` - Contract clauses input
- `JsonViewer.tsx` - JSON visualization
- `DraftPreview.tsx` - Draft output display
- `AuditLogPreview.tsx` - Audit log viewer

### Adding New Features

1. **Backend**: Add routes in `server/routes/`, business logic in `server/modules/`
2. **Frontend**: Add components in `client/components/`, pages in `client/app/`
3. **API Client**: Update `client/lib/api.ts` for new endpoints

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**

```bash
uvicorn main:app --reload --port 8001
```

**CORS errors:**

- Check `FRONTEND_ORIGIN` in `.env`
- Ensure frontend URL matches exactly

**Gemini API errors:**

- Verify API key is correct
- Check API quota limits
- Ensure model name is valid

### Frontend Issues

**API connection failed:**

- Verify backend is running
- Check `NEXT_PUBLIC_BACKEND_URL` in `.env.local`
- Check browser console for CORS errors

**Build errors:**

```bash
rm -rf .next
npm install
npm run dev
```

## 📦 Deployment

### Backend Deployment

**Using Docker:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Environment:**

- Set production `FRONTEND_ORIGIN`
- Use production-grade ASGI server
- Configure proper logging
- Set up monitoring

### Frontend Deployment

**Build for production:**

```bash
npm run build
npm start
```

**Deploy to Vercel:**

```bash
vercel deploy --prod
```

Set environment variables in Vercel dashboard.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is private and proprietary.

## 👥 Authors

- Atharv

## 🙏 Acknowledgments

- Google Gemini AI for powerful language models
- Shadcn for beautiful UI components
- FastAPI team for excellent documentation
- Next.js team for the amazing framework

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check existing documentation
- Review audit logs for debugging

---

**Built with ❤️ using AI-powered technology**
