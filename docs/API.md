# API Documentation

## Base URL

```
http://localhost:8000
```

For production, replace with your deployed backend URL.

## Authentication

Currently, the API does not require authentication. For production deployments, implement appropriate authentication mechanisms.

## CORS Configuration

The API accepts requests from the configured `FRONTEND_ORIGIN` (default: `http://localhost:3000`).

---

## Endpoints

### 1. Analyze Email

Parses and analyzes a legal email to extract structured information.

**Endpoint:** `POST /analyze/`

**Tags:** `analysis`

**Request Body:**

```json
{
  "email_text": "string"
}
```

**Parameters:**

| Field        | Type   | Required | Description                                |
| ------------ | ------ | -------- | ------------------------------------------ |
| `email_text` | string | Yes      | The raw text of the legal email to analyze |

**Response:**

```json
{
  "intent": "string",
  "primary_topic": "string",
  "parties": {
    "client": "string | null",
    "counterparty": "string | null"
  },
  "agreement_reference": {
    "type": "string | null",
    "date": "string | null"
  },
  "questions": ["string"],
  "requested_due_date": "string | null",
  "urgency_level": "string"
}
```

**Response Fields:**

| Field                      | Type           | Description                                                                      |
| -------------------------- | -------------- | -------------------------------------------------------------------------------- |
| `intent`                   | string         | The primary intent of the email (e.g., "seek clarification", "request approval") |
| `primary_topic`            | string         | Main topic discussed in the email                                                |
| `parties.client`           | string \| null | Name of the client party                                                         |
| `parties.counterparty`     | string \| null | Name of the counterparty                                                         |
| `agreement_reference.type` | string \| null | Type of agreement (e.g., "MSA", "NDA")                                           |
| `agreement_reference.date` | string \| null | Agreement date in ISO format (YYYY-MM-DD)                                        |
| `questions`                | array[string]  | List of legal questions extracted from the email                                 |
| `requested_due_date`       | string \| null | Requested response date in ISO format (YYYY-MM-DD)                               |
| `urgency_level`            | string         | Urgency level: "low", "medium", or "high"                                        |

**Example Request:**

```http
POST /analyze/
Content-Type: application/json

{
  "email_text": "Dear Legal Team,\n\nI hope this email finds you well. I am writing regarding the Master Service Agreement (MSA) dated March 15, 2024, between ABC Corp and XYZ Ltd.\n\nWe have a few questions that require clarification:\n\n1. What are the payment terms outlined in Section 9.1?\n2. Are there any late payment fees mentioned in the agreement?\n3. Can we request an extension on the delivery timeline?\n\nWe would appreciate a response by March 20, 2024, as we have an upcoming board meeting.\n\nBest regards,\nJohn Smith"
}
```

**Example Response:**

```json
{
  "intent": "seek clarification",
  "primary_topic": "payment terms and delivery timeline",
  "parties": {
    "client": "ABC Corp",
    "counterparty": "XYZ Ltd"
  },
  "agreement_reference": {
    "type": "Master Service Agreement",
    "date": "2024-03-15"
  },
  "questions": [
    "What are the payment terms outlined in Section 9.1?",
    "Are there any late payment fees mentioned in the agreement?",
    "Can we request an extension on the delivery timeline?"
  ],
  "requested_due_date": "2024-03-20",
  "urgency_level": "medium"
}
```

**Status Codes:**

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | Success - Analysis completed            |
| 422  | Validation Error - Invalid request body |
| 500  | Internal Server Error - Analysis failed |

**Error Response:**

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

### 2. Draft Reply

Generates a professional legal reply email based on the analysis and provided contract clauses.

**Endpoint:** `POST /draft/`

**Tags:** `drafting`

**Request Body:**

```json
{
  "email_text": "string",
  "analysis": {
    "intent": "string",
    "primary_topic": "string",
    "parties": {
      "client": "string | null",
      "counterparty": "string | null"
    },
    "agreement_reference": {
      "type": "string | null",
      "date": "string | null"
    },
    "questions": ["string"],
    "requested_due_date": "string | null",
    "urgency_level": "string"
  },
  "contract_text": "string"
}
```

**Parameters:**

| Field           | Type   | Required | Description                                         |
| --------------- | ------ | -------- | --------------------------------------------------- |
| `email_text`    | string | Yes      | The original email text                             |
| `analysis`      | object | Yes      | The structured analysis from `/analyze/` endpoint   |
| `contract_text` | string | Yes      | Relevant contract clauses to reference in the reply |

**Response:**

```json
{
  "draft": "string"
}
```

**Response Fields:**

| Field   | Type   | Description                          |
| ------- | ------ | ------------------------------------ |
| `draft` | string | The generated legal reply email text |

**Example Request:**

```http
POST /draft/
Content-Type: application/json

{
  "email_text": "Dear Legal Team,\n\nI hope this email finds you well. I am writing regarding the Master Service Agreement (MSA) dated March 15, 2024, between ABC Corp and XYZ Ltd.\n\nWe have a few questions that require clarification:\n\n1. What are the payment terms outlined in Section 9.1?\n2. Are there any late payment fees mentioned in the agreement?\n\nWe would appreciate a response by March 20, 2024.\n\nBest regards,\nJohn Smith",
  "analysis": {
    "intent": "seek clarification",
    "primary_topic": "payment terms",
    "parties": {
      "client": "ABC Corp",
      "counterparty": "XYZ Ltd"
    },
    "agreement_reference": {
      "type": "Master Service Agreement",
      "date": "2024-03-15"
    },
    "questions": [
      "What are the payment terms outlined in Section 9.1?",
      "Are there any late payment fees mentioned in the agreement?"
    ],
    "requested_due_date": "2024-03-20",
    "urgency_level": "medium"
  },
  "contract_text": "Clause 9.1 - Payment Terms: Payment shall be made within 30 days of invoice date. All payments must be made via wire transfer.\n\nClause 9.2 - Late Payment Fees: If payment is not received within the specified period, a late fee of 1.5% per month will be applied to the outstanding balance."
}
```

**Example Response:**

```json
{
  "draft": "Dear Mr. Smith,\n\nThank you for your email dated regarding the Master Service Agreement between ABC Corp and XYZ Ltd, executed on March 15, 2024.\n\nI am pleased to address your questions:\n\n1. Payment Terms (Section 9.1): As per Clause 9.1 of the MSA, payment shall be made within 30 days of the invoice date. All payments must be made via wire transfer.\n\n2. Late Payment Fees: Clause 9.2 stipulates that if payment is not received within the specified 30-day period, a late fee of 1.5% per month will be applied to the outstanding balance.\n\nPlease let me know if you require any further clarification on these matters.\n\nBest regards,\n[Your Name]\nLegal Department"
}
```

**Status Codes:**

| Code | Description                                     |
| ---- | ----------------------------------------------- |
| 200  | Success - Draft generated                       |
| 422  | Validation Error - Invalid request body         |
| 500  | Internal Server Error - Draft generation failed |

**Error Response:**

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Data Models

### AnalyzeRequest

```typescript
{
  email_text: string;
}
```

### DraftRequest

```typescript
{
  email_text: string;
  analysis: AnalysisSchema;
  contract_text: string;
}
```

### AnalysisSchema

```typescript
{
  intent: string
  primary_topic: string
  parties: {
    client: string | null
    counterparty: string | null
  }
  agreement_reference: {
    type: string | null
    date: string | null  // ISO format: YYYY-MM-DD
  }
  questions: string[]
  requested_due_date: string | null  // ISO format: YYYY-MM-DD
  urgency_level: "low" | "medium" | "high"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "detail": "Error description"
}
```

Common error scenarios:

1. **Invalid JSON**: Malformed request body
2. **Missing Required Fields**: Required parameters not provided
3. **LLM Failures**: Google Gemini API issues
4. **Validation Errors**: Data doesn't match expected schema

---

## Best Practices

### 1. Email Analysis

- Provide complete email text including headers, body, and signature
- Include all relevant context in the email
- Ensure dates are clearly stated

### 2. Draft Generation

- Always pass the complete analysis object from `/analyze/`
- Provide relevant and accurate contract clauses
- Include specific clause numbers or sections when available

### 3. Error Handling

```typescript
try {
  const analysis = await analyzeEmail(emailText);
  // Process analysis
} catch (error) {
  console.error("Analysis failed:", error.message);
  // Handle error appropriately
}
```

### 4. Performance

- Analysis typically takes 2-5 seconds
- Drafting typically takes 3-6 seconds
- Consider implementing loading states in your UI

---

## Code Examples

### JavaScript/TypeScript

```typescript
// Analyze email
async function analyzeEmail(emailText: string) {
  const response = await fetch("http://localhost:8000/analyze/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email_text: emailText }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

// Draft reply
async function draftReply(
  emailText: string,
  analysis: any,
  contractText: string
) {
  const response = await fetch("http://localhost:8000/draft/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email_text: emailText,
      analysis: analysis,
      contract_text: contractText,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}
```

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Analyze email
def analyze_email(email_text: str):
    response = requests.post(
        f"{BASE_URL}/analyze/",
        json={"email_text": email_text}
    )
    response.raise_for_status()
    return response.json()

# Draft reply
def draft_reply(email_text: str, analysis: dict, contract_text: str):
    response = requests.post(
        f"{BASE_URL}/draft/",
        json={
            "email_text": email_text,
            "analysis": analysis,
            "contract_text": contract_text
        }
    )
    response.raise_for_status()
    return response.json()
```

### cURL

```bash
# Analyze email
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Your email text here..."}'

# Draft reply
curl -X POST "http://localhost:8000/draft/" \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Original email...",
    "analysis": {...},
    "contract_text": "Contract clauses..."
  }'
```

---

## OpenAPI Specification

The FastAPI backend automatically generates OpenAPI documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

Visit these URLs when the server is running to explore the interactive API documentation.

---

## Changelog

### Version 1.0.0 (Current)

- Initial release
- `/analyze/` endpoint for email analysis
- `/draft/` endpoint for reply generation
- Pydantic validation for all inputs/outputs
- Google Gemini AI integration
- Audit logging support

---

## Support

For API-related issues:

1. Check the error message in the response
2. Review the request payload format
3. Verify environment variables are set correctly
4. Check the backend logs for detailed error traces
5. Consult the OpenAPI documentation at `/docs`

---

**Last Updated:** November 19, 2025
