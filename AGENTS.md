# AGENTS.md

# Signova AI - AI Agent Instructions

## 1. Project Overview

**Project Name:** Signova AI  
**Project Type:** AI-powered Indian Sign Language (ISL) Recognition Application

Signova AI is an accessibility-focused application designed to help bridge communication gaps between people who use Indian Sign Language (ISL) and people who do not understand sign language.

The application uses a camera to capture sign gestures, processes them through a suitable pretrained machine learning model, and displays the recognised output as text. Speech output may also be provided where supported.

### Core Objectives

- Recognise supported Indian Sign Language gestures.
- Convert recognised gestures into readable text.
- Provide optional text-to-speech output.
- Build a simple, accessible, and responsive user interface.
- Keep the application modular so additional ISL recognition capabilities can be added later.

**Important:** Do not describe the application as a complete continuous ISL translator unless the selected model and implementation genuinely support continuous sign language interpretation.

---

## 2. Mandatory Instructions for AI Agents

Before making any changes:

1. Inspect the existing project structure.
2. Read this `AGENTS.md` completely.
3. Read the relevant documentation inside the `docs/` directory.
4. Read the specific rules inside `.agents/rules/` and workflows in `.agents/workflows/`.
5. Check the existing implementation before creating new files.
6. Understand the current architecture and dependencies.
7. Identify which features are implemented, partially implemented, or not implemented.
8. Follow the existing coding patterns unless there is a clear reason to change them.

### Important Rules

- Do not unnecessarily rewrite existing code.
- Do not create duplicate components, functions, API routes, or services.
- Do not install unnecessary dependencies.
- Do not replace the selected technology stack without approval.
- Do not invent API endpoints, model outputs, or database fields.
- Do not claim that a feature works without testing it.
- Do not remove existing functionality without approval.
- Do not introduce mock data as real production data.
- Do not expose API keys, passwords, tokens, or secrets.
- Do not make large architectural changes without explaining the reason.
- Do not mark tasks as completed unless they have been implemented and verified.

If an important requirement is unclear, inspect the related documentation and existing code before making assumptions.

---

## 3. Documentation Reading Order

Before implementing a feature, read the relevant documentation.

Recommended reading order:

1. `docs/PRD.md`
2. `docs/PROJECT_OVERVIEW.md`
3. `docs/FEATURES.md`
4. `docs/TECH_STACK.md`
5. `docs/SYSTEM_ARCHITECTURE.md`
6. `docs/AI_MODEL_STRATEGY.md`
7. `docs/PHASE_ROADMAP.md`
8. `docs/UI_UX_GUIDELINES.md`
9. `docs/API_DOCUMENTATION.md`
10. `docs/DATABASE_SCHEMA.md`
11. `docs/TESTING_STRATEGY.md`
12. `docs/SECURITY.md`
13. `docs/DEPLOYMENT.md`
14. `docs/PROGRESS_TRACKER.md`

Do not read every document repeatedly for a small change. Read the documents relevant to the task.

If documentation conflicts with the actual implementation, inspect the code, identify the mismatch, and report it before making a significant change.

---

## 4. Technology Stack

Use the following technologies unless the project documentation or an approved decision specifies otherwise.

### Frontend

- React
- JavaScript (ES6+)
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- Lucide React

### Backend

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn

### AI and Machine Learning

- Python
- PyTorch
- OpenCV
- MediaPipe, when required by the selected model
- NumPy
- Pandas
- scikit-learn

### Speech and Language

- Sarvam AI, where required for supported speech or language features.

### Database

- PostgreSQL, only when persistent storage is required.
- SQLAlchemy, when using relational database access.
- Alembic, for database migrations.

### Testing

- Pytest
- FastAPI TestClient
- HTTPX
- Vitest
- React Testing Library
- Playwright

### Deployment

- Vercel for the frontend.
- Render or another compatible service for the FastAPI backend.

Do not introduce additional technologies without checking whether they solve an actual project requirement.

---

## 5. Coding Standards

### General

- Write clean, readable, maintainable code.
- Use meaningful variable and function names.
- Keep functions focused on one responsibility.
- Avoid unnecessary complexity.
- Handle errors properly.
- Use reusable components and services.
- Avoid duplicated logic.
- Add comments only when they explain non-obvious logic.
- Keep all project files and comments in English.

### Frontend

- Use JavaScript, not TypeScript.
- Use functional React components and hooks.
- Keep components modular.
- Separate API calls from UI components.
- Keep reusable UI elements inside an appropriate components directory.
- Avoid putting the entire application inside one component.
- Use consistent naming conventions.
- Handle loading, error, empty, and success states.
- Ensure the application works on desktop and mobile screens.

### Backend

- Use FastAPI routers to organise API endpoints.
- Keep business logic outside route handlers where appropriate.
- Use Pydantic for request and response validation.
- Use dependency injection where useful.
- Handle exceptions with appropriate HTTP status codes.
- Keep model loading and inference logic separate from API routes.
- Do not block the event loop with long-running inference operations.

### Python

- Follow PEP 8.
- Use type hints where practical.
- Use virtual environments.
- Keep dependencies documented.
- Avoid unnecessary global variables.
- Use structured logging instead of excessive print statements.

---

## 6. Project Architecture

Maintain a clear separation between the frontend, backend, AI model, and supporting services.

### Repository Organisation

The repository is organised into dedicated directories for clear separation of concerns:

- `docs/`: Contains all project specifications, architecture documents, and development guides.
- `.agents/rules/`: Contains agent rules for frontend, backend, AI/ML, and security development.
- `.agents/workflows/`: Contains structured development and implementation workflows.
- `frontend/`: All frontend code, components, pages, state management, and assets.
- `backend/`: FastAPI backend application, API routes, schemas, core services, and AI inference services.
- `models/`: Machine learning model assets, checkpoints, configs, and label mappings.
- `tests/`: Integration and end-to-end tests (`backend/tests/` maintains backend-specific tests).
- `scripts/`: Operational, setup, data, and maintenance scripts.

Expected high-level architecture:

```text
Signova-AI/
│
├── .agents/
│   ├── rules/
│   │   ├── frontend-rules.md
│   │   ├── backend-rules.md
│   │   ├── ai-ml-rules.md
│   │   └── security-rules.md
│   │
│   └── workflows/
│       └── development-workflow.md
│
├── docs/
│   ├── PRD.md
│   ├── PROJECT_OVERVIEW.md
│   ├── FEATURES.md
│   ├── TECH_STACK.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── AI_MODEL_STRATEGY.md
│   ├── PHASE_ROADMAP.md
│   ├── UI_UX_GUIDELINES.md
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   ├── TESTING_STRATEGY.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   └── PROGRESS_TRACKER.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── camera/
│   │   │   └── recognition/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   ├── utils/
│   │   ├── constants/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   │   ├── models/
│   │   │   ├── preprocessing/
│   │   │   ├── inference/
│   │   │   └── postprocessing/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── models/
│   ├── checkpoints/
│   ├── configs/
│   ├── labels/
│   └── README.md
│
├── scripts/
│
├── tests/
│   ├── integration/
│   └── e2e/
│
├── .gitignore
├── .env.example
├── AGENTS.md
├── CONTRIBUTING.md
└── README.md
```

This is the standard repository structure. Place new files, features, and assets into their respective directories.

---

## 7. AI Model Integration Rules

AI model integration is a critical part of Signova AI.

The project should prioritise suitable pretrained Indian Sign Language models rather than training a new model from scratch for the initial prototype.

### Model Selection

Before integrating any model, verify:

- Whether the model supports Indian Sign Language.
- Whether it recognises static signs, dynamic signs, or continuous sign sequences.
- Supported sign classes and labels.
- Model architecture.
- Input format and dimensions.
- Required preprocessing.
- Checkpoint format.
- Python and PyTorch compatibility.
- Hardware requirements.
- Model licence and usage restrictions.
- Availability of inference code and example predictions.

Do not assume that a GitHub repository contains a ready-to-use model checkpoint.

### Model Integration Workflow

Follow this order:

1. Inspect the model repository.
2. Read its README and installation instructions.
3. Identify the model architecture.
4. Locate the pretrained checkpoint.
5. Understand the preprocessing pipeline.
6. Install compatible dependencies.
7. Load the checkpoint.
8. Test inference independently of the web application.
9. Verify the predicted labels.
10. Integrate the working inference pipeline into the backend.
11. Connect the backend to the frontend.
12. Test the complete camera-to-prediction workflow.

### Model Integration Restrictions

- Never assume two different models use the same input format.
- Do not replace model preprocessing with a generic MediaPipe pipeline.
- Do not change input dimensions without verifying model requirements.
- Do not rename or reorder class labels without checking the training configuration.
- Do not load untrusted model checkpoints.
- Do not load an ASL model and present it as an ISL model.
- Do not report accuracy unless supported by actual evaluation results.
- Do not claim real-time performance without measuring inference latency.
- Do not retrain a pretrained model unless explicitly requested.

### Static and Dynamic Sign Recognition

Keep these recognition tasks separate.

**Static recognition:**
- Recognises signs from individual images or frames.
- Suitable for supported static hand gestures and alphabet recognition.

**Dynamic recognition:**
- Requires sequences of frames or extracted temporal features.
- Suitable for supported signs involving movement.

**Continuous sign language interpretation:**
- Requires a model and pipeline capable of interpreting connected signs and their context.
- Must not be claimed based on isolated alphabet or word classification.

If a model supports only static signs, implement only the supported static recognition features in the MVP.

---

## 8. Camera and Recognition Workflow

The expected recognition workflow is:

```text
User Opens Camera
        |
        v
Camera Permission
        |
        v
Capture Frames
        |
        v
Preprocessing
        |
        v
AI Model Inference
        |
        v
Prediction Processing
        |
        v
Recognised Text
        |
        v
Optional Speech Output
```

### Camera Rules

- Request camera permission only when needed.
- Show a clear message when permission is denied.
- Allow the user to start and stop the camera.
- Provide a visible camera status.
- Handle unavailable cameras.
- Handle camera errors gracefully.
- Avoid unnecessary frame processing.
- Do not upload or store camera footage without clear user consent.

### Recognition Rules

- Display the recognised output clearly.
- Handle low-confidence predictions.
- Avoid showing unreliable predictions as confirmed results.
- Prevent unnecessary duplicate predictions.
- Provide a useful message when no supported sign is detected.
- Keep recognition processing separate from UI rendering.

---

## 9. API Development Rules

All API endpoints must follow the actual API design documented in `docs/API_DOCUMENTATION.md`.

### Rules

- Use REST APIs where appropriate.
- Use WebSockets only when real-time communication requires them.
- Validate incoming requests.
- Return consistent response structures.
- Use meaningful HTTP status codes.
- Handle invalid requests.
- Handle model loading and inference errors.
- Avoid exposing internal stack traces.
- Keep API documentation updated when endpoints change.

Do not create endpoints based only on assumptions.

If an endpoint is not documented or implemented, identify the requirement before adding it.

---

## 10. Database Rules

PostgreSQL is optional.

Do not introduce a database simply because it appears in the technology stack.

First identify whether the feature needs persistent information.

Examples of data that may require storage:

- User accounts.
- User preferences.
- Recognition history, with user consent.
- Application settings.
- Learning resources.

### Database Rules

- Use SQLAlchemy for relational database access.
- Use Alembic for schema migrations.
- Use UUID identifiers where appropriate.
- Validate all database inputs.
- Avoid storing raw camera footage by default.
- Do not store sensitive information unnecessarily.
- Never hardcode database credentials.
- Keep development and production database configurations separate.

---

## 11. UI/UX Design Rules

The application must feel modern, accessible, simple, and professional.

### Design Principles

- Clean and minimal interface.
- Consistent spacing.
- Clear visual hierarchy.
- Readable typography.
- Responsive layouts.
- Accessible colour contrast.
- Clear interaction feedback.
- Consistent component styling.
- Avoid unnecessary animations.
- Avoid cluttered dashboards.

### Important UI States

Every major feature should consider:

- Default state.
- Loading state.
- Success state.
- Error state.
- Empty state.
- Permission denied state.
- Camera unavailable state.
- Model unavailable state.

### Accessibility

- Use semantic HTML.
- Provide labels for interactive controls.
- Support keyboard navigation.
- Use accessible contrast.
- Provide clear error messages.
- Do not rely only on colour to communicate status.
- Make important actions easy to understand.

Follow `docs/UI_UX_GUIDELINES.md`.

---

## 12. Security and Privacy Rules

Security and user privacy must be considered in every implementation.

### API Keys and Secrets

- Never place API keys in frontend source code.
- Store secrets in environment variables.
- Never commit `.env` files.
- Maintain a `.env.example` file with placeholder values.
- Keep provider credentials on the backend.

### Camera Privacy

- Ask permission before camera access.
- Make camera usage visible.
- Provide a stop-camera option.
- Do not save camera recordings by default.
- Do not transmit camera data to external services without a clear reason and user consent.

### Backend Security

- Validate incoming data.
- Restrict CORS to approved origins.
- Apply rate limits where appropriate.
- Avoid exposing internal errors.
- Protect user-specific records.
- Validate file uploads.
- Secure WebSocket connections when used.

### Model Security

- Use trusted model sources.
- Review model licences.
- Avoid loading untrusted pickle checkpoints.
- Prefer safer formats such as Safetensors when supported.
- Do not expose private model files or credentials.

Follow `docs/SECURITY.md`.

---

## 13. Error Handling

All major application services must handle failures safely.

Examples:

| Situation | Expected Behaviour |
|---|---|
| Camera permission denied | Show permission guidance |
| Camera unavailable | Show a clear error |
| Backend unavailable | Display connection error |
| Model not loaded | Return a controlled error |
| Invalid input | Return validation error |
| Unsupported sign | Show no supported sign detected |
| Low confidence | Avoid presenting an uncertain prediction as confirmed |
| Speech service unavailable | Keep recognised text available |
| Database unavailable | Handle the failure without exposing internal details |

Never silently ignore important errors.

---

## 14. Testing Requirements

Every major feature must be tested before it is considered complete.

### Frontend

- Component rendering.
- User interactions.
- Camera permission states.
- Loading and error states.
- API integration.
- Responsive layout.

### Backend

- API request validation.
- API response validation.
- Error handling.
- Model loading.
- Model inference.
- Service integration.

### AI Model

- Checkpoint loading.
- Correct preprocessing.
- Correct class mapping.
- Prediction output.
- Confidence handling.
- Inference latency.
- Unsupported input handling.

### Integration

Test the complete workflow:

```text
Frontend Camera
      |
      v
Backend API
      |
      v
Preprocessing
      |
      v
AI Model
      |
      v
Prediction
      |
      v
Frontend Result
```

Do not report tests as passed unless they have actually been executed.

---

## 15. Development Workflow

Follow this workflow for every feature.

### Step 1: Understand

- Read the relevant documentation.
- Inspect existing code.
- Understand dependencies.
- Identify affected files.

### Step 2: Plan

- Define the required behaviour.
- Identify frontend and backend changes.
- Identify model or database dependencies.
- Identify possible risks.
- Decide which tests are required.

### Step 3: Implement

- Make focused changes.
- Reuse existing components.
- Follow project conventions.
- Avoid unnecessary dependencies.
- Keep frontend and backend responsibilities separate.

### Step 4: Verify

- Run relevant tests.
- Check the application.
- Verify API responses.
- Verify model inference if affected.
- Check error handling.

### Step 5: Document

- Update relevant documentation.
- Update API documentation when endpoints change.
- Update model documentation when model integration changes.
- Update the progress tracker only after verification.

### Step 6: Report

At the end of the task, provide:

1. What was implemented.
2. Files created or modified.
3. Dependencies added or removed.
4. Commands executed.
5. Tests performed and their actual results.
6. Known limitations.
7. Remaining work.

---

## 16. Git and Repository Rules

- Use meaningful branch names.
- Write clear commit messages.
- Do not commit generated files unnecessarily.
- Do not commit secrets.
- Do not commit large model checkpoints unless explicitly required.
- Use `.gitignore` for virtual environments, caches, build outputs, local environment files, and other generated files.
- Do not force-push or rewrite Git history without approval.
- Do not delete branches or tags without approval.

Example commit messages:

```text
feat: add camera capture interface
feat: integrate ISL recognition model
fix: handle camera permission errors
fix: improve prediction confidence handling
test: add recognition API tests
docs: update AI model strategy
refactor: separate model inference service
```

---

## 17. Dependency Management

Before installing a package:

1. Check whether an equivalent package is already installed.
2. Confirm that the package is compatible with the current environment.
3. Check whether it is actively maintained.
4. Check whether it is actually needed.
5. Avoid unnecessary package upgrades.

### Frontend

Use npm and the existing lockfile.

### Backend

Use the existing Python virtual environment and dependency management approach.

Do not create multiple competing dependency files without a clear reason.

---

## 18. Environment Variables

Use environment variables for configuration.

Example `.env.example`:

```env
APP_ENV=development
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

FRONTEND_URL=http://localhost:5173

SARVAM_API_KEY=

DATABASE_URL=

MODEL_PATH=
```

These are example variable names only. Confirm the actual application configuration before using them.

Never commit real credentials.

---

## 19. Performance Guidelines

- Avoid unnecessary React re-renders.
- Avoid processing every camera frame when the model does not require it.
- Use appropriate frame sampling.
- Load the model once when practical.
- Avoid repeatedly loading model weights during inference.
- Keep inference separate from API request validation.
- Monitor memory and GPU usage.
- Measure actual latency before claiming real-time performance.
- Handle backend timeouts and disconnected clients.

Do not optimise code prematurely. First identify the actual bottleneck.

---

## 20. Documentation Maintenance

Update documentation when implementation changes affect:

- Project requirements.
- Features.
- Technology stack.
- System architecture.
- AI model selection.
- Model preprocessing.
- API endpoints.
- Database schema.
- Testing.
- Security.
- Deployment.
- Development progress.

Keep documentation consistent with the actual source code.

Do not leave outdated instructions after changing implementation.

---

## 21. Antigravity Agent Behaviour

When working as an autonomous coding agent:

- Inspect before editing.
- Plan before implementing complex features.
- Work in small, verifiable steps.
- Follow the existing architecture.
- Ask before making major architectural decisions.
- Ask before removing important files or functionality.
- Ask before introducing paid services.
- Ask before changing the selected AI model.
- Do not assume a model is available just because a repository URL exists.
- Do not generate fake test results.
- Do not mark incomplete work as complete.
- Do not modify unrelated files.
- Keep changes easy to review and reverse.

For tasks that can be completed independently, proceed without unnecessary questions.

If blocked by missing credentials, model weights, hardware support, or external services, explain the blocker and provide a safe alternative.

---

## 22. Definition of Done

A task is complete only when:

- The requested feature is implemented.
- The implementation follows the project architecture.
- Existing functionality is not unintentionally broken.
- Relevant tests have been executed.
- Errors are handled.
- Security and privacy requirements are followed.
- Documentation is updated when necessary.
- No secrets or unnecessary generated files are committed.
- Actual limitations are clearly reported.

A feature must not be marked complete simply because its UI has been created.

---

## 23. Final Project Principle

Build Signova AI as a practical, reliable, accessible, and maintainable Indian Sign Language recognition application.

Prioritise:

1. Correct ISL recognition.
2. Reliable pretrained model integration.
3. Simple and accessible user experience.
4. Secure camera and data handling.
5. Accurate text and optional speech output.
6. Tested frontend and backend integration.
7. Clear and maintainable code.

**The main priority is a working and verified application, not unnecessary complexity or impressive-looking but non-functional features.**