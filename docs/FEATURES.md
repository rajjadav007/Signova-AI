# Features

## Signova AI

**Project:** Signova AI  
**Version:** 1.0  
**Status:** Development Planning  
**Platform:** Web Application

---

# 1. Product Overview

Signova AI is a web-based Indian Sign Language recognition application.

It aims to capture signing through a camera, process visual information using a suitable pretrained ISL model, and display recognised text with optional speech output.

The application will use a modular AI architecture so different recognition models can be tested and integrated without redesigning the entire system.

The initial focus is a working and measurable ISL recognition prototype.

---

# 2. Feature Categories

Features are divided into:

- **MVP:** Required for the initial working prototype.
- **Phase 2:** Improvements after the initial prototype.
- **Future:** Advanced features requiring further research and development.
- **Out of Scope:** Features not planned for the current project version.

---

# 3. MVP Features

## 3.1 Camera Access

**Priority:** Critical

Allow users to provide signing input through their device camera.

Features:

- Request browser camera permission.
- Start and stop camera capture.
- Display live camera preview.
- Handle camera permission denial.
- Handle unavailable camera devices.
- Stop camera tracks when recognition ends.

Acceptance criteria:

- Camera preview works in supported browsers.
- Users can start and stop camera access.
- Permission errors are displayed clearly.
- Camera resources are released when no longer needed.

## 3.2 Image and Frame Processing

**Priority:** Critical

Prepare camera frames or uploaded images for the selected recognition pipeline.

Features:

- Capture image frames.
- Validate incoming image data.
- Resize frames when required.
- Convert image formats when required.
- Prepare input for the selected model.
- Handle invalid or empty frames.

Acceptance criteria:

- Valid input reaches the preprocessing pipeline.
- Invalid input returns a clear error.
- Processing follows the selected model's input requirements.

## 3.3 Visual Feature Extraction

**Priority:** Critical, model-dependent

Extract the visual information required by the selected AI model.

Possible techniques:

- Hand landmark extraction.
- Body landmark extraction.
- Pose estimation.
- Image feature extraction.

MediaPipe may be used when compatible with the selected model.

Features:

- Extract required visual features.
- Preserve landmark ordering.
- Handle missing landmarks.
- Validate feature dimensions.
- Prepare data for model-specific preprocessing.

Acceptance criteria:

- Extracted features match the model's expected format.
- Invalid or incomplete features are handled safely.
- No arbitrary landmark format is passed into a model.

## 3.4 Model Preprocessing

**Priority:** Critical

Convert extracted input into the format expected by the pretrained model.

Features:

- Input validation.
- Coordinate normalisation.
- Sequence preparation.
- Tensor conversion.
- Required frame sampling.
- Model-specific feature formatting.

Acceptance criteria:

- Preprocessing matches the original model implementation.
- Input dimensions are validated.
- The same preprocessing logic is used during testing and application inference.

## 3.5 Pretrained Model Inference

**Priority:** Critical

Run the selected pretrained ISL recognition model.

Initial candidate:

`manavdhamecha77/iSign-t5-pose-to-text`

Initial checkpoint for experimentation:

`t5-small`

Features:

- Load model checkpoint.
- Select CPU or CUDA when available.
- Run inference.
- Handle model loading errors.
- Handle inference errors.
- Return genuine model output.
- Report model status.

Acceptance criteria:

- The model loads successfully.
- Input is compatible with the model.
- Predictions come from actual inference.
- Unsupported inputs are rejected.
- Model limitations are documented.

**Important:** iSign T5 is a pose-to-text candidate. It does not directly accept raw webcam images. Its suitability must be validated before it is selected as the final model.

## 3.6 Text Output

**Priority:** Critical

Display recognised text to the user.

Features:

- Display prediction results.
- Show recognition status.
- Handle empty predictions.
- Indicate uncertain predictions.
- Provide clear error messages.

Acceptance criteria:

- Genuine model output is displayed.
- Failed inference is not represented as a successful prediction.
- Unsupported or uncertain results are clearly identified.

## 3.7 Text-to-Speech

**Priority:** High

Convert recognised text into spoken audio.

Features:

- Generate speech from recognised text.
- Play audio output.
- Provide play and stop controls.
- Handle unavailable speech services.
- Allow users to enable or disable speech.

The browser SpeechSynthesis API can be used for the initial prototype.

Acceptance criteria:

- Supported recognised text can be spoken.
- Speech controls work correctly.
- Speech failures do not interrupt recognition.

## 3.8 Backend API

**Priority:** Critical

Provide communication between the frontend and AI system through FastAPI.

Features:

- Backend health endpoint.
- AI service health endpoint.
- Model information endpoint.
- Supported prediction endpoints.
- Request validation.
- Structured responses.
- Error handling.

Acceptance criteria:

- Backend starts successfully.
- Health endpoints return actual service status.
- Supported inputs reach the AI service.
- API responses follow the documented format.
- Model failures return appropriate errors.

## 3.9 Model Status

**Priority:** High

Show whether the AI service and selected model are ready.

Features:

- Backend connection status.
- AI service status.
- Model loading status.
- Selected model information.
- Model availability errors.

Acceptance criteria:

- Status reflects the actual runtime state.
- A model that has not loaded is never reported as ready.

---

# 4. Phase 2 Features

These features should be implemented after the initial recognition pipeline works.

## 4.1 Improved Live Recognition

- Continuous frame capture.
- Efficient frame sampling.
- Stable prediction display.
- Duplicate prediction suppression.
- Recognition start and stop controls.
- Improved inference latency.

## 4.2 Recognition Feedback

- Display recognition confidence when supported.
- Show uncertain predictions.
- Provide feedback when a sign is not recognised.
- Display model processing time.
- Improve error messages.

Confidence must be based on meaningful model output, not an invented score.

## 4.3 Expanded Vocabulary

- Add verified ISL signs.
- Support additional sign classes.
- Evaluate new model checkpoints.
- Improve recognition across different signers.

New vocabulary must be supported by compatible model training or checkpoints.

## 4.4 UI Improvements

- Recognition result panel.
- Camera status indicator.
- Model status indicator.
- Speech controls.
- Clear and reset controls.
- Responsive layout.
- Loading and error states.

## 4.5 Performance Improvements

- Optimise frame processing.
- Reduce unnecessary model calls.
- Improve GPU utilisation.
- Add CPU fallback where practical.
- Measure end-to-end latency.

---

# 5. Future Features

These features require additional research, compatible datasets, and model development.

## 5.1 Dynamic ISL Recognition

Recognise signs that involve movement over time.

Potential capabilities:

- Video sequence recognition.
- Temporal feature extraction.
- Motion-based recognition.
- Sign transition detection.
- Improved recognition of dynamic gestures.

Possible model approaches:

- LSTM.
- Transformer.
- 3D CNN.
- Other suitable temporal models.

## 5.2 Continuous ISL Translation

Interpret connected signing and convert it into meaningful text.

Potential capabilities:

- Continuous video understanding.
- Sign boundary detection.
- Multiple sign recognition.
- Sentence construction.
- Context-aware text generation.
- ISL grammar handling.

This requires a suitable continuous ISL dataset and validated sequence-to-text model.

It is not included in the initial MVP.

## 5.3 Facial and Non-Manual Features

Investigate additional visual information such as:

- Facial expressions.
- Head movements.
- Body posture.
- Non-manual linguistic markers.

These features may improve interpretation where supported by the target ISL model and dataset.

## 5.4 User Accounts

Potential capabilities:

- User registration.
- User login.
- User preferences.
- Personal settings.

Authentication is not required for the initial MVP.

## 5.5 Recognition History

Potential capabilities:

- Save recognised text.
- View previous results.
- Delete saved history.
- Search previous recognition records.

Saving history should require user consent.

## 5.6 Multilingual Speech Output

Potential capabilities:

- Select supported speech languages.
- Use additional text-to-speech providers.
- Configure voice and playback speed.

This feature changes the spoken output language. It does not replace the ISL recognition model.

---

# 6. Out-of-Scope Features

The following are not part of the initial MVP:

- Training a complete ISL model from scratch.
- Claiming full continuous ISL translation.
- Treating ASL recognition as ISL recognition.
- Supporting every ISL sign and regional variation.
- Automatic sentence translation without a validated sequence model.
- User authentication.
- Persistent recognition history.
- Mandatory PostgreSQL integration.
- Permanent cloud GPU infrastructure.
- Automatic storage of webcam recordings.
- Fabricated model predictions or confidence scores.

---

# 7. Feature Priority Matrix

| Feature | Priority | Phase |
|---|---|---|
| Camera access | Critical | MVP |
| Image/frame processing | Critical | MVP |
| Visual feature extraction | Critical | MVP |
| Model preprocessing | Critical | MVP |
| Pretrained model inference | Critical | MVP |
| Text output | Critical | MVP |
| FastAPI integration | Critical | MVP |
| Model status | High | MVP |
| Text-to-speech | High | MVP |
| Improved live recognition | High | Phase 2 |
| Recognition feedback | High | Phase 2 |
| Expanded vocabulary | High | Phase 2 |
| Performance optimisation | High | Phase 2 |
| Dynamic ISL recognition | Future | Future |
| Continuous ISL translation | Future | Future |
| Facial and non-manual features | Future | Future |
| User accounts | Future | Future |
| Recognition history | Future | Future |
| Multilingual speech output | Future | Future |

---

# 8. User Workflow

The initial user workflow:

```text
Open Signova AI
       |
       v
Grant Camera Permission
       |
       v
Start Camera
       |
       v
Capture Signing Input
       |
       v
Process Frames
       |
       v
Extract Required Features
       |
       v
Preprocess Model Input
       |
       v
Run Pretrained Model
       |
       v
Validate Prediction
       |
       v
Display Recognised Text
       |
       v
Generate Speech
       |
       v
User Hears Output
```

The workflow must follow the actual capabilities of the integrated model.

---

# 9. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The application must request camera permission. |
| FR-02 | The application must display camera preview. |
| FR-03 | The application must support camera start and stop. |
| FR-04 | The system must validate incoming input. |
| FR-05 | The AI pipeline must apply model-compatible preprocessing. |
| FR-06 | The AI system must load the configured pretrained model. |
| FR-07 | The backend must execute genuine model inference. |
| FR-08 | The application must display recognised text. |
| FR-09 | The application must handle uncertain predictions. |
| FR-10 | The application must provide speech output. |
| FR-11 | The backend must report service health. |
| FR-12 | The application must handle model and API errors. |

---

# 10. Non-Functional Requirements

## 10.1 Performance

- Avoid unnecessary frame processing.
- Load the model once and reuse it.
- Measure inference latency.
- Use GPU when available and compatible.
- Provide CPU fallback where practical.

## 10.2 Reliability

- Handle invalid inputs.
- Handle camera errors.
- Handle model loading failures.
- Handle inference failures.
- Avoid fabricated predictions.

## 10.3 Usability

- Simple interface.
- Clear camera controls.
- Readable text output.
- Clear recognition status.
- Accessible speech controls.
- Responsive design.

## 10.4 Privacy

- Request camera permission.
- Do not save webcam footage by default.
- Do not upload unnecessary camera data.
- Require consent before storing recognition history.

## 10.5 Maintainability

- Keep frontend and backend separate.
- Keep model adapters modular.
- Separate preprocessing from inference.
- Write tests for important AI components.
- Maintain clear documentation.

---

# 11. MVP Acceptance Criteria

The initial prototype is considered functional when:

- [ ] Frontend runs successfully.
- [ ] Backend runs successfully.
- [ ] Camera access works.
- [ ] Supported input can be captured.
- [ ] Model-compatible preprocessing works.
- [ ] Selected pretrained model loads successfully.
- [ ] Real inference produces output on compatible samples.
- [ ] Recognised text is displayed.
- [ ] Speech output works.
- [ ] API errors are handled.
- [ ] Model status is accurate.
- [ ] Recognition limitations are documented.

A successful application demo does not by itself establish production-level ISL translation accuracy.

---

# 12. Development Order

Implement features in this order:

1. Repository and environment setup.
2. FastAPI backend foundation.
3. Model experimentation.
4. Standalone inference testing.
5. Model adapter implementation.
6. Visual feature extraction.
7. Preprocessing integration.
8. Prediction API.
9. Frontend camera integration.
10. Recognition result display.
11. Text-to-speech integration.
12. End-to-end testing.
13. Performance improvements.

Do not start advanced features before the initial recognition pipeline is validated.

---

# 13. Instructions for Antigravity

Before implementing features:

1. Read `AGENTS.md` if present.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read `docs/TECH_STACK.md`.
5. Read `docs/SYSTEM_ARCHITECTURE.md`.
6. Read `docs/AI_MODEL_STRATEGY.md`.
7. Read this document.
8. Inspect the existing repository.

Implementation rules:

- Follow the MVP scope.
- Work backend-first.
- Test model inference independently.
- Use pretrained models.
- Do not train from scratch without approval.
- Do not treat ASL as ISL.
- Do not claim continuous translation without validation.
- Keep model-specific code modular.
- Do not add PostgreSQL unless required.
- Do not create unnecessary files.
- Do not implement future features prematurely.
- Update documentation when feature scope changes.

After each task, report:

- Features implemented.
- Files created or modified.
- Tests executed.
- Actual test results.
- Known limitations.
- Remaining tasks.

---

# 14. Final Product Direction

The first version of Signova AI should focus on a reliable and demonstrable ISL recognition workflow.

The priority is not to implement the largest number of features. It is to build a working system that uses a verified model, processes compatible signing input, returns genuine predictions, and provides clear text and speech output.

Advanced dynamic and continuous ISL translation will be developed only after the initial recognition pipeline is validated.