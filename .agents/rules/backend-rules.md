# Backend Development Rules

# Signova AI

These rules apply to all backend development, API creation, business logic, AI model integration, inference processing, database operations, security, and backend deployment in Signova AI.

The primary goal is to build a reliable, secure, modular, and maintainable backend that supports Indian Sign Language recognition.

---

## 1. Backend Technology Stack

Use the following technologies unless an approved project decision changes them.

| Category | Technology |
|---|---|
| Language | Python 3.11 |
| Backend Framework | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic |
| AI Framework | PyTorch |
| Computer Vision | OpenCV |
| Landmark Processing | MediaPipe, when required |
| Numerical Processing | NumPy |
| Data Processing | Pandas |
| ML Utilities | scikit-learn |
| Database | PostgreSQL, when required |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Testing | Pytest |
| API Testing | HTTPX / FastAPI TestClient |

### Strict Rules

- Use Python 3.11.
- Use FastAPI for backend APIs.
- Use Pydantic for request and response validation.
- Use PyTorch for supported model inference.
- Use Uvicorn as the ASGI development server.
- Keep model inference separate from API route handlers.
- Do not introduce unnecessary frameworks.
- Do not replace the selected backend stack without approval.

---

## 2. Backend Project Structure

Follow the existing repository structure.

A recommended structure is:

```text
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       ├── recognition.py
│   │       └── speech.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── schemas/
│   │   ├── recognition.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── recognition_service.py
│   │   ├── preprocessing_service.py
│   │   └── speech_service.py
│   │
│   ├── ml/
│   │   ├── model_loader.py
│   │   ├── inference.py
│   │   ├── preprocessing.py
│   │   └── postprocessing.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   └── utils/
│       └── validators.py
│
├── models/
│   └── .gitkeep
│
├── tests/
│   ├── test_health.py
│   ├── test_recognition.py
│   └── test_services.py
│
├── .env.example
├── requirements.txt
└── README.md
```

This is a recommended structure, not a requirement to create every file immediately.

### Structure Rules

- API routes belong inside `api/routes/`.
- Request and response schemas belong inside `schemas/`.
- Business logic belongs inside `services/`.
- Model loading belongs inside `ml/model_loader.py`.
- Model inference belongs inside `ml/inference.py`.
- Preprocessing must be isolated from API routes.
- Database logic belongs inside `database/`.
- Shared configuration belongs inside `core/`.
- Tests belong inside `tests/`.

Do not create unnecessary directories or duplicate existing modules.

---

## 3. Backend Architecture

Maintain separation between the API, business logic, AI model, and database.

Expected request flow:

```text
Frontend
   |
   v
FastAPI API Route
   |
   v
Request Validation
   |
   v
Recognition Service
   |
   v
Preprocessing Service
   |
   v
AI Model Inference
   |
   v
Postprocessing
   |
   v
Response Validation
   |
   v
Frontend
```

### Architecture Rules

- Keep API endpoints lightweight.
- Do not place model implementation directly inside route handlers.
- Keep business logic inside service modules.
- Keep preprocessing and postprocessing independently testable.
- Keep model loading separate from inference.
- Avoid circular imports.
- Avoid unnecessary abstraction layers.
- Keep services independently testable.

---

## 4. Python Coding Standards

Follow PEP 8.

### Rules

- Use meaningful variable names.
- Use descriptive function names.
- Use type hints where practical.
- Keep functions focused on one responsibility.
- Use clear exception handling.
- Avoid unnecessary global variables.
- Avoid deeply nested conditions.
- Avoid duplicated logic.
- Use structured logging.
- Keep functions reasonably small.

Example:

```python
def calculate_prediction_confidence(
    probabilities: list[float],
) -> float:
    if not probabilities:
        raise ValueError("Prediction probabilities are empty.")

    return max(probabilities)
```

Do not use generic names such as:

```python
def process(data):
    pass
```

Prefer:

```python
def preprocess_sign_frame(frame):
    pass
```

---

## 5. FastAPI Application Rules

### Application Setup

- Create the FastAPI application in the existing application entry point.
- Register API routers centrally.
- Configure application metadata.
- Configure CORS using approved frontend origins.
- Use startup and shutdown lifecycle handling when required.
- Keep configuration outside route files.

Example:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialise shared application resources here.
    yield
    # Release resources here.


app = FastAPI(
    title="Signova AI API",
    description="Backend API for Indian Sign Language recognition.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")
```

This is an example. Adapt it to the actual project structure and resource lifecycle.

### Route Rules

- Use APIRouter.
- Keep routes grouped by feature.
- Use appropriate HTTP methods.
- Use meaningful HTTP status codes.
- Validate every incoming request.
- Use response models where practical.
- Add endpoint descriptions.
- Keep route handlers focused.
- Avoid exposing internal implementation details.

---

## 6. API Design Rules

Follow `docs/API_DOCUMENTATION.md`.

Do not create endpoints based on assumptions.

Potential API groups include:

| API Group | Responsibility |
|---|---|
| Health | Application health |
| Recognition | ISL gesture recognition |
| Speech | Optional text-to-speech |
| Users | User management, if implemented |
| History | Recognition history, if implemented |

Example endpoint structure:

```text
/api/health
/api/recognition/predict
/api/speech/generate
```

These paths are illustrative. Use the actual documented and implemented API contract.

### API Requirements

- Use consistent JSON responses.
- Validate request bodies and query parameters.
- Handle unsupported input.
- Return useful error messages.
- Avoid unnecessary response fields.
- Avoid exposing model internals.
- Document API changes.
- Maintain backward compatibility where practical.

### Example Response

```json
{
  "success": true,
  "data": {
    "label": "Example sign",
    "confidence": 0.95
  },
  "message": "Recognition completed"
}
```

This is an illustrative response only. Do not use it as the actual response contract unless the API documentation and implementation adopt it.

---

## 7. Request and Response Validation

Use Pydantic models for structured request and response data.

### Rules

- Validate required fields.
- Validate input types.
- Set reasonable length and size limits.
- Reject malformed input.
- Avoid accepting arbitrary data structures.
- Use clear validation errors.
- Do not trust frontend validation alone.

Example:

```python
from pydantic import BaseModel, Field


class RecognitionResponse(BaseModel):
    label: str | None
    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    success: bool
```

Only include fields that the actual recognition pipeline can provide.

Do not fabricate prediction labels or confidence values.

---

## 8. AI Model Integration Rules

AI model integration is a core responsibility of the backend.

The project should use suitable pretrained Indian Sign Language models where possible.

### Model Verification

Before integrating any model, verify:

1. Original repository.
2. Model licence.
3. ISL support.
4. Supported classes.
5. Model architecture.
6. Input dimensions.
7. Preprocessing requirements.
8. Output format.
9. Checkpoint format.
10. Python compatibility.
11. PyTorch compatibility.
12. Hardware requirements.
13. Model size.
14. Inference performance.

Do not assume a repository contains a working checkpoint.

### Model Loading

- Load model weights once when practical.
- Avoid loading the model for every request.
- Use a controlled application lifecycle.
- Handle missing checkpoints.
- Handle incompatible checkpoint formats.
- Validate model configuration.
- Keep model paths configurable.
- Avoid hardcoded absolute paths.
- Do not silently fall back to a different model.

### Device Selection

Use an appropriate inference device.

Possible devices:

- CUDA GPU.
- CPU.

Example:

```python
import torch


def get_inference_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")
```

Do not assume that the deployment environment has an NVIDIA GPU.

### Inference Rules

- Use the preprocessing required by the selected model.
- Match the model's expected tensor dimensions.
- Use the correct class mapping.
- Use evaluation mode.
- Disable gradient calculation during inference.
- Handle invalid inputs.
- Return controlled errors.
- Measure actual inference latency.

Example:

```python
import torch


def run_inference(model, input_tensor, device):
    model.eval()

    input_tensor = input_tensor.to(device)

    with torch.inference_mode():
        output = model(input_tensor)

    return output
```

This example is not a complete model pipeline. Adapt it to the selected architecture and checkpoint.

---

## 9. Static and Dynamic Sign Recognition

Do not treat every sign recognition model as a complete ISL translation model.

### Static Recognition

Static recognition may use:

- Individual images.
- Single video frames.
- Hand landmarks.
- Static gesture classification.

### Dynamic Recognition

Dynamic recognition may require:

- Multiple video frames.
- Temporal sequences.
- Landmark sequences.
- Motion features.
- Sequence models.

### Continuous ISL Interpretation

Continuous interpretation requires a model and processing pipeline that can handle connected signs, transitions, and context.

### Mandatory Rules

- Document the exact model capability.
- Keep static and dynamic pipelines separate where necessary.
- Do not pass single images into a sequence model without the required sequence construction.
- Do not pass landmark vectors into an image model.
- Do not claim continuous translation when only isolated signs are recognised.

---

## 10. Image and Video Input Processing

Camera input must be validated and processed safely.

### Image Validation

Check:

- File type.
- File size.
- Image dimensions.
- Decoding success.
- Empty or corrupted input.

Do not trust file extensions alone.

### Video and Frame Processing

- Validate frame format.
- Respect model input requirements.
- Avoid unnecessary frame processing.
- Apply frame sampling only when compatible with the model.
- Preserve the required frame order for dynamic models.
- Release temporary resources.
- Handle invalid video input safely.

### Privacy

- Process frames only for the requested purpose.
- Do not persist raw camera footage by default.
- Avoid logging image contents.
- Do not send camera data to external services without user consent.

---

## 11. Preprocessing Rules

Preprocessing must match the selected model's training and inference pipeline.

Potential operations include:

- Image resizing.
- Normalisation.
- Colour conversion.
- Landmark extraction.
- Frame sampling.
- Sequence padding.
- Tensor conversion.

### Strict Rules

- Do not invent preprocessing values.
- Do not assume RGB or BGR without checking.
- Do not change image dimensions arbitrarily.
- Do not reorder landmark coordinates.
- Do not change normalisation without verification.
- Keep preprocessing reproducible.
- Test preprocessing independently.
- Document the exact input format.

If the original model repository provides preprocessing code, inspect and reuse it where appropriate.

---

## 12. Prediction Postprocessing

The backend must convert raw model outputs into a meaningful response.

### Responsibilities

- Map output indices to the correct labels.
- Calculate confidence only when supported.
- Apply thresholds only when justified.
- Handle unknown or unsupported signs.
- Avoid repeated predictions where appropriate.
- Preserve the original class mapping.

### Confidence Rules

- Do not treat softmax probability as guaranteed real-world accuracy.
- Do not invent confidence scores.
- Do not present low-confidence predictions as confirmed.
- Make thresholds configurable when appropriate.
- Evaluate thresholds against validation data.

Example:

```python
def is_prediction_acceptable(
    confidence: float,
    threshold: float,
) -> bool:
    return confidence >= threshold
```

The threshold must come from evaluation, not guesswork.

---

## 13. Recognition Service Rules

The recognition service coordinates the recognition workflow.

Responsibilities may include:

1. Accept validated input.
2. Prepare model-compatible input.
3. Run preprocessing.
4. Execute inference.
5. Process model output.
6. Apply confidence handling.
7. Return a structured result.

### Rules

- Keep route handlers independent of model internals.
- Avoid duplicating preprocessing.
- Handle model-unavailable states.
- Avoid returning raw tensors.
- Keep response data serialisable.
- Test the service independently.

Do not introduce complex queues or background workers unless inference workload requires them.

---

## 14. Speech Service Rules

Speech generation is optional.

Sarvam AI or another approved speech provider may be used when supported.

### Rules

- Keep provider integration inside a dedicated service.
- Store API credentials on the backend.
- Use environment variables for secrets.
- Handle provider errors.
- Handle network timeouts.
- Validate text length.
- Avoid unnecessary repeated speech requests.
- Do not block recognition when speech generation fails.
- Do not claim speech generation works until it is tested.

Speech generation does not perform sign gesture recognition.

Keep gesture recognition and speech generation as separate services.

---

## 15. External AI Service Integration

When integrating Sarvam AI or another external service:

- Read the provider's current API documentation.
- Verify supported models and endpoints.
- Verify request and response formats.
- Check authentication requirements.
- Check usage limits and pricing.
- Handle timeouts and provider failures.
- Avoid exposing credentials.
- Avoid logging sensitive request content.
- Make external calls only when needed.

Never assume an API endpoint or model identifier exists.

Use environment variables for provider configuration.

---

## 16. Database Rules

PostgreSQL is optional.

Do not introduce a database unless a feature requires persistent data.

Possible use cases:

- User accounts.
- User preferences.
- Recognition history with consent.
- Application configuration.
- Learning resources.
- User learning progress.

### Database Standards

- Use SQLAlchemy when relational persistence is required.
- Use Alembic for migrations.
- Use UUID identifiers where appropriate.
- Use transactions for multi-step updates.
- Add appropriate indexes.
- Validate all stored input.
- Avoid unnecessary data collection.
- Avoid storing raw camera recordings by default.

### Database Security

- Never hardcode database credentials.
- Use environment variables.
- Restrict database access.
- Separate development and production databases.
- Do not expose database errors to clients.
- Do not run destructive migrations without approval.

Follow `docs/DATABASE_SCHEMA.md`.

---

## 17. Authentication and Authorisation

Only implement authentication when required by the approved product scope.

If authentication is introduced:

- Use a well-maintained authentication approach.
- Hash passwords with an appropriate password hashing algorithm.
- Never store plaintext passwords.
- Validate access tokens.
- Protect user-specific resources.
- Enforce ownership checks.
- Avoid trusting user IDs supplied by the client.
- Protect sensitive endpoints.

Do not introduce authentication complexity solely for architectural appearance.

---

## 18. Configuration and Environment Variables

Use a central configuration module.

Example `.env.example`:

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

FRONTEND_URL=http://localhost:5173

MODEL_PATH=
MODEL_DEVICE=auto

SARVAM_API_KEY=

DATABASE_URL=
```

These are example names only. Confirm the actual configuration before using them.

### Rules

- Never commit real `.env` files.
- Never hardcode API keys.
- Never expose backend secrets to the frontend.
- Validate required configuration at startup.
- Provide useful configuration errors.
- Keep `.env.example` updated.
- Separate development and production configuration.

---

## 19. CORS and API Security

Configure CORS for approved frontend origins.

### Rules

- Do not use unrestricted origins in production.
- Do not allow unnecessary HTTP methods.
- Do not allow unnecessary headers.
- Handle credentials carefully.
- Do not expose internal stack traces.
- Validate uploaded files.
- Restrict request sizes.
- Apply rate limits where appropriate.
- Use HTTPS in production.

CORS is not a replacement for authentication or authorisation.

---

## 20. Error Handling

Use consistent error handling across the backend.

### Expected Situations

| Situation | Expected Behaviour |
|---|---|
| Invalid request | Return validation error |
| Invalid image | Return controlled input error |
| Unsupported format | Return appropriate client error |
| Model unavailable | Return controlled service error |
| Model inference failure | Log safe diagnostic details and return controlled error |
| Low confidence | Return an uncertain or unsupported result |
| External provider unavailable | Return controlled provider error |
| Database unavailable | Return controlled service error |
| Internal failure | Return generic error without exposing stack trace |

### Rules

- Use appropriate HTTP status codes.
- Log diagnostic information safely.
- Do not leak secrets.
- Do not expose internal file paths.
- Do not silently ignore failures.
- Do not return successful responses for failed operations.

---

## 21. Logging and Monitoring

Use Python's logging module or the existing structured logging setup.

Log useful events such as:

- Application startup.
- Application shutdown.
- Model loading success or failure.
- Recognition request completion.
- External provider failures.
- Database connection failures.
- Unexpected backend errors.

### Logging Restrictions

- Never log API keys.
- Never log passwords or tokens.
- Avoid logging raw camera frames.
- Avoid unnecessary personal information.
- Do not log entire request bodies when they may contain sensitive data.
- Avoid excessive debug logging in production.

Measure:

- Request latency.
- Model inference latency.
- Error rate.
- Model loading time.
- Memory usage.
- GPU usage, when available.

Do not claim performance improvements without measurements.

---

## 22. Performance and Resource Management

- Load model weights once when practical.
- Avoid repeated model initialisation.
- Use inference mode for PyTorch inference.
- Avoid unnecessary CPU/GPU transfers.
- Release temporary resources.
- Avoid blocking asynchronous endpoints with long-running work.
- Use thread pools or suitable execution strategies when required.
- Limit input size.
- Handle concurrent requests safely.
- Measure memory usage.
- Measure inference latency.

### Important

Do not introduce Redis, Celery, message queues, or distributed inference unless the workload genuinely requires them.

Start with a simple, reliable backend.

---

## 23. Asynchronous Processing

Use asynchronous endpoints for operations involving asynchronous I/O.

### Rules

- Do not assume every function must be asynchronous.
- Do not block the event loop with CPU-heavy inference.
- Use an appropriate execution strategy for CPU-bound tasks.
- Manage shared model access safely.
- Avoid unnecessary background tasks.
- Handle client disconnections when processing streaming requests.

The selected execution strategy must be tested under the expected workload.

---

## 24. WebSocket Rules

Use WebSockets only if the recognition workflow requires continuous frame or result streaming.

### Requirements

- Validate connection requests.
- Handle disconnect events.
- Handle malformed messages.
- Limit message sizes.
- Avoid unbounded frame queues.
- Avoid processing frames faster than the model can handle.
- Return structured messages.
- Handle inference failures.
- Protect authenticated connections when authentication exists.

Do not introduce WebSockets merely because the application uses a camera.

A normal HTTP request may be sufficient for a simpler MVP.

---

## 25. Testing Rules

Use Pytest for backend testing.

### Required Areas

**API testing**
- Health endpoint.
- Recognition endpoint.
- Invalid request handling.
- Response validation.
- Error status codes.

**Service testing**
- Recognition service.
- Preprocessing service.
- Postprocessing service.
- Speech service.

**Model testing**
- Checkpoint loading.
- Correct input shape.
- Correct preprocessing.
- Output shape.
- Class mapping.
- Confidence handling.
- Unsupported input.
- Inference failure.

**Integration testing**
- API to recognition service.
- Recognition service to model.
- Speech service to external provider.
- Database integration, if implemented.

### Example Commands

```bash
pytest
```

For a focused test:

```bash
pytest tests/test_recognition.py -v
```

Check the actual test configuration before using these commands.

Do not report tests as passed unless they have been executed.

---

## 26. API Documentation

Keep `docs/API_DOCUMENTATION.md` aligned with the actual implementation.

Whenever an endpoint changes, document:

- HTTP method.
- Endpoint path.
- Purpose.
- Request parameters.
- Request body.
- Response format.
- Error responses.
- Authentication requirements.
- Example request.
- Example response.

FastAPI OpenAPI documentation should also reflect the actual API implementation.

Do not document example endpoints as implemented endpoints.

---

## 27. Deployment Rules

The backend may be deployed to Render or another compatible hosting platform.

Before deployment, verify:

- Python version support.
- Dependency compatibility.
- Model checkpoint availability.
- RAM requirements.
- CPU/GPU availability.
- Startup command.
- Environment variables.
- Request timeouts.
- Upload limits.
- WebSocket support, if used.
- Persistent storage requirements.
- Provider API connectivity.
- Actual hosting cost.

### Deployment Restrictions

- Do not assume a free hosting plan supports GPU inference.
- Do not assume model files persist on ephemeral storage.
- Do not commit large model checkpoints unnecessarily.
- Do not expose environment variables in logs.
- Do not claim deployment succeeded without verification.

Follow `docs/DEPLOYMENT.md`.

---

## 28. Dependency Management

Before adding a package:

1. Check whether it already exists.
2. Confirm it is necessary.
3. Verify Python 3.11 compatibility.
4. Check PyTorch compatibility.
5. Check operating system compatibility.
6. Check package maintenance and licence.
7. Avoid unnecessary dependency upgrades.

### Rules

- Keep dependencies documented.
- Use the existing dependency management method.
- Avoid installing packages globally.
- Do not install multiple packages for the same purpose without a reason.
- Keep development and production dependencies organised where practical.

---

## 29. Git and Repository Rules

- Use meaningful branch names.
- Write clear commit messages.
- Do not commit `.env` files.
- Do not commit virtual environments.
- Do not commit Python cache files.
- Do not commit large checkpoints without approval.
- Do not commit raw camera recordings.
- Keep `.gitignore` updated.
- Do not force-push without approval.
- Do not rewrite Git history without approval.

Example commits:

```text
feat: add recognition API endpoint
feat: integrate pretrained ISL model
fix: handle model loading errors
fix: validate uploaded image input
test: add inference service tests
docs: update API documentation
refactor: separate model inference service
```

---

## 30. AI Coding Agent Rules

When working as Antigravity or another coding agent:

1. Inspect the repository before editing.
2. Read the root `AGENTS.md`.
3. Read relevant project documentation.
4. Understand the existing backend architecture.
5. Check existing dependencies.
6. Plan the changes.
7. Implement only the requested functionality.
8. Add relevant tests.
9. Execute the tests.
10. Update documentation where necessary.
11. Report the actual results.

### Never

- Invent model checkpoints.
- Invent model performance metrics.
- Invent API responses.
- Claim an endpoint works without testing it.
- Replace the selected model without approval.
- Treat ASL as ISL.
- Claim continuous translation from static recognition.
- Add unnecessary database infrastructure.
- Expose API keys.
- Delete important project files without approval.
- Mark unimplemented features as completed.

If blocked by missing model files, credentials, or incompatible dependencies, explain the blocker clearly.

---

## 31. Backend Definition of Done

A backend task is complete only when:

- [ ] The requested functionality is implemented.
- [ ] The code follows the existing architecture.
- [ ] Input validation is implemented.
- [ ] Error handling is implemented.
- [ ] Model integration matches the selected model requirements.
- [ ] No credentials are exposed.
- [ ] Relevant tests are executed.
- [ ] API documentation is updated.
- [ ] No unrelated functionality is broken.
- [ ] Actual limitations are reported.

---

## 32. Final Rule

Build the Signova AI backend as a reliable foundation for Indian Sign Language recognition.

Prioritise:

1. Correct model integration.
2. Reliable preprocessing and inference.
3. Accurate prediction handling.
4. Secure API communication.
5. Camera and data privacy.
6. Maintainable FastAPI architecture.
7. Tested frontend and backend integration.

**The backend must reflect the real capabilities of the selected AI model. Never create fake recognition results or claim unsupported ISL translation functionality.**