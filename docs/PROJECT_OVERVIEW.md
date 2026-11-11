# Project Overview

## Signova AI

**Project Name:** Signova AI  
**Category:** Artificial Intelligence / Accessibility Technology  
**Primary Domain:** Indian Sign Language Recognition  
**Application Type:** Web Application  
**Development Status:** Prototype Development  
**Architecture:** React Frontend + FastAPI Backend + Modular AI Pipeline

---

# 1. Introduction

Signova AI is an AI-powered accessibility application designed to recognise Indian Sign Language (ISL) signing input and convert recognised signs into readable text and spoken output.

The application aims to make communication easier between people who use sign language and people who may not understand it.

Signova AI uses computer vision, pretrained machine learning models, and speech technologies to create a practical sign recognition experience.

The initial development focuses on a functional prototype using pretrained models rather than training a new model from scratch.

---

# 2. Problem Statement

Communication between sign language users and non-signers can be difficult because many people do not understand Indian Sign Language.

Existing communication methods may require:

- A human interpreter.
- Written communication.
- Manual assistance.
- Knowledge of sign language from both participants.

There is a need for an accessible technology solution that can process signing input and provide understandable text and speech output.

Signova AI aims to address this problem through an AI-based recognition workflow.

---

# 3. Project Vision

Build an accessible and practical Indian Sign Language recognition system that can interpret supported signing input and communicate the recognised meaning through text and speech.

The long-term vision is to develop a system capable of handling dynamic signs and continuous ISL communication.

---

# 4. Project Objectives

- Recognise supported ISL signing input.
- Process visual input using computer vision.
- Integrate suitable pretrained recognition models.
- Convert model predictions into readable text.
- Provide text-to-speech output.
- Build a simple and accessible web interface.
- Keep AI components modular and replaceable.
- Evaluate recognition performance using suitable ISL data.
- Explore dynamic and continuous ISL translation as future development.

---

# 5. Target Users

### Primary Users

- People who communicate using Indian Sign Language.
- People with hearing or speech disabilities who use ISL.

### Secondary Users

- Family members and friends of ISL users.
- Teachers and students.
- Accessibility organisations.
- People interested in learning about ISL.

---

# 6. Core Application Workflow

The planned application workflow is:

```text
User
 |
 v
Webcam / Video Input
 |
 v
Frame Capture
 |
 v
Visual Processing
 |
 v
Feature Extraction
 |
 v
Model-Specific Preprocessing
 |
 v
Pretrained ISL Model
 |
 v
Prediction Processing
 |
 v
Recognised Text
 |
 v
Text-to-Speech
 |
 v
User
```

The exact visual processing and feature extraction steps depend on the selected pretrained model.

For example, a pose-based model requires compatible pose landmarks, while an image-based model requires the image input format expected by that model.

---

# 7. Main Features

## 7.1 Camera Input

- Request webcam permission.
- Display live camera preview.
- Start and stop camera input.
- Capture frames for recognition.

## 7.2 Visual Processing

- Process image or video frames.
- Extract required visual features.
- Prepare model-compatible inputs.
- Validate incoming data.

## 7.3 AI Recognition

- Load a pretrained model.
- Run model inference.
- Process prediction outputs.
- Display recognised text.
- Handle unsupported or uncertain predictions.

## 7.4 Text Output

- Display recognised text.
- Show recognition status.
- Provide useful feedback when recognition fails.

## 7.5 Speech Output

- Convert recognised text into speech.
- Provide play and stop controls.
- Handle browser speech support.

---

# 8. AI Model Strategy

Signova AI follows a pretrained-model-first strategy.

Training a complete recognition model from scratch is outside the initial hackathon scope.

### Initial Experimental Candidate

**Model:** `manavdhamecha77/iSign-t5-pose-to-text`

**Initial checkpoint:** `t5-small`

**Model type:** Pose-to-text sequence generation.

The model expects structured pose and hand landmark inputs. It is not a direct raw-webcam-image-to-text model.

Before integration, the project must verify:

- Model architecture.
- Expected input dimensions.
- Landmark ordering.
- Preprocessing and normalisation.
- Compatible dataset samples.
- Prediction quality.
- Model and dataset licences.

This is an experimental candidate, not a confirmed production-ready ISL model.

### Model Integration Principles

- Keep model loading separate from API routes.
- Keep preprocessing model-specific.
- Use reusable model adapters.
- Avoid hardcoding model logic into the frontend.
- Evaluate models before selecting them.
- Keep large checkpoints outside Git.

---

# 9. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Language | TypeScript |
| Build Tool | Vite |
| Backend | FastAPI |
| Backend Language | Python |
| AI Framework | PyTorch |
| Computer Vision | OpenCV |
| Landmark Extraction | MediaPipe, if required |
| Model Repository | Hugging Face |
| Speech Output | Browser SpeechSynthesis API |
| Database | PostgreSQL, optional future integration |
| Testing | Pytest and Vitest |

The final AI dependencies will depend on the selected pretrained model and its original implementation.

---

# 10. System Architecture

Signova AI is designed with separate application layers.

## Frontend Layer

Responsible for:

- User interface.
- Camera access.
- Frame capture.
- API communication.
- Prediction display.
- Speech controls.

## Backend Layer

Responsible for:

- API endpoints.
- Input validation.
- Application configuration.
- AI service coordination.
- Error handling.
- Response formatting.

## AI Layer

Responsible for:

- Model loading.
- Visual preprocessing.
- Landmark extraction when required.
- Model-specific input preparation.
- Inference.
- Prediction postprocessing.

## Data Layer

PostgreSQL may be introduced for future features such as:

- User accounts.
- Recognition history.
- User preferences.
- Model metadata.

Database integration is not required for the initial recognition MVP.

---

# 11. Development Strategy

Development will follow a backend-first approach.

| Stage | Focus |
|---|---|
| 1 | Repository and environment setup |
| 2 | FastAPI backend foundation |
| 3 | Pretrained model research |
| 4 | Model evaluation |
| 5 | Model adapter and inference |
| 6 | Visual input processing |
| 7 | Prediction API |
| 8 | React frontend |
| 9 | Text-to-speech |
| 10 | Testing and demo preparation |

Each stage must be tested before moving to dependent stages.

See `PHASE_ROADMAP.md` for detailed development phases and `PROGRESS_TRACKER.md` for implementation status.

---

# 12. MVP Scope

The initial prototype focuses on:

- Webcam or supported visual input.
- Model-compatible preprocessing.
- A verified pretrained recognition model.
- Genuine prediction output.
- Recognised text display.
- Text-to-speech.
- Basic error handling.
- End-to-end demonstration.

The MVP must only support input types that the selected model can process.

---

# 13. Future Scope

Potential future improvements include:

### Expanded ISL Recognition

- Larger verified vocabulary.
- Better recognition across different signers.
- Improved lighting and background handling.

### Dynamic ISL Recognition

- Movement-based sign recognition.
- Temporal sequence processing.
- Better sign transition handling.

### Continuous ISL Translation

- Continuous sign segmentation.
- Connected sign recognition.
- Context-aware sentence generation.
- ISL grammar-aware translation.

### Application Improvements

- Recognition history.
- User accounts.
- Advanced accessibility options.
- Improved speech controls.
- Additional deployment options.

These features require suitable models, datasets, and evaluation.

---

# 14. Project Limitations

The initial prototype has important limitations:

- Recognition depends on the selected model's supported vocabulary and input format.
- A pose-to-text model cannot directly process raw webcam frames without preprocessing.
- Isolated sign recognition does not automatically provide continuous sentence translation.
- ASL models are not interchangeable with ISL models.
- Model performance must be verified using compatible ISL samples.
- Lighting, camera position, signing speed, and signer variation may affect recognition.
- Browser speech availability depends on the user's device and browser.

The project must communicate these limitations honestly.

---

# 15. Project Success Criteria

The initial prototype will be considered successful when:

1. The backend runs reliably.
2. A suitable pretrained model has been evaluated.
3. The model accepts correctly prepared input.
4. Genuine recognition predictions are produced.
5. The frontend communicates with the backend.
6. Recognised text is displayed.
7. Speech output works.
8. Critical errors are handled.
9. The complete workflow is demonstrated.
10. Model performance and limitations are documented.

---

# 16. Project Documentation

The following documents define the project:

| Document | Purpose |
|---|---|
| `PRD.md` | Product requirements |
| `PROJECT_OVERVIEW.md` | Project introduction and direction |
| `FEATURES.md` | Feature scope |
| `TECH_STACK.md` | Technology selection |
| `SYSTEM_ARCHITECTURE.md` | System design |
| `AI_MODEL_STRATEGY.md` | Model research and integration |
| `PHASE_ROADMAP.md` | Development phases |
| `PROGRESS_TRACKER.md` | Actual implementation progress |
| `API_DOCUMENTATION.md` | Backend API contract |
| `DATABASE_SCHEMA.md` | Database design |
| `DEPLOYMENT.md` | Local and production deployment |

---

# 17. Final Direction

Signova AI aims to become a practical Indian Sign Language recognition and communication platform.

The immediate priority is to establish a reliable pretrained-model inference pipeline and connect it to a working web application.

The long-term direction is to move beyond limited sign recognition towards dynamic and continuous ISL understanding.