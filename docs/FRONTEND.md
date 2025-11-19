# Frontend Documentation

## Overview

The Legal Email Assistant frontend is built with **Next.js 16**, **React 19**, and **TypeScript**, providing a modern, type-safe, and responsive user interface for legal email analysis and drafting.

## Tech Stack

- **Next.js 16** - React framework with App Router
- **React 19** - Latest React with improved performance
- **TypeScript 5** - Static type checking
- **Tailwind CSS 4** - Utility-first CSS framework
- **Shadcn UI** - High-quality component library
- **Lucide React** - Icon library
- **React JSON View Lite** - JSON visualization

## Project Structure

```
client/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── assistant/         # Assistant feature
│       └── page.tsx       # Main assistant page
│
├── components/            # React components
│   ├── ui/               # Shadcn UI components
│   │   ├── badge.tsx
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── scroll-area.tsx
│   │   └── textarea.tsx
│   │
│   ├── EmailInput.tsx        # Email text input component
│   ├── ContractInput.tsx     # Contract clauses input
│   ├── JsonViewer.tsx        # JSON visualization
│   ├── DraftPreview.tsx      # Draft output display
│   └── AuditLogPreview.tsx   # Audit log viewer
│
├── lib/                   # Utility functions and API client
│   ├── api.ts            # Backend API client
│   ├── json_converter.ts # JSON parsing utilities
│   └── utils.ts          # Helper functions
│
├── public/               # Static assets
├── components.json       # Shadcn UI configuration
├── next.config.ts        # Next.js configuration
├── tailwind.config.ts    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies and scripts
```

## Key Components

### 1. Assistant Page (`app/assistant/page.tsx`)

The main interface for the email analysis and drafting workflow.

**Features:**

- Step-by-step wizard interface
- State management for multi-step workflow
- Error handling and loading states
- Dark theme with gradient accents

**Component Structure:**

```tsx
export default function IntelligentAssistantPage() {
  // State management
  const [step, setStep] = useState(1);
  const [emailText, setEmailText] = useState("");
  const [analysisJson, setAnalysisJson] = useState("");
  const [analysisObj, setAnalysisObj] = useState<any>(null);
  const [contractText, setContractText] = useState("");
  const [draftOutput, setDraftOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Handlers
  async function handleAnalyze() { /* ... */ }
  async function handleDraft() { /* ... */ }

  return (
    // Step-by-step UI
  );
}
```

**Workflow Steps:**

1. **Step 1**: Email input and analysis
2. **Step 2**: Review and edit JSON analysis
3. **Step 3**: Provide contract clauses
4. **Step 4**: View generated draft

### 2. EmailInput Component

Reusable textarea component for email input.

```tsx
interface EmailInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function EmailInput({ value, onChange }: EmailInputProps) {
  return (
    <Textarea
      placeholder="Paste the legal email here..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="min-h-[300px]"
    />
  );
}
```

### 3. ContractInput Component

Textarea for entering contract clauses.

```tsx
interface ContractInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function ContractInput({ value, onChange }: ContractInputProps) {
  return (
    <Textarea
      placeholder="Paste relevant contract clauses here..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="min-h-[250px]"
    />
  );
}
```

### 4. JsonViewer Component

Visual JSON viewer with syntax highlighting.

```tsx
interface JsonViewerProps {
  data: any;
}

export function JsonViewer({ data }: JsonViewerProps) {
  return (
    <ScrollArea className="h-[400px] rounded-lg border p-4">
      <JsonView data={data} />
    </ScrollArea>
  );
}
```

### 5. DraftPreview Component

Displays the generated draft with copy functionality.

```tsx
interface DraftPreviewProps {
  text: string;
}

export function DraftPreview({ text }: DraftPreviewProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generated Draft</CardTitle>
      </CardHeader>
      <CardContent>
        <pre className="whitespace-pre-wrap">{text}</pre>
      </CardContent>
      <CardFooter>
        <Button onClick={handleCopy}>Copy to Clipboard</Button>
      </CardFooter>
    </Card>
  );
}
```

## API Client (`lib/api.ts`)

Centralized API communication layer.

### Functions

#### `analyzeEmail(emailText: string): Promise<AnalysisResult>`

Calls the backend `/analyze/` endpoint.

```typescript
export async function analyzeEmail(emailText: string): Promise<AnalysisResult> {
  const url = `${BACKEND_URL}/analyze/`;
  const body = { email_text: emailText };

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`Analyze failed: ${res.status}`);
  }

  return await res.json();
}
```

#### `draftReply(emailText: string, analysis: any, contractText: string): Promise<{ draft: string }>`

Calls the backend `/draft/` endpoint.

```typescript
export async function draftReply(
  emailText: string,
  analysis: any,
  contractText: string
): Promise<{ draft: string }> {
  const url = `${BACKEND_URL}/draft/`;
  const body = { email_text: emailText, analysis, contract_text: contractText };

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`Draft failed: ${res.status}`);
  }

  return await res.json();
}
```

## Utilities

### JSON Converter (`lib/json_converter.ts`)

Handles parsing and normalization of JSON data.

```typescript
/**
 * Normalizes various JSON formats to a standard object
 */
export function normalizeToJson(input: string): any {
  try {
    // Try parsing as JSON
    return JSON.parse(input);
  } catch {
    // Try parsing as key-value pairs
    return parseKeyValuePairs(input);
  }
}

function parseKeyValuePairs(text: string): any {
  // Implementation for parsing key: value format
  const lines = text.split("\n");
  const result: any = {};

  for (const line of lines) {
    const match = line.match(/^([^:]+):\s*(.+)$/);
    if (match) {
      result[match[1].trim()] = match[2].trim();
    }
  }

  return result;
}
```

### Utils (`lib/utils.ts`)

Common utility functions including Tailwind class merging.

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merges Tailwind CSS classes intelligently
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Styling

### Tailwind Configuration

The project uses **Tailwind CSS 4** with custom theme configuration.

**Key Features:**

- Dark mode by default
- Custom color palette
- Responsive design utilities
- Animation utilities

### Color Scheme

```css
:root {
  --background: #000000;
  --foreground: #ffffff;
  --card: #171717;
  --card-foreground: #fafafa;
  --primary: #ea580c; /* orange-600 */
  --primary-foreground: #ffffff;
  --accent: #dc2626; /* red-600 */
}
```

### Custom Gradients

```tsx
// Gradient button class
const gradientButtonClass =
  "bg-gradient-to-r from-orange-500 to-red-600 text-white";
```

## State Management

### Local State with Hooks

The application uses React hooks for state management:

```tsx
// Step tracking
const [step, setStep] = useState(1);

// Form data
const [emailText, setEmailText] = useState("");
const [analysisJson, setAnalysisJson] = useState("");
const [contractText, setContractText] = useState("");
const [draftOutput, setDraftOutput] = useState("");

// UI state
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");
```

### State Flow

1. User enters email → `emailText` state
2. Analysis completes → `analysisJson` and `analysisObj` states
3. User reviews/edits → `analysisJson` state updated
4. User enters contract → `contractText` state
5. Draft generated → `draftOutput` state

## Error Handling

### API Error Handling

```tsx
async function handleAnalyze() {
  setLoading(true);
  setError("");

  try {
    const result = await analyzeEmail(emailText);
    setAnalysisObj(result);
    setStep(2);
  } catch (e: any) {
    setError(e.message || "Failed to analyze email.");
  } finally {
    setLoading(false);
  }
}
```

### Error Display

```tsx
{
  error && <p className="text-red-500 font-medium text-center">{error}</p>;
}
```

## Loading States

```tsx
<Button onClick={handleAnalyze} disabled={loading || !emailText}>
  {loading ? "Analyzing..." : "Analyze Email"}
</Button>
```

## Responsive Design

The UI is fully responsive with Tailwind breakpoints:

```tsx
<div className="p-8 md:p-16">
  <main className="max-w-4xl mx-auto">{/* Content */}</main>
</div>
```

**Breakpoints:**

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

## Performance Optimization

### Code Splitting

Next.js automatically code-splits pages and components.

### Client-Side Components

Components using hooks are marked with `"use client"`:

```tsx
"use client";

import { useState } from "react";
// Component code
```

### Image Optimization

Use Next.js `Image` component for optimized images:

```tsx
import Image from "next/image";

<Image src="/logo.png" alt="Logo" width={200} height={50} />;
```

## Environment Variables

Create `.env.local` in the client directory:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

Access in code:

```typescript
const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
```

## Development Workflow

### Running Development Server

```bash
npm run dev
```

Runs at `http://localhost:3000` with hot reload.

### Building for Production

```bash
npm run build
```

Creates optimized production build.

### Starting Production Server

```bash
npm start
```

Runs the production build.

### Linting

```bash
npm run lint
```

## Adding New Features

### 1. Create Component

```tsx
// components/MyComponent.tsx
interface MyComponentProps {
  data: string;
}

export function MyComponent({ data }: MyComponentProps) {
  return <div>{data}</div>;
}
```

### 2. Add to Page

```tsx
import { MyComponent } from "@/components/MyComponent";

// In component
<MyComponent data={someData} />;
```

### 3. Add API Function

```typescript
// lib/api.ts
export async function myNewApiCall(param: string): Promise<Response> {
  const res = await fetch(`${BACKEND_URL}/my-endpoint/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ param }),
  });

  return await res.json();
}
```

## Testing

### Manual Testing Checklist

- [ ] Email analysis works with various email formats
- [ ] JSON editor allows editing and validation
- [ ] Contract input accepts multi-line text
- [ ] Draft generation produces readable output
- [ ] Error messages display correctly
- [ ] Loading states show during API calls
- [ ] Responsive design works on mobile/tablet/desktop

### Browser Testing

Test in:

- Chrome/Edge (Chromium)
- Firefox
- Safari (if on macOS)

## Accessibility

### Keyboard Navigation

All interactive elements are keyboard accessible:

- Tab navigation
- Enter to submit
- Escape to close dialogs

### Screen Reader Support

- Semantic HTML elements
- ARIA labels where needed
- Proper heading hierarchy

### Color Contrast

All text meets WCAG AA standards for color contrast.

## Common Issues

### Issue: API Connection Failed

**Solution:**

1. Verify backend is running
2. Check `NEXT_PUBLIC_BACKEND_URL` in `.env.local`
3. Check browser console for CORS errors

### Issue: Hot Reload Not Working

**Solution:**

```bash
rm -rf .next
npm install
npm run dev
```

### Issue: TypeScript Errors

**Solution:**

```bash
npm run lint
# Fix reported issues
```

### Issue: Styling Not Applied

**Solution:**

1. Check Tailwind classes are correct
2. Verify `globals.css` is imported in `layout.tsx`
3. Clear browser cache

## Best Practices

### 1. Component Organization

- Keep components small and focused
- Use TypeScript interfaces for props
- Extract reusable logic into hooks

### 2. State Management

- Use local state for UI-only state
- Consider Context for shared state
- Keep API calls in dedicated functions

### 3. Error Handling

- Always handle API errors
- Provide user-friendly error messages
- Log errors for debugging

### 4. Performance

- Use React.memo for expensive components
- Implement proper loading states
- Lazy load heavy components

### 5. Code Style

- Use consistent naming conventions
- Follow ESLint rules
- Add comments for complex logic

## Deployment

### Vercel (Recommended)

1. Connect GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

```bash
vercel deploy --prod
```

### Docker

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
RUN npm ci --production

CMD ["npm", "start"]
```

### Environment Variables for Production

```env
NEXT_PUBLIC_BACKEND_URL=https://your-backend-api.com
```

## Security Considerations

### 1. Environment Variables

- Never commit `.env.local`
- Use `NEXT_PUBLIC_` prefix only for client-side variables
- Store sensitive data on backend

### 2. API Security

- Validate all user inputs
- Sanitize data before display
- Use HTTPS in production

### 3. XSS Prevention

- React automatically escapes content
- Be careful with `dangerouslySetInnerHTML`
- Validate JSON before parsing

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Shadcn UI Components](https://ui.shadcn.com)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

---

**Last Updated:** November 19, 2025
