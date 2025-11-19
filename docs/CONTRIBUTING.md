# Contributing Guide

Thank you for considering contributing to the Legal Email Assistant! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Issue Guidelines](#issue-guidelines)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Node.js 20+
- Python 3.11+
- Git
- A code editor (VS Code recommended)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/legal-email-assistant.git
cd legal-email-assistant
```

3. Add upstream remote:

```bash
git remote add upstream https://github.com/original-owner/legal-email-assistant.git
```

### Setup Development Environment

Follow the instructions in [SETUP.md](./SETUP.md) to set up your development environment.

## Development Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch Naming Convention:**

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

### 2. Make Changes

- Write clear, concise code
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Changes

```bash
git add .
git commit -m "Type: Brief description

Detailed explanation of changes (if needed)"
```

**Commit Message Format:**

```
Type: Brief description (max 50 chars)

Detailed explanation (if needed):
- What changed
- Why it changed
- Any breaking changes

Closes #issue-number (if applicable)
```

**Types:**

- `Feature:` - New feature
- `Fix:` - Bug fix
- `Docs:` - Documentation changes
- `Style:` - Code style changes (formatting, etc.)
- `Refactor:` - Code refactoring
- `Test:` - Adding or updating tests
- `Chore:` - Maintenance tasks

### 4. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push Changes

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Code Style

Follow [PEP 8](https://pep8.org/) guidelines:

```python
# Good
def analyze_email(email_text: str) -> dict:
    """
    Analyze email and extract structured information.

    Args:
        email_text: The raw email text to analyze

    Returns:
        Dictionary containing analysis results
    """
    result = perform_analysis(email_text)
    return result


# Bad
def AnalyzeEmail(emailText):
    result=perform_analysis(emailText)
    return result
```

**Key Points:**

- Use snake_case for functions and variables
- Use PascalCase for classes
- Maximum line length: 100 characters
- Use type hints
- Write docstrings for all functions/classes
- Use f-strings for string formatting

### TypeScript/JavaScript Code Style

Follow standard TypeScript conventions:

```typescript
// Good
interface EmailInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function EmailInput({ value, onChange }: EmailInputProps) {
  return <Textarea value={value} onChange={(e) => onChange(e.target.value)} />;
}

// Bad
export function emailInput(props) {
  return (
    <Textarea
      value={props.value}
      onChange={(e) => props.onChange(e.target.value)}
    />
  );
}
```

**Key Points:**

- Use PascalCase for components and interfaces
- Use camelCase for functions and variables
- Use const for immutable values
- Prefer arrow functions
- Use destructuring for props
- Add proper type annotations

### React Component Guidelines

```tsx
// Prefer functional components with hooks
export function MyComponent({ prop1, prop2 }: Props) {
  const [state, setState] = useState(initialValue);

  useEffect(() => {
    // Side effects
  }, [dependencies]);

  return <div className="container">{/* JSX */}</div>;
}

// Use meaningful names
// ✅ Good
const [isLoading, setIsLoading] = useState(false);
const [emailText, setEmailText] = useState("");

// ❌ Bad
const [loading, setLoading] = useState(false);
const [text, setText] = useState("");
```

### File Organization

**Backend:**

```
server/
├── routes/          # API endpoints
├── services/        # Business logic orchestration
├── modules/         # Core business logic
├── models/          # Data models
└── utils/           # Utility functions
```

**Frontend:**

```
client/
├── app/             # Next.js pages
├── components/      # React components
│   └── ui/         # Reusable UI components
└── lib/            # Utility functions and API client
```

## Testing Guidelines

### Backend Tests

Use `pytest` for testing:

```python
# test_analyzer.py
import pytest
from modules.analyzer import analyze_email

def test_analyze_email_basic():
    """Test basic email analysis."""
    email_text = "Test email content"
    result = analyze_email(email_text)

    assert "intent" in result
    assert "primary_topic" in result
    assert isinstance(result["questions"], list)

def test_analyze_email_with_date():
    """Test date extraction."""
    email_text = "Please respond by 2024-03-15"
    result = analyze_email(email_text)

    assert result["requested_due_date"] == "2024-03-15"

@pytest.mark.asyncio
async def test_analyze_service():
    """Test analyzer service."""
    from services.analyzer_service import analyze_email_service
    result = await analyze_email_service("Test email")
    assert result is not None
```

**Running Tests:**

```bash
cd server
pytest
pytest -v  # Verbose output
pytest test_analyzer.py  # Specific file
pytest -k "test_analyze"  # Tests matching pattern
```

### Frontend Tests (Future)

Consider adding:

- Unit tests with Jest
- Component tests with React Testing Library
- E2E tests with Playwright

## Pull Request Process

### Before Submitting

1. **Test your changes:**

   ```bash
   # Backend
   cd server
   pytest

   # Frontend
   cd client
   npm run lint
   npm run build
   ```

2. **Update documentation:**

   - Update README.md if needed
   - Update API.md for API changes
   - Add JSDoc/docstrings for new functions

3. **Check code style:**

   ```bash
   # Python
   black server/
   isort server/

   # TypeScript
   npm run lint
   ```

### Submitting PR

1. Push your branch to your fork
2. Create Pull Request on GitHub
3. Fill out the PR template:

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

How has this been tested?

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings generated
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

### After Merge

1. Delete your feature branch:

   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

2. Update your local main:
   ```bash
   git checkout main
   git pull upstream main
   ```

## Issue Guidelines

### Reporting Bugs

Use the bug report template:

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:

1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment:**

- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

### Suggesting Features

Use the feature request template:

```markdown
**Is your feature related to a problem?**
Description of the problem

**Describe the solution**
Your proposed solution

**Alternatives considered**
Other approaches you've thought about

**Additional context**
Mockups, examples, etc.
```

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## Code Review Guidelines

### For Contributors

- Respond to feedback promptly
- Be open to suggestions
- Ask questions if unclear
- Don't take criticism personally

### For Reviewers

- Be constructive and respectful
- Explain the "why" behind suggestions
- Acknowledge good work
- Focus on code, not the person

## Development Tools

### Recommended VS Code Extensions

- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens
- Thunder Client (API testing)

### Useful Commands

```bash
# Backend
cd server
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd client
npm install
npm run dev
npm run build
npm run lint

# Git
git status
git diff
git log --oneline
git stash
git stash pop
```

## Questions?

If you have questions:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with the `question` label
4. Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉
