# Development Workflow

## Signova AI

**Project:** Signova AI  
**Development Approach:** Backend First  
**Frontend:** React + JavaScript + Vite  
**Backend:** Python 3.11 + FastAPI  
**AI Framework:** PyTorch  
**Primary Environment:** Local Windows Development  
**Fallback Environment:** Kaggle

---

# 1. Development Principles

Follow these principles throughout development:

1. Work in small, testable steps.
2. Follow the documented project architecture.
3. Build the backend before connecting the frontend.
4. Validate pretrained models before integration.
5. Keep AI, backend, and frontend modules separate.
6. Reuse existing code wherever possible.
7. Test each feature before moving forward.
8. Avoid unnecessary dependencies and files.
9. Never use fake AI predictions.
10. Update progress based on actual implementation.

---

# 2. Initial Repository Inspection

Before writing code, inspect the existing repository.

### Tasks

- Review the current folder structure.
- Identify existing frontend and backend files.
- Identify installed dependencies.
- Inspect existing AI experiments.
- Identify available datasets and model checkpoints.
- Review existing configuration files.
- Read the relevant project documentation.

### Important Rules

- Do not delete existing files without approval.
- Do not overwrite working implementations without inspection.
- Do not duplicate existing modules.
- Do not assume the proposed folder structure has already been created.
- Report missing dependencies and configuration.

**Completion condition:** The existing project structure and implementation status are understood.

---

# 3. Phase 1: Project Foundation

### Backend Setup

- Set up Python 3.11 virtual environment.
- Install required backend dependencies.
- Configure FastAPI.
- Create the application entry point.
- Configure environment variables.
- Add the health endpoint.
- Verify local server startup.

### Frontend Setup

- Set up React with Vite.
- Use JavaScript and JSX only.
- Configure the CSS foundation.
- Create the main application entry point.
- Verify frontend startup.

### Completion condition

Both applications start locally without critical errors.

---

# 4. Phase 2: Backend API Foundation

Implement the backend before connecting the frontend.

### Tasks

- Organise FastAPI routes.
- Create Pydantic schemas.
- Add API versioning.
- Configure CORS.
- Add centralised error handling.
- Configure logging.
- Add backend health status.
- Add AI service status.

### Planned Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/health` | Backend health |
| `GET /api/v1/ai/health` | AI service status |
| `GET /api/v1/ai/models` | Available model information |

Do not expose model-dependent prediction endpoints as functional until their underlying pipeline is ready.

### Completion condition

Backend routes respond correctly and pass their initial tests.

---

# 5. Phase 3: AI Model Research

Identify a suitable pretrained model for ISL recognition.

### Tasks

- Search for pretrained ISL models.
- Inspect model documentation.
- Verify supported sign language.
- Identify model input requirements.
- Inspect architecture and checkpoints.
- Check preprocessing requirements.
- Verify model licence.
- Check hardware requirements.
- Identify compatible test samples.

### Model Evaluation Candidates

Treat research candidates as unverified until tested.

The `manavdhamecha77/iSign-t5-pose-to-text` model is an experimental pose-to-text candidate.

It must not be assumed to accept raw webcam images or video frames.

### Completion condition

A candidate model has documented input requirements, a usable checkpoint, and a practical validation plan.

If no compatible model is available, report the limitation rather than pretending the model is ready.

---

# 6. Phase 4: Standalone Model Testing

Test the model independently from FastAPI.

### Tasks

1. Configure the model environment.
2. Download the required checkpoint.
3. Verify checkpoint compatibility.
4. Implement or reproduce original preprocessing.
5. Prepare a compatible sample.
6. Run standalone inference.
7. Compare prediction with expected output.
8. Record inference time.
9. Record errors and limitations.

### Validation Record

| Field | Description |
|---|---|
| Model | Selected checkpoint |
| Input | Test sample |
| Input Format | Image, video, or landmarks |
| Expected Output | Ground truth |
| Predicted Output | Actual model result |
| Preprocessing | Configuration used |
| Inference Time | Measured duration |
| Status | Pass, Fail, or Inconclusive |

### Completion condition

The model loads and produces a result on compatible input, with its limitations recorded.

A single successful prediction does not establish general model accuracy.

---

# 7. Phase 5: AI Module Development

After standalone validation, integrate the model into modular AI code.

### Tasks

- Implement model loading.
- Implement model configuration.
- Implement preprocessing.
- Implement model adapters.
- Implement inference.
- Implement postprocessing.
- Add input validation.
- Add error handling.
- Add model status reporting.

### Suggested Module Structure

```text
ai/
├── preprocessing/
├── pose_extraction/
├── inference/
├── model_adapters/
├── postprocessing/
└── config/
```

Reuse existing modules wherever possible.

### Completion condition

The AI pipeline can be called independently and returns structured results or clear errors.

---

# 8. Phase 6: AI and Backend Integration

Connect the validated AI pipeline to FastAPI.

### Tasks

- Create the AI service layer.
- Load the model once during startup or controlled lazy loading.
- Add compatible prediction endpoints.
- Validate incoming requests.
- Connect preprocessing and inference.
- Return structured JSON responses.
- Handle model and inference failures.
- Add API tests.

### Planned Prediction Endpoints

| Endpoint | Condition |
|---|---|
| `POST /api/v1/ai/predict/image` | Only when an image-compatible model is ready |
| `POST /api/v1/ai/predict/video` | Only when a compatible video pipeline is ready |
| `POST /api/v1/ai/predict/landmarks` | Only when landmark input compatibility is verified |

### Completion condition

The backend returns actual model predictions using compatible input.

---

# 9. Phase 7: Frontend Development

After the backend API is ready, build the main user interface.

### Tasks

- Create the application layout.
- Implement reusable React components.
- Build the camera interface.
- Add camera permission handling.
- Add start and stop controls.
- Implement recognition status.
- Add the recognition result panel.
- Add loading and error states.
- Follow `UI_UX_GUIDELINES.md`.

### Technology Rules

- React.
- JavaScript ES6+.
- Vite.
- CSS.
- `.js` and `.jsx` files only.
- No TypeScript.

### Completion condition

The frontend works locally and its main interactions function correctly.

---

# 10. Phase 8: Frontend and Backend Connection

Connect the frontend to the actual FastAPI endpoints.

### Tasks

- Configure the API base URL.
- Create API service modules.
- Connect backend health status.
- Send supported recognition input.
- Display actual prediction responses.
- Handle loading states.
- Handle network failures.
- Handle unsupported model input.
- Verify API response handling.

### Completion condition

The frontend can send supported input and display genuine backend results.

Do not simulate successful recognition when the model is unavailable.

---

# 11. Phase 9: Speech Output

Implement text-to-speech after recognition output is available.

### Tasks

- Use browser SpeechSynthesis API.
- Add speak control.
- Add stop control.
- Handle empty recognition results.
- Handle unsupported browser functionality.
- Show speech status.
- Prevent unexpected overlapping speech.

### Completion condition

Recognised text can be spoken when valid text is available.

---

# 12. Phase 10: Testing and Validation

Test the complete application.

### Backend Tests

- API health.
- Request validation.
- AI service status.
- Model loading.
- Preprocessing.
- Inference.
- Error handling.

### Frontend Tests

- Component rendering.
- Camera permissions.
- Camera cleanup.
- API integration.
- Recognition result display.
- Speech controls.
- Responsive layout.

### AI Tests

- Model compatibility.
- Correct input shape.
- Preprocessing correctness.
- Prediction output.
- Evaluation metrics.
- Inference performance.

### Completion condition

Critical application flows pass testing, and known model limitations are documented.

---

# 13. Phase 11: Hackathon Preparation

Prepare a stable demonstration.

### Tasks

- Verify local environment setup.
- Confirm backend startup.
- Confirm frontend startup.
- Verify model loading.
- Test the camera.
- Test recognition using compatible samples.
- Test speech output.
- Prepare fallback demo samples.
- Prepare a short product explanation.
- Document known limitations.

### Demo Priorities

1. Explain the problem.
2. Introduce Signova AI.
3. Show the camera interface.
4. Demonstrate actual recognition.
5. Show text output.
6. Demonstrate speech output.
7. Explain the model and architecture.
8. Clearly state current limitations.

Never demonstrate fake recognition results as actual AI output.

---

# 14. Future Development

The following features are outside the initial MVP unless separately approved:

- Expanded ISL vocabulary.
- Dynamic sign recognition.
- Continuous ISL sentence translation.
- Facial expression recognition.
- Non-manual sign features.
- User accounts.
- Recognition history.
- Persistent database storage.
- Mobile application.

Add these features only when suitable models, data, and implementation plans are available.

---

# 15. Development Environment Rules

### Local Development

Use the Windows environment as the primary development environment.

- Python 3.11.
- Virtual environment.
- Compatible PyTorch installation.
- NVIDIA GPU when available.
- CPU fallback.

Verify CUDA availability rather than assuming it works.

### Kaggle Fallback

Use Kaggle when local hardware or environment limitations prevent practical experimentation.

- Avoid downloading unnecessarily large datasets.
- Check available storage first.
- Keep experiments reproducible.
- Record package versions.
- Do not make Kaggle a mandatory application dependency.

---

# 16. Progress Tracking Rules

Update `PROGRESS_TRACKER.md` after completing meaningful development work.

Use these statuses:

| Status | Meaning |
|---|---|
| Pending | Not started |
| In Progress | Currently being implemented |
| Blocked | Waiting for a dependency or decision |
| Completed | Implemented and verified |
| Failed | Attempted but unsuccessful |
| Not Applicable | Not required for the current scope |

### Progress Requirements

- Update only after actual work.
- Record test results.
- Record blockers.
- Record model validation results.
- Do not mark planned features as completed.
- Do not claim tests passed without running them.

---

# 17. Git and Repository Rules

- Keep commits focused.
- Use clear commit messages.
- Keep project files in English.
- Do not commit `.env` files.
- Do not commit large model checkpoints.
- Do not commit restricted datasets.
- Do not delete useful experiments without approval.
- Inspect changes before committing.
- Never push changes without explicit approval.

---

# 18. Strict Rules for Antigravity

Before implementing any phase:

1. Read the relevant documentation.
2. Inspect the existing implementation.
3. Identify dependencies.
4. Make the smallest required change.
5. Avoid unnecessary file creation.
6. Preserve working code.
7. Test the change.
8. Report modified and created files.
9. Report test results honestly.
10. Update the progress tracker when appropriate.

Do not skip a phase's validation just to move faster.

If a phase is blocked, explain the blocker and suggest the smallest practical next step.

---

# 19. Definition of MVP Completion

The initial MVP can be considered complete when:

- The frontend runs locally.
- The FastAPI backend runs locally.
- The backend health endpoint works.
- A compatible pretrained ISL model is integrated.
- The model receives correctly formatted input.
- The model produces genuine prediction output.
- The frontend displays the actual result.
- Speech output works for available text.
- Critical errors are handled.
- Core tests pass.
- Known limitations are documented.

A working camera interface alone does not mean ISL recognition is complete.

---

# 20. Final Development Goal

Build Signova AI in a controlled and testable order.

**Priority order:**

1. Repository understanding.
2. Backend foundation.
3. Pretrained model validation.
4. AI pipeline integration.
5. Frontend implementation.
6. End-to-end connection.
7. Testing.
8. Hackathon demonstration.

The goal is a functional and honest ISL recognition prototype, not a collection of unfinished features.