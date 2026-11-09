# Signova AI Development Workflow

## 1. Purpose

This document defines the standard development workflow for Signova AI.

All developers and AI coding agents must follow this workflow when creating features, fixing bugs, integrating AI models, or modifying existing code.

The main goals are:

- Keep the codebase organised and maintainable.
- Avoid unnecessary changes.
- Verify AI model compatibility before integration.
- Test changes before marking tasks complete.
- Keep documentation aligned with the actual implementation.
- Protect user privacy and application security.

---

## 2. Before Starting Development

Before modifying any files, the coding agent must:

1. Inspect the existing project structure.
2. Read the root `AGENTS.md`.
3. Read the relevant files inside `docs/`.
4. Read the applicable rules from `.agents/rules/`.
5. Check existing components, APIs, services, and utilities.
6. Understand the current implementation before proposing changes.

### Required documentation

| Task | Documents to read |
|---|---|
| General development | `docs/PROJECT_OVERVIEW.md`, `docs/FEATURES.md` |
| Frontend | `docs/UI_UX_GUIDELINES.md`, `.agents/rules/frontend-rules.md` |
| Backend | `docs/SYSTEM_ARCHITECTURE.md`, `.agents/rules/backend-rules.md` |
| AI/ML integration | `docs/AI_MODEL_STRATEGY.md`, `.agents/rules/ai-ml-rules.md` |
| API development | `docs/API_DOCUMENTATION.md` |
| Database changes | `docs/DATABASE_SCHEMA.md` |
| Testing | `docs/TESTING_STRATEGY.md` |
| Security changes | `docs/SECURITY.md`, `.agents/rules/security-rules.md` |
| Deployment | `docs/DEPLOYMENT.md` |
| Project progress | `docs/PROGRESS_TRACKER.md` |

Do not assume that a planned feature or example in documentation already exists in the codebase.

---

## 3. Task Understanding and Planning

Before writing code:

1. Identify the exact task and expected outcome.
2. Identify the files and modules likely to be affected.
3. Check whether existing functionality can be reused.
4. Identify dependencies and possible risks.
5. Check whether the task requires frontend, backend, AI/ML, or database changes.
6. Create a short implementation plan.

For larger tasks, divide the work into small, testable steps.

Do not start implementation when essential requirements are unclear. Ask one focused question when necessary.

---

## 4. Development Workflow

Follow this sequence for every development task:

### Step 1: Inspect

- Inspect the relevant source files.
- Understand existing coding patterns.
- Check dependencies and configuration.
- Identify related tests.
- Avoid duplicating existing functionality.

### Step 2: Plan

- Define the expected behaviour.
- Identify the smallest required changes.
- Decide which modules need updates.
- Define how the changes will be tested.

### Step 3: Implement

- Follow the existing project structure.
- Write modular and reusable code.
- Use clear naming conventions.
- Keep frontend and backend responsibilities separate.
- Handle loading, error, empty, and success states.
- Avoid unrelated refactoring.

### Step 4: Validate

- Run relevant linting and formatting checks.
- Run affected unit and integration tests.
- Test API behaviour.
- Verify frontend interactions.
- Check browser console and backend logs.
- Fix errors introduced by the changes.

### Step 5: Review

- Review the final code changes.
- Check for security and privacy issues.
- Check for unused dependencies and files.
- Verify that no secrets or personal data were exposed.
- Confirm that existing features still work.

### Step 6: Document

- Update relevant documentation.
- Update API documentation when endpoints change.
- Update model documentation when AI behaviour changes.
- Update environment examples when configuration changes.
- Update `docs/PROGRESS_TRACKER.md` only after verifying completion.

### Step 7: Report

Provide a concise summary containing:

- What was implemented.
- Which files were changed.
- Tests and checks performed.
- Test results.
- Known limitations or remaining tasks.

Never claim that a test passed if it was not executed successfully.

---

## 5. Frontend Development Workflow

**Technology:** React, JavaScript, Vite, Tailwind CSS, shadcn/ui and Lucide React.

When developing frontend features:

1. Check whether a reusable component already exists.
2. Follow the established UI design guidelines.
3. Use JavaScript, not TypeScript.
4. Keep components focused and reusable.
5. Use React hooks appropriately.
6. Keep API calls separate from presentation components when practical.
7. Add proper loading, error, empty, and success states.
8. Make layouts responsive.
9. Support keyboard navigation and accessible labels.
10. Test important user interactions.

### Frontend quality checks

- No unnecessary component duplication.
- No hardcoded API secrets.
- No broken navigation.
- No console errors.
- No unhandled API failures.
- No misleading AI recognition results.
- Camera and microphone access must require appropriate user permission.

---

## 6. Backend Development Workflow

**Technology:** Python 3.11, FastAPI, Pydantic and Uvicorn.

When developing backend features:

1. Inspect existing API routes and service modules.
2. Keep routes separate from business logic.
3. Validate all incoming data.
4. Use Pydantic schemas for request and response validation.
5. Add appropriate error handling.
6. Avoid blocking asynchronous endpoints unnecessarily.
7. Keep configuration in environment variables.
8. Protect external API credentials.
9. Add tests for new endpoints and services.
10. Update API documentation.

### Backend quality checks

- Correct HTTP status codes.
- Consistent response structures.
- Input validation.
- Safe exception handling.
- Appropriate logging.
- No exposed credentials.
- No unnecessary database queries.
- No unbounded processing of uploaded media.

---

## 7. AI/ML Integration Workflow

AI/ML functionality is a core part of Signova AI.

Before integrating any model:

1. Identify whether the model supports Indian Sign Language.
2. Confirm whether it recognises static signs, dynamic signs, or continuous sign sequences.
3. Inspect the model architecture.
4. Verify the checkpoint format and loading requirements.
5. Identify the required input format and dimensions.
6. Verify preprocessing requirements.
7. Confirm the class labels and output mapping.
8. Check dependencies and hardware requirements.
9. Test inference independently before connecting it to the API.
10. Document limitations and evaluation results.

### Model integration sequence

```text
Pretrained Model
       |
       v
Architecture Verification
       |
       v
Checkpoint Loading
       |
       v
Input Preprocessing
       |
       v
Model Inference
       |
       v
Output Processing
       |
       v
Prediction + Confidence
       |
       v
FastAPI Integration
       |
       v
React Frontend
```

### Important AI/ML rules

- Do not train a model from scratch unless explicitly approved.
- Do not assume an ASL model supports ISL.
- Do not treat alphabet classification as complete sign-language translation.
- Do not invent model accuracy or performance metrics.
- Do not invent model output labels.
- Handle unsupported signs and low-confidence predictions.
- Verify the actual model before changing its preprocessing pipeline.
- Never load an untrusted checkpoint without appropriate safety checks.
- Do not claim real-time performance without measuring it.

### Model evaluation

Where applicable, evaluate:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Inference latency.
- Per-class performance.
- Performance under different lighting and camera conditions.

Report only measured results.

---

## 8. Database Development Workflow

PostgreSQL is optional and should only be introduced when persistent data is required.

Before making database changes:

1. Check `docs/DATABASE_SCHEMA.md`.
2. Confirm that the feature actually needs persistent storage.
3. Reuse existing database models where possible.
4. Use migrations for schema changes.
5. Validate database input.
6. Apply appropriate access controls.
7. Avoid storing raw camera footage by default.
8. Test database operations.
9. Update the database documentation.

Never introduce a database table or migration without a clear feature requirement.

---

## 9. API Integration Workflow

When connecting the frontend and backend:

1. Confirm the actual API endpoint.
2. Verify the HTTP method and request schema.
3. Verify the response schema.
4. Implement appropriate loading and error states.
5. Handle network failures and timeouts.
6. Validate returned data before displaying it.
7. Test the complete request-response flow.

For real-time features:

- Use WebSockets only when needed.
- Validate connection permissions.
- Handle connection interruptions.
- Release resources when the session ends.
- Avoid sending unnecessary video frames.

Do not create frontend API calls for endpoints that have not been implemented.

---

## 10. External AI Service Integration

Signova AI may use external services such as Sarvam AI for supported speech and language features.

Before integrating an external service:

1. Confirm that the service supports the required task.
2. Read the current provider documentation.
3. Verify the request and response formats.
4. Store API keys on the backend.
5. Handle API failures and rate limits.
6. Avoid sending unnecessary personal information.
7. Document provider dependencies and limitations.

Important distinction:

Sarvam AI can support speech and language processing. It does not independently perform ISL gesture recognition.

Keep sign recognition and speech processing as separate responsibilities.

---

## 11. Testing Workflow

Run the appropriate tests after implementation.

| Area | Recommended tools |
|---|---|
| Backend | Pytest |
| API | FastAPI TestClient, HTTPX |
| Frontend | Vitest |
| React components | React Testing Library |
| End-to-end | Playwright |
| Code quality | Ruff, ESLint |
| ML evaluation | scikit-learn metrics |

### Minimum testing requirements

- Test new functionality.
- Test expected failure cases.
- Test invalid inputs.
- Test API responses.
- Test important frontend interactions.
- Test model loading and inference separately.
- Run relevant regression tests.

Do not skip tests silently. If a test cannot run, report the reason.

---

## 12. Security and Privacy Workflow

Every feature must follow `docs/SECURITY.md` and `.agents/rules/security-rules.md`.

Required practices:

- Request camera and microphone permission appropriately.
- Process camera data only for the required functionality.
- Do not store raw recordings by default.
- Never expose API keys in frontend code.
- Validate uploaded images and videos.
- Protect API endpoints.
- Apply appropriate CORS settings.
- Avoid logging sensitive user information.
- Keep dependencies updated.
- Do not commit `.env` files or secrets.

---

## 13. Git Workflow

Use clear, meaningful commits.

Suggested commit prefixes:

| Prefix | Usage |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `test:` | Tests |
| `chore:` | Configuration or maintenance |
| `perf:` | Performance improvement |
| `security:` | Security improvement |

Examples:

```bash
git add .
git commit -m "feat: add ISL recognition interface"

git commit -m "fix: handle low-confidence predictions"

git commit -m "docs: update AI model strategy"
```

Before committing:

- Review changed files.
- Remove debug statements.
- Check for secrets.
- Run relevant tests.
- Ensure generated files are not committed unnecessarily.

Do not create commits or push changes unless explicitly requested.

---

## 14. Environment and Dependency Management

- Use Python 3.11 for backend development.
- Use the existing Node.js and npm versions unless a verified compatibility issue requires a change.
- Use a Python virtual environment.
- Keep dependencies documented.
- Pin versions where appropriate.
- Avoid unnecessary packages.
- Do not upgrade major dependencies without checking compatibility.
- Keep `.env.example` updated without real credentials.

Example setup:

```bash
# Backend
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

# Frontend
npm install
npm run dev
```

Use the actual scripts and dependency files present in the repository. Do not assume these commands are already configured.

---

## 15. Performance and Resource Management

Signova AI should work within practical hardware and hosting limits.

- Avoid loading the same model repeatedly.
- Load model weights once when appropriate.
- Release camera and video resources.
- Avoid unnecessary image processing.
- Measure inference latency.
- Optimise only after measuring bottlenecks.
- Consider CPU and GPU availability.
- Avoid adding infrastructure without a clear need.

Do not promise a specific frame rate or response time without testing.

---

## 16. AI Coding Agent Rules

When using Antigravity or another AI coding agent:

1. Read `AGENTS.md` before starting.
2. Read the relevant `.agents/rules/` files.
3. Follow the selected project stack.
4. Inspect existing files before editing.
5. Make focused changes.
6. Do not rewrite unrelated modules.
7. Do not create duplicate components or services.
8. Do not invent APIs, datasets, models, or metrics.
9. Do not remove existing functionality without approval.
10. Do not install unnecessary dependencies.
11. Run tests after implementation.
12. Report incomplete work honestly.

### Approval required before

Ask the user before:

- Replacing the selected ML model.
- Changing the main technology stack.
- Introducing paid services.
- Adding major infrastructure.
- Removing important existing features.
- Changing authentication or data-storage policies.
- Making destructive database or file changes.

---

## 17. Definition of Done

A task can be marked complete only when:

- [ ] Requirements are understood.
- [ ] Existing code has been inspected.
- [ ] Relevant project rules have been followed.
- [ ] Implementation is complete.
- [ ] Relevant tests have been executed.
- [ ] Tests pass, or remaining failures are clearly reported.
- [ ] No known security issue was introduced.
- [ ] Documentation is updated where required.
- [ ] No unrelated changes were made.
- [ ] Final implementation summary is provided.

If any required item is incomplete, mark the task as partially complete instead.

---

## 18. Final Development Principle

Build Signova AI incrementally.

Prioritise a working, tested ISL recognition flow over unnecessary features or complex architecture.

**Understand → Plan → Implement → Test → Review → Document → Report.**

Every change must improve the application without introducing unnecessary complexity.