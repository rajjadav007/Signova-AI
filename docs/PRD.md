# Product Requirements Document (PRD)

# Signova AI
## AI-Powered Indian Sign Language Recognition and Communication Platform

**Document Version:** 1.0  
**Project Name:** Signova AI  
**Document Type:** Product Requirements Document  
**Project Status:** Planning and Development  
**Primary Platform:** Web Application  
**Primary Market:** India  
**Primary Sign Language:** Indian Sign Language (ISL)

---

# 1. Product Overview

## 1.1 What is Signova AI?

Signova AI is an AI-powered accessibility platform designed to reduce communication barriers between Indian Sign Language (ISL) users and people who do not understand sign language.

The platform uses computer vision, machine learning, and speech technologies to recognise sign language gestures through a camera and convert supported signs into readable text and spoken output.

It also aims to support reverse communication by allowing non-signers to communicate with sign language users through speech-to-text and text-based interactions.

The long-term vision is to develop an intelligent, accessible communication assistant that makes everyday interactions easier for people with hearing and speech disabilities.

Signova AI will progressively move from isolated sign recognition towards word recognition, sign sequences, and context-aware communication as the underlying models and datasets become available and validated.

## 1.2 Core Concept

The platform will support two communication directions.

**Direction 1: Sign Language to Speech and Text**

ISL user → Camera → Sign Recognition Model → Recognised Text → Speech Output

**Direction 2: Speech to Text**

Non-signer → Microphone → Speech Recognition → Text Output

The second direction will use Sarvam AI's supported speech technologies where suitable.

## 1.3 Product Vision

To make communication more accessible by using artificial intelligence to connect sign language, text, and speech through an affordable and easy-to-use platform.

## 1.4 Product Mission

- Improve communication accessibility for ISL users.
- Reduce dependence on manual text-based communication.
- Make sign recognition more accessible through everyday devices.
- Support communication between sign language users and non-signers.
- Promote awareness and learning of Indian Sign Language.
- Build a foundation for more advanced AI-powered accessibility tools.

---

# 2. Problem Statement

People with hearing and speech disabilities often experience communication barriers in everyday situations, including education, healthcare, workplaces, and public services.

Many people do not understand Indian Sign Language, which makes spontaneous conversations difficult.

Existing communication methods frequently depend on human interpreters, written messages, or assistance from other people. These methods may not always be available or convenient.

There is a need for accessible technology that can recognise supported sign language gestures and convert them into understandable text and speech.

Signova AI aims to address this challenge through computer vision, deep learning, and Indian-language speech technologies.

---

# 3. Problem Analysis

## 3.1 Current Challenges

1. Limited awareness of Indian Sign Language among the general population.
2. Communication difficulties between sign language users and non-signers.
3. Limited availability of interpreters in everyday environments.
4. Difficulty communicating independently in public places.
5. Lack of accessible and affordable digital communication tools.
6. Existing gesture recognition demonstrations often support only a limited vocabulary.
7. Recognition of continuous sign language is technically challenging because meaning can depend on movement, hand position, facial expressions, body posture, and context.

## 3.2 Why Existing Approaches Are Not Enough

Basic gesture detection systems generally identify individual hand poses or isolated signs.

However, practical sign language understanding requires more than recognising hand shapes.

A useful system must progressively account for:

- Hand shape and orientation.
- Hand movement and motion patterns.
- Position of hands relative to the body.
- Two-handed gestures.
- Facial expressions and non-manual signals.
- Sign language grammar and context.
- Differences in signing styles and regional variations.

Signova AI will treat these as important development requirements rather than assuming that alphabet detection is equivalent to complete sign language translation.

---

# 4. Target Users

## 4.1 Primary Users

### A. ISL Users

People who communicate using Indian Sign Language.

Needs:
- Convert supported signs into text.
- Access spoken output for recognised text.
- Communicate more independently with non-signers.
- Use an accessible and simple interface.

### B. Non-Signers

People who do not understand Indian Sign Language.

Needs:
- Understand supported signs through text and speech.
- Communicate through voice or text.
- Interact with sign language users more easily.

## 4.2 Secondary Users

### C. Students and Educators

Needs:
- Learn basic ISL signs.
- Practise supported gestures.
- Use accessibility tools in educational environments.

### D. Families and Caregivers

Needs:
- Improve everyday communication.
- Learn common signs.
- Support more independent interactions.

### E. Organisations and Public Service Providers

Needs:
- Explore accessible communication support.
- Improve interactions with ISL users.
- Use assistive communication technology in suitable environments.

---

# 5. Product Goals and Objectives

## 5.1 Primary Goals

1. Develop an AI-based ISL gesture recognition system.
2. Build a real-time camera-based recognition interface.
3. Convert recognised signs into readable text.
4. Provide speech output for supported recognised text.
5. Implement reverse speech-to-text communication.
6. Create an accessible and responsive user interface.
7. Build a modular architecture that supports future ML model improvements.

## 5.2 Secondary Goals

- Add a basic ISL learning section.
- Support multiple Indian spoken languages through suitable speech services.
- Maintain conversation history with user consent.
- Improve recognition accuracy through evaluation and dataset improvements.
- Prepare the platform for future mobile deployment.

## 5.3 Success Criteria

The project will be evaluated based on:

- Recognition performance on supported signs.
- Precision, recall, F1-score, and confusion matrix.
- Recognition latency.
- Stability of predictions during camera use.
- Speech output reliability.
- Frontend usability and accessibility.
- Successful integration between frontend, backend, and ML services.
- Testing with diverse signing styles where suitable participants and consent are available.

No accuracy or performance value should be claimed before it is measured.

---

# 6. Product Scope

## 6.1 MVP Scope

The Minimum Viable Product will focus on demonstrating a working end-to-end accessibility workflow.

### MVP Features

1. Landing page.
2. Responsive application dashboard.
3. Camera permission and live camera preview.
4. Supported ISL sign recognition.
5. Recognised text display.
6. Prediction confidence display, where supported by the model.
7. Basic prediction stabilisation.
8. Text-to-speech output using supported Sarvam AI capabilities.
9. Reverse speech-to-text communication.
10. Basic conversation interface.
11. Error handling and loading states.
12. Clear indication of unsupported or uncertain signs.

The initial recognition vocabulary must be defined by the selected model and verified dataset.

## 6.2 Future Scope

The following capabilities are planned for later versions.

- Continuous ISL sequence recognition.
- Word-level and sentence-level interpretation.
- Context-aware sign understanding.
- Facial expression and non-manual cue analysis.
- Improved recognition of two-handed gestures.
- User accounts and personalised settings.
- Conversation history.
- ISL learning modules.
- Interactive practice and quizzes.
- More Indian spoken language options.
- Mobile application.
- Offline recognition, where hardware and model size permit.
- Improved personalisation and recognition robustness.

## 6.3 Out of Scope for Initial MVP

The initial version will not claim:

- Complete ISL grammar understanding.
- Accurate translation of every ISL conversation.
- Universal recognition of all signs and regional variations.
- Automatic recognition of every facial expression.
- Medical diagnosis or healthcare decision support.
- Legal or emergency interpretation guarantees.
- Replacement of qualified human interpreters.

---

# 7. Core Features and Functional Requirements

## 7.1 Landing Page

**Description:** Introduce Signova AI and explain its purpose.

Requirements:

- Display project name and branding.
- Show a clear explanation of the platform.
- Include a primary call-to-action.
- Introduce the main accessibility features.
- Explain the supported communication workflow.
- Include an overview of how the system works.
- Provide navigation to relevant application sections.

Acceptance criteria:

- The page loads without errors.
- Main navigation works.
- Layout is responsive.
- Content clearly explains the product.
- Primary action navigates to the application.

## 7.2 User Dashboard

**Description:** Provide a central interface for accessing Signova AI features.

Requirements:

- Display available communication tools.
- Provide access to sign recognition.
- Provide access to reverse voice communication.
- Display basic usage information.
- Provide navigation to learning and settings sections when available.

Acceptance criteria:

- Main features are accessible.
- Navigation works correctly.
- Interface supports desktop and mobile layouts.

## 7.3 Camera Integration

**Description:** Capture live video through the user's device camera.

Requirements:

- Request camera permission.
- Display live camera preview.
- Support starting and stopping the camera.
- Provide pause and resume controls.
- Display camera permission errors.
- Display a message when the camera is unavailable.
- Avoid uploading or storing camera footage unless explicitly required and consented to.

Acceptance criteria:

- Camera starts when permission is granted.
- Camera stops when requested.
- Permission denial is handled gracefully.
- Camera resources are released when the feature is closed.

## 7.4 ISL Sign Recognition

**Description:** Recognise supported ISL signs using a trained or verified pretrained model.

Requirements:

- Accept camera frames or supported image input.
- Apply the model's required preprocessing.
- Load the correct model checkpoint.
- Perform inference.
- Return the recognised class.
- Return confidence information if supported.
- Handle unknown or unsupported gestures.
- Avoid showing unreliable predictions as confirmed results.

Important model requirements:

- Use an ISL-specific model or dataset.
- Verify the model's class labels.
- Verify its input dimensions and preprocessing.
- Verify the checkpoint and model architecture.
- Verify the model licence.
- Test inference before integrating it into the application.
- Record the actual evaluation results.

Acceptance criteria:

- The selected model loads successfully.
- Valid inputs produce predictions.
- Invalid inputs return meaningful errors.
- Predictions match the model's documented label set.
- Model performance is evaluated on a separate test dataset.

## 7.5 Prediction Stabilisation

**Description:** Reduce unstable output caused by frame-to-frame prediction changes.

Requirements:

- Maintain a short prediction history.
- Apply a suitable smoothing or voting strategy.
- Use confidence thresholds where appropriate.
- Avoid repeatedly displaying the same recognised result.
- Provide a mechanism to handle uncertain predictions.

Acceptance criteria:

- Temporary prediction changes do not immediately produce repeated output.
- Stable predictions are displayed consistently.
- Thresholds are configurable.
- Recognition performance is not misrepresented as improved merely because output is smoothed.

## 7.6 Sign-to-Text Output

**Description:** Convert recognised model labels into readable text.

Requirements:

- Map model class labels to display labels.
- Display the latest recognised sign.
- Maintain a sequence of recognised outputs where supported.
- Allow users to edit the generated text.
- Provide a clear/reset option.
- Provide copy-to-clipboard functionality.

Important:

A recognised alphabet or isolated sign must not automatically be treated as a complete word or sentence.

Sentence construction must be implemented only when the recognition model and vocabulary support the required output.

Acceptance criteria:

- Recognised labels are displayed correctly.
- Unsupported labels are handled.
- Users can edit and clear the output.
- Text output is not presented as a verified translation when it is only a sequence of isolated predictions.

## 7.7 Text-to-Speech

**Description:** Convert recognised text into spoken output.

Requirements:

- Accept recognised or user-edited text.
- Send text to the backend speech service.
- Integrate Sarvam AI TTS where supported.
- Allow selection of supported output languages and voices.
- Play generated speech.
- Provide replay and stop controls.
- Handle API errors and unavailable services.
- Keep API credentials on the backend.

Acceptance criteria:

- Valid text can be converted into speech.
- Supported languages are displayed correctly.
- Users can replay or stop audio.
- API keys are never exposed in frontend code.

## 7.8 Reverse Communication: Speech-to-Text

**Description:** Allow non-signers to communicate through speech converted into readable text.

Requirements:

- Request microphone permission.
- Capture speech input.
- Send audio to the backend.
- Integrate Sarvam AI STT where supported.
- Display transcription results.
- Allow users to edit transcription.
- Provide a clear/reset option.
- Display errors for microphone or API failures.

Acceptance criteria:

- Microphone permission is handled correctly.
- Valid audio can be submitted.
- Transcription is displayed when the service returns a result.
- Errors are handled without crashing the application.

## 7.9 Conversation Interface

**Description:** Provide a shared interface for communication between ISL users and non-signers.

Requirements:

- Display recognised sign text.
- Display speech transcription.
- Visually distinguish communication directions.
- Allow text editing.
- Provide copy and clear controls.
- Display speech playback controls where applicable.

Acceptance criteria:

- Both communication directions are easy to understand.
- Messages are displayed in the correct order.
- The interface works on supported screen sizes.

## 7.10 ISL Learning Centre

**Description:** Provide an educational section for learning supported signs.

Requirements:

- Display available signs.
- Show the sign name and category.
- Provide an image or video demonstration where licensed and available.
- Show instructions for performing the sign.
- Allow browsing by category.

Future enhancements:

- Practice mode.
- Camera-based practice feedback.
- Quizzes.
- Learning progress.

Acceptance criteria:

- Only verified learning content is displayed.
- Sign demonstrations use suitable and properly licensed material.
- Learning content is clearly separated from the live recognition feature.

## 7.11 User Preferences and Settings

**Description:** Allow users to customise basic application behaviour.

Potential requirements:

- Spoken output language.
- Text size.
- Theme preference.
- Camera settings.
- Audio playback settings.
- Accessibility preferences.

Account-based preferences will be implemented only when authentication and database functionality are introduced.

---

# 8. AI and Machine Learning Requirements

## 8.1 AI Architecture

Signova AI will use a modular AI architecture.

Main components:

1. Camera input.
2. Frame processing.
3. Hand and relevant visual feature extraction.
4. Sign recognition model.
5. Prediction processing.
6. Label mapping.
7. Text output.
8. Optional speech generation.

## 8.2 Computer Vision

Expected technologies:

- OpenCV for image and video processing.
- MediaPipe for landmark extraction where appropriate.
- NumPy for numerical processing.
- PyTorch for model loading and inference.

The preprocessing pipeline must match the selected model's actual training and inference requirements.

MediaPipe landmarks must not be substituted for image-based model inputs unless the selected architecture supports that representation.

## 8.3 Model Strategy

The project may use:

- Verified pretrained ISL models.
- Public ISL datasets.
- Transfer learning.
- Custom training and fine-tuning.
- Temporal models for dynamic signs.

Potential model approaches:

- CNN-based architectures for static sign recognition.
- Vision Transformers for image recognition.
- CNN or 3D CNN models for video-based recognition.
- LSTM or other temporal models for movement sequences.

Model selection must be based on:

- ISL compatibility.
- Dataset quality.
- Number of supported classes.
- Model architecture.
- Preprocessing requirements.
- Licence and usage restrictions.
- Inference speed.
- Hardware requirements.
- Measured evaluation performance.

## 8.4 Static and Dynamic Recognition

Static recognition identifies signs from individual images or hand poses.

Dynamic recognition analyses movement across multiple frames.

These are separate capabilities and must be developed and evaluated separately.

A static alphabet classifier cannot be described as a continuous ISL translation system.

## 8.5 Model Evaluation

Every recognition model must be evaluated using suitable test data.

Required metrics:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Per-class performance.
- Inference latency.

Where possible, evaluate performance across different:

- Lighting conditions.
- Backgrounds.
- Camera positions.
- Signing speeds.
- Users and signing styles.

Do not report training accuracy as test accuracy.

## 8.6 Unknown Sign Handling

The system should avoid forcing every input into one of its known classes.

Requirements:

- Apply a suitable confidence threshold.
- Identify uncertain predictions.
- Display an understandable message.
- Avoid producing misleading speech output for uncertain predictions.

## 8.7 Model Improvement

Future improvements may include:

- Dataset expansion.
- Data augmentation.
- Transfer learning.
- Temporal sequence modelling.
- Improved preprocessing.
- Model quantisation.
- Inference optimisation.

All improvements must be validated using consistent evaluation procedures.

---

# 9. Sarvam AI Integration

## 9.1 Purpose

Sarvam AI will support speech and Indian-language processing capabilities.

It is not the primary sign recognition model.

Sign recognition will be handled by the computer vision and machine learning pipeline.

## 9.2 Planned Integrations

### Speech-to-Text

Convert microphone input into readable text.

### Text-to-Speech

Convert recognised or edited text into spoken output.

### Translation

Where required, translate between supported spoken languages using available Sarvam capabilities.

## 9.3 Integration Rules

- Use backend API routes for external service requests.
- Store API keys in environment variables.
- Never expose credentials in frontend code.
- Validate inputs before sending requests.
- Handle API timeouts and service failures.
- Check current supported languages and API capabilities.
- Avoid assuming that every Indian language is supported by every service.

## 9.4 Separation of Responsibilities

| Component | Responsibility |
|---|---|
| Computer Vision | Process camera input |
| ISL Recognition Model | Recognise supported signs |
| Backend | Manage inference and service requests |
| Sarvam STT | Convert speech into text |
| Sarvam TTS | Convert text into speech |
| Sarvam Translation | Translate supported spoken languages |
| Frontend | Display and manage user interactions |

---

# 10. Technology Stack

The following is the proposed technology stack. Confirm package compatibility and exact versions before implementation.

## 10.1 Frontend

- React
- JavaScript
- Vite
- Tailwind CSS
- shadcn/ui where suitable
- React Router
- Lucide React
- Axios or Fetch API

Responsibilities:

- User interface.
- Camera and microphone access.
- Live recognition display.
- Conversation interface.
- Accessibility controls.
- API communication.

TypeScript is not part of the selected frontend stack.

## 10.2 Backend

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- WebSockets

Responsibilities:

- API management.
- Model loading and inference.
- Camera frame or image processing requests.
- Speech API integration.
- Input validation.
- Error handling.
- Service monitoring.

## 10.3 Machine Learning

- PyTorch
- OpenCV
- MediaPipe where required
- NumPy
- scikit-learn
- Pandas for dataset analysis

Responsibilities:

- Preprocessing.
- Feature extraction.
- Model inference.
- Model evaluation.
- Model training and fine-tuning where necessary.

## 10.4 Database

Proposed:

- PostgreSQL

Potential future use:

- User profiles.
- User preferences.
- Conversation metadata.
- Learning progress.
- Application activity.

The initial MVP should not require a database unless a feature genuinely needs persistent data.

## 10.5 External Services

- Sarvam AI for supported speech and language features.
- Hugging Face Hub for model discovery and model hosting.
- GitHub for source control.

## 10.6 Deployment

Proposed deployment options:

- Vercel for the frontend.
- Render or another compatible Python hosting provider for the backend.
- Hugging Face Hub for model distribution.

Deployment decisions must account for model size, RAM, GPU availability, cold starts, and inference cost.

---

# 11. System Architecture

## 11.1 High-Level Architecture

User Interface
    |
    v
React Frontend
    |
    v
FastAPI Backend
    |
    +-------------------------+
    |                         |
    v                         v
ISL Recognition Service   Speech Services
    |                         |
    v                         v
PyTorch Model              Sarvam AI
    |                         |
    v                         v
Recognised Text          Speech/Text Output
    |                         |
    +------------+------------+
                 |
                 v
          Frontend Display

## 11.2 Frontend Responsibilities

- Display the application.
- Request camera and microphone permissions.
- Capture user input.
- Send supported input to backend endpoints.
- Display recognition and transcription results.
- Manage application state.
- Handle loading and error states.

## 11.3 Backend Responsibilities

- Expose versioned API endpoints.
- Load and manage the recognition model.
- Process incoming data.
- Coordinate speech service requests.
- Validate inputs.
- Manage errors and service status.
- Keep secrets secure.

## 11.4 ML Service Responsibilities

- Load the verified model.
- Apply model-specific preprocessing.
- Perform inference.
- Return predictions and relevant metadata.
- Handle unsupported or invalid inputs.
- Support evaluation and monitoring.

## 11.5 Communication Between Services

Use REST APIs for standard requests.

Use WebSockets where continuous camera streaming or real-time updates are required.

The initial implementation should favour a simple, testable request-response flow before adding complex streaming behaviour.

---

# 12. Proposed API Requirements

The exact API contracts will be documented in `docs/API_DOCUMENTATION.md`.

Proposed endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Backend health |
| GET | `/api/v1/model/status` | Recognition model status |
| POST | `/api/v1/recognition/predict` | Recognise a supported image |
| POST | `/api/v1/speech/stt` | Speech-to-text |
| POST | `/api/v1/speech/tts` | Text-to-speech |
| POST | `/api/v1/speech/translate` | Supported text translation |
| WS | `/api/v1/ws/recognition` | Real-time recognition stream |

These are proposed routes, not existing implemented endpoints.

API responses should use a consistent structure and meaningful HTTP status codes.

---

# 13. UI/UX Requirements

## 13.1 Design Direction

Signova AI should have a modern, clean, professional, and accessible interface.

The design should communicate trust, simplicity, inclusivity, and intelligent technology.

## 13.2 Design Principles

- Accessibility first.
- Clear visual hierarchy.
- Minimal and intuitive navigation.
- Responsive layouts.
- Readable typography.
- Consistent spacing.
- Clear action buttons.
- Accessible colour contrast.
- Useful feedback for all important actions.

## 13.3 Important UI States

Every interactive feature should account for:

- Initial state.
- Loading state.
- Success state.
- Empty state.
- Error state.
- Permission denied state.
- Unsupported input state.
- Network failure state.

## 13.4 Recognition Interface

The recognition page should include:

- Live camera preview.
- Start and stop controls.
- Recognition status.
- Recognised sign or text.
- Confidence information when available.
- Speech playback.
- Clear/reset action.
- Error and unsupported-sign messages.

## 13.5 Accessibility

- Use semantic HTML.
- Support keyboard navigation.
- Provide accessible labels.
- Maintain sufficient colour contrast.
- Avoid relying on colour alone to communicate status.
- Provide readable text.
- Make controls easy to use on mobile devices.

---

# 14. Non-Functional Requirements

## 14.1 Performance

- The application should remain responsive during recognition.
- Avoid unnecessary API calls.
- Process frames efficiently.
- Use suitable frame sampling for real-time inference.
- Measure end-to-end latency.
- Avoid loading large ML models repeatedly.

Performance targets will be defined after the selected model and hosting environment are benchmarked.

## 14.2 Reliability

- Handle model loading failures.
- Handle camera and microphone errors.
- Handle external API failures.
- Provide useful error messages.
- Prevent invalid input from crashing the application.

## 14.3 Security

- Keep API credentials on the backend.
- Use environment variables for secrets.
- Validate incoming requests.
- Restrict file uploads by size and type.
- Apply appropriate CORS settings.
- Avoid logging sensitive user content.
- Protect user data if accounts are introduced.

## 14.4 Privacy

- Camera and microphone access must require user permission.
- Do not record or store video/audio by default.
- Explain clearly when external services receive user data.
- Request consent before storing conversation content.
- Provide a way to clear stored information where storage is implemented.

## 14.5 Scalability

- Keep recognition, speech, and frontend modules independent.
- Support replacing the recognition model without rewriting the entire application.
- Keep external service integrations modular.
- Avoid unnecessary microservices in the initial MVP.

## 14.6 Maintainability

- Use clear folder structures.
- Follow consistent naming conventions.
- Keep functions focused.
- Add tests for important logic.
- Document API contracts.
- Update documentation when architecture changes.

---

# 15. Data and Dataset Requirements

## 15.1 Dataset Selection

Only use datasets that are relevant to Indian Sign Language.

Before using a dataset, verify:

- Source and ownership.
- Licence and permitted usage.
- ISL vocabulary.
- Class labels.
- Number of samples.
- Image or video format.
- Data quality.
- Annotation quality.
- Train, validation, and test splits.

## 15.2 Dataset Processing

The data pipeline should support:

- Dataset inspection.
- Duplicate detection.
- Missing or invalid sample checks.
- Label validation.
- Preprocessing.
- Data augmentation where suitable.
- Train and validation splitting.
- Test set isolation.

## 15.3 Data Leakage Prevention

Samples from the same signer or recording session should not be unintentionally distributed across training and testing sets when that could inflate evaluation results.

Where possible, use signer-independent evaluation to measure generalisation to unseen users.

## 15.4 Data Ethics

- Respect dataset licences.
- Protect participant privacy.
- Obtain consent when collecting new recordings.
- Avoid publishing identifiable recordings without permission.
- Document dataset limitations and possible biases.

---

# 16. Development Roadmap

Development will follow a phased approach.

A phase must be validated before dependent phases are considered complete.

## Phase 0: Project Foundation

Tasks:

- Create repository.
- Prepare documentation.
- Configure Antigravity instructions.
- Set up frontend, backend, and ML directories.
- Configure environment files.
- Establish coding standards.

Expected output:

A documented and organised project foundation.

## Phase 1: AI Model Research and Verification

Tasks:

- Research ISL datasets and pretrained models.
- Inspect architecture and checkpoint requirements.
- Verify class labels and preprocessing.
- Check model licences.
- Run inference tests.
- Evaluate available model options.

Expected output:

A verified model selection and a working local inference demonstration.

## Phase 2: ML Recognition Pipeline

Tasks:

- Implement preprocessing.
- Implement model loading.
- Implement prediction logic.
- Add confidence handling.
- Add prediction stabilisation.
- Add unknown-sign handling.
- Implement evaluation scripts.

Expected output:

A reusable and testable ISL recognition service.

## Phase 3: Backend Development

Tasks:

- Configure FastAPI.
- Implement API routes.
- Integrate the ML service.
- Implement input validation.
- Add error handling.
- Add WebSocket support if required.

Expected output:

A working backend with tested recognition endpoints.

## Phase 4: Frontend Development

Tasks:

- Build landing page.
- Build dashboard.
- Build recognition interface.
- Build reusable components.
- Implement responsive design.
- Connect frontend to backend.

Expected output:

A functional frontend connected to backend services.

## Phase 5: Real-Time Recognition

Tasks:

- Integrate browser camera.
- Capture frames.
- Send frames to backend.
- Display predictions.
- Add pause and resume controls.
- Improve recognition stability.
- Measure latency.

Expected output:

A working live camera recognition demonstration.

## Phase 6: Sign-to-Text Communication

Tasks:

- Map supported signs to readable labels.
- Display recognised output.
- Add text editing.
- Add copy and reset controls.
- Implement sequence handling where supported.

Expected output:

A usable sign-to-text workflow for the validated vocabulary.

## Phase 7: Sarvam AI Speech Integration

Tasks:

- Configure secure Sarvam API integration.
- Implement text-to-speech.
- Add supported language selection.
- Add audio playback controls.
- Handle API errors.

Expected output:

Recognised or edited text can be converted into spoken output.

## Phase 8: Reverse Communication

Tasks:

- Implement microphone access.
- Capture audio.
- Integrate speech-to-text.
- Display transcription.
- Add text editing.
- Integrate the communication interface.

Expected output:

A working speech-to-text communication workflow.

## Phase 9: Supporting Features

Tasks:

- Add ISL learning centre.
- Add preferences.
- Add optional user authentication.
- Add database persistence where required.
- Add conversation history with user consent.

Expected output:

A more complete accessibility platform.

## Phase 10: Testing and Deployment

Tasks:

- Test ML performance.
- Test API behaviour.
- Test frontend functionality.
- Test camera and microphone permissions.
- Test responsive layouts.
- Benchmark latency.
- Review security and privacy.
- Deploy the application.
- Prepare demonstration material.

Expected output:

A tested and demonstrable Signova AI application.

---

# 17. Testing Requirements

## 17.1 ML Testing

- Test model loading.
- Test preprocessing.
- Test individual predictions.
- Test invalid inputs.
- Test unknown signs.
- Measure precision, recall, and F1-score.
- Review confusion matrix.
- Benchmark inference time.

## 17.2 Backend Testing

- Test health endpoint.
- Test model status.
- Test prediction endpoint.
- Test invalid file handling.
- Test service failures.
- Test speech API errors.
- Test WebSocket connections if implemented.

## 17.3 Frontend Testing

- Test page navigation.
- Test camera permissions.
- Test microphone permissions.
- Test prediction display.
- Test speech playback.
- Test empty and error states.
- Test mobile responsiveness.

## 17.4 Integration Testing

Verify that:

1. Frontend can communicate with backend.
2. Backend can load the recognition model.
3. Recognition results return correctly.
4. Sarvam services work through secure backend integration.
5. Errors are displayed properly.
6. The full user workflow operates without unexpected failures.

---

# 18. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Limited ISL datasets | Limited vocabulary | Research multiple datasets and document coverage |
| ASL model mistaken for ISL | Incorrect recognition | Verify dataset and labels before use |
| Poor recognition accuracy | Unreliable output | Evaluate models and improve data quality |
| Dynamic sign complexity | Incomplete interpretation | Develop temporal recognition separately |
| Lighting and camera differences | Prediction instability | Test across different environments |
| Sarvam API failure | Speech feature unavailable | Add error handling and service status |
| Large model size | Slow deployment | Benchmark and optimise model |
| Network latency | Poor real-time experience | Reduce frame frequency and optimise requests |
| Limited hardware | Slow inference | Use efficient models and suitable deployment |
| Incorrect sentence generation | Misleading communication | Restrict output to validated recognition capabilities |

---

# 19. Product Limitations

Signova AI must communicate its limitations honestly.

1. Recognition will initially support only the vocabulary available in the verified model.
2. Static sign recognition does not represent complete ISL understanding.
3. Continuous sign interpretation requires temporal and linguistic modelling.
4. Recognition accuracy may vary between users and environments.
5. Regional signing variations may affect performance.
6. Speech services depend on supported languages and external service availability.
7. Model confidence is not a guarantee that a prediction is correct.
8. The application is an assistive tool, not a replacement for qualified interpreters.

---

# 20. Privacy and Responsible AI

Signova AI must be developed with accessibility, user dignity, and privacy as core principles.

Requirements:

- Request explicit camera and microphone permission.
- Avoid recording users without their knowledge.
- Do not store raw video or audio by default.
- Make external AI service usage clear.
- Protect API credentials.
- Use licensed datasets.
- Avoid misleading claims about recognition accuracy.
- Test with diverse participants where possible.
- Seek feedback from ISL users and qualified sign language experts.
- Treat user feedback as an important part of product improvement.

---

# 21. Future Product Vision

Future versions of Signova AI may include:

### Advanced ISL Recognition
- Continuous sign sequence recognition.
- Word and sentence interpretation.
- Temporal movement analysis.
- Facial expression and non-manual cue analysis.
- Context-aware language processing.

### Improved Accessibility
- Mobile application.
- Offline recognition.
- Personalised settings.
- Improved low-light performance.
- More accessible user interactions.

### Learning and Education
- Structured ISL lessons.
- Interactive sign practice.
- Learning progress.
- Quizzes and assessments.

### Expanded Communication
- More supported Indian spoken languages.
- Improved conversation workflows.
- Better speech output.
- Additional accessibility integrations.

These capabilities are future goals and should not be presented as completed features until implemented and validated.

---

# 22. Definition of Done

A feature can be considered complete only when:

1. Its requirements have been implemented.
2. It follows the approved architecture.
3. It handles expected error conditions.
4. Its relevant tests pass.
5. It works with dependent components.
6. It does not expose secrets or sensitive data.
7. Its documentation is updated.
8. Its actual limitations are recorded.
9. Its output has been manually verified where appropriate.

A phase is complete only after its acceptance criteria have been reviewed and its expected output has been demonstrated.

---

# 23. Instructions for AI Coding Agents

This section is especially important for Antigravity and other AI coding agents working on Signova AI.

## 23.1 Understand Before Implementing

Before writing code:

1. Read the root `AGENTS.md`.
2. Read this PRD.
3. Read the relevant architecture and technical documentation.
4. Inspect the existing repository structure.
5. Identify existing implementations.
6. Understand dependencies between features.
7. Confirm which phase is currently being implemented.

Do not assume that a feature already exists.

## 23.2 Development Rules

- Implement only the requested phase or feature.
- Follow the documented technology stack.
- Use React and JavaScript for the frontend.
- Use Python and FastAPI for the backend.
- Use PyTorch for supported ML model integration.
- Keep modules reusable and maintainable.
- Follow existing naming conventions.
- Avoid unnecessary dependencies.
- Never expose API keys.
- Do not create fake model predictions.
- Do not invent evaluation metrics.
- Do not confuse ASL with ISL.
- Do not claim unsupported sign language translation capabilities.
- Do not remove working functionality without a clear reason.
- Add tests for important functionality.
- Update documentation after implementation.

## 23.3 Implementation Workflow

For every development task:

1. Understand the requirement.
2. Inspect relevant existing files.
3. Prepare a short implementation plan.
4. Implement the requested feature.
5. Run relevant tests.
6. Fix errors.
7. Review the changes.
8. Update documentation.
9. Report the outcome.

## 23.4 Completion Report

After every task, provide:

- Features implemented.
- Files created or modified.
- Dependencies added.
- Tests executed.
- Actual test results.
- Known issues.
- Remaining work.
- Recommended next feature.

Do not mark incomplete features as completed.

---

# 24. Final Product Definition

Signova AI is an AI-powered accessibility platform focused on Indian Sign Language recognition and communication.

Its initial goal is to demonstrate a reliable workflow that recognises a defined set of supported ISL signs, displays the results as text, and converts that text into speech.

The platform will also support reverse speech-to-text communication using suitable Indian-language AI services.

Its long-term goal is to advance towards continuous, context-aware ISL understanding while maintaining accessibility, privacy, reliability, and responsible AI practices.

**Core Product Principle: Build a working, measurable, and accessible solution first. Expand recognition capabilities only when supported by suitable data, validated models, and real-world testing.**