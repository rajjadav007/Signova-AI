# Signova AI
## Project Overview and Product Blueprint

**Project Name:** Signova AI  
**Document:** Project Overview  
**Version:** 1.0  
**Status:** Planning and Development  
**Primary Platform:** Web Application  
**Primary Sign Language:** Indian Sign Language (ISL)  
**Primary Market:** India  
**Frontend:** React + JavaScript + Vite  
**Backend:** Python + FastAPI  
**Machine Learning:** PyTorch + OpenCV  
**Speech AI:** Sarvam AI  

---

# 1. Introduction

## 1.1 About the Project

Signova AI is an AI-powered accessibility and communication platform designed to reduce communication barriers between Indian Sign Language (ISL) users and people who do not understand sign language.

The platform combines computer vision, machine learning, and speech technologies to recognise supported ISL signs through a camera and convert recognised output into readable text and spoken language.

It also aims to provide reverse communication through speech-to-text technology, allowing non-signers to communicate with ISL users through spoken input converted into readable text.

Signova AI focuses on making communication more accessible, intuitive, and convenient through a unified digital platform.

The initial implementation will concentrate on a limited, validated vocabulary of ISL signs. The system will progressively expand towards dynamic sign recognition and more advanced language understanding.

## 1.2 Project Vision

To build an intelligent accessibility platform that connects sign language, text, and speech, helping people communicate more independently regardless of their ability to understand sign language.

## 1.3 Project Mission

- Reduce communication barriers for ISL users.
- Make supported sign recognition accessible through everyday devices.
- Convert recognised signs into readable text and speech.
- Support reverse communication using speech-to-text.
- Promote Indian Sign Language awareness and learning.
- Use AI responsibly to improve accessibility and inclusion.

## 1.4 Core Idea

Signova AI acts as a communication bridge between two groups:

1. People who communicate using Indian Sign Language.
2. People who communicate using spoken or written language.

The platform connects these communication methods through AI-based recognition and speech technologies.

---

# 2. Problem and Opportunity

## 2.1 The Problem

Communication between sign language users and non-signers can be difficult because many people do not understand Indian Sign Language.

This creates challenges in:

- Educational institutions.
- Hospitals and healthcare environments.
- Workplaces.
- Government and public service offices.
- Shops and businesses.
- Public transportation.
- Everyday social interactions.

People who use sign language may need to depend on interpreters, written communication, or assistance from other people.

These options are not always available or convenient.

## 2.2 The Opportunity

Modern computer vision and AI speech technologies create opportunities to develop assistive communication tools.

Signova AI aims to combine these capabilities into one accessible platform.

Instead of treating sign recognition and speech processing as unrelated tools, the platform connects them through a common communication interface.

## 2.3 Proposed Approach

Signova AI will:

1. Capture sign gestures through a device camera.
2. Process the visual input.
3. Recognise supported ISL signs using an appropriate ML model.
4. Convert recognised labels into readable text.
5. Generate spoken output using a supported TTS service.
6. Accept spoken input from non-signers.
7. Convert speech into text using a supported STT service.
8. Display both communication directions through a common interface.

---

# 3. Product Objectives

## 3.1 Primary Objectives

| ID | Objective | Expected Result |
|---|---|---|
| OBJ-01 | Develop ISL recognition | Recognise a validated set of ISL signs |
| OBJ-02 | Build camera integration | Capture live visual input |
| OBJ-03 | Build sign-to-text | Display recognised signs as text |
| OBJ-04 | Integrate speech output | Convert supported text into speech |
| OBJ-05 | Build reverse communication | Convert spoken input into text |
| OBJ-06 | Create a unified interface | Connect both communication directions |
| OBJ-07 | Build modular AI services | Allow future model replacement and improvements |
| OBJ-08 | Ensure accessibility | Provide a usable and responsive interface |

## 3.2 Secondary Objectives

- Introduce an ISL learning section.
- Support additional Indian spoken languages where available.
- Improve model performance through evaluation.
- Introduce optional conversation history.
- Support future mobile deployment.
- Explore offline inference where technically practical.

## 3.3 Product Success

The project will be considered successful when it demonstrates:

- A working camera-based ISL recognition workflow.
- Correct handling of the selected vocabulary.
- Reliable text output for supported signs.
- Functional speech generation.
- Functional speech-to-text communication.
- Successful frontend and backend integration.
- Measured ML performance.
- Clear handling of unsupported and uncertain inputs.

Success must be demonstrated through actual tests, not assumed from implementation.

---

# 4. Target Users

## 4.1 Primary Users

### ISL Users

People who communicate using Indian Sign Language.

Expected benefits:

- More accessible communication with non-signers.
- Text output from supported signs.
- Spoken output from recognised text.
- A simple communication interface.

### Non-Signers

People who do not understand Indian Sign Language.

Expected benefits:

- Better understanding of supported signs.
- Spoken communication converted into readable text.
- A shared interface for conversations.

## 4.2 Secondary Users

### Students and Educators

- Explore basic ISL signs.
- Use the learning section.
- Improve awareness of accessible communication.

### Families and Caregivers

- Learn supported signs.
- Improve daily communication.
- Support independent interactions.

### Organisations and Public Services

- Explore accessible communication support.
- Improve interactions with ISL users.
- Use assistive tools in suitable environments.

---

# 5. Product Structure

Signova AI is divided into independent but connected modules.

## 5.1 Main Modules

| Module | Responsibility | Priority |
|---|---|---|
| User Interface | Main application and navigation | High |
| Camera Module | Capture live visual input | High |
| ISL Recognition Engine | Recognise supported signs | Critical |
| Prediction Processor | Stabilise and validate predictions | High |
| Sign-to-Text Engine | Convert model labels into readable text | High |
| Speech Engine | Convert text into speech | High |
| Reverse Communication | Convert speech into text | High |
| Conversation Interface | Present both communication directions | High |
| Learning Centre | Teach supported ISL signs | Medium |
| User Preferences | Store accessibility preferences | Low |
| User Management | Optional account and profile functionality | Low |
| Conversation History | Optional persistent conversation records | Low |

## 5.2 Module Boundaries

Each module should have a clear responsibility.

For example:

- The camera module captures frames. It does not decide what a sign means.
- The recognition engine predicts a supported class. It does not generate natural language by itself.
- The text engine converts validated predictions into display text.
- The speech engine converts text into audio.
- The conversation interface displays the results of these services.

This separation will make the application easier to test, maintain, and extend.

---

# 6. Core Communication Workflows

## 6.1 Workflow A: Sign Language to Text and Speech

This is the primary workflow of Signova AI.

**Flow:**

ISL User  
↓  
Device Camera  
↓  
Live Frame Capture  
↓  
Image or Video Preprocessing  
↓  
ISL Recognition Model  
↓  
Prediction Validation  
↓  
Sign Label Mapping  
↓  
Readable Text Output  
↓  
Sarvam AI Text-to-Speech  
↓  
Audio Playback

### Detailed Explanation

**Step 1: Camera Input**

The application requests permission to access the camera and displays a live preview.

**Step 2: Frame Capture**

The frontend captures appropriate frames from the camera.

The system should avoid sending every frame unnecessarily. Frame sampling and transmission frequency must be selected based on measured performance.

**Step 3: Preprocessing**

The backend or ML service prepares input according to the selected model's requirements.

Preprocessing may include:

- Resizing.
- Normalisation.
- Colour conversion.
- Frame selection.
- Landmark extraction, if supported by the selected architecture.

**Step 4: Recognition**

The selected ISL model processes the input and returns a prediction.

The model may recognise:

- Static signs.
- Supported individual words.
- Dynamic sign sequences, if a suitable temporal model is implemented.

These capabilities must be treated separately.

**Step 5: Prediction Validation**

The system checks whether the prediction is reliable enough to display.

Potential methods:

- Confidence threshold.
- Temporal smoothing.
- Majority voting.
- Duplicate suppression.

**Step 6: Text Conversion**

The recognised model label is mapped to a readable display label.

For example, an individual alphabet prediction may display its corresponding character.

The system must not automatically combine isolated alphabet predictions into meaningful sentences without an appropriate sequence interpretation system.

**Step 7: Speech Generation**

Validated text is sent to the backend speech service.

Sarvam AI TTS may generate speech in a supported spoken language.

**Step 8: Audio Playback**

The frontend receives the audio response and provides playback controls.

---

## 6.2 Workflow B: Speech to Text

This workflow allows non-signers to communicate through spoken input.

**Flow:**

Non-Signer  
↓  
Microphone  
↓  
Audio Capture  
↓  
FastAPI Backend  
↓  
Sarvam AI Speech-to-Text  
↓  
Transcription Processing  
↓  
Readable Text  
↓  
Conversation Interface

### Detailed Explanation

**Step 1: Microphone Permission**

The user grants microphone permission.

**Step 2: Audio Capture**

The application captures the user's spoken input.

**Step 3: Audio Submission**

Audio is sent securely to the backend.

**Step 4: Speech Recognition**

The backend sends the audio to Sarvam AI STT using an appropriate supported API.

**Step 5: Text Result**

The transcription is returned and displayed to the user.

**Step 6: Editing**

The user can review and edit the transcription before sharing it.

---

## 6.3 Workflow C: Shared Conversation

Both workflows connect through a common conversation interface.

The interface should distinguish between:

- Sign recognition results.
- Spoken input transcriptions.
- Generated speech output.
- User-edited messages.

A conversation message should include appropriate metadata, such as:

- Message content.
- Communication direction.
- Timestamp, if required.
- Message status.
- Source type.

The initial MVP can keep conversations in temporary frontend state.

Persistent conversation history is a future feature requiring database storage and explicit privacy controls.

---

# 7. AI and Machine Learning Overview

## 7.1 Role of AI in Signova AI

AI is used for two separate responsibilities:

1. Visual recognition of supported Indian Sign Language signs.
2. Speech and language processing for spoken communication.

The visual recognition system is independent of Sarvam AI speech processing.

## 7.2 Computer Vision Pipeline

The computer vision pipeline handles camera input and visual recognition.

Expected components:

| Component | Technology | Purpose |
|---|---|---|
| Image processing | OpenCV | Frame processing |
| Numerical operations | NumPy | Data manipulation |
| Landmark extraction | MediaPipe, if required | Hand and body landmarks |
| Model inference | PyTorch | Recognition |
| Evaluation | scikit-learn | Metrics and analysis |

The exact preprocessing pipeline depends on the selected model.

## 7.3 Recognition Categories

### Static Recognition

Recognises a sign from an image or a static hand pose.

Suitable for an initial, limited recognition demonstration.

### Dynamic Recognition

Recognises a sign using movement across multiple video frames.

Requires temporal information and an appropriate video or sequence model.

### Continuous Sign Language Understanding

Interprets connected signs and their meaning within a broader linguistic context.

This is a more advanced future capability. It may require:

- Temporal modelling.
- Linguistic modelling.
- Facial expression analysis.
- Body and spatial information.
- ISL grammar and context.

Signova AI must not describe static gesture recognition as full continuous sign language translation.

## 7.4 Model Selection Principles

Before integrating a model, verify:

1. It is actually trained for ISL.
2. Its dataset is documented.
3. Its supported classes are known.
4. Its preprocessing requirements are understood.
5. Its checkpoint is available and compatible.
6. Its licence permits the intended use.
7. Its inference requirements match available hardware.
8. Its performance can be independently evaluated.

## 7.5 Model Evaluation

Use:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Per-class metrics.
- Inference latency.

Do not use unsupported or invented accuracy values in project documentation or demonstrations.

---

# 8. Sarvam AI Overview

## 8.1 Purpose

Sarvam AI provides speech and Indian-language processing capabilities for Signova AI.

It supports the spoken communication side of the platform.

It is not responsible for recognising visual ISL gestures.

## 8.2 Planned Services

### Speech-to-Text

Convert microphone audio into text.

### Text-to-Speech

Convert recognised or edited text into spoken audio.

### Translation

Where required, translate supported spoken-language text.

## 8.3 Integration Architecture

Frontend  
↓  
FastAPI Backend  
↓  
Sarvam AI API  
↓  
Speech or Text Result  
↓  
Frontend

## 8.4 Security Requirements

- API credentials must remain on the backend.
- Use environment variables.
- Validate incoming requests.
- Handle timeouts and service errors.
- Check current supported languages.
- Do not assume that every language or feature is supported.

---

# 9. System Architecture Overview

## 9.1 Architecture Principles

Signova AI will follow a modular client-server architecture.

Main principles:

- Separate frontend and backend.
- Separate ML inference from UI logic.
- Keep speech integrations independent.
- Use clear API contracts.
- Make model replacement possible.
- Keep the MVP simple.
- Avoid unnecessary microservices.
- Introduce additional infrastructure only when required.

## 9.2 High-Level Architecture

                    SIGNOVA AI
                         |
             +-----------+-----------+
             |                       |
             v                       v
       SIGN RECOGNITION        VOICE COMMUNICATION
             |                       |
             v                       v
       React Frontend           React Frontend
             |                       |
             v                       v
       Camera Capture          Microphone Capture
             |                       |
             +-----------+-----------+
                         |
                         v
                   FastAPI Backend
                         |
             +-----------+-----------+
             |                       |
             v                       v
       ML Recognition          Speech Services
             |                       |
             v                       v
        PyTorch Model             Sarvam AI
             |                       |
             v                       v
       Recognised Text         Speech Transcription
             |                       |
             +-----------+-----------+
                         |
                         v
                Conversation Interface

This is a logical architecture. The actual implementation may combine some services into fewer modules.

## 9.3 Frontend Architecture

Technology:

- React.
- JavaScript.
- Vite.
- Tailwind CSS.
- shadcn/ui where suitable.
- React Router.

Responsibilities:

- Application layout.
- Navigation.
- Camera access.
- Microphone access.
- Recognition interface.
- Conversation interface.
- Learning interface.
- API integration.
- User feedback and error handling.

## 9.4 Backend Architecture

Technology:

- Python.
- FastAPI.
- Pydantic.
- Uvicorn.
- WebSockets where required.

Responsibilities:

- API routing.
- Model management.
- Recognition requests.
- Speech service integration.
- Input validation.
- Error handling.
- Health monitoring.

## 9.5 Machine Learning Architecture

Technology:

- PyTorch.
- OpenCV.
- NumPy.
- MediaPipe where appropriate.
- scikit-learn.

Responsibilities:

- Preprocessing.
- Model loading.
- Inference.
- Prediction validation.
- Model evaluation.
- Future training and fine-tuning.

## 9.6 Database Architecture

Proposed database:

PostgreSQL.

The initial MVP does not require persistent database functionality unless necessary.

Future database features may include:

- User profiles.
- Preferences.
- Learning progress.
- Conversation metadata.
- Application activity.

Avoid storing raw video or audio by default.

---

# 10. Technology Stack Summary

| Layer | Selected Technology | Responsibility |
|---|---|---|
| Frontend | React | UI development |
| Frontend Language | JavaScript | Application logic |
| Build Tool | Vite | Development and bundling |
| Styling | Tailwind CSS | UI styling |
| Components | shadcn/ui | Reusable interface |
| Icons | Lucide React | Interface icons |
| Backend | FastAPI | API services |
| Backend Language | Python 3.11 | Backend and ML |
| API Validation | Pydantic | Request and response validation |
| Real-Time Communication | WebSockets | Live updates where required |
| ML Framework | PyTorch | Model inference |
| Image Processing | OpenCV | Video and image handling |
| Landmark Extraction | MediaPipe | Visual landmarks where required |
| Data Processing | NumPy, Pandas | Numerical and dataset processing |
| ML Evaluation | scikit-learn | Evaluation metrics |
| Database | PostgreSQL | Optional persistent storage |
| Speech AI | Sarvam AI | STT, TTS and supported translation |
| Model Repository | Hugging Face Hub | Model discovery and distribution |
| Version Control | Git and GitHub | Source management |
| Frontend Deployment | Vercel | Frontend hosting |
| Backend Deployment | Compatible Python hosting | API and inference hosting |

Use compatible package versions. Do not blindly install the latest version of every dependency.

---

# 11. Main Application Sections

The proposed application navigation is:

## 11.1 Home

Purpose:

- Introduce Signova AI.
- Explain the problem.
- Present the solution.
- Show key features.
- Guide users to the application.

## 11.2 Dashboard

Purpose:

- Provide access to the main communication features.
- Display application status.
- Provide shortcuts to important modules.

## 11.3 Sign Recognition

Purpose:

- Capture camera input.
- Recognise supported ISL signs.
- Display text results.
- Provide speech output.

## 11.4 Voice Communication

Purpose:

- Capture spoken input.
- Convert speech to text.
- Display transcription.
- Allow editing.

## 11.5 Conversation

Purpose:

- Display messages from both communication directions.
- Provide a common interface for communication.
- Support basic editing and clearing.

## 11.6 ISL Learning

Purpose:

- Display available learning content.
- Show supported sign demonstrations.
- Provide sign descriptions.
- Support future practice and quizzes.

## 11.7 Settings

Purpose:

- Manage supported language preferences.
- Configure accessibility options.
- Manage audio and display preferences.

---

# 12. Proposed User Journey

## 12.1 First-Time User

1. User visits the Signova AI website.
2. User reads the project introduction.
3. User opens the application.
4. User selects a communication feature.
5. The application explains required permissions.
6. User grants camera or microphone permission.
7. User starts the interaction.
8. The system displays results.
9. User can review, edit, copy, or play supported output.

## 12.2 ISL User Journey

1. Open sign recognition.
2. Allow camera access.
3. Position hands within the camera view.
4. Start recognition.
5. Perform a supported sign.
6. Wait for the prediction.
7. Review recognised text.
8. Play speech output if required.

## 12.3 Non-Signer Journey

1. Open voice communication.
2. Allow microphone access.
3. Start audio capture.
4. Speak naturally.
5. Wait for transcription.
6. Review the text.
7. Edit the text if required.
8. Display the message in the conversation interface.

---

# 13. Project Development Strategy

Development will follow the phased roadmap defined in `docs/PHASE_ROADMAP.md`.

## Phase 0: Foundation

- Documentation.
- Repository structure.
- Antigravity configuration.
- Environment setup.

## Phase 1: Model Verification

- Research ISL models.
- Inspect datasets.
- Check licences.
- Test pretrained checkpoints.
- Compare model suitability.

## Phase 2: ML Pipeline

- Preprocessing.
- Model loading.
- Inference.
- Prediction validation.
- Evaluation.

## Phase 3: Backend

- FastAPI setup.
- API routes.
- Recognition integration.
- Input validation.
- Error handling.

## Phase 4: Frontend

- Landing page.
- Dashboard.
- Recognition interface.
- Voice interface.
- Reusable components.

## Phase 5: Real-Time Recognition

- Camera integration.
- Frame processing.
- Live inference.
- Prediction display.
- Performance measurement.

## Phase 6: Sign-to-Text

- Label mapping.
- Text display.
- Output editing.
- Sequence support where validated.

## Phase 7: Speech Integration

- Sarvam AI configuration.
- Text-to-speech.
- Language selection.
- Audio playback.

## Phase 8: Reverse Communication

- Microphone access.
- Speech-to-text.
- Transcription editing.
- Conversation integration.

## Phase 9: Supporting Features

- Learning centre.
- User preferences.
- Optional authentication.
- Optional history.

## Phase 10: Testing and Deployment

- Functional testing.
- ML evaluation.
- Performance testing.
- Security review.
- Deployment.
- Demo preparation.

---

# 14. Repository Responsibilities

The repository will separate different parts of the application.

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

This is the intended structure. Create directories and files incrementally as their implementation phases begin.

Do not generate empty files for every planned module without a functional reason.

---

# 15. External Services and Dependencies

## 15.1 Sarvam AI

Used for:

- Speech-to-text.
- Text-to-speech.
- Supported spoken-language translation.

The backend must manage all external API calls.

## 15.2 Hugging Face

Used for:

- Discovering suitable ISL models.
- Accessing pretrained checkpoints.
- Model distribution where appropriate.
- Recording model metadata.

All model licences and compatibility requirements must be checked.

## 15.3 GitHub

Used for:

- Source control.
- Issue tracking.
- Development collaboration.
- Version history.
- Documentation.

## 15.4 Browser APIs

The frontend may use:

- MediaDevices API for camera and microphone access.
- MediaRecorder API for audio capture where suitable.
- WebSocket API for real-time backend communication.

All permissions and browser compatibility requirements must be handled properly.

---

# 16. Performance and Quality Principles

Signova AI must prioritise correctness and usability over unrealistic performance claims.

## 16.1 Performance

- Avoid unnecessary frame transmission.
- Load the ML model once when appropriate.
- Reuse model resources.
- Measure recognition latency.
- Optimise image resolution and frame rate.
- Monitor memory usage.
- Avoid blocking the frontend during inference.

## 16.2 Recognition Quality

- Use validated ISL datasets.
- Evaluate on unseen samples.
- Test across different users and environments.
- Handle unsupported signs.
- Avoid false certainty.
- Record actual model metrics.

## 16.3 User Experience

- Keep interactions simple.
- Provide immediate feedback.
- Explain camera and microphone permissions.
- Display useful error messages.
- Support responsive layouts.
- Make important actions accessible.

---

# 17. Security, Privacy, and Responsible AI

## 17.1 Privacy

- Do not access camera or microphone without permission.
- Do not record or store media by default.
- Explain when audio is sent to an external service.
- Do not store conversation content without appropriate consent.
- Provide clear/reset controls.

## 17.2 Security

- Store API keys in backend environment variables.
- Validate uploaded media.
- Restrict file sizes and formats.
- Configure CORS appropriately.
- Avoid logging private conversation data.
- Apply appropriate protection to future account functionality.

## 17.3 Responsible AI

- Clearly state supported recognition capabilities.
- Do not describe limited gesture recognition as full ISL translation.
- Do not invent model metrics.
- Respect dataset licences.
- Seek feedback from ISL users and qualified experts.
- Design for diverse users and signing styles.

---

# 18. Project Risks

| Risk | Description | Response |
|---|---|---|
| Dataset limitations | Available ISL data may have limited vocabulary | Compare datasets and document coverage |
| Model mismatch | A model may support ASL rather than ISL | Verify training data and class labels |
| Low recognition accuracy | Predictions may be unreliable | Evaluate and improve the model |
| Dynamic gesture complexity | Individual images may not capture movement | Use suitable temporal models |
| Hardware limitations | Model inference may be resource-intensive | Benchmark and optimise |
| External API dependency | Speech services may fail or be unavailable | Implement error handling |
| Network latency | Real-time recognition may be delayed | Optimise frame transmission |
| Privacy concerns | Camera and microphone data are sensitive | Minimise collection and storage |

---

# 19. Future Expansion

Signova AI is designed to support future improvements without requiring a complete architectural redesign.

Potential future capabilities:

### Advanced Recognition

- Dynamic sign recognition.
- Continuous sign sequences.
- Word and sentence interpretation.
- Facial expression analysis.
- Body posture and spatial information.
- Context-aware language processing.

### Accessibility

- Mobile application.
- Offline recognition.
- Improved accessibility settings.
- Better camera compatibility.
- More responsive interfaces.

### Learning

- ISL learning modules.
- Interactive practice.
- Sign demonstrations.
- Quizzes.
- Progress tracking.

### Communication

- Additional spoken languages.
- Better conversation management.
- More natural speech output.
- Improved real-time interaction.

All future features remain subject to technical feasibility, suitable data, testing, and user feedback.

---

# 20. Key Product Decisions

The following decisions define the current direction of Signova AI.

| Area | Decision |
|---|---|
| Product name | Signova AI |
| Main purpose | Accessible ISL communication |
| Primary sign language | Indian Sign Language |
| Platform | Web application |
| Frontend | React + JavaScript + Vite |
| Backend | Python + FastAPI |
| ML framework | PyTorch |
| Computer vision | OpenCV |
| Landmark extraction | MediaPipe where model-compatible |
| Speech services | Sarvam AI |
| Database | PostgreSQL when persistence is needed |
| Model strategy | Verify pretrained ISL models before training |
| Development style | Modular, phased implementation |
| Initial focus | Working MVP |
| Future focus | Advanced and continuous sign understanding |

---

# 21. Instructions for Antigravity and AI Coding Agents

This document is a core reference for understanding Signova AI.

Before implementing any feature, AI coding agents must:

1. Read the root `AGENTS.md`.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read the relevant technical documentation.
5. Inspect the existing repository.
6. Understand the current development phase.
7. Check dependencies before changing architecture.

## Development Rules

- Use JavaScript, not TypeScript, for the frontend.
- Use Python and FastAPI for the backend.
- Use PyTorch for ML model integration.
- Keep recognition logic separate from UI logic.
- Keep speech integrations separate from recognition logic.
- Follow the documented architecture.
- Implement one phase at a time.
- Do not invent model outputs or metrics.
- Do not confuse ASL and ISL.
- Do not claim unsupported functionality.
- Do not expose API keys.
- Write tests for important features.
- Update documentation when implementation changes.

## Expected Task Report

After completing a task, provide:

- Summary of implementation.
- Files created.
- Files modified.
- Dependencies added.
- Tests executed.
- Actual test results.
- Known limitations.
- Remaining tasks.
- Recommended next step.

Do not mark a feature or phase complete unless its requirements have been implemented and verified.

---

# 22. Final Project Summary

Signova AI is an AI-powered Indian Sign Language recognition and communication platform.

It connects visual sign recognition with text and speech output, while providing reverse speech-to-text communication for non-signers.

The platform combines:

- Computer vision for visual input processing.
- Deep learning for supported sign recognition.
- Text processing for readable output.
- Sarvam AI for supported speech and language features.
- React for the user interface.
- FastAPI for backend services.

The initial goal is to build a working and measurable accessibility MVP with a clearly defined recognition vocabulary.

The long-term goal is to develop more advanced sign sequence recognition and context-aware communication capabilities.

**Signova AI's guiding principle: Build technology that improves communication accessibility through reliable AI, honest capability claims, and user-centred design.**
