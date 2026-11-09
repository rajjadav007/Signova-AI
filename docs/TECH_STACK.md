# Signova AI
# Technology Stack and Development Standards

**Document:** TECH_STACK.md  
**Version:** 1.0  
**Project:** Signova AI  
**Status:** Planning and Development  
**Primary Platform:** Web Application  
**Primary Sign Language:** Indian Sign Language (ISL)

---

# 1. Purpose of This Document

This document defines the approved technology stack for Signova AI.

It explains:

- Which technologies the project will use.
- Why each technology is selected.
- Where each technology will be used.
- How frontend, backend, AI/ML, and external services communicate.
- Which libraries and packages are expected.
- How the development environment should be configured.
- How dependencies should be managed.
- Which technical standards Antigravity must follow.

This document is a technical reference for developers and AI coding agents.

Before adding a new framework, library, database, or external service, check this document.

Do not introduce alternative technologies without a clear technical reason and approval.

## Related Documentation

| Document | Responsibility |
|---|---|
| `PRD.md` | Product requirements |
| `PROJECT_OVERVIEW.md` | Product and system overview |
| `FEATURES.md` | Feature specifications |
| `TECH_STACK.md` | Technology selection and usage |
| `SYSTEM_ARCHITECTURE.md` | Component architecture |
| `AI_MODEL_STRATEGY.md` | AI models and datasets |
| `PHASE_ROADMAP.md` | Implementation sequence |
| `UI_UX_GUIDELINES.md` | Interface and design standards |
| `API_DOCUMENTATION.md` | API contracts |
| `DATABASE_SCHEMA.md` | Database design |

---

# 2. Technology Stack Overview

Signova AI uses a modular client-server architecture.

The application has five main technical areas:

1. Frontend application.
2. Backend API.
3. AI and machine learning.
4. Speech and language services.
5. Optional persistent data storage.

## 2.1 Approved Technology Stack

| Layer | Technology | Primary Purpose |
|---|---|---|
| Frontend Framework | React | Build the user interface |
| Frontend Language | JavaScript | Application logic |
| Frontend Build Tool | Vite | Development and production builds |
| Styling | Tailwind CSS | Responsive UI styling |
| UI Components | shadcn/ui | Reusable interface components |
| Routing | React Router | Page navigation |
| Icons | Lucide React | Interface icons |
| API Communication | Fetch API or Axios | HTTP requests |
| Backend Language | Python 3.11 | Backend and ML development |
| Backend Framework | FastAPI | REST API and WebSocket services |
| Data Validation | Pydantic | Request and response validation |
| ASGI Server | Uvicorn | Run FastAPI |
| ML Framework | PyTorch | Model loading and inference |
| Computer Vision | OpenCV | Image and video processing |
| Landmark Extraction | MediaPipe | Hand and body landmarks when required |
| Numerical Processing | NumPy | Numerical operations |
| Data Analysis | Pandas | Dataset inspection and processing |
| ML Evaluation | scikit-learn | Evaluation metrics |
| Database | PostgreSQL | Optional persistent storage |
| Speech AI | Sarvam AI | Supported STT, TTS and translation |
| Model Repository | Hugging Face Hub | Model discovery and distribution |
| Version Control | Git and GitHub | Source code management |
| Frontend Hosting | Vercel | Frontend deployment |
| Backend Hosting | Compatible Python hosting | Backend and inference deployment |

## 2.2 Technology Selection Principles

All technology decisions must follow these principles:

- Prefer stable and actively maintained technologies.
- Prefer tools with good documentation.
- Avoid unnecessary dependencies.
- Keep the application modular.
- Consider hardware and hosting limitations.
- Prefer affordable solutions during development.
- Avoid introducing infrastructure that the MVP does not need.
- Check compatibility before installing packages.

---

# 3. Frontend Technology Stack

## 3.1 React

**Purpose:** Build the Signova AI user interface.

React will manage:

- Application layout.
- Navigation.
- Landing page.
- Dashboard.
- Sign recognition interface.
- Camera preview.
- Voice communication.
- Conversation interface.
- Learning centre.
- Settings.

Development rules:

- Use functional components.
- Use React Hooks.
- Keep components reusable.
- Keep business logic outside presentation components where practical.
- Avoid unnecessarily large components.
- Separate API services from UI components.
- Handle loading and error states.

## 3.2 JavaScript

**Purpose:** Main frontend programming language.

JavaScript is the selected frontend language.

Rules:

- Use `.js` and `.jsx` files.
- Use modern ES modules.
- Use `const` and `let`.
- Prefer async/await for asynchronous operations.
- Use clear variable and function names.
- Use JSDoc comments for important complex functions where useful.

**Do not introduce TypeScript or convert the frontend to TypeScript without explicit approval.**

## 3.3 Vite

**Purpose:** Frontend development server and build tool.

Responsibilities:

- Start the local development server.
- Bundle frontend code.
- Manage development environment variables.
- Generate production builds.

Expected scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

These are expected script definitions, not a requirement to overwrite an existing package configuration.

## 3.4 Tailwind CSS

**Purpose:** Style the application.

Use Tailwind CSS for:

- Layout.
- Spacing.
- Responsive design.
- Typography.
- Colours.
- Borders.
- Component states.
- Accessibility-related styling.

Rules:

- Use consistent design tokens.
- Avoid unnecessary custom CSS.
- Avoid repeated arbitrary values.
- Keep responsive behaviour consistent.
- Maintain sufficient colour contrast.

## 3.5 shadcn/ui

**Purpose:** Provide reusable UI components.

Potential components:

- Button.
- Card.
- Dialog.
- Dropdown menu.
- Input.
- Textarea.
- Select.
- Tabs.
- Tooltip.
- Toast or notification components.
- Sheet.
- Alert dialog.

Rules:

- Use components only where they improve consistency.
- Keep components accessible.
- Customise components to match Signova AI's design.
- Do not install the entire component collection unnecessarily.
- Follow the installed version's setup instructions.

## 3.6 React Router

**Purpose:** Manage application navigation.

Proposed routes:

| Route | Page |
|---|---|
| `/` | Landing page |
| `/app` | Dashboard |
| `/app/recognition` | ISL recognition |
| `/app/voice` | Voice communication |
| `/app/conversation` | Conversation interface |
| `/app/learn` | ISL learning centre |
| `/app/settings` | Settings |

Routes can be added incrementally.

Do not create non-functional pages merely to populate navigation.

## 3.7 Lucide React

**Purpose:** Provide consistent icons.

Potential uses:

- Camera.
- Mic.
- Volume.
- Play.
- Pause.
- Settings.
- Home.
- Languages.
- Accessibility.
- Copy.
- Trash.
- Alert.
- Check.

Rules:

- Use icons with clear meaning.
- Use consistent icon sizes.
- Add accessible labels to icon-only controls.
- Avoid decorative icons that reduce clarity.

## 3.8 Frontend API Communication

Use the browser Fetch API by default.

Axios may be introduced if its additional functionality becomes useful.

Responsibilities:

- Send requests to FastAPI.
- Handle API responses.
- Handle errors.
- Configure request timeouts where appropriate.
- Manage API base URL through environment configuration.

Do not place backend API URLs throughout individual components.

Create a central API configuration and service layer.

## 3.9 Browser APIs

Use browser-native APIs where suitable.

### MediaDevices API

Purpose:

- Access camera.
- Access microphone.
- Request user permission.

### MediaRecorder API

Purpose:

- Record audio for speech-to-text requests.
- Produce audio blobs in supported formats.

### WebSocket API

Purpose:

- Communicate with the backend during live recognition.
- Receive prediction updates.

### Clipboard API

Purpose:

- Copy recognised text.
- Copy transcriptions.

### HTMLMediaElement

Purpose:

- Play generated speech audio.
- Control playback.

Rules:

- Handle unsupported browser features.
- Handle permission denial.
- Release camera and microphone resources.
- Never access camera or microphone without user permission.

---

# 4. Backend Technology Stack

## 4.1 Python 3.11

**Purpose:** Main backend and machine learning programming language.

The project will use Python 3.11 as its initial development baseline.

Reasons:

- Compatibility with common ML libraries.
- Strong ecosystem for computer vision.
- Good support for deep learning.
- Integration with FastAPI.
- Suitable for data processing and model evaluation.

Development rules:

- Use Python virtual environments.
- Use clear module structures.
- Follow PEP 8 where practical.
- Use type hints where helpful.
- Handle exceptions properly.
- Avoid unnecessary global state.

## 4.2 FastAPI

**Purpose:** Main backend framework.

FastAPI will handle:

- REST APIs.
- Recognition requests.
- Model management.
- Speech API integration.
- Request validation.
- Error handling.
- WebSocket communication.
- Health checks.

Expected API structure:

```text
backend/
└── app/
    ├── api/
    │   └── v1/
    │       └── endpoints/
    ├── core/
    ├── models/
    ├── schemas/
    ├── services/
    ├── websocket/
    ├── database/
    └── main.py
```

Rules:

- Use routers to organise API endpoints.
- Keep ML inference outside route functions.
- Use Pydantic schemas.
- Handle exceptions consistently.
- Avoid blocking operations in asynchronous request handlers.
- Document endpoints.
- Version APIs under `/api/v1`.

## 4.3 Pydantic

**Purpose:** Validate request and response data.

Use Pydantic for:

- Recognition request validation.
- Prediction response structure.
- Speech request validation.
- Service configuration.
- API response schemas.

Example prediction response:

```json
{
  "success": true,
  "prediction": {
    "class_id": 1,
    "label": "A",
    "confidence": 0.95
  },
  "status": "recognized"
}
```

This is an illustrative response format.

Actual class IDs, labels, and confidence values must come from the selected model.

## 4.4 Uvicorn

**Purpose:** Run the FastAPI application.

Expected local development command:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Use reload mode only for development.

Production configuration must be appropriate for the selected hosting environment.

## 4.5 WebSockets

**Purpose:** Support real-time communication between frontend and backend.

Potential use:

- Camera frame transmission.
- Recognition result updates.
- Live processing status.
- Connection status.

Rules:

- Define a documented message format.
- Validate incoming messages.
- Handle connection interruptions.
- Avoid sending excessive frames.
- Release resources after disconnection.
- Avoid unnecessary WebSocket complexity in the first implementation.

A REST-based image prediction endpoint may be used first to verify model integration before implementing live streaming.

---

# 5. AI and Machine Learning Stack

## 5.1 PyTorch

**Purpose:** Main deep learning framework.

Use PyTorch for:

- Loading pretrained recognition models.
- Running inference.
- Training and fine-tuning where required.
- Saving model checkpoints.
- Evaluating model performance.
- Optimising inference.

Rules:

- Verify checkpoint compatibility.
- Match model architecture to the checkpoint.
- Use inference mode for inference.
- Avoid loading the model repeatedly.
- Support CPU inference where practical.
- Use GPU acceleration when available and compatible.
- Document model requirements.

## 5.2 OpenCV

**Purpose:** Image and video processing.

Use OpenCV for:

- Image loading.
- Frame extraction.
- Resizing.
- Colour conversion.
- Image preprocessing.
- Video frame processing.

Rules:

- Match preprocessing to the selected model.
- Do not change image normalisation without validation.
- Avoid unnecessary image copies.
- Validate input dimensions.

## 5.3 MediaPipe

**Purpose:** Extract hand, pose, or other supported visual landmarks.

Potential uses:

- Hand landmark extraction.
- Body pose extraction.
- Visual feature preprocessing.

Important:

MediaPipe is not automatically required for every model.

Use it only when:

- The selected model expects landmark input.
- It improves the chosen recognition pipeline.
- Its output format matches the model architecture.

Do not replace an image-based model's expected input with landmarks without adapting and validating the model.

## 5.4 NumPy

**Purpose:** Numerical data processing.

Use for:

- Array operations.
- Image data manipulation.
- Model input preparation.
- Prediction processing.

## 5.5 Pandas

**Purpose:** Dataset inspection and analysis.

Use for:

- Dataset loading.
- Data quality checks.
- Class distribution analysis.
- Duplicate detection.
- Dataset reports.

Pandas should not be added to the live inference path unless necessary.

## 5.6 scikit-learn

**Purpose:** Machine learning evaluation and utility functions.

Use for:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Classification reports.
- Dataset splitting where appropriate.

Evaluation must use appropriate held-out data.

## 5.7 Additional ML Libraries

Additional packages may be introduced when required by the selected model.

Examples:

- `torchvision` for compatible vision model utilities.
- `Pillow` for image handling.
- `tqdm` for training progress.
- `matplotlib` for evaluation visualisations.

Do not install every possible ML package in advance.

First inspect the selected model repository and its actual dependencies.

---

# 6. ISL Model Integration Strategy

## 6.1 Model Selection

Signova AI must use a model trained for Indian Sign Language for its primary recognition capability.

Before model integration, verify:

- Sign language compatibility.
- Dataset source.
- Model architecture.
- Class labels.
- Input format.
- Preprocessing.
- Checkpoint availability.
- Licence.
- Inference requirements.
- Reported and independently measured performance.

## 6.2 Model Types

### Static Recognition

Potential architecture:

- CNN.
- MobileNet.
- EfficientNet.
- Vision Transformer.

Purpose:

Recognise supported signs from individual images or static visual input.

### Dynamic Recognition

Potential architecture:

- 3D CNN.
- Video Transformer.
- CNN + LSTM.
- Other temporal sequence models.

Purpose:

Recognise supported signs from ordered video frames.

### Continuous Sign Understanding

Future capability involving:

- Temporal sequence modelling.
- Sign language grammar.
- Facial and non-manual cues.
- Body posture.
- Spatial relationships.
- Contextual interpretation.

This is not guaranteed by static or isolated word recognition.

## 6.3 Model Integration Rules

- Keep model code separate from API code.
- Keep preprocessing separate from frontend code.
- Maintain a model configuration.
- Document class labels.
- Document checkpoint location.
- Validate input shapes.
- Record actual model evaluation results.
- Provide an unknown-sign handling strategy.

## 6.4 Model Storage

Potential structure:

```text
ml/
├── configs/
├── datasets/
├── preprocessing/
├── models/
├── training/
├── inference/
├── evaluation/
├── notebooks/
└── checkpoints/
```

Rules:

- Do not commit large checkpoints without a clear reason.
- Use appropriate model hosting or download instructions.
- Keep dataset files out of Git unless permitted and necessary.
- Document model download and setup steps.

---

# 7. Sarvam AI Integration

## 7.1 Purpose

Sarvam AI will provide supported Indian-language speech and language processing features.

It will not perform primary visual sign recognition.

## 7.2 Planned Services

### Speech-to-Text

Convert recorded spoken audio into readable text.

### Text-to-Speech

Convert recognised or edited text into spoken output.

### Translation

Translate supported spoken-language text where needed.

## 7.3 Integration Architecture

```text
React Frontend
      |
      v
FastAPI Backend
      |
      v
Sarvam AI API
      |
      v
Speech or Text Response
      |
      v
React Frontend
```

## 7.4 Backend Integration Rules

- Make external requests from the backend.
- Store credentials in environment variables.
- Validate input before sending requests.
- Handle API errors.
- Handle network timeouts.
- Check supported languages.
- Check the current API documentation.
- Avoid exposing raw credentials in logs.

## 7.5 Environment Variables

Expected configuration example:

```env
SARVAM_API_KEY=your_api_key
```

This is a placeholder.

Never commit an actual API key.

## 7.6 Service Abstraction

Keep speech integrations inside independent backend services.

Example:

```text
backend/app/services/
├── sarvam_client.py
├── speech_to_text.py
├── text_to_speech.py
└── translation.py
```

This is a proposed organisation. Create only modules that are actually needed.

---

# 8. Database Technology

## 8.1 PostgreSQL

**Purpose:** Store structured application data when persistent features are introduced.

Potential use cases:

- User profiles.
- User preferences.
- Conversation metadata.
- Learning progress.
- Application records.

The initial recognition MVP should not depend on PostgreSQL unless a specific feature requires persistent data.

## 8.2 Database Access

Use a suitable Python database library and ORM after the database scope is approved.

Potential choices:

- SQLAlchemy.
- Alembic for database migrations.
- Psycopg for PostgreSQL connectivity.

Choose compatible versions and a consistent database access approach.

Do not introduce multiple ORM systems.

## 8.3 Database Rules

- Keep database models separate from API schemas.
- Use migrations for schema changes.
- Use environment variables for connection settings.
- Validate user input.
- Avoid storing raw video or audio by default.
- Implement user-level access restrictions if accounts are introduced.

---

# 9. Frontend and Backend Communication

## 9.1 REST API

Use REST APIs for:

- Health checks.
- Model status.
- Image prediction.
- Speech-to-text requests.
- Text-to-speech requests.
- Translation requests.

Proposed endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Check backend health |
| GET | `/api/v1/model/status` | Check model availability |
| POST | `/api/v1/recognition/predict` | Predict a supported sign |
| POST | `/api/v1/speech/stt` | Convert speech to text |
| POST | `/api/v1/speech/tts` | Convert text to speech |
| POST | `/api/v1/speech/translate` | Translate supported text |

These are proposed endpoints, not existing implementations.

## 9.2 WebSocket Communication

Use WebSockets for real-time recognition only when needed.

Proposed endpoint:

```text
/api/v1/ws/recognition
```

Potential flow:

1. Frontend establishes connection.
2. Backend confirms connection.
3. Frontend sends a frame or supported message.
4. Backend validates input.
5. Recognition service processes the input.
6. Backend sends a prediction result.
7. Frontend updates the recognition interface.

## 9.3 API Response Standards

Responses should be consistent.

Example:

```json
{
  "success": true,
  "data": {},
  "message": "Request completed successfully"
}
```

Error example:

```json
{
  "success": false,
  "error": {
    "code": "MODEL_UNAVAILABLE",
    "message": "Recognition service is currently unavailable."
  }
}
```

Use suitable HTTP status codes.

Do not return successful responses for failed operations.

---

# 10. Development Tools

## 10.1 Node.js and npm

Frontend development uses Node.js and npm.

The current development environment may use:

- Node.js 24.x.
- npm 11.x.

These versions should be tested with the selected Vite and frontend dependencies before project setup.

Rules:

- Use npm consistently.
- Commit the lockfile.
- Avoid switching package managers without approval.
- Check compatibility when adding packages.

## 10.2 Python Virtual Environment

Use a virtual environment for backend and ML dependencies.

Windows setup:

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip
```

Install dependencies from the maintained requirements file.

Do not install packages globally unless there is a specific reason.

## 10.3 Git and GitHub

Use Git for:

- Version control.
- Feature branches.
- Change tracking.
- Collaboration.
- Rollbacks.

Recommended branch structure:

```text
main
develop
feature/frontend-setup
feature/isl-recognition
feature/fastapi-backend
feature/sarvam-integration
feature/camera-integration
```

Use clear commit messages.

Example:

```text
feat: add camera permission handling
feat: integrate ISL recognition service
fix: handle invalid prediction input
docs: update API documentation
test: add recognition service tests
```

---

# 11. Testing Technologies

## 11.1 Backend Testing

Recommended:

- Pytest.
- FastAPI TestClient.
- HTTPX where required.

Use for:

- API tests.
- Service tests.
- Model loading tests.
- Input validation tests.
- Error handling tests.

## 11.2 Frontend Testing

Recommended:

- Vitest.
- React Testing Library.
- Playwright for end-to-end tests where useful.

Use for:

- Component testing.
- User interaction testing.
- API state testing.
- Camera and microphone UI state testing.
- Navigation testing.

Browser permission behaviour should also be checked in a real browser environment.

## 11.3 ML Testing

Use:

- Pytest.
- scikit-learn metrics.
- Model-specific evaluation scripts.

Test:

- Checkpoint loading.
- Preprocessing.
- Inference.
- Invalid input handling.
- Prediction outputs.
- Performance.

---

# 12. Code Quality Standards

## 12.1 Frontend

- Use functional React components.
- Keep components focused.
- Use reusable hooks where appropriate.
- Separate API calls into services.
- Keep camera logic separate from presentation.
- Avoid unnecessary state.
- Handle asynchronous operations.
- Use accessible HTML elements.
- Keep JavaScript code readable.

## 12.2 Backend

- Follow a modular FastAPI structure.
- Use Pydantic schemas.
- Separate routes from services.
- Keep model inference separate from API logic.
- Handle errors consistently.
- Use environment-based configuration.
- Add tests for important services.

## 12.3 ML

- Separate preprocessing, inference, training, and evaluation.
- Keep model configurations explicit.
- Reuse loaded models.
- Record model metadata.
- Document dataset sources.
- Avoid data leakage.
- Do not fabricate evaluation metrics.

## 12.4 Naming Conventions

| Area | Convention | Example |
|---|---|---|
| React Components | PascalCase | `CameraPreview.jsx` |
| JavaScript Functions | camelCase | `startCamera()` |
| JavaScript Variables | camelCase | `predictionResult` |
| Python Functions | snake_case | `load_model()` |
| Python Variables | snake_case | `prediction_result` |
| Python Classes | PascalCase | `RecognitionService` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL` |
| React Hooks | use + camelCase | `useCamera.js` |

---

# 13. Hardware and Performance Considerations

## 13.1 Development Hardware

The development environment may include:

- Windows system.
- Python 3.11.
- Node.js 24.
- 24 GB RAM.
- NVIDIA GPU with 4 GB VRAM.

Hardware availability must be checked at runtime.

Do not assume CUDA is available merely because an NVIDIA GPU exists.

Verify:

- GPU model.
- NVIDIA driver.
- CUDA compatibility.
- Installed PyTorch build.
- Available GPU memory.

## 13.2 CPU and GPU Support

The ML service should support CPU inference where practical.

GPU acceleration may be used when compatible.

Rules:

- Detect available devices.
- Avoid hardcoding CUDA.
- Handle GPU memory limitations.
- Provide a CPU fallback where supported.
- Benchmark the selected model.

## 13.3 Model Size

Before downloading or deploying a model, check:

- Checkpoint size.
- Required RAM.
- Required VRAM.
- Inference latency.
- Dependency requirements.
- Deployment constraints.

Do not download large checkpoints without first inspecting their requirements.

## 13.4 Real-Time Processing

For live recognition:

- Avoid unnecessary frame processing.
- Use appropriate frame sampling.
- Resize frames according to model requirements.
- Reuse the loaded model.
- Avoid blocking the browser interface.
- Measure end-to-end latency.

Do not define performance targets without benchmarking the actual model and hosting environment.

---

# 14. Environment Configuration

## 14.1 Frontend Environment Variables

Example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Only public configuration should use frontend environment variables.

Never put secret API keys in variables prefixed with `VITE_`.

## 14.2 Backend Environment Variables

Example:

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

SARVAM_API_KEY=your_api_key

DATABASE_URL=your_database_connection_string

MODEL_PATH=ml/checkpoints/model.pt
```

These are configuration examples.

Not all variables need to be configured during the initial MVP.

## 14.3 Environment Rules

- Maintain `.env.example`.
- Keep actual `.env` files out of Git.
- Validate required settings at startup.
- Provide meaningful configuration errors.
- Use different settings for development and production.

---

# 15. Proposed Project Structure

```text
signova-ai/
│
├── .agents/
│   ├── rules/
│   ├── workflows/
│   └── skills/
│
├── .github/
│   └── workflows/
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
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── pages/
│       ├── features/
│       ├── hooks/
│       ├── context/
│       ├── services/
│       ├── utils/
│       ├── constants/
│       ├── styles/
│       ├── App.jsx
│       └── main.jsx
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── websocket/
│   │   ├── database/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── ml/
│   ├── configs/
│   ├── datasets/
│   ├── preprocessing/
│   ├── models/
│   ├── training/
│   ├── inference/
│   ├── evaluation/
│   ├── notebooks/
│   └── checkpoints/
│
├── database/
├── scripts/
├── tests/
│
├── .env.example
├── .gitignore
├── AGENTS.md
├── README.md
└── LICENSE
```

This is the target architecture.

Create directories incrementally as their features are implemented.

---

# 16. Technologies Not Required for the Initial MVP

The following technologies are not approved as mandatory dependencies for the initial MVP.

| Technology | Reason |
|---|---|
| Next.js | Vite + React is the selected frontend setup |
| TypeScript | JavaScript is the selected frontend language |
| MongoDB | PostgreSQL is the proposed database |
| Redis | Not required until a specific caching or session need exists |
| Docker | Can be introduced when environment consistency or deployment requires it |
| Kubernetes | Unnecessary for the initial project scale |
| Microservices | A modular FastAPI backend is sufficient initially |
| Firebase | Not required for the current architecture |
| Multiple state management libraries | React state and context may be sufficient initially |

These technologies are not permanently prohibited. Any change must be justified and documented.

---

# 17. Dependency Management Rules

Antigravity must follow these rules when installing packages.

1. Inspect existing dependencies before adding new ones.
2. Check official documentation.
3. Verify Python and Node compatibility.
4. Install only packages needed for the current feature.
5. Avoid unnecessary duplicate libraries.
6. Maintain lockfiles where applicable.
7. Keep dependencies in their correct environment.
8. Document important new dependencies.
9. Run relevant tests after installation.
10. Avoid blindly upgrading all dependencies.

## Version Policy

Do not assume that the latest version of every package is compatible with the project.

Use compatible, tested versions.

Maintain exact resolved dependency versions through lockfiles or dependency constraints where appropriate.

Record any important compatibility decisions in the repository.

---

# 18. Deployment Stack

## 18.1 Frontend Deployment

Proposed platform: Vercel.

Responsibilities:

- Build frontend application.
- Host static frontend assets.
- Configure production environment variables.
- Connect to backend API.

## 18.2 Backend Deployment

Use a Python-compatible hosting provider.

Possible options include Render or another service that supports the selected FastAPI and ML requirements.

Before choosing a provider, verify:

- RAM.
- CPU.
- GPU availability if required.
- Persistent storage.
- Model size restrictions.
- Request timeout limits.
- WebSocket support.
- Cold-start behaviour.
- Cost.

## 18.3 Model Hosting

Potential option: Hugging Face Hub.

Use it for:

- Model distribution.
- Checkpoint hosting.
- Model metadata.

Do not assume the hosting service provides free production inference for every model.

## 18.4 Production Configuration

Production must use:

- Secure environment variables.
- HTTPS.
- Correct CORS settings.
- Appropriate request limits.
- Secure backend configuration.
- Verified model availability.
- Error monitoring.

---

# 19. Security Requirements

All technologies must follow these rules.

## Frontend

- Do not store secret credentials.
- Validate user inputs.
- Handle permission requests clearly.
- Avoid unnecessary local storage of private content.

## Backend

- Protect external API credentials.
- Validate uploaded files.
- Limit request sizes.
- Use secure configuration.
- Handle exceptions.
- Avoid exposing internal stack traces to users.

## Machine Learning

- Verify model source.
- Check model licences.
- Avoid loading untrusted checkpoints without inspection.
- Document model provenance.
- Avoid storing private input data unnecessarily.

## External Services

- Use secure API connections.
- Send only necessary data.
- Explain external audio processing.
- Handle service errors safely.

---

# 20. Antigravity Development Rules

Antigravity must treat this document as the approved technology reference.

Before implementing a feature:

1. Read `AGENTS.md`.
2. Read `PRD.md`.
3. Read `PROJECT_OVERVIEW.md`.
4. Read `FEATURES.md`.
5. Read `TECH_STACK.md`.
6. Read the relevant architecture and AI documentation.
7. Inspect existing dependencies.
8. Confirm the current development phase.

## Mandatory Technology Rules

- Frontend must use React and JavaScript.
- Do not use TypeScript without approval.
- Use Vite for the selected frontend setup.
- Use Python 3.11 as the initial backend baseline.
- Use FastAPI for backend services.
- Use PyTorch for supported model integration.
- Use OpenCV for image and video processing where required.
- Use MediaPipe only when compatible with the selected model.
- Use Sarvam AI for supported speech and language services.
- Use PostgreSQL only when persistent data features require it.
- Do not expose API keys.
- Do not introduce unnecessary technologies.

## Implementation Rules

- Implement one feature at a time.
- Follow the approved architecture.
- Inspect files before editing.
- Reuse existing code.
- Avoid unnecessary dependencies.
- Write tests.
- Update documentation.
- Report actual test results.
- Document any proposed technology change before applying it.

## Technology Change Approval

If Antigravity believes another technology would be better:

1. Identify the existing technology.
2. Explain the limitation.
3. Propose the alternative.
4. Explain the benefits and trade-offs.
5. Explain migration impact.
6. Wait for approval before replacing the selected technology.

---

# 21. Final Technology Decision Summary

| Area | Approved Choice |
|---|---|
| Product | Signova AI |
| Frontend | React |
| Frontend Language | JavaScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Routing | React Router |
| Icons | Lucide React |
| Backend | FastAPI |
| Backend Language | Python 3.11 |
| API Validation | Pydantic |
| Server | Uvicorn |
| ML Framework | PyTorch |
| Image Processing | OpenCV |
| Landmark Extraction | MediaPipe when required |
| Numerical Processing | NumPy |
| Data Analysis | Pandas |
| ML Evaluation | scikit-learn |
| Speech Services | Sarvam AI |
| Database | PostgreSQL when needed |
| Model Hosting | Hugging Face Hub |
| Version Control | Git and GitHub |
| Frontend Hosting | Vercel |
| Backend Hosting | Compatible Python hosting |
| Testing | Pytest, Vitest, React Testing Library |
| E2E Testing | Playwright where useful |

---

# 22. Final Technical Principle

Signova AI should use a simple, modular, and reliable technology stack.

Every technology must have a clear purpose.

The project must prioritise:

1. Correct ISL model integration.
2. Reliable camera input.
3. Accurate and measurable recognition.
4. Secure speech service integration.
5. Responsive and accessible frontend development.
6. Maintainable backend architecture.
7. Affordable development and deployment.
8. Honest reporting of actual capabilities.

**Core Principle: Use the right technology for each responsibility. Keep the architecture simple, validate every integration, and introduce complexity only when the product requires it.**