# Contributing to Signova AI

Thank you for your interest in contributing to **Signova AI**.

Signova AI is an AI-powered accessibility project focused on recognising supported Indian Sign Language (ISL) gestures and converting them into readable text and optional speech output.

We welcome contributions that improve recognition accuracy, accessibility, performance, usability, security, documentation, and overall application quality.

Please read this guide before making changes.

---

## 1. Code of Conduct

All contributors are expected to:

- Be respectful and professional.
- Communicate clearly and constructively.
- Respect different perspectives and experiences.
- Provide useful feedback.
- Avoid harassment, discrimination, and personal attacks.
- Focus discussions on improving the project.

---

## 2. Before Contributing

Before starting work:

1. Read the root `AGENTS.md`.
2. Read the relevant documentation inside `docs/`.
3. Check existing issues and pull requests.
4. Inspect the current implementation.
5. Understand the feature or bug you want to work on.

Do not duplicate existing work.

For major features or architectural changes, discuss the proposed approach before implementation.

---

## 3. Project Technology Stack

The project uses the following technologies.

| Area | Technology |
|---|---|
| Frontend | React |
| Language | JavaScript (ES6+) |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Backend | Python 3.11 |
| Backend Framework | FastAPI |
| AI Framework | PyTorch |
| Computer Vision | OpenCV |
| Landmark Processing | MediaPipe, when required |
| Data Processing | NumPy, Pandas |
| Database | PostgreSQL, when required |
| Testing | Pytest, Vitest, Playwright |
| Frontend Hosting | Vercel |
| Backend Hosting | Render or compatible platform |

Do not introduce a new technology without explaining why it is needed.

---

## 4. Getting Started

### Prerequisites

Install the required tools:

- Git
- Node.js
- npm
- Python 3.11
- A code editor
- A supported browser
- Webcam for camera-based features

Check your installations:

```bash
git --version
node --version
npm --version
python --version
```

### Clone the Repository

```bash
git clone <repository-url>
cd Signova-AI
```

Replace `<repository-url>` with the actual repository URL.

### Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Use the local URL printed by Vite.

### Backend Setup

Open another terminal and navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies using the repository's existing dependency file:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The exact paths and commands must match the actual repository structure. If the application uses different entry points, follow its existing configuration.

---

## 5. Contribution Areas

Contributions are welcome in the following areas.

### Frontend Development

- React components.
- Camera interface.
- Recognition interface.
- Responsive layouts.
- Accessibility improvements.
- Loading and error states.
- Text and speech output.
- User experience improvements.

### Backend Development

- FastAPI endpoints.
- API validation.
- Model integration.
- Recognition services.
- Prediction processing.
- Error handling.
- Backend performance.

### AI and Machine Learning

- Pretrained ISL model integration.
- Model preprocessing.
- Inference optimisation.
- Prediction confidence handling.
- Model evaluation.
- Recognition testing.
- Dataset documentation.

### Documentation

- Setup guides.
- API documentation.
- Architecture documentation.
- Model integration instructions.
- Testing guides.
- Troubleshooting guides.

### Testing and Quality

- Unit tests.
- Integration tests.
- API tests.
- Frontend tests.
- End-to-end tests.
- Accessibility tests.
- Performance testing.

---

## 6. Branching Strategy

Use meaningful branch names.

| Branch | Purpose |
|---|---|
| `main` | Stable project code |
| `develop` | Integration of ongoing development |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `docs/*` | Documentation changes |
| `test/*` | Testing improvements |
| `refactor/*` | Code restructuring |

Examples:

```bash
git checkout -b feature/camera-interface
git checkout -b feature/isl-model-integration
git checkout -b fix/camera-permission
git checkout -b docs/update-api-documentation
git checkout -b test/recognition-api
```

Do not commit experimental or unfinished changes directly to `main`.

---

## 7. Commit Message Guidelines

Write clear and meaningful commit messages.

Follow this format:

```text
type: short description
```

### Supported Types

| Type | Usage |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting changes |
| `refactor` | Code restructuring |
| `test` | Test changes |
| `perf` | Performance improvements |
| `chore` | Maintenance tasks |
| `build` | Build configuration changes |
| `ci` | CI/CD changes |

### Examples

```bash
git commit -m "feat: add camera capture interface"

git commit -m "feat: integrate pretrained ISL model"

git commit -m "fix: handle camera permission errors"

git commit -m "test: add recognition API tests"

git commit -m "docs: update model integration guide"

git commit -m "refactor: separate inference service"
```

Avoid unclear messages such as:

```text
update
changes
final
new code
fix
```

---

## 8. Coding Guidelines

### JavaScript and React

- Use JavaScript, not TypeScript.
- Use functional components and React hooks.
- Follow existing project naming conventions.
- Keep components small and reusable.
- Avoid unnecessary re-renders.
- Separate API requests from UI components.
- Handle loading, error, and empty states.
- Avoid duplicating existing components.
- Use semantic HTML.
- Ensure responsive behaviour.

### Python and FastAPI

- Follow PEP 8.
- Use meaningful function and variable names.
- Use type hints where practical.
- Use Pydantic for request validation.
- Keep API routes separate from business logic.
- Keep model inference separate from route handlers.
- Handle exceptions properly.
- Avoid unnecessary global state.
- Use structured logging.

### General

- Write readable code.
- Avoid unnecessary complexity.
- Keep functions focused.
- Add comments for non-obvious logic.
- Do not hardcode secrets.
- Avoid unnecessary dependencies.
- Follow the existing architecture.

---

## 9. AI Model Contribution Guidelines

AI and machine learning contributions must follow strict verification rules.

### Model Requirements

Before adding or changing a model, document:

- Model name.
- Source repository.
- Model licence.
- ISL support.
- Supported signs or classes.
- Model architecture.
- Input dimensions.
- Preprocessing requirements.
- Checkpoint format.
- Required dependencies.
- Hardware requirements.
- Inference procedure.
- Evaluation results, if available.

### Pretrained Model Integration

Contributors should:

1. Inspect the original model repository.
2. Verify the model's ISL support.
3. Check its licence.
4. Understand preprocessing.
5. Verify checkpoint compatibility.
6. Test inference independently.
7. Confirm the output labels.
8. Add integration tests.
9. Document limitations.

### Important Restrictions

- Do not present ASL recognition as ISL recognition.
- Do not claim continuous translation from a static classifier.
- Do not report invented accuracy values.
- Do not modify model preprocessing without verification.
- Do not commit large checkpoints without approval.
- Do not upload private datasets or sensitive recordings.
- Do not replace the selected model without explaining the reason.

A model contribution must include enough information for another developer to reproduce its inference process.

---

## 10. Camera and Privacy Guidelines

Camera-based features must respect user privacy.

Contributors must:

- Request camera permission before accessing the camera.
- Provide a clear camera status.
- Allow users to stop camera access.
- Handle permission denial.
- Avoid unnecessary video storage.
- Avoid sending recordings to external services without consent.
- Process frames locally when practical.
- Explain any external processing clearly.

Do not introduce hidden camera or microphone recording.

---

## 11. API Contribution Guidelines

When adding or changing an API endpoint:

- Follow the existing FastAPI architecture.
- Validate request data.
- Use meaningful HTTP status codes.
- Maintain consistent response formats.
- Handle errors safely.
- Update `docs/API_DOCUMENTATION.md`.
- Add relevant automated tests.
- Avoid exposing internal error details.

Do not break existing endpoints without discussing the change.

---

## 12. Testing Requirements

Test all changes before submitting a pull request.

### Frontend

```bash
npm run lint
npm run test
npm run build
```

These commands depend on the scripts configured in `package.json`. Check the available scripts before running them.

### Backend

```bash
pytest
```

Run the relevant tests and confirm the results.

### AI Model

Verify:

- Checkpoint loading.
- Input preprocessing.
- Output shape.
- Correct label mapping.
- Confidence handling.
- Inference errors.
- Inference latency.

### Full Application

Test the complete workflow:

```text
Camera
  |
  v
Frame Capture
  |
  v
Preprocessing
  |
  v
Backend
  |
  v
AI Model
  |
  v
Prediction
  |
  v
Recognised Text
  |
  v
Optional Speech Output
```

Do not report a test as passed unless it was actually executed.

---

## 13. Documentation Guidelines

Update documentation whenever a contribution changes project behaviour or setup.

Relevant files include:

- `docs/PRD.md`
- `docs/PROJECT_OVERVIEW.md`
- `docs/FEATURES.md`
- `docs/TECH_STACK.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/AI_MODEL_STRATEGY.md`
- `docs/API_DOCUMENTATION.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/TESTING_STRATEGY.md`
- `docs/SECURITY.md`
- `docs/DEPLOYMENT.md`
- `docs/PROGRESS_TRACKER.md`

Documentation rules:

- Use Markdown.
- Keep explanations clear.
- Use correct commands.
- Include working examples.
- Do not document unimplemented features as completed.
- Keep documentation consistent with the source code.

---

## 14. Pull Request Guidelines

Before opening a pull request:

1. Make sure your branch is up to date.
2. Review your changes.
3. Remove debugging code.
4. Check for exposed secrets.
5. Run relevant tests.
6. Update documentation.
7. Confirm that unrelated files were not modified.

### Pull Request Title

Use a clear title.

Examples:

```text
feat: add ISL camera recognition interface
fix: improve prediction error handling
docs: update backend setup instructions
test: add model inference tests
```

### Pull Request Description Template

Use the following template:

```markdown
## Summary

Briefly describe the changes.

## Related Issue

Closes #issue-number

## Changes Made

- Change 1
- Change 2
- Change 3

## Testing

- [ ] Frontend tests passed
- [ ] Backend tests passed
- [ ] Build completed
- [ ] Relevant model tests passed

## Screenshots

Add screenshots if the UI has changed.

## Documentation

- [ ] Documentation updated
- [ ] API documentation updated if required

## Checklist

- [ ] Code follows project guidelines
- [ ] No secrets or credentials added
- [ ] No unrelated files changed
- [ ] No unverified claims added
```

Do not mark checklist items as completed unless they are true.

---

## 15. Issue Reporting

When reporting a bug, include:

- A clear title.
- A short description.
- Steps to reproduce.
- Expected behaviour.
- Actual behaviour.
- Browser and operating system.
- Relevant logs or error messages.
- Screenshots where useful.

### Bug Report Template

```markdown
## Bug Description

Describe the issue.

## Steps to Reproduce

1.
2.
3.

## Expected Behaviour

Describe what should happen.

## Actual Behaviour

Describe what happens.

## Environment

- OS:
- Browser:
- Node version:
- Python version:

## Logs or Screenshots

Add relevant information.
```

Do not include API keys, passwords, personal data, or private camera recordings in public issues.

---

## 16. Feature Requests

Before proposing a new feature, explain:

- What problem it solves.
- Who benefits from it.
- How it should work.
- Whether it requires a new model or external service.
- Whether it introduces additional cost.
- How it can be tested.

Prefer features that improve the core ISL recognition experience.

Avoid adding features that increase complexity without a clear benefit.

---

## 17. Security Reporting

Do not publish sensitive security vulnerabilities in public issues.

For security concerns:

- Avoid sharing credentials or private user data.
- Describe the affected component.
- Explain the possible impact.
- Share reproduction steps privately with the project maintainers.

Follow the project's `docs/SECURITY.md` for the security reporting process.

---

## 18. Contribution Checklist

Before submitting a contribution, confirm:

- [ ] I read `AGENTS.md`.
- [ ] I checked the relevant documentation.
- [ ] I inspected the existing implementation.
- [ ] My changes follow the project architecture.
- [ ] I used JavaScript for frontend development.
- [ ] I followed Python coding standards.
- [ ] I tested the changes.
- [ ] I updated documentation where required.
- [ ] I did not commit secrets or credentials.
- [ ] I did not add unnecessary dependencies.
- [ ] I did not make unsupported AI model claims.
- [ ] I described known limitations honestly.

---

## 19. Final Note

Every contribution should help make Signova AI more accurate, accessible, secure, and reliable.

The priority is to build a working and verifiable Indian Sign Language recognition application.

Thank you for contributing to Signova AI.