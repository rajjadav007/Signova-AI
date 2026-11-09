# Signova AI: API Documentation

## 1. Overview

This document defines the API architecture and communication standards for Signova AI.

Signova AI uses a Python FastAPI backend to connect the React frontend with the Indian Sign Language (ISL) recognition pipeline and speech services.

The backend is responsible for:

- Receiving image, video, and audio inputs.
- Validating incoming requests.
- Processing inputs through the ML pipeline.
- Returning ISL recognition predictions.
- Managing real-time recognition connections.
- Integrating Sarvam AI speech and language services.
- Managing user preferences and conversation data when persistence is enabled.
- Handling errors and protecting sensitive information.

### Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend development |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| Uvicorn | ASGI server |
| PyTorch | ML model inference |
| OpenCV | Image and video processing |
| WebSocket | Real-time communication |
| PostgreSQL | Optional persistent storage |
| Sarvam AI | Speech and language services |

---

# 2. API Architecture

The backend follows a modular architecture.

```text
React Frontend
      |
      v
FastAPI Backend
      |
      ├── API Routes
      |
      ├── Request Validation
      |
      ├── Authentication (Optional)
      |
      ├── Recognition Service
      |       |
      |       v
      |   ML Inference Pipeline
      |       |
      |       ├── Model Loader
      |       ├── Preprocessing
      |       ├── Prediction
      |       └── Validation
      |
      ├── Speech Service
      |       |
      |       v
      |   Sarvam AI APIs
      |
      ├── Conversation Service
      |
      └── Database Service (Optional)
```

### Communication Methods

| Method | Usage |
|---|---|
| REST API | Standard requests and responses |
| WebSocket | Live recognition streaming |
| Multipart Upload | Image, video, and audio uploads |
| JSON | Structured data exchange |

---

# 3. Base URL and API Versioning

All API endpoints should use versioning.

### Development

```text
http://localhost:8000/api/v1
```

### Production

```text
https://YOUR_BACKEND_DOMAIN/api/v1
```

Replace the production placeholder with the actual deployed backend URL.

### Versioning Rules

- Current API version: `v1`.
- All REST endpoints must use `/api/v1`.
- WebSocket routes must follow the same versioning convention.
- Breaking changes should be introduced through a new API version.
- Backward-compatible changes can be added to the existing version.

---

# 4. Standard Request and Response Format

## 4.1 JSON Request

Example:

```json
{
  "text": "Hello",
  "language": "en-IN"
}
```

## 4.2 Standard Success Response

Example:

```json
{
  "success": true,
  "message": "Request completed successfully",
  "data": {}
}
```

## 4.3 Standard Error Response

Example:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request data is invalid",
    "details": null
  }
}
```

### Response Rules

- Use consistent response structures.
- Return appropriate HTTP status codes.
- Never expose internal stack traces.
- Do not return API credentials.
- Use clear and actionable error messages.
- Keep response fields consistent across endpoints.

File upload and binary audio responses may use their appropriate content types instead of the standard JSON envelope.

---

# 5. API Endpoint Overview

The following endpoints define the planned API surface.

An endpoint is considered implemented only after its backend logic and tests are complete.

| Module | Method | Endpoint | Purpose |
|---|---|---|---|
| Health | GET | `/health` | Check backend status |
| AI Health | GET | `/ai/health` | Check ML service |
| Models | GET | `/ai/models` | List approved models |
| Recognition | POST | `/ai/predict/image` | Predict from image |
| Recognition | POST | `/ai/predict/video` | Predict from video |
| Recognition | WS | `/ai/predict/stream` | Live recognition |
| Speech | POST | `/speech/tts` | Generate speech |
| Speech | POST | `/speech/stt` | Transcribe audio |
| Translation | POST | `/speech/translate` | Translate text |
| Conversation | POST | `/conversations` | Create session |
| Conversation | GET | `/conversations` | List sessions |
| Conversation | GET | `/conversations/{id}` | Get session |
| Conversation | DELETE | `/conversations/{id}` | Delete session |
| Preferences | GET | `/users/me/preferences` | Get preferences |
| Preferences | PUT | `/users/me/preferences` | Update preferences |

The user, preference, and conversation endpoints require their corresponding authentication and database features to be implemented. They are not prerequisites for the initial recognition prototype.

---

# 6. Health Check APIs

## 6.1 Backend Health

**Endpoint:**

```http
GET /health
```

**Purpose:**

Check whether the FastAPI backend is running.

### Successful Response

HTTP `200 OK`

```json
{
  "success": true,
  "status": "healthy",
  "service": "signova-ai-backend"
}
```

### Implementation Requirements

- Return application health.
- Do not load heavy ML models just to answer this endpoint.
- Keep the response lightweight.

## 6.2 AI Service Health

**Endpoint:**

```http
GET /api/v1/ai/health
```

**Purpose:**

Check the ML inference service and approved model availability.

### Successful Response

```json
{
  "success": true,
  "data": {
    "status": "ready",
    "models": [
      {
        "name": "isl_static_recognition",
        "version": "1.0",
        "loaded": true
      }
    ]
  }
}
```

The model name and status must reflect the actual loaded model.

If the model is unavailable, return an appropriate service-unavailable response.

---

# 7. AI Model APIs

## 7.1 List Available Models

**Endpoint:**

```http
GET /api/v1/ai/models
```

**Purpose:**

Return the approved models available for inference.

### Successful Response

```json
{
  "success": true,
  "data": {
    "models": [
      {
        "id": "isl_static_recognition",
        "name": "ISL Static Recognition",
        "version": "1.0",
        "task": "static_gesture_recognition",
        "status": "available"
      }
    ]
  }
}
```

### Requirements

- Only list configured models.
- Return actual model status.
- Do not list unverified candidates as available.
- Do not expose private checkpoint paths.

---

## 7.2 Image Prediction API

<badge color="success">Core API</badge>

**Endpoint:**

```http
POST /api/v1/ai/predict/image
```

**Content-Type:**

```http
multipart/form-data
```

**Purpose:**

Receive an image and predict a supported ISL sign using the selected static recognition model.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | File | Yes | Input image |
| `model_id` | String | No | Approved model identifier |

### Example Request

```bash
curl -X POST \
  http://localhost:8000/api/v1/ai/predict/image \
  -F "file=@sample.jpg" \
  -F "model_id=isl_static_recognition"
```

### Successful Response

HTTP `200 OK`

```json
{
  "success": true,
  "data": {
    "prediction": {
      "label": "A",
      "class_id": 0,
      "confidence": 0.94
    },
    "recognition": {
      "type": "static",
      "status": "recognised"
    },
    "model": {
      "name": "isl_static_recognition",
      "version": "1.0"
    },
    "processing_time_ms": 85
  }
}
```

The prediction values above are illustrative only. Actual output must come from model inference.

### Possible Recognition Statuses

| Status | Meaning |
|---|---|
| `recognised` | A supported class was predicted |
| `uncertain` | Prediction confidence is insufficient |
| `unknown` | Input cannot be assigned reliably |
| `failed` | Inference could not be completed |

### Validation Requirements

- Accept only configured image formats.
- Validate file size.
- Validate image decoding.
- Reject corrupted images.
- Validate model identifiers.
- Apply model-specific preprocessing.
- Handle inference failures safely.

### Possible Errors

| HTTP Status | Error Code | Meaning |
|---|---|---|
| 400 | `INVALID_IMAGE` | Invalid image |
| 413 | `FILE_TOO_LARGE` | Upload exceeds limit |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Unsupported format |
| 422 | `INVALID_REQUEST` | Invalid parameters |
| 503 | `MODEL_NOT_READY` | Model unavailable |
| 500 | `INFERENCE_FAILED` | Prediction failed |

---

## 7.3 Video Prediction API

**Endpoint:**

```http
POST /api/v1/ai/predict/video
```

**Content-Type:**

```http
multipart/form-data
```

**Purpose:**

Process a video sequence using an approved dynamic ISL recognition model.

This endpoint must only be enabled after a suitable dynamic recognition model has been verified.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | File | Yes | Input video |
| `model_id` | String | No | Approved dynamic model |
| `max_frames` | Integer | No | Frame processing limit |

### Example Request

```bash
curl -X POST \
  http://localhost:8000/api/v1/ai/predict/video \
  -F "file=@sample.mp4" \
  -F "model_id=isl_dynamic_recognition"
```

### Successful Response

```json
{
  "success": true,
  "data": {
    "prediction": {
      "label": "HELLO",
      "confidence": 0.87
    },
    "recognition": {
      "type": "dynamic",
      "status": "recognised"
    },
    "model": {
      "name": "isl_dynamic_recognition",
      "version": "1.0"
    },
    "processing_time_ms": 420
  }
}
```

Example values are illustrative.

### Requirements

- Validate video format.
- Validate duration and file size.
- Extract frames safely.
- Apply the model's expected frame sampling.
- Preserve temporal ordering.
- Reject invalid sequences.
- Return actual model predictions.

Do not use a static alphabet model to claim dynamic word recognition.

---

# 8. Real-Time Recognition WebSocket API

<badge color="success">Core Feature</badge>

**Endpoint:**

```text
ws://localhost:8000/api/v1/ai/predict/stream
```

Production must use secure WebSocket:

```text
wss://YOUR_BACKEND_DOMAIN/api/v1/ai/predict/stream
```

**Purpose:**

Support live camera recognition by receiving image frames and returning prediction messages.

### 8.1 Connection Flow

```text
React Frontend
      |
      v
Open WebSocket
      |
      v
Send Recognition Configuration
      |
      v
Capture Camera Frame
      |
      v
Send Frame to Backend
      |
      v
Run Model Inference
      |
      v
Return Prediction
      |
      v
Update Recognition Interface
```

### 8.2 Client Start Message

The client should first send a configuration message.

```json
{
  "type": "start",
  "request_id": "session-001",
  "model_id": "isl_static_recognition"
}
```

### 8.3 Frame Message

For an initial implementation, frames can be sent as JSON with Base64-encoded image data.

```json
{
  "type": "frame",
  "request_id": "session-001",
  "frame_id": 1,
  "image": "BASE64_ENCODED_IMAGE"
}
```

The encoded image is a placeholder. Actual requests must contain valid encoded image data.

For better performance, consider binary WebSocket frames after defining and testing a compatible frame protocol.

### 8.4 Prediction Response

```json
{
  "type": "prediction",
  "request_id": "session-001",
  "frame_id": 1,
  "data": {
    "label": "A",
    "confidence": 0.94,
    "status": "recognised"
  },
  "processing_time_ms": 85
}
```

### 8.5 Uncertain Prediction Response

```json
{
  "type": "prediction",
  "request_id": "session-001",
  "frame_id": 2,
  "data": {
    "label": null,
    "confidence": 0.42,
    "status": "uncertain"
  }
}
```

### 8.6 Stop Message

```json
{
  "type": "stop",
  "request_id": "session-001"
}
```

### 8.7 Error Message

```json
{
  "type": "error",
  "request_id": "session-001",
  "error": {
    "code": "INFERENCE_FAILED",
    "message": "Unable to process the supplied frame"
  }
}
```

### 8.8 WebSocket Requirements

- Validate the initial configuration.
- Validate frame messages.
- Limit frame size.
- Limit incoming frame frequency.
- Process frames in order when sequence order matters.
- Prevent unbounded inference queues.
- Handle disconnected clients.
- Release resources after disconnection.
- Return clear errors.
- Avoid exposing internal exceptions.

### 8.9 Performance Considerations

- Resize frames according to model requirements.
- Avoid sending every camera frame.
- Apply a controlled frame rate.
- Limit concurrent inference.
- Measure processing latency.
- Consider binary messages for large frame payloads.

For dynamic models, preserve the sequence of frames needed by the model. Do not independently classify every frame if the model requires temporal input.

---

# 9. Sarvam AI Speech APIs

Sarvam AI will provide speech and language capabilities around the ISL recognition system.

All Sarvam API calls must go through the backend.

The exact external endpoint paths, model identifiers, request fields, and supported languages must be confirmed against the currently selected Sarvam API documentation before implementation. The internal Signova API contracts below are application-level contracts, not claims about Sarvam's external API format.

## 9.1 Text-to-Speech API

**Endpoint:**

```http
POST /api/v1/speech/tts
```

**Purpose:**

Convert recognised text into spoken audio using a supported Sarvam TTS model.

### Request

```json
{
  "text": "Hello, how are you?",
  "target_language": "en-IN"
}
```

### Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | String | Yes | Text to speak |
| `target_language` | String | Yes | Supported language code |
| `speaker` | String | No | Supported speaker identifier |
| `model_id` | String | No | Configured TTS model |

### Successful Response

A binary audio response is recommended.

```http
HTTP/1.1 200 OK
Content-Type: audio/wav
```

The actual audio format must match the configured Sarvam output format.

Alternatively, the backend may return a temporary audio reference if a secure audio storage service is introduced.

### Validation

- Text must not be empty.
- Text length must be within configured limits.
- Target language must be supported.
- Speaker and model identifiers must be valid.
- External API failures must be handled.

---

## 9.2 Speech-to-Text API

**Endpoint:**

```http
POST /api/v1/speech/stt
```

**Content-Type:**

```http
multipart/form-data
```

**Purpose:**

Convert supported audio input into text.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | File | Yes | Audio input |
| `language_code` | String | No | Expected language |
| `model_id` | String | No | Configured STT model |

### Example Request

```bash
curl -X POST \
  http://localhost:8000/api/v1/speech/stt \
  -F "file=@speech.wav" \
  -F "language_code=gu-IN"
```

### Successful Response

```json
{
  "success": true,
  "data": {
    "transcript": "Hello, how are you?",
    "language_code": "en-IN",
    "status": "completed"
  }
}
```

Example transcription is illustrative.

### Requirements

- Validate audio format.
- Validate file size and duration.
- Support only configured languages.
- Handle empty audio.
- Handle speech recognition failures.
- Avoid storing raw audio unless explicitly required and consented to.

---

## 9.3 Text Translation API

**Endpoint:**

```http
POST /api/v1/speech/translate
```

**Purpose:**

Translate recognised or transcribed text between supported languages using a configured translation service.

### Request

```json
{
  "text": "Hello, how are you?",
  "source_language": "en-IN",
  "target_language": "gu-IN"
}
```

### Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | String | Yes | Text to translate |
| `source_language` | String | Yes | Source language |
| `target_language` | String | Yes | Target language |

### Successful Response

```json
{
  "success": true,
  "data": {
    "original_text": "Hello, how are you?",
    "translated_text": "તમ કેમ છો?",
    "source_language": "en-IN",
    "target_language": "gu-IN"
  }
}
```

The translated text is an illustrative example. Actual translation quality must be evaluated.

### Requirements

- Validate language codes.
- Validate text length.
- Handle unsupported languages.
- Preserve original text.
- Return the actual translation.
- Handle external service errors.

---

# 10. Conversation APIs

These endpoints support optional persistent conversation history.

They should only be implemented when authentication and database storage are configured.

## 10.1 Create Conversation

**Endpoint:**

```http
POST /api/v1/conversations
```

### Request

```json
{
  "conversation_type": "sign_to_speech",
  "source_language": "isl",
  "target_language": "en-IN"
}
```

### Successful Response

```json
{
  "success": true,
  "data": {
    "conversation_id": "conv_001",
    "status": "active",
    "created_at": "2026-11-08T10:30:00Z"
  }
}
```

The identifier and timestamp are illustrative.

## 10.2 List Conversations

**Endpoint:**

```http
GET /api/v1/conversations
```

### Optional Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `page` | Integer | Page number |
| `limit` | Integer | Number of records |
| `type` | String | Conversation type |

### Successful Response

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 0
    }
  }
}
```

## 10.3 Get Conversation

**Endpoint:**

```http
GET /api/v1/conversations/{conversation_id}
```

Returns the selected conversation and its permitted stored messages.

## 10.4 Delete Conversation

**Endpoint:**

```http
DELETE /api/v1/conversations/{conversation_id}
```

### Successful Response

```json
{
  "success": true,
  "message": "Conversation deleted successfully"
}
```

### Privacy Requirements

- Users must only access their own conversations.
- Validate ownership before reading or deleting.
- Do not store raw camera footage by default.
- Apply retention rules.
- Provide clear deletion behaviour.
- Avoid storing audio unless required and consented to.

---

# 11. User Preference APIs

These endpoints are optional and require authentication.

## 11.1 Get Preferences

**Endpoint:**

```http
GET /api/v1/users/me/preferences
```

### Successful Response

```json
{
  "success": true,
  "data": {
    "theme": "light",
    "preferred_language": "gu-IN",
    "speech_enabled": true
  }
}
```

## 11.2 Update Preferences

**Endpoint:**

```http
PUT /api/v1/users/me/preferences
```

### Request

```json
{
  "theme": "dark",
  "preferred_language": "gu-IN",
  "speech_enabled": true
}
```

### Requirements

- Validate accepted values.
- Associate preferences with the authenticated user.
- Do not allow one user to update another user's settings.

---

# 12. Authentication and Authorisation

Authentication is optional for the initial recognition prototype.

If user accounts are implemented, all protected endpoints must enforce authentication.

### Recommended Authentication Flow

```text
User
 |
 v
Login
 |
 v
Authentication Provider
 |
 v
Access Token
 |
 v
React Frontend
 |
 v
FastAPI Backend
 |
 v
Token Validation
 |
 v
Protected API
```

### Authentication Requirements

- Validate access tokens on protected routes.
- Verify token expiration.
- Verify user identity.
- Restrict access to user-owned records.
- Never expose secret keys in frontend code.
- Never log access tokens.
- Use HTTPS in production.

The exact authentication provider and token format must be selected before implementation.

---

# 13. Database API Data Contracts

If PostgreSQL persistence is implemented, the backend should use clearly defined database models.

### 13.1 User

| Field | Type | Description |
|---|---|---|
| `id` | UUID | User identifier |
| `email` | String | User email |
| `created_at` | Timestamp | Account creation time |

### 13.2 Conversation

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Conversation identifier |
| `user_id` | UUID | Owner |
| `conversation_type` | String | Conversation type |
| `source_language` | String | Source language |
| `target_language` | String | Target language |
| `created_at` | Timestamp | Creation time |

### 13.3 Message

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Message identifier |
| `conversation_id` | UUID | Parent conversation |
| `message_type` | String | Sign, speech, or text |
| `content` | Text | Message content |
| `language_code` | String | Language identifier |
| `created_at` | Timestamp | Message time |

### Database Rules

- Use UUIDs for record identifiers.
- Add appropriate foreign keys.
- Add indexes for frequently queried fields.
- Validate ownership.
- Avoid unnecessary personal data.
- Do not store raw video by default.
- Apply retention and deletion policies.

The database schema must be finalised in `docs/DATABASE_SCHEMA.md` before implementing persistence.

---

# 14. HTTP Status Codes

Use standard HTTP status codes.

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 204 | Request successful, no response body |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Access denied |
| 404 | Resource not found |
| 409 | Resource conflict |
| 413 | Payload too large |
| 415 | Unsupported media type |
| 422 | Validation failed |
| 429 | Too many requests |
| 500 | Internal server error |
| 502 | External service error |
| 503 | Service unavailable |
| 504 | External service timeout |

Use the most appropriate status code for each failure.

---

# 15. Error Code Reference

| Error Code | Meaning |
|---|---|
| `INVALID_REQUEST` | Invalid request data |
| `INVALID_IMAGE` | Image could not be processed |
| `INVALID_VIDEO` | Video could not be processed |
| `INVALID_AUDIO` | Audio could not be processed |
| `UNSUPPORTED_MEDIA_TYPE` | Unsupported file type |
| `FILE_TOO_LARGE` | Upload exceeds limit |
| `MODEL_NOT_FOUND` | Requested model does not exist |
| `MODEL_NOT_READY` | Model is not loaded |
| `INFERENCE_FAILED` | Model inference failed |
| `LOW_CONFIDENCE` | Prediction is uncertain |
| `UNKNOWN_SIGN` | Unsupported or unknown sign |
| `CAMERA_FRAME_INVALID` | Invalid camera frame |
| `WEBSOCKET_ERROR` | WebSocket processing failed |
| `SPEECH_GENERATION_FAILED` | TTS failed |
| `TRANSCRIPTION_FAILED` | STT failed |
| `TRANSLATION_FAILED` | Translation failed |
| `UNSUPPORTED_LANGUAGE` | Language is unavailable |
| `AUTHENTICATION_REQUIRED` | Authentication required |
| `ACCESS_DENIED` | User is not authorised |
| `RESOURCE_NOT_FOUND` | Resource does not exist |
| `RATE_LIMIT_EXCEEDED` | Request limit reached |
| `EXTERNAL_SERVICE_ERROR` | External API failed |
| `INTERNAL_SERVER_ERROR` | Unexpected backend failure |

---

# 16. Rate Limiting and Upload Limits

Apply reasonable limits to protect the backend.

### Recommended Initial Configuration

These values are starting configuration targets, not fixed production limits.

| Setting | Initial Value |
|---|---|
| Image upload size | 5 MB |
| Video upload size | 25 MB |
| Audio upload size | 15 MB |
| Image formats | JPEG, PNG |
| Video formats | MP4, WebM |
| Audio formats | WAV, MP3, WebM |
| REST request timeout | Endpoint-specific |
| WebSocket frame rate | Configurable |
| Maximum concurrent inference | Based on hardware capacity |

Actual limits must be adjusted based on model requirements and hosting resources.

### Rate Limiting Requirements

- Limit expensive inference requests.
- Limit speech API requests.
- Limit WebSocket connections.
- Validate upload sizes before processing.
- Prevent unbounded processing queues.
- Return HTTP `429` when limits are exceeded.

---

# 17. Environment Variables

Store backend configuration in environment variables.

Example `.env.example`:

```env
APP_NAME=Signova AI
APP_ENV=development
DEBUG=false

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

FRONTEND_ORIGIN=http://localhost:5173

DATABASE_URL=

MODEL_DEVICE=auto
MODEL_CONFIG_PATH=ml/configs/static_model.yaml

SARVAM_API_KEY=
SARVAM_BASE_URL=

ACCESS_TOKEN_SECRET=
```

### Environment Rules

- Never commit `.env`.
- Keep `.env.example` free of real secrets.
- Do not expose Sarvam credentials to the frontend.
- Validate required environment variables at startup.
- Use separate development and production settings.
- Do not hardcode secrets in source code.

The exact Sarvam API base URL and configuration must be taken from the selected service documentation.

---

# 18. Backend Folder Structure

Recommended structure:

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── health.py
│   │           ├── ai.py
│   │           ├── speech.py
│   │           ├── conversations.py
│   │           └── preferences.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   ├── ai.py
│   │   ├── speech.py
│   │   └── conversation.py
│   │
│   ├── services/
│   │   ├── recognition_service.py
│   │   ├── speech_service.py
│   │   ├── translation_service.py
│   │   └── conversation_service.py
│   │
│   ├── websocket/
│   │   └── recognition.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   └── main.py
│
├── tests/
│   ├── test_health.py
│   ├── test_ai.py
│   ├── test_speech.py
│   └── test_websocket.py
│
├── requirements.txt
└── .env.example
```

Create optional modules only when the related feature is approved for implementation.

---

# 19. API Testing Strategy

Use Pytest and FastAPI TestClient or HTTPX.

### 19.1 Health Tests

- Backend health.
- AI service health.
- Model loading status.

### 19.2 Recognition Tests

- Valid image.
- Invalid image.
- Unsupported format.
- Oversized image.
- Model not loaded.
- Invalid model ID.
- Low-confidence prediction.
- Inference failure.

### 19.3 Video Tests

- Valid video.
- Invalid video.
- Unsupported codec.
- Oversized upload.
- Invalid frame sequence.
- Dynamic model unavailable.

### 19.4 WebSocket Tests

- Successful connection.
- Invalid start message.
- Valid frame message.
- Invalid frame data.
- Inference failure.
- Client disconnection.
- Stop message.
- Rate limit handling.

### 19.5 Speech Tests

- Valid TTS request.
- Empty text.
- Unsupported language.
- Valid audio transcription.
- Invalid audio.
- External API timeout.
- External API failure.

### 19.6 Conversation Tests

- Create conversation.
- List conversations.
- Retrieve conversation.
- Delete conversation.
- Access another user's conversation.
- Unauthenticated access.

### Testing Rules

- Mock external Sarvam API calls during unit tests.
- Use a controlled test model or test fixture for API tests.
- Do not require a paid API call for every test run.
- Test real model inference separately.
- Do not hardcode expected predictions unless the test input and model output are deterministic.
- Record actual test results.

---

# 20. Security Guidelines

The backend must follow these security practices:

### Input Validation

- Validate every incoming request.
- Validate file content, not only file extensions.
- Limit payload sizes.
- Validate model IDs.
- Validate language codes.
- Reject malformed data.

### API Security

- Configure CORS with approved origins.
- Use HTTPS in production.
- Apply rate limits.
- Protect authenticated endpoints.
- Avoid exposing stack traces.
- Keep dependencies updated.

### Model Security

- Use trusted checkpoint sources.
- Verify model files.
- Avoid loading arbitrary user-supplied checkpoints.
- Restrict access to model files.
- Validate inference inputs.

### Privacy

- Request permission before camera or microphone access.
- Do not save raw media by default.
- Clearly disclose external API processing.
- Keep API credentials secure.
- Apply deletion and retention policies to stored data.

---

# 21. API Performance Guidelines

The API must remain responsive during recognition and speech processing.

### Recognition

- Reuse loaded model instances.
- Avoid loading the checkpoint for every request.
- Use inference mode.
- Limit concurrent model execution based on hardware.
- Measure preprocessing and inference separately.
- Avoid unnecessary frame processing.

### Speech Services

- Apply external API timeouts.
- Handle rate limits.
- Avoid unnecessary repeated requests.
- Return clear service status.
- Avoid blocking unrelated API requests during long-running tasks.

### WebSocket

- Limit frame rate.
- Limit message size.
- Control inference queues.
- Handle disconnects.
- Measure end-to-end latency.

Do not claim a particular response time until it has been measured under documented conditions.

---

# 22. Frontend API Integration

The React frontend must communicate with the backend through service modules.

Recommended files:

```text
frontend/src/services/
├── api.js
├── recognitionService.js
├── speechService.js
├── communicationService.js
└── conversationService.js
```

### API Base URL

Configure through the frontend environment:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Example Fetch Service

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function predictImage(file, modelId) {
  const formData = new FormData();

  formData.append("file", file);

  if (modelId) {
    formData.append("model_id", modelId);
  }

  const response = await fetch(
    `${API_BASE_URL}/ai/predict/image`,
    {
      method: "POST",
      body: formData,
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(
      result?.error?.message || "Image prediction failed"
    );
  }

  return result.data;
}
```

Do not manually set the multipart `Content-Type` header when using browser `FormData`. The browser must add the boundary.

### WebSocket URL

The frontend should derive the WebSocket URL from its configured backend origin and use `wss` in production.

Do not hardcode production URLs inside individual components.

### Frontend Rules

- Keep API calls outside presentation components.
- Handle loading states.
- Handle errors.
- Validate user input.
- Avoid exposing secret keys.
- Clean up WebSocket connections.
- Clean up camera and microphone streams.

---

# 23. API Implementation Phases

| Phase | API Work | Expected Result |
|---|---|---|
| 1 | Health endpoints | Backend health checks |
| 2 | Model information endpoint | Approved model listing |
| 3 | Image prediction endpoint | Static ISL inference |
| 4 | Video prediction endpoint | Dynamic inference when supported |
| 5 | WebSocket endpoint | Live recognition |
| 6 | TTS endpoint | Spoken text output |
| 7 | STT endpoint | Audio transcription |
| 8 | Translation endpoint | Supported language translation |
| 9 | Conversation endpoints | Persistent sessions |
| 10 | Preference endpoints | User settings |
| 11 | Testing and security | Verified API implementation |

Implement only endpoints needed by the current project phase.

---

# 24. Definition of Done

An API endpoint is complete only when:

1. Its purpose and contract are documented.
2. Request validation is implemented.
3. Response schema is defined.
4. Correct status codes are returned.
5. Error handling is implemented.
6. Security requirements are addressed.
7. Unit tests are written.
8. Tests have been executed.
9. Integration behaviour is verified.
10. API documentation is updated.

A route that only returns a placeholder response is not considered a completed API.

---

# 25. Instructions for Antigravity

Before implementing any backend API:

1. Read `AGENTS.md`.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read `docs/FEATURES.md`.
5. Read `docs/TECH_STACK.md`.
6. Read `docs/SYSTEM_ARCHITECTURE.md`.
7. Read `docs/AI_MODEL_STRATEGY.md`.
8. Read `docs/PHASE_ROADMAP.md`.
9. Read this `docs/API_DOCUMENTATION.md`.
10. Inspect existing backend code and tests.

### Development Rules

- Use Python 3.11.
- Use FastAPI.
- Use Pydantic for request and response validation.
- Follow API versioning.
- Keep routes separate from service logic.
- Keep ML inference inside the ML/service layer.
- Keep Sarvam API calls on the backend.
- Use environment variables for credentials.
- Validate all incoming files.
- Implement meaningful error responses.
- Add tests for every new endpoint.
- Do not create fake model predictions.
- Do not claim unimplemented endpoints are available.
- Do not add unnecessary infrastructure.
- Update documentation after implementation.

### Completion Report

After every API task, provide:

- Endpoint implemented.
- HTTP method and path.
- Request schema.
- Response schema.
- Files created or modified.
- Dependencies added.
- Tests executed.
- Actual test results.
- Security considerations.
- Known limitations.
- Recommended next task.

---

# 26. Final API Strategy

The Signova AI backend should be developed in this order:

1. Establish backend health checks.
2. Connect the verified ISL model.
3. Implement image prediction.
4. Implement video prediction only when a dynamic model is ready.
5. Build WebSocket recognition.
6. Integrate Sarvam TTS.
7. Integrate Sarvam STT.
8. Add supported language translation.
9. Add optional conversation storage.
10. Add authentication and preferences if required.
11. Complete API testing and security review.

**Final Goal:** Provide a secure, modular, and reliable API layer that connects Signova AI's computer vision recognition pipeline with its React interface and Sarvam AI speech capabilities.