# Backend Development Rules

## Signova AI

**Project:** Signova AI  
**Backend Framework:** FastAPI  
**Language:** Python 3.11  
**AI Framework:** PyTorch  
**API Style:** REST  
**Development Approach:** Backend First, Modular, Local Development First

---

# 1. Core Backend Principles

All backend development must follow these rules:

1. Use Python 3.11.
2. Use FastAPI for backend APIs.
3. Keep API routes separate from business logic.
4. Keep AI model code separate from API code.
5. Use Pydantic for request and response validation.
6. Use environment variables for configuration.
7. Handle errors consistently.
8. Write testable and maintainable code.
9. Avoid unnecessary dependencies.
10. Do not implement features outside the agreed project scope.

---

# 2. Backend Architecture

Follow a modular architecture.

```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── models.py
│   │   │   └── recognition.py
│   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   └── recognition.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   └── model_service.py
│   │
│   └── main.py
│
├── tests/
├── requirements.txt
└── .env.example
```

This is the suggested structure. Inspect the existing repository before creating folders or files. Reuse existing modules where possible.

---

# 3. FastAPI Rules

- Use FastAPI for all backend HTTP endpoints.
- Keep route handlers small.
- Use `APIRouter` to organise routes.
- Add request and response schemas.
- Use dependency injection where appropriate.
- Add API documentation through FastAPI's OpenAPI support.
- Use suitable HTTP status codes.
- Add clear endpoint descriptions.
- Avoid placing model inference logic directly inside route handlers.

The backend must start through a clear application entry point.

---

# 4. API Design Rules

Use a consistent API prefix:

```text
/api/v1
```

Planned endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Backend health |
| GET | `/api/v1/ai/health` | AI service status |
| GET | `/api/v1/ai/models` | Available model information |
| POST | `/api/v1/ai/predict/image` | Image prediction, only if supported |
| POST | `/api/v1/ai/predict/video` | Video prediction, only if supported |
| POST | `/api/v1/ai/predict/landmarks` | Landmark or pose prediction, only if supported |

These endpoints are planned API contracts. Do not expose an endpoint as functional until its implementation and underlying model pipeline are ready.

### API Requirements

- Use meaningful endpoint names.
- Validate every request.
- Return predictable JSON.
- Keep response formats consistent.
- Document required fields.
- Set reasonable request size limits.
- Handle unsupported input types.
- Avoid exposing internal file paths.

---

# 5. Request and Response Validation

Use Pydantic models for API validation.

Example:

```python
from pydantic import BaseModel, Field


class RecognitionRequest(BaseModel):
    model_id: str = Field(min_length=1)
    input_type: str
```

### Validation Rules

- Validate required fields.
- Validate data types.
- Validate supported input formats.
- Validate input dimensions where relevant.
- Reject invalid requests with useful errors.
- Never silently accept malformed input.
- Do not trust frontend validation alone.

Validation must match the actual model's requirements.

---

# 6. AI Integration Rules

The backend must communicate with AI modules through service and adapter layers.

Recommended flow:

```text
API Route
    |
    v
AI Service
    |
    v
Model Service
    |
    v
Model Adapter
    |
    v
Preprocessing
    |
    v
Inference
    |
    v
Postprocessing
    |
    v
API Response
```

### Strict Requirements

- Do not load models inside individual API requests.
- Load models during startup or through controlled lazy loading.
- Reuse loaded models.
- Keep preprocessing outside route handlers.
- Keep inference outside route handlers.
- Validate model availability before prediction.
- Handle model failures.
- Return real model output only.
- Never hardcode example predictions as production results.

### Model Compatibility

Before connecting a model, verify:

- Supported sign language.
- Input type.
- Input shape.
- Landmark format, if applicable.
- Preprocessing requirements.
- Checkpoint configuration.
- Output format.

Do not assume that a model supporting image classification can perform continuous ISL translation.

---

# 7. Error Handling

Use consistent error responses.

Recommended structure:

```json
{
  "success": false,
  "error": {
    "code": "MODEL_UNAVAILABLE",
    "message": "The recognition model is currently unavailable."
  }
}
```

Handle these conditions:

- Invalid request.
- Unsupported input format.
- Missing input.
- Model unavailable.
- Model loading failure.
- Preprocessing failure.
- Inference failure.
- Invalid model output.
- Request too large.
- Internal server error.

### Rules

- Use appropriate HTTP status codes.
- Do not expose stack traces to frontend users.
- Log technical details on the backend.
- Return clear and safe error messages.
- Do not convert errors into successful responses.

---

# 8. Configuration and Environment Variables

Keep configuration centralised.

Use environment variables for:

- Application environment.
- API host and port.
- CORS origins.
- Model directory.
- Model checkpoint.
- Device selection.
- Logging level.
- Optional database connection.

Example `.env.example`:

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

CORS_ORIGINS=http://localhost:5173

MODEL_DIR=../models
MODEL_DEVICE=auto

LOG_LEVEL=INFO
```

### Configuration Rules

- Never commit `.env`.
- Keep `.env.example` free of secrets.
- Do not hardcode machine-specific paths.
- Validate required configuration at startup.
- Use sensible development defaults.
- Do not expose secrets through API responses or logs.

---

# 9. CORS Rules

Configure CORS for the frontend origin.

Development frontend:

```text
http://localhost:5173
```

Requirements:

- Allow only required origins.
- Configure required HTTP methods.
- Configure required headers.
- Do not use unrestricted CORS in production.
- Keep production origins in environment configuration.

---

# 10. File and Input Handling

When accepting images or videos:

- Validate file extensions.
- Validate MIME types.
- Check file size.
- Avoid trusting filenames.
- Use safe temporary file handling.
- Reject unsupported formats.
- Clean up temporary files.
- Avoid storing user media unless explicitly required.

Do not record or persist webcam footage by default.

For landmark input, validate the structure and dimensions expected by the selected model.

---

# 11. Camera and Privacy Rules

The browser should handle camera permission and camera capture.

The backend should receive only the input required for recognition.

Requirements:

- Do not request camera access from the backend.
- Do not store camera footage by default.
- Do not log image or video contents.
- Do not expose uploaded media publicly.
- Process temporary files safely.
- Clearly document any future data storage feature.

---

# 12. Logging Rules

Use Python's logging module.

Log important backend events:

- Application startup.
- Application shutdown.
- Model loading.
- Model availability.
- Prediction requests.
- Processing failures.
- Unexpected exceptions.

Do not log:

- Secrets.
- Authentication tokens.
- Full user media.
- Sensitive personal information.
- Unnecessary request payloads.

Use appropriate logging levels:

| Level | Usage |
|---|---|
| DEBUG | Development details |
| INFO | Normal application events |
| WARNING | Recoverable problems |
| ERROR | Failed operations |
| CRITICAL | Serious application failures |

---

# 13. Performance Rules

- Load models once and reuse them.
- Avoid unnecessary file operations.
- Validate inputs before expensive processing.
- Avoid unnecessary frame processing.
- Use suitable request limits.
- Monitor CPU and GPU memory.
- Avoid blocking unrelated requests with long-running tasks.
- Use asynchronous endpoints when they provide a real benefit.

Do not add background workers or queues unless the actual workload requires them.

---

# 14. Database Rules

PostgreSQL is optional for the initial MVP.

Do not add a database dependency unless a required feature needs persistent storage.

If a database is introduced:

- Keep database logic separate from API routes.
- Use environment-based connection settings.
- Use parameterised queries or a suitable ORM.
- Validate stored data.
- Handle connection failures.
- Do not store raw camera footage by default.
- Use migrations for schema changes.

Basic recognition must not depend on a database.

---

# 15. Security Rules

- Validate all incoming requests.
- Limit upload sizes.
- Restrict CORS.
- Keep secrets outside source code.
- Avoid exposing internal paths.
- Avoid exposing stack traces.
- Keep dependencies updated.
- Restrict file access.
- Handle temporary files safely.
- Use HTTPS in production.
- Add rate limiting when deployment requirements justify it.

Do not add authentication unless it is part of the approved product scope.

---

# 16. Testing Rules

Use Pytest for backend tests.

Test these areas:

- Application startup.
- Health endpoints.
- API request validation.
- Response schemas.
- Error responses.
- CORS configuration.
- AI service behaviour.
- Model loading failures.
- Input preprocessing.
- Inference integration.
- File upload validation.

Use mocked AI services for API tests when actual model weights are unavailable.

Clearly distinguish mocked tests from real model inference tests.

---

# 17. Dependency Management

Keep dependencies in `requirements.txt`.

Rules:

- Install only required packages.
- Avoid duplicate dependencies.
- Use compatible package versions.
- Do not install packages without a clear reason.
- Keep development-only dependencies separate when practical.
- Verify imports after dependency changes.
- Document important version requirements.

Do not upgrade PyTorch or other major AI dependencies without checking model compatibility.

---

# 18. Development Workflow

Follow this order:

### Phase 1: Backend Foundation

- Set up Python environment.
- Install backend dependencies.
- Create FastAPI application.
- Configure settings.
- Add health endpoint.
- Verify local server startup.

### Phase 2: API Structure

- Add API versioning.
- Create route modules.
- Add Pydantic schemas.
- Configure CORS.
- Add error handling.

### Phase 3: AI Service

- Create the AI service layer.
- Integrate the verified model adapter.
- Add model loading.
- Add input validation.
- Add inference handling.

### Phase 4: Testing

- Test backend endpoints.
- Test request validation.
- Test model loading.
- Test inference with compatible samples.
- Test error handling.

### Phase 5: Frontend Connection

- Connect React frontend.
- Use Fetch API or Axios.
- Handle loading states.
- Handle API errors.
- Display actual prediction results.

---

# 19. Strict Rules for Antigravity

Before making backend changes:

1. Inspect the existing backend.
2. Read the relevant project documentation.
3. Reuse existing working code.
4. Do not create duplicate services or routes.
5. Do not delete existing files without approval.
6. Do not change AI model logic unnecessarily.
7. Do not put all backend code in `main.py`.
8. Do not place model inference inside API routes.
9. Do not invent API responses.
10. Do not claim an endpoint works without testing it.
11. Do not install unnecessary dependencies.
12. Do not commit secrets or model weights.
13. Keep code, comments, and tests in English.
14. Update relevant documentation when API contracts change.

If a requirement is unclear, inspect the existing implementation and report the uncertainty before making a risky change.

---

# 20. Final Backend Goal

The Signova AI backend must be:

- Modular.
- Secure.
- Testable.
- Maintainable.
- Efficient.
- Compatible with verified AI models.
- Independent from frontend implementation.

**The backend must return genuine model results and clearly report failures or unsupported capabilities.**