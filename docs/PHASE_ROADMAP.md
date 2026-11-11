# Phase Roadmap

## Signova AI

**Project:** Signova AI  
**Version:** 1.0  
**Status:** Development Planning  
**Development Approach:** Backend First  
**Primary Environment:** Local Windows  
**Fallback Environment:** Kaggle GPU

---

# 1. Roadmap Overview

This roadmap defines the development phases for Signova AI, from initial repository setup to a working ISL recognition application.

The development strategy prioritises:

- Building a stable backend.
- Testing pretrained models independently.
- Validating model compatibility.
- Integrating AI inference.
- Connecting the frontend.
- Completing the recognition and speech workflow.

The initial goal is to build a functional prototype within the hackathon timeline without training a model from scratch.

---

# 2. Development Phases

<badge color="success">Current priority: MVP</badge>

## Phase 0: Repository and Environment Setup

**Priority:** Critical  
**Status:** Pending

### Objectives

Prepare the project structure and development environments.

### Tasks

- [ ] Inspect the existing repository.
- [ ] Review existing project documentation.
- [ ] Confirm frontend and backend directories.
- [ ] Configure Python 3.11.
- [ ] Configure Node.js and npm.
- [ ] Create Python virtual environment.
- [ ] Verify PyTorch installation.
- [ ] Check NVIDIA CUDA availability.
- [ ] Configure `.gitignore`.
- [ ] Configure environment variable examples.
- [ ] Keep model checkpoints and datasets outside Git.

### Deliverables

- Working development environment.
- Clean project structure.
- Verified dependency setup.
- Local GPU status report.

### Completion Criteria

Python, Node.js, backend dependencies, and frontend dependencies must work without environment errors.

---

## Phase 1: Backend Foundation

**Priority:** Critical  
**Status:** Pending

### Objectives

Create the FastAPI backend before frontend integration.

### Tasks

- [ ] Create FastAPI application entry point.
- [ ] Configure application settings.
- [ ] Configure CORS for local frontend.
- [ ] Create API route structure.
- [ ] Implement backend health endpoint.
- [ ] Implement AI service health endpoint.
- [ ] Configure error handling.
- [ ] Add request validation.
- [ ] Configure API documentation.
- [ ] Add initial backend tests.

### Deliverables

- Running FastAPI application.
- Working health endpoints.
- API documentation.
- Basic backend tests.

### Completion Criteria

The backend starts successfully and returns correct health responses.

No AI model integration is required in this phase.

---

## Phase 2: AI Model Research and Experimentation

**Priority:** Critical  
**Status:** Pending

### Objectives

Identify and test suitable pretrained ISL models.

### Initial Candidate

`manavdhamecha77/iSign-t5-pose-to-text`

Initial checkpoint:

`t5-small`

### Tasks

- [ ] Inspect the original model repository.
- [ ] Verify model architecture.
- [ ] Inspect model inference code.
- [ ] Verify checkpoint files.
- [ ] Understand required input format.
- [ ] Inspect preprocessing requirements.
- [ ] Identify compatible sample data.
- [ ] Download only the required checkpoint.
- [ ] Run standalone inference.
- [ ] Record actual predictions.
- [ ] Record model loading time.
- [ ] Measure inference latency.
- [ ] Monitor CPU and GPU memory.
- [ ] Record model limitations.

### Environment

Primary: Local Windows machine.

Fallback: Kaggle GPU if local hardware is insufficient.

### Deliverables

- Model experiment results.
- Working standalone inference script.
- Verified checkpoint information.
- Input and output format documentation.

### Completion Criteria

The selected candidate must load successfully and produce genuine output on compatible samples.

A model is not approved merely because its checkpoint downloads or inference runs.

---

## Phase 3: Model Evaluation and Selection

**Priority:** Critical  
**Status:** Pending

### Objectives

Determine whether the experimental model is suitable for the Signova AI recognition task.

### Tasks

- [ ] Obtain compatible labeled ISL samples.
- [ ] Verify input and annotation alignment.
- [ ] Reproduce original preprocessing.
- [ ] Run inference on multiple samples.
- [ ] Compare predictions with ground truth.
- [ ] Review incorrect predictions.
- [ ] Calculate suitable evaluation metrics.
- [ ] Measure inference latency.
- [ ] Evaluate memory requirements.
- [ ] Review model and dataset licences.
- [ ] Compare alternative pretrained candidates if necessary.

### Evaluation Metrics

Depending on the model task:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Macro F1.
- Confusion matrix.
- BLEU or ROUGE for suitable sequence-generation tasks.
- Inference latency.
- GPU memory usage.

### Deliverables

- Evaluation results.
- Model comparison.
- Model selection decision.
- Documented limitations.

### Completion Criteria

A model can be selected for integration only after evaluation on suitable data.

If the candidate fails compatibility or evaluation requirements, return to Phase 2 and investigate another model.

---

## Phase 4: Model Adapter and Inference Integration

**Priority:** Critical  
**Status:** Pending

### Objectives

Integrate the selected model into a reusable AI architecture.

### Tasks

- [ ] Create a base model adapter interface.
- [ ] Implement the selected model adapter.
- [ ] Implement model loading.
- [ ] Implement model configuration.
- [ ] Implement model-specific preprocessing.
- [ ] Implement inference execution.
- [ ] Implement prediction validation.
- [ ] Implement output formatting.
- [ ] Implement model status reporting.
- [ ] Add inference tests.

### Deliverables

- Model adapter.
- Model manager.
- Inference engine.
- Model configuration.
- Tested inference module.

### Completion Criteria

The selected model can be loaded and executed through a reusable AI module without depending on frontend code.

---

## Phase 5: Visual Input and Processing Pipeline

**Priority:** Critical  
**Status:** Pending

### Objectives

Connect camera images or video frames to the model-compatible input pipeline.

### Tasks

- [ ] Implement image or video input processing.
- [ ] Implement frame extraction.
- [ ] Add frame validation.
- [ ] Implement required visual feature extraction.
- [ ] Add hand landmark extraction if required.
- [ ] Add body landmark extraction if required.
- [ ] Match the model's original landmark ordering.
- [ ] Implement coordinate normalisation.
- [ ] Implement sequence preparation where required.
- [ ] Validate processed model input.
- [ ] Test with compatible samples.

### Deliverables

- Visual input processing module.
- Model-compatible preprocessing pipeline.
- Input validation tests.

### Completion Criteria

Camera or video input can be converted into the exact format required by the selected model.

Do not assume that generic MediaPipe landmarks are automatically compatible with iSign T5.

---

## Phase 6: AI Prediction API

**Priority:** Critical  
**Status:** Pending

### Objectives

Expose supported AI inference through FastAPI.

### Tasks

- [ ] Create AI service layer.
- [ ] Connect the model manager.
- [ ] Implement supported prediction endpoints.
- [ ] Add image validation where supported.
- [ ] Add video validation where supported.
- [ ] Add landmark validation where supported.
- [ ] Implement structured prediction responses.
- [ ] Implement inference error handling.
- [ ] Add processing time measurement.
- [ ] Test successful and failed requests.

### Deliverables

- Working AI prediction API.
- Request and response schemas.
- API tests.
- Updated API documentation.

### Completion Criteria

Supported input reaches the selected model and returns genuine predictions through FastAPI.

Only expose prediction endpoints that have working model pipelines.

---

## Phase 7: Frontend Development and Integration

**Priority:** Critical  
**Status:** Pending

### Objectives

Connect the React frontend to the backend.

### Tasks

- [ ] Configure React and TypeScript.
- [ ] Build the main application layout.
- [ ] Implement camera permission handling.
- [ ] Implement live camera preview.
- [ ] Add start and stop camera controls.
- [ ] Implement frame capture.
- [ ] Connect frontend API services.
- [ ] Display recognition status.
- [ ] Display model status.
- [ ] Display prediction results.
- [ ] Display error messages.
- [ ] Add loading states.
- [ ] Test frontend and backend communication.

### Deliverables

- Functional web interface.
- Camera preview.
- Backend connection.
- Prediction result display.

### Completion Criteria

Users can provide supported signing input through the frontend and receive actual backend model predictions.

---

## Phase 8: Text-to-Speech Integration

**Priority:** High  
**Status:** Pending

### Objectives

Convert recognised text into spoken output.

### Tasks

- [ ] Integrate browser SpeechSynthesis API.
- [ ] Add speech play control.
- [ ] Add speech stop control.
- [ ] Add speech enable and disable setting.
- [ ] Handle unsupported browser speech features.
- [ ] Test speech output with recognised text.

### Deliverables

- Working speech output.
- Speech controls.
- Error handling.

### Completion Criteria

Recognised text can be converted into speech using a supported browser voice.

---

## Phase 9: Testing and Optimisation

**Priority:** High  
**Status:** Pending

### Objectives

Test the complete application and improve reliability.

### Tasks

- [ ] Test backend APIs.
- [ ] Test model loading.
- [ ] Test model inference.
- [ ] Test input preprocessing.
- [ ] Test camera permissions.
- [ ] Test frontend integration.
- [ ] Test speech output.
- [ ] Test invalid inputs.
- [ ] Test model failure handling.
- [ ] Measure end-to-end latency.
- [ ] Monitor GPU memory.
- [ ] Improve frame processing.
- [ ] Fix critical bugs.

### Deliverables

- Tested application.
- Test results.
- Performance measurements.
- Bug fixes.

### Completion Criteria

The complete supported workflow operates reliably and known limitations are documented.

---

## Phase 10: Demo and Hackathon Preparation

**Priority:** Critical for submission  
**Status:** Pending

### Objectives

Prepare Signova AI for a clear and reliable hackathon demonstration.

### Tasks

- [ ] Verify all MVP features.
- [ ] Prepare compatible demonstration samples.
- [ ] Test the complete demo workflow.
- [ ] Prepare fallback sample inputs.
- [ ] Verify model and backend startup.
- [ ] Check camera permissions.
- [ ] Prepare project presentation.
- [ ] Prepare system architecture explanation.
- [ ] Document model selection and evaluation.
- [ ] Document current limitations.
- [ ] Prepare demo recording if required.

### Deliverables

- Working demonstration.
- Project presentation.
- Architecture explanation.
- Evaluation summary.
- Known limitations.

### Completion Criteria

The demonstration works using genuine model predictions and does not depend on fabricated outputs.

---

# 3. Future Development Phases

These phases are outside the initial MVP.

## Phase 11: Expanded ISL Vocabulary

Potential tasks:

- Add additional verified signs.
- Evaluate more pretrained models.
- Improve recognition across signers.
- Test different backgrounds and lighting.
- Improve class-level performance.

## Phase 12: Dynamic ISL Recognition

Potential tasks:

- Introduce temporal recognition models.
- Process longer video sequences.
- Recognise movement-based signs.
- Improve sign transition detection.
- Evaluate dynamic recognition datasets.

## Phase 13: Continuous ISL Translation

Potential tasks:

- Investigate continuous ISL datasets.
- Implement sign segmentation.
- Recognise connected signs.
- Add context-aware sentence generation.
- Evaluate sentence-level translation.
- Investigate ISL grammar.

This phase requires a suitable continuous ISL model and dataset.

## Phase 14: Advanced Application Features

Potential tasks:

- User authentication.
- Recognition history.
- PostgreSQL integration.
- User preferences.
- Improved speech options.
- Advanced accessibility features.

---

# 4. Hackathon MVP Scope

The hackathon MVP should focus on the smallest complete and demonstrable recognition workflow.

| Feature | MVP requirement |
|---|---|
| Backend | FastAPI application |
| Model | Verified pretrained candidate |
| Inference | Genuine model output |
| Input | Model-compatible image, video, or landmarks |
| Frontend | React + TypeScript |
| Camera | Permission and live preview |
| Result | Recognised text |
| Speech | Text-to-speech |
| Testing | End-to-end demonstration |
| Documentation | Architecture and limitations |

Do not attempt to complete all future phases during the hackathon.

---

# 5. Development Dependencies

The following order must be maintained because later phases depend on earlier work.

```text
Phase 0: Environment Setup
          |
          v
Phase 1: Backend Foundation
          |
          v
Phase 2: Model Experimentation
          |
          v
Phase 3: Model Evaluation
          |
          v
Phase 4: Model Integration
          |
          v
Phase 5: Visual Processing
          |
          v
Phase 6: Prediction API
          |
          v
Phase 7: Frontend Integration
          |
          v
Phase 8: Speech Output
          |
          v
Phase 9: Testing
          |
          v
Phase 10: Hackathon Demo
```

If model evaluation fails, revisit model research before proceeding with model-dependent implementation.

---

# 6. Milestone Summary

| Milestone | Expected outcome |
|---|---|
| M0 | Development environment ready |
| M1 | Backend running |
| M2 | Pretrained model tested |
| M3 | Model evaluation completed |
| M4 | Model adapter working |
| M5 | Visual input pipeline working |
| M6 | Prediction API working |
| M7 | Frontend connected |
| M8 | Speech output working |
| M9 | Complete application tested |
| M10 | Hackathon demo ready |

---

# 7. Progress Tracking Rules

Update the roadmap whenever a phase starts or finishes.

Use these statuses:

- `Pending`
- `In Progress`
- `Blocked`
- `Completed`
- `Cancelled`

A phase should be marked completed only when its completion criteria are satisfied.

Do not mark a feature completed merely because its files or functions have been created.

Record actual test results and blockers.

---

# 8. Instructions for Antigravity

Before starting a development phase:

1. Read `AGENTS.md` if present.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read `docs/FEATURES.md`.
5. Read `docs/TECH_STACK.md`.
6. Read `docs/SYSTEM_ARCHITECTURE.md`.
7. Read `docs/AI_MODEL_STRATEGY.md`.
8. Read `docs/API_DOCUMENTATION.md`.
9. Read this roadmap.
10. Inspect the current repository state.

Implementation rules:

- Follow the phase order.
- Work backend-first.
- Do not skip model evaluation.
- Do not train a model from scratch without approval.
- Do not treat ASL as ISL.
- Do not claim continuous ISL translation without validation.
- Do not create unnecessary files.
- Preserve existing useful code and data.
- Keep model weights outside Git.
- Test each phase before moving forward.
- Update the relevant documentation.

After each phase, report:

- Phase completed.
- Files created or modified.
- Features implemented.
- Tests executed.
- Actual results.
- Blockers.
- Remaining tasks.
- Recommended next phase.

---

# 9. Final Roadmap Goal

The immediate goal is to deliver a working Signova AI prototype that:

1. Accepts supported signing input.
2. Processes it using the correct model-specific pipeline.
3. Runs a verified pretrained recognition model.
4. Displays genuine recognised text.
5. Provides speech output.
6. Handles uncertain predictions and errors.
7. Demonstrates measurable recognition performance.

The long-term goal is to expand Signova AI into a reliable dynamic and continuous Indian Sign Language understanding system.