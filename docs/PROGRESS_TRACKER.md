# Progress Tracker

## Signova AI

**Project:** Signova AI  
**Version:** 1.0  
**Last Updated:** YYYY-MM-DD  
**Overall Status:** Pending  
**Development Approach:** Backend First

---

# 1. Project Progress

Use this document to track the actual development progress of Signova AI.

| Area | Status | Notes |
|---|---|---|
| Repository Setup | Pending | |
| Backend Foundation | Pending | |
| Pretrained Model Research | Pending | |
| Model Evaluation | Pending | |
| Model Integration | Pending | |
| Visual Processing | Pending | |
| Prediction API | Pending | |
| Frontend Development | Pending | |
| Text-to-Speech | Pending | |
| Testing | Pending | |
| Hackathon Demo | Pending | |

**Status values:**
- `Pending`
- `In Progress`
- `Blocked`
- `Completed`
- `Cancelled`

Only mark a task completed after implementation and testing.

---

# 2. Phase-wise Progress

## Phase 0: Repository and Environment Setup

**Status:** Pending

- [ ] Inspect existing repository.
- [ ] Review project documentation.
- [ ] Verify project structure.
- [ ] Configure Python environment.
- [ ] Configure Node.js environment.
- [ ] Install backend dependencies.
- [ ] Install frontend dependencies.
- [ ] Verify PyTorch installation.
- [ ] Verify CUDA availability.
- [ ] Configure `.gitignore`.
- [ ] Configure environment variables.

**Completion evidence:**

- Environment setup verified.
- Required dependencies installed.
- GPU availability checked.

**Blockers:**

None recorded.

---

## Phase 1: Backend Foundation

**Status:** Pending

- [ ] Create FastAPI application.
- [ ] Configure application settings.
- [ ] Configure CORS.
- [ ] Create API route structure.
- [ ] Implement `/api/v1/health`.
- [ ] Implement `/api/v1/ai/health`.
- [ ] Add request validation.
- [ ] Add error handling.
- [ ] Configure API documentation.
- [ ] Add backend tests.

**Completion evidence:**

- Backend starts successfully.
- Health endpoints return valid responses.
- Backend tests pass.

**Blockers:**

None recorded.

---

## Phase 2: AI Model Research and Experimentation

**Status:** Pending

**Primary candidate:** `manavdhamecha77/iSign-t5-pose-to-text`

**Initial checkpoint:** `t5-small`

- [ ] Inspect model repository.
- [ ] Verify model architecture.
- [ ] Inspect original inference code.
- [ ] Verify checkpoint configuration.
- [ ] Understand required input dimensions.
- [ ] Verify landmark ordering.
- [ ] Understand preprocessing and normalisation.
- [ ] Find compatible sample data.
- [ ] Download required checkpoint.
- [ ] Run standalone inference.
- [ ] Record predictions.
- [ ] Measure inference latency.
- [ ] Monitor memory usage.

**Completion evidence:**

- Model loads successfully.
- Compatible sample inference works.
- Actual outputs are recorded.
- Model limitations are documented.

**Blockers:**

None recorded.

---

## Phase 3: Model Evaluation and Selection

**Status:** Pending

- [ ] Obtain compatible labeled ISL samples.
- [ ] Verify sample annotations.
- [ ] Reproduce original preprocessing.
- [ ] Evaluate multiple samples.
- [ ] Compare predictions with ground truth.
- [ ] Calculate evaluation metrics.
- [ ] Measure inference performance.
- [ ] Check model licence.
- [ ] Check dataset licence.
- [ ] Decide whether the candidate is suitable.

**Evaluation results:**

| Metric | Result |
|---|---|
| Accuracy | Not evaluated |
| Precision | Not evaluated |
| Recall | Not evaluated |
| F1-score | Not evaluated |
| Inference latency | Not measured |
| GPU memory | Not measured |

**Completion evidence:**

A documented evaluation and model selection decision based on compatible ISL data.

**Blockers:**

None recorded.

---

## Phase 4: Model Adapter and Inference Integration

**Status:** Pending

- [ ] Define model adapter interface.
- [ ] Implement model loading.
- [ ] Implement model configuration.
- [ ] Implement model-specific preprocessing.
- [ ] Implement inference execution.
- [ ] Implement output formatting.
- [ ] Implement prediction validation.
- [ ] Implement model status reporting.
- [ ] Add inference tests.

**Completion evidence:**

The selected model runs through a reusable AI module independently of the frontend.

**Blockers:**

None recorded.

---

## Phase 5: Visual Input and Processing Pipeline

**Status:** Pending

- [ ] Implement image or video input processing.
- [ ] Implement frame extraction.
- [ ] Add frame validation.
- [ ] Implement required feature extraction.
- [ ] Add hand landmark extraction if required.
- [ ] Add body landmark extraction if required.
- [ ] Match model-specific landmark ordering.
- [ ] Implement coordinate normalisation.
- [ ] Implement sequence preparation if required.
- [ ] Validate processed inputs.
- [ ] Test with compatible samples.

**Completion evidence:**

Visual input is converted into the exact format expected by the selected model.

**Blockers:**

None recorded.

---

## Phase 6: AI Prediction API

**Status:** Pending

- [ ] Create AI service layer.
- [ ] Connect model manager.
- [ ] Implement supported prediction endpoints.
- [ ] Add input validation.
- [ ] Add structured response schemas.
- [ ] Add inference error handling.
- [ ] Measure processing time.
- [ ] Test successful requests.
- [ ] Test invalid requests.
- [ ] Update API documentation.

**Completion evidence:**

Supported input reaches the model through FastAPI and returns genuine predictions.

**Blockers:**

None recorded.

---

## Phase 7: Frontend Development and Integration

**Status:** Pending

- [ ] Configure React and TypeScript.
- [ ] Build main application layout.
- [ ] Implement camera permission handling.
- [ ] Implement live camera preview.
- [ ] Add camera start and stop controls.
- [ ] Implement frame capture.
- [ ] Connect frontend API services.
- [ ] Display recognition status.
- [ ] Display model status.
- [ ] Display prediction results.
- [ ] Display errors and loading states.
- [ ] Test frontend-backend communication.

**Completion evidence:**

The frontend sends supported input to the backend and displays actual model predictions.

**Blockers:**

None recorded.

---

## Phase 8: Text-to-Speech

**Status:** Pending

- [ ] Integrate SpeechSynthesis API.
- [ ] Add speech play control.
- [ ] Add speech stop control.
- [ ] Add speech enable and disable setting.
- [ ] Handle unsupported browser features.
- [ ] Test spoken output.

**Completion evidence:**

Recognised text can be spoken through a supported browser voice.

**Blockers:**

None recorded.

---

## Phase 9: Testing and Optimisation

**Status:** Pending

- [ ] Test backend endpoints.
- [ ] Test model loading.
- [ ] Test inference.
- [ ] Test preprocessing.
- [ ] Test camera permissions.
- [ ] Test frontend integration.
- [ ] Test speech output.
- [ ] Test invalid inputs.
- [ ] Test error handling.
- [ ] Measure end-to-end latency.
- [ ] Monitor memory usage.
- [ ] Fix critical bugs.

**Completion evidence:**

The supported application workflow passes the required tests.

**Blockers:**

None recorded.

---

## Phase 10: Hackathon Demo Preparation

**Status:** Pending

- [ ] Verify MVP features.
- [ ] Prepare compatible demonstration samples.
- [ ] Test complete demo workflow.
- [ ] Prepare fallback sample inputs.
- [ ] Verify model and backend startup.
- [ ] Check camera permissions.
- [ ] Prepare project presentation.
- [ ] Prepare architecture explanation.
- [ ] Prepare model evaluation summary.
- [ ] Document known limitations.

**Completion evidence:**

A working demonstration using genuine model predictions.

**Blockers:**

None recorded.

---

# 3. Future Development Tracking

These features are not part of the initial MVP.

| Feature | Status |
|---|---|
| Expanded ISL vocabulary | Not Started |
| Improved signer variation handling | Not Started |
| Dynamic ISL recognition | Not Started |
| Continuous ISL translation | Not Started |
| Sign segmentation | Not Started |
| Context-aware sentence generation | Not Started |
| Recognition history | Not Started |
| User authentication | Not Started |
| Advanced accessibility features | Not Started |

---

# 4. Model Experiment Tracker

Use this table to record every model experiment.

| Model | Input Type | Checkpoint | Test Status | Decision |
|---|---|---|---|---|
| iSign T5 | Pose landmarks | t5-small | Not Evaluated | Experimental |
| Other candidates | To be verified | To be verified | Not Evaluated | Not Selected |

For each experiment, record:

- Model repository.
- Model architecture.
- Checkpoint.
- Required input format.
- Preprocessing method.
- Dataset used.
- Number of test samples.
- Evaluation metrics.
- Inference latency.
- Hardware used.
- Licence information.
- Final decision.

Do not mark a model as working based only on successful loading.

---

# 5. Bug and Blocker Tracker

| ID | Issue | Priority | Status | Resolution |
|---|---|---|---|---|
| B-001 | No blockers recorded yet | - | - | - |

Use these priority levels:

- Critical
- High
- Medium
- Low

Record problems that prevent progress, affect recognition quality, or break the application workflow.

---

# 6. Development Activity Log

Record meaningful development updates.

| Date | Phase | Work Completed | Test Result | Next Action |
|---|---|---|---|---|
| YYYY-MM-DD | Phase 0 | Initial tracking setup | Not tested | Inspect repository |

Add a new row after each meaningful development session.

Avoid logging every small code edit.

---

# 7. MVP Completion Checklist

The MVP is complete only when all required items below are verified.

- [ ] Backend runs successfully.
- [ ] A suitable pretrained model is selected.
- [ ] Model evaluation is documented.
- [ ] Model inference works.
- [ ] Visual input processing works.
- [ ] Prediction API works.
- [ ] Frontend connects to the backend.
- [ ] Camera input works.
- [ ] Recognised text is displayed.
- [ ] Text-to-speech works.
- [ ] Critical errors are handled.
- [ ] End-to-end testing is complete.
- [ ] Hackathon demo is ready.

---

# 8. Progress Update Rules

1. Update task status only after checking the actual implementation.
2. Record test results instead of assuming success.
3. Keep failed experiments in the tracker.
4. Record blockers and their resolutions.
5. Do not remove completed work from the history.
6. Update model results whenever a new experiment is performed.
7. Keep this tracker consistent with `PHASE_ROADMAP.md`.
8. Do not mark continuous ISL translation complete unless it has been implemented and evaluated.

---

# 9. Current Development Priority

Follow this order:

1. Repository and environment inspection.
2. Backend foundation.
3. Pretrained model experimentation.
4. Model evaluation.
5. Model integration.
6. Visual input pipeline.
7. Prediction API.
8. Frontend integration.
9. Text-to-speech.
10. Testing and demo preparation.

**Immediate next action:** Inspect the current repository and verify the development environment before implementing the next phase.