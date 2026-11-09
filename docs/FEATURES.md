# Signova AI
# Complete Feature Specification

**Document:** FEATURES.md  
**Version:** 1.0  
**Project:** Signova AI  
**Status:** Planning and Development  
**Platform:** Web Application  
**Primary Language:** Indian Sign Language (ISL)  
**Frontend:** React + JavaScript + Vite  
**Backend:** Python + FastAPI  
**AI/ML:** PyTorch + OpenCV  
**Speech AI:** Sarvam AI  

---

# 1. Purpose of This Document

This document defines the complete feature set of Signova AI.

It serves as the central feature reference for developers, AI coding agents, and project contributors.

Every feature must have:

- A unique feature ID.
- A clear description.
- A defined purpose.
- Functional requirements.
- Expected behaviour.
- Dependencies.
- Acceptance criteria.
- Implementation priority.
- Development status.

Antigravity must use this document to understand what needs to be developed and how each feature should behave.

This document works alongside:

| Document | Responsibility |
|---|---|
| `PRD.md` | Product requirements and goals |
| `PROJECT_OVERVIEW.md` | Product vision and system overview |
| `FEATURES.md` | Complete feature specifications |
| `TECH_STACK.md` | Technologies and implementation choices |
| `SYSTEM_ARCHITECTURE.md` | Technical architecture |
| `AI_MODEL_STRATEGY.md` | Recognition models and datasets |
| `PHASE_ROADMAP.md` | Development phases and sequence |
| `UI_UX_GUIDELINES.md` | Visual and accessibility standards |

---

# 2. Feature Development Principles

All features must follow these principles.

## 2.1 Modular Development

- Keep features separated into logical modules.
- Avoid putting the entire application inside one component or file.
- Keep frontend, backend, and ML responsibilities separate.
- Use reusable components and services.
- Avoid unnecessary code duplication.

## 2.2 Accuracy and Reliability

- Do not invent AI predictions.
- Do not display unsupported signs as recognised signs.
- Do not invent model confidence values.
- Do not claim full ISL translation from an alphabet classifier.
- Handle uncertain predictions clearly.
- Test features using real and valid inputs.

## 2.3 Accessibility

- Keep the interface simple.
- Use readable typography.
- Support keyboard navigation.
- Provide accessible labels.
- Maintain sufficient colour contrast.
- Display useful error messages.
- Make the application responsive.

## 2.4 Privacy

- Request permission before camera or microphone access.
- Do not record or store media by default.
- Do not expose external API keys.
- Do not store conversation content without appropriate consent.
- Keep sensitive data out of application logs.

## 2.5 Implementation Rules

- Implement features according to the approved roadmap.
- Follow existing architecture.
- Inspect the repository before changing files.
- Add tests for important functionality.
- Update documentation after implementation.
- Do not mark incomplete features as completed.

---

# 3. Feature Priority Definitions

| Priority | Meaning |
|---|---|
| P0 | Critical, required for the initial working MVP |
| P1 | Important, required for a complete MVP experience |
| P2 | Secondary, useful after the core MVP |
| P3 | Future enhancement |

Feature status:

| Status | Meaning |
|---|---|
| Not Started | Implementation has not started |
| In Progress | Currently being implemented |
| Implemented | Code has been written |
| Testing | Under verification |
| Completed | Acceptance criteria have passed |
| Blocked | Waiting for a dependency or decision |

A feature must not be marked Completed simply because code has been generated.

---

# 4. Feature Overview

Signova AI is divided into the following modules.

| Module ID | Module | Main Responsibility |
|---|---|---|
| MOD-01 | Project Foundation | Application setup and configuration |
| MOD-02 | Landing Page | Introduce Signova AI |
| MOD-03 | Dashboard | Central application navigation |
| MOD-04 | Camera System | Capture visual input |
| MOD-05 | ISL Recognition | Recognise supported ISL signs |
| MOD-06 | Prediction Processing | Validate and stabilise predictions |
| MOD-07 | Sign-to-Text | Display recognised signs as text |
| MOD-08 | Speech Output | Convert text into speech |
| MOD-09 | Reverse Communication | Convert speech into text |
| MOD-10 | Conversation Interface | Connect both communication directions |
| MOD-11 | ISL Learning Centre | Provide sign learning content |
| MOD-12 | User Preferences | Accessibility and application settings |
| MOD-13 | Data Management | Optional persistent application data |
| MOD-14 | Security and Privacy | Protect user information |
| MOD-15 | Testing and Deployment | Validate and release the application |

---

# 5. MOD-01: Project Foundation

**Priority:** P0  
**Development Phase:** Phase 0

## F001: Repository Structure

**Description:** Establish an organised repository structure.

Requirements:

- Separate frontend, backend, and ML code.
- Create a documentation directory.
- Create appropriate testing directories.
- Maintain configuration files.
- Avoid unnecessary empty directories.

Expected output:

A clean and maintainable project structure.

Acceptance criteria:

- Required directories exist.
- Files have clear responsibilities.
- Frontend and backend code are separated.
- Documentation is accessible.

## F002: Development Environment

**Description:** Configure the project development environment.

Requirements:

- Configure React and Vite.
- Configure Python backend environment.
- Establish dependency management.
- Configure environment variables.
- Provide local development instructions.

Acceptance criteria:

- Frontend starts successfully.
- Backend starts successfully.
- Dependencies install correctly.
- Environment configuration is documented.

## F003: Antigravity Instructions

**Description:** Configure AI coding agent instructions.

Requirements:

- Maintain root `AGENTS.md`.
- Define coding standards.
- Define architecture rules.
- Define documentation requirements.
- Define testing expectations.
- Define implementation workflow.

Acceptance criteria:

- Antigravity can understand project instructions.
- Coding standards are clear.
- Agents are instructed to inspect documentation before development.

## F004: Environment Configuration

**Description:** Maintain application configuration securely.

Requirements:

- Create `.env.example`.
- Keep secrets outside source code.
- Separate development and production settings.
- Configure backend API settings.
- Configure Sarvam API settings when integration begins.

Acceptance criteria:

- No real secrets are committed.
- Missing configuration produces useful errors.
- Setup instructions are documented.

---

# 6. MOD-02: Landing Page

**Priority:** P1  
**Development Phase:** Phase 4

## F005: Landing Page Layout

**Description:** Create the public-facing introduction page.

Requirements:

- Display Signova AI branding.
- Display a clear headline.
- Explain the communication problem.
- Introduce the proposed solution.
- Present the primary features.
- Provide a call-to-action.
- Include navigation.

Acceptance criteria:

- The page loads correctly.
- The content communicates the product purpose.
- Navigation works.
- Layout is responsive.

## F006: Hero Section

**Description:** Introduce the product through a strong visual section.

Requirements:

- Display project name.
- Display a concise value proposition.
- Include an appropriate visual.
- Include a primary action to open the application.
- Use accessible typography and contrast.

Acceptance criteria:

- The main message is immediately understandable.
- Primary action works.
- Layout adapts to different screen sizes.

## F007: How It Works Section

**Description:** Explain the communication workflow.

Requirements:

Display the sign-to-text workflow:

Camera → Recognition → Text → Speech

Display the reverse workflow:

Voice → Speech Recognition → Text

Acceptance criteria:

- Both communication directions are explained.
- The distinction between the workflows is clear.
- No unsupported capabilities are advertised.

## F008: Features Overview

**Description:** Introduce the main application features.

Requirements:

- Sign recognition.
- Sign-to-text.
- Speech output.
- Reverse speech-to-text.
- ISL learning.

Only implemented or clearly marked planned features should be presented as available.

Acceptance criteria:

- Feature descriptions are accurate.
- Links navigate to relevant sections.

## F009: Footer and Navigation

**Description:** Provide navigation and basic project information.

Requirements:

- Footer navigation.
- Project information.
- Contact or feedback link if available.
- Privacy information.
- Responsive layout.

Acceptance criteria:

- Links work.
- Footer is readable.
- No broken navigation items.

---

# 7. MOD-03: User Dashboard

**Priority:** P1  
**Development Phase:** Phase 4

## F010: Dashboard Layout

**Description:** Create a central application dashboard.

Requirements:

- Display application branding.
- Provide navigation.
- Display primary communication features.
- Provide shortcuts.
- Maintain a clean layout.

Acceptance criteria:

- Main modules are accessible.
- Layout is responsive.
- Navigation works.

## F011: Feature Navigation

**Description:** Allow users to move between application modules.

Requirements:

- Recognition page.
- Voice communication page.
- Conversation page.
- Learning page.
- Settings page.

Acceptance criteria:

- All implemented navigation items work.
- Active navigation state is visible.
- Invalid routes are handled.

## F012: Application Status

**Description:** Display relevant service availability.

Requirements:

- Show backend connection status where useful.
- Show recognition model availability.
- Show speech service status where available.
- Display loading or unavailable states.

Acceptance criteria:

- Status reflects actual backend responses.
- The UI does not display fake service availability.

---

# 8. MOD-04: Camera System

**Priority:** P0  
**Development Phase:** Phase 5

## F013: Camera Permission

**Description:** Request permission to access the device camera.

Requirements:

- Use browser camera permissions.
- Explain why camera access is required.
- Handle permission denial.
- Handle unavailable camera devices.
- Display useful error messages.

Acceptance criteria:

- Permission is requested only when needed.
- Permission denial does not crash the application.
- The user can retry after changing permissions.

## F014: Live Camera Preview

**Description:** Display live camera footage.

Requirements:

- Display camera stream.
- Use an appropriate video aspect ratio.
- Support responsive layouts.
- Display camera status.
- Provide a clear camera placeholder when inactive.

Acceptance criteria:

- Video displays when permission is granted.
- Video stops when the camera is disabled.
- No unnecessary camera stream remains active.

## F015: Camera Start and Stop

**Description:** Allow users to control camera activity.

Requirements:

- Start camera.
- Stop camera.
- Pause recognition.
- Resume recognition.
- Release camera resources.

Acceptance criteria:

- All controls work.
- Camera resources are released properly.
- UI state matches camera state.

## F016: Frame Capture

**Description:** Capture video frames for recognition.

Requirements:

- Capture frames from the video element.
- Use the required model input dimensions.
- Avoid excessive frame transmission.
- Handle unavailable frames.
- Manage capture frequency.

Acceptance criteria:

- Valid frames can be captured.
- Frame dimensions match the selected processing requirements.
- Invalid frames are rejected safely.

---

# 9. MOD-05: ISL Recognition Engine

**Priority:** P0  
**Development Phase:** Phases 1 and 2

## F017: ISL Model Research

**Description:** Identify suitable pretrained ISL recognition models.

Requirements:

- Research available ISL models.
- Inspect source code.
- Verify model architecture.
- Verify supported classes.
- Check model licences.
- Check checkpoint availability.
- Check inference requirements.

Acceptance criteria:

- Candidate models are documented.
- ASL models are not incorrectly classified as ISL models.
- A model selection decision is recorded.

## F018: Dataset Verification

**Description:** Verify the dataset used by the selected model.

Requirements:

- Identify dataset source.
- Verify language and vocabulary.
- Inspect class distribution.
- Check annotation quality.
- Check dataset licence.
- Document dataset limitations.

Acceptance criteria:

- Dataset provenance is documented.
- Model class labels are understood.
- Dataset limitations are recorded.

## F019: Model Loading

**Description:** Load the verified recognition model.

Requirements:

- Load the correct checkpoint.
- Match architecture to checkpoint.
- Support configured device selection.
- Handle missing checkpoint errors.
- Avoid loading the model for every prediction.

Acceptance criteria:

- Model loads successfully.
- Model loading errors are handled.
- Device selection is verified.
- Model is reusable during inference.

## F020: Input Preprocessing

**Description:** Prepare camera or image inputs for model inference.

Requirements:

- Match the original model's preprocessing.
- Apply required resizing.
- Apply normalisation if required.
- Apply colour conversion if required.
- Maintain correct tensor dimensions.
- Handle invalid inputs.

Acceptance criteria:

- Preprocessed input matches model requirements.
- Inference can run without dimension errors.
- Preprocessing is tested independently.

## F021: Static Sign Recognition

**Description:** Recognise supported static ISL signs.

Requirements:

- Accept valid image input.
- Apply model preprocessing.
- Run model inference.
- Return the predicted class.
- Return model confidence information where available.
- Handle unsupported or uncertain inputs.

Acceptance criteria:

- Valid images produce predictions.
- Predictions belong to the model's known classes.
- Invalid inputs return meaningful errors.
- Evaluation results are documented.

## F022: Dynamic Sign Recognition

**Description:** Recognise supported signs using movement across video frames.

**Priority:** P3, future capability unless a suitable verified pretrained model is available.

Requirements:

- Accept sequences of frames.
- Maintain temporal order.
- Apply sequence preprocessing.
- Use a suitable temporal model.
- Return a supported sign prediction.

Acceptance criteria:

- The selected model genuinely supports video or temporal input.
- Sequence processing is tested.
- Performance is evaluated on suitable video data.

Important:

This feature must not be simulated using a static classifier.

## F023: Recognition Service

**Description:** Provide a reusable prediction interface.

Requirements:

- Accept validated model input.
- Run inference.
- Return structured predictions.
- Provide clear error handling.
- Keep inference separate from API and UI logic.

Acceptance criteria:

- Recognition can be called independently.
- Input and output formats are documented.
- Tests cover valid and invalid inputs.

---

# 10. MOD-06: Prediction Processing

**Priority:** P0  
**Development Phase:** Phase 2

## F024: Confidence Handling

**Description:** Handle model prediction confidence.

Requirements:

- Read confidence values from model output where available.
- Configure a suitable threshold.
- Mark uncertain predictions.
- Avoid inventing confidence values.
- Document threshold selection.

Acceptance criteria:

- Low-confidence outputs are handled.
- Confidence values match actual model outputs.
- Threshold behaviour is tested.

## F025: Prediction Smoothing

**Description:** Reduce unstable predictions across consecutive frames.

Requirements:

- Maintain a short prediction history.
- Apply suitable temporal smoothing or voting.
- Configure smoothing parameters.
- Avoid excessive delays.
- Preserve the actual recognised class.

Acceptance criteria:

- Unstable frame predictions are handled.
- Stable predictions appear consistently.
- Smoothing behaviour is tested.

## F026: Duplicate Prediction Suppression

**Description:** Avoid repeatedly displaying identical results.

Requirements:

- Track recent predictions.
- Suppress unnecessary duplicates.
- Allow repeated signs when a valid new gesture is detected.
- Provide configurable timing or sequence logic.

Acceptance criteria:

- Repeated frame predictions do not flood the interface.
- Intentional repeated signs remain possible.

## F027: Unknown Sign Detection

**Description:** Handle signs outside the supported vocabulary.

Requirements:

- Apply a suitable uncertainty strategy.
- Display an unsupported-sign message.
- Avoid forced class interpretation.
- Avoid generating speech for uncertain results unless the user explicitly confirms the text.

Acceptance criteria:

- Unsupported inputs are not silently presented as verified signs.
- UI displays a clear message.

---

# 11. MOD-07: Sign-to-Text

**Priority:** P0  
**Development Phase:** Phase 6

## F028: Sign Label Mapping

**Description:** Convert model class IDs into display labels.

Requirements:

- Maintain a mapping for supported model classes.
- Preserve original class IDs.
- Handle missing mappings.
- Keep mapping data separate from UI components.

Acceptance criteria:

- Every supported class has an appropriate display label.
- Unknown class IDs are handled safely.

## F029: Latest Recognition Display

**Description:** Display the latest recognised sign.

Requirements:

- Display recognised label.
- Display recognition state.
- Display confidence when available.
- Display uncertain or unsupported states.

Acceptance criteria:

- The UI updates with actual backend results.
- No fabricated predictions are displayed.

## F030: Text Sequence Builder

**Description:** Build readable text from supported recognised outputs.

Requirements:

- Store accepted recognition results.
- Preserve recognition order.
- Allow editing.
- Support clear and reset.
- Apply sequence rules only when appropriate.

Important:

A sequence of alphabet predictions is not automatically a correct ISL translation. Any word or sentence construction must have explicit rules or a validated sequence model.

Acceptance criteria:

- Supported output is displayed in order.
- Unsupported combinations are not presented as verified language.
- Editing and reset controls work.

## F031: Text Editing

**Description:** Allow users to edit recognised text.

Requirements:

- Editable text area.
- Update displayed content.
- Preserve user edits until cleared or replaced intentionally.
- Provide a reset action.

Acceptance criteria:

- Users can modify text.
- Edited text can be used by the speech module.

## F032: Copy and Clear

**Description:** Provide basic text controls.

Requirements:

- Copy text.
- Clear current output.
- Provide user feedback.
- Handle empty content.

Acceptance criteria:

- Copy works.
- Clear works.
- Empty content does not cause errors.

---

# 12. MOD-08: Speech Output

**Priority:** P1  
**Development Phase:** Phase 7

## F033: Sarvam API Configuration

**Description:** Configure secure access to Sarvam AI.

Requirements:

- Store API credentials on the backend.
- Configure base service settings.
- Validate service configuration.
- Handle missing credentials.
- Document setup instructions.

Acceptance criteria:

- Credentials are not exposed in frontend code.
- Missing credentials produce useful errors.

## F034: Text-to-Speech Service

**Description:** Convert text into spoken audio.

Requirements:

- Accept text input.
- Validate text length.
- Select supported language or voice.
- Send request to Sarvam AI.
- Process audio response.
- Handle service errors.

Acceptance criteria:

- Valid supported text produces audio when the service is available.
- API failures are handled safely.

## F035: Audio Playback

**Description:** Play generated speech.

Requirements:

- Play audio.
- Pause or stop audio where supported.
- Replay audio.
- Display playback state.
- Handle playback errors.

Acceptance criteria:

- Audio playback works.
- Controls reflect actual playback state.
- Failed audio responses do not crash the interface.

## F036: Speech Language Selection

**Description:** Allow users to choose a supported spoken output language.

Requirements:

- Display available supported languages.
- Maintain selected language.
- Send the correct language parameter to the backend.
- Handle unsupported selections.

Acceptance criteria:

- Only verified supported languages are selectable.
- Selected language is applied to speech requests.

## F037: Speech Error Handling

**Description:** Handle speech service failures.

Requirements:

- Handle network errors.
- Handle invalid text.
- Handle service errors.
- Handle unsupported language.
- Provide retry where appropriate.

Acceptance criteria:

- Errors are displayed clearly.
- The rest of the application remains functional.

---

# 13. MOD-09: Reverse Communication

**Priority:** P1  
**Development Phase:** Phase 8

## F038: Microphone Permission

**Description:** Request microphone access.

Requirements:

- Explain microphone usage.
- Request browser permission.
- Handle denial.
- Handle missing microphone.
- Provide retry.

Acceptance criteria:

- Permission is requested when needed.
- Permission failures are handled.

## F039: Audio Capture

**Description:** Capture speech input.

Requirements:

- Start recording.
- Stop recording.
- Capture valid audio.
- Validate audio format.
- Release microphone resources.
- Avoid recording without user action.

Acceptance criteria:

- Audio can be captured.
- Recording controls work.
- Microphone is released after recording.

## F040: Speech-to-Text Service

**Description:** Convert captured audio into text.

Requirements:

- Submit audio to backend.
- Integrate supported Sarvam STT API.
- Validate request.
- Handle transcription response.
- Handle API failures.

Acceptance criteria:

- Supported audio can be transcribed.
- Errors are handled.
- Credentials remain on backend.

## F041: Transcription Display

**Description:** Display transcribed speech.

Requirements:

- Display transcription.
- Provide loading state.
- Provide error state.
- Allow text editing.
- Allow copying and clearing.

Acceptance criteria:

- Transcription appears correctly.
- Editing and clearing work.

## F042: Transcription Language Support

**Description:** Configure supported speech input languages.

Requirements:

- Check supported STT languages.
- Provide language selection where required.
- Validate language parameters.
- Handle unsupported languages.

Acceptance criteria:

- Only supported options are presented.
- Selected language is applied correctly.

---

# 14. MOD-10: Conversation Interface

**Priority:** P1  
**Development Phase:** Phase 8

## F043: Conversation Layout

**Description:** Create a common interface for both communication directions.

Requirements:

- Display sign-to-text messages.
- Display speech-to-text messages.
- Visually distinguish message sources.
- Maintain message order.
- Support responsive layouts.

Acceptance criteria:

- Both message types are displayed correctly.
- Users can distinguish their origin.

## F044: Message Representation

**Description:** Represent communication messages in a consistent format.

Potential fields:

- Message ID.
- Message content.
- Source type.
- Direction.
- Timestamp.
- Status.

Acceptance criteria:

- Messages follow a consistent data structure.
- Missing optional metadata is handled safely.

## F045: Conversation Controls

**Description:** Provide basic conversation actions.

Requirements:

- Copy message.
- Edit text where permitted.
- Clear conversation.
- Scroll to recent content.

Acceptance criteria:

- Controls work correctly.
- Clearing removes the displayed messages.
- User edits are preserved appropriately.

## F046: Temporary Conversation State

**Description:** Maintain conversation messages during the current application session.

Requirements:

- Store messages in frontend state.
- Preserve message order.
- Avoid persistent storage in the initial MVP.
- Clear state when requested.

Acceptance criteria:

- Messages remain visible during the active session.
- Clearing resets the conversation.

---

# 15. MOD-11: ISL Learning Centre

**Priority:** P2  
**Development Phase:** Phase 9

## F047: Learning Centre Layout

**Description:** Create an educational area for supported ISL signs.

Requirements:

- Display available learning categories.
- Display sign cards.
- Provide search or filtering where appropriate.
- Show available demonstrations.

Acceptance criteria:

- Learning content is organised.
- Layout is responsive.

## F048: Sign Detail Page

**Description:** Display information about an individual sign.

Requirements:

- Sign name.
- Category.
- Description.
- Image or video demonstration where available.
- Instructions where verified.

Acceptance criteria:

- Sign information is accurate.
- Content has suitable usage rights.
- Missing demonstrations are handled gracefully.

## F049: Learning Categories

**Description:** Organise supported signs into useful categories.

Potential categories:

- Alphabet.
- Numbers.
- Greetings.
- Common words.
- Everyday communication.

Only categories with verified learning content should be displayed.

Acceptance criteria:

- Filtering works.
- Category content is accurate.

## F050: Interactive Practice

**Description:** Allow users to practise supported signs.

Priority: P3.

Requirements:

- Display a reference sign.
- Capture a practice attempt.
- Compare against supported model classes.
- Provide feedback only when the recognition model supports the task.

Acceptance criteria:

- Feedback is based on actual model output.
- The system does not claim to assess unsupported sign correctness.

## F051: Learning Quiz

**Description:** Provide quizzes for available learning content.

Priority: P3.

Requirements:

- Display a sign or question.
- Provide answer options.
- Check the answer.
- Display feedback.
- Track progress only if persistence is implemented.

Acceptance criteria:

- Questions are based on verified learning content.
- Answer validation works.

---

# 16. MOD-12: User Preferences

**Priority:** P2  
**Development Phase:** Phase 9

## F052: Language Preferences

**Description:** Store preferred spoken output language.

Requirements:

- Display supported language options.
- Allow selection.
- Apply selection to speech services.
- Persist preference only when storage is implemented.

Acceptance criteria:

- Selected language is respected.
- Unsupported languages are rejected.

## F053: Accessibility Preferences

**Description:** Provide accessibility settings.

Potential settings:

- Text size.
- High contrast.
- Reduced motion.
- Interface theme.
- Audio controls.

Acceptance criteria:

- Selected settings work.
- Accessibility options do not break the layout.

## F054: Theme Preferences

**Description:** Allow users to select supported application themes.

Requirements:

- Theme selection.
- Consistent colours.
- Readable contrast.
- Persistent preference only if storage is implemented.

Acceptance criteria:

- Theme changes work across application pages.

---

# 17. MOD-13: Data Management

**Priority:** P2  
**Development Phase:** Phase 9

## F055: Database Setup

**Description:** Configure PostgreSQL when persistent features are required.

Requirements:

- Configure database connection.
- Use environment variables.
- Define schemas.
- Add migrations.
- Handle connection errors.

Acceptance criteria:

- Database connects successfully.
- Schema is documented.
- Credentials remain secure.

## F056: User Authentication

**Description:** Allow users to create and access accounts.

Priority: P3.

Requirements:

- Registration.
- Login.
- Logout.
- Secure authentication.
- Session management.
- Input validation.

Acceptance criteria:

- Authentication works securely.
- Protected features require valid sessions.

Authentication is not required for the initial camera recognition demonstration.

## F057: Conversation History

**Description:** Allow users to access previous conversations.

Priority: P3.

Requirements:

- Save conversation metadata.
- Require appropriate user consent.
- Display previous records.
- Allow deletion.
- Avoid storing raw media by default.

Acceptance criteria:

- Records belong to the correct user.
- Deletion works.
- Privacy requirements are respected.

## F058: Learning Progress

**Description:** Track learning progress for signed-in users.

Priority: P3.

Requirements:

- Track completed lessons.
- Track quiz results.
- Store progress.
- Display progress summary.

Acceptance criteria:

- Progress is saved correctly.
- Users can access their own records.

---

# 18. MOD-14: Security and Privacy

**Priority:** P0  
**Development Phase:** All phases

## F059: Secret Management

Requirements:

- Store API keys in environment variables.
- Never commit real credentials.
- Never expose credentials in frontend bundles.
- Document secret configuration.

Acceptance criteria:

- Repository contains no active secrets.
- External service requests are handled by the backend.

## F060: Camera Privacy

Requirements:

- Request permission.
- Show camera status.
- Stop camera when requested.
- Release media streams.
- Avoid storing video by default.

Acceptance criteria:

- Camera cannot run without permission.
- Camera stops when the user exits the feature.

## F061: Microphone Privacy

Requirements:

- Request permission.
- Show recording status.
- Stop recording when requested.
- Release microphone resources.
- Avoid recording without user action.

Acceptance criteria:

- Recording state is visible.
- Microphone is released after use.

## F062: API Validation

Requirements:

- Validate request data.
- Validate file types.
- Limit upload size.
- Handle malformed requests.
- Use appropriate HTTP status codes.

Acceptance criteria:

- Invalid requests do not crash services.
- Error responses are understandable.

## F063: Privacy Information

Requirements:

- Explain camera and microphone usage.
- Explain external AI service usage.
- Document data retention.
- Explain conversation storage if introduced.

Acceptance criteria:

- Users can understand how their data is processed.

---

# 19. MOD-15: Testing and Deployment

**Priority:** P0  
**Development Phase:** Phase 10

## F064: ML Unit Testing

Requirements:

- Test model loading.
- Test preprocessing.
- Test inference.
- Test invalid inputs.
- Test output structure.

Acceptance criteria:

- Tests pass.
- Model behaviour is reproducible.

## F065: Backend Testing

Requirements:

- Test health endpoint.
- Test recognition endpoint.
- Test invalid requests.
- Test model unavailable state.
- Test speech service errors.

Acceptance criteria:

- Expected responses are returned.
- Error conditions are handled.

## F066: Frontend Testing

Requirements:

- Test navigation.
- Test camera controls.
- Test microphone controls.
- Test recognition display.
- Test speech playback.
- Test empty and error states.

Acceptance criteria:

- Main user workflows work.
- No critical console errors remain.

## F067: Integration Testing

Requirements:

- Test frontend to backend communication.
- Test backend to ML integration.
- Test backend to Sarvam integration.
- Test complete sign-to-text flow.
- Test reverse speech-to-text flow.

Acceptance criteria:

- All implemented modules communicate correctly.
- Failures are handled.

## F068: Performance Testing

Requirements:

- Measure inference latency.
- Measure API response time.
- Measure end-to-end recognition latency.
- Monitor memory usage.
- Test under realistic conditions.

Acceptance criteria:

- Measurements are recorded.
- Bottlenecks are documented.
- No unsupported performance claims are made.

## F069: Responsive Testing

Requirements:

- Test desktop layout.
- Test tablet layout.
- Test mobile layout.
- Test camera interface sizing.
- Test accessibility controls.

Acceptance criteria:

- Main workflows remain usable across supported screen sizes.

## F070: Deployment

Requirements:

- Configure frontend deployment.
- Configure backend deployment.
- Configure environment variables.
- Configure CORS.
- Verify model availability.
- Test production API connectivity.
- Document deployment steps.

Acceptance criteria:

- Application is accessible in the deployment environment.
- Frontend can communicate with backend.
- Secrets are protected.
- Main user workflows are tested.

## F071: Demo Preparation

Requirements:

- Prepare a working demonstration.
- Prepare representative supported sign examples.
- Prepare speech input examples.
- Explain supported vocabulary.
- Explain model limitations.
- Record actual evaluation results.

Acceptance criteria:

- Demonstration uses working features.
- Claims match actual capabilities.
- Known limitations are disclosed.

---

# 20. Feature Dependency Map

The following dependencies define the recommended implementation order.

| Feature | Depends On |
|---|---|
| F013 Camera Permission | F002 |
| F014 Live Camera Preview | F013 |
| F016 Frame Capture | F014 |
| F017 Model Research | F002 |
| F018 Dataset Verification | F017 |
| F019 Model Loading | F018 |
| F020 Input Preprocessing | F019 |
| F021 Static Recognition | F020 |
| F023 Recognition Service | F021 |
| F024 Confidence Handling | F023 |
| F025 Prediction Smoothing | F024 |
| F028 Sign Label Mapping | F023 |
| F029 Recognition Display | F028 |
| F030 Text Sequence Builder | F028 |
| F033 Sarvam Configuration | F004 |
| F034 Text-to-Speech | F033 |
| F035 Audio Playback | F034 |
| F039 Audio Capture | F038 |
| F040 Speech-to-Text | F033, F039 |
| F041 Transcription Display | F040 |
| F043 Conversation Layout | F029, F041 |
| F055 Database Setup | Database decision |
| F056 Authentication | F055 |
| F057 Conversation History | F055, F056 |
| F064-F070 Testing and Deployment | Relevant implemented features |

These dependencies may be refined when the actual architecture and model are verified.

---

# 21. MVP Feature Selection

The first working MVP must prioritise the core communication workflow.

## 21.1 Must-Have Features

| ID | Feature | Priority |
|---|---|---|
| F001 | Repository Structure | P0 |
| F002 | Development Environment | P0 |
| F003 | Antigravity Instructions | P0 |
| F004 | Environment Configuration | P0 |
| F013 | Camera Permission | P0 |
| F014 | Live Camera Preview | P0 |
| F015 | Camera Start and Stop | P0 |
| F016 | Frame Capture | P0 |
| F017 | Model Research | P0 |
| F018 | Dataset Verification | P0 |
| F019 | Model Loading | P0 |
| F020 | Input Preprocessing | P0 |
| F021 | Static Sign Recognition | P0 |
| F023 | Recognition Service | P0 |
| F024 | Confidence Handling | P0 |
| F025 | Prediction Smoothing | P0 |
| F027 | Unknown Sign Detection | P0 |
| F028 | Sign Label Mapping | P0 |
| F029 | Recognition Display | P0 |
| F032 | Copy and Clear | P0 |
| F059 | Secret Management | P0 |
| F060 | Camera Privacy | P0 |
| F062 | API Validation | P0 |

## 21.2 Important MVP Features

| ID | Feature | Priority |
|---|---|---|
| F005-F009 | Landing Page | P1 |
| F010-F012 | Dashboard | P1 |
| F030 | Text Sequence Builder | P1, only within supported capabilities |
| F031 | Text Editing | P1 |
| F033-F037 | Speech Output | P1 |
| F038-F042 | Reverse Communication | P1 |
| F043-F046 | Conversation Interface | P1 |

## 21.3 Post-MVP Features

- ISL learning centre.
- Interactive practice.
- Learning quizzes.
- User accounts.
- Persistent conversation history.
- Learning progress.
- Advanced dynamic sign recognition.
- Continuous sign language interpretation.
- Mobile application.
- Offline recognition.

---

# 22. Feature Acceptance Rules

Every feature must satisfy its acceptance criteria before being marked Completed.

Antigravity must:

1. Read the feature requirements.
2. Identify dependencies.
3. Inspect existing implementation.
4. Prepare an implementation plan.
5. Implement the feature.
6. Add or update tests.
7. Execute relevant tests.
8. Fix errors.
9. Verify actual behaviour.
10. Update documentation.
11. Report completion status.

A feature is not complete merely because:

- A UI component exists.
- An API route exists.
- A placeholder response is returned.
- A button is visible.
- A mock prediction is displayed.
- A service integration is written but not tested.

---

# 23. Antigravity Feature Implementation Instructions

These instructions apply to every feature implementation task.

## 23.1 Before Coding

Read:

- `AGENTS.md`
- `docs/PRD.md`
- `docs/PROJECT_OVERVIEW.md`
- `docs/FEATURES.md`
- Relevant architecture and technical documents.

Then:

- Identify the feature ID.
- Confirm its requirements.
- Check dependencies.
- Inspect existing code.
- Identify affected modules.

## 23.2 During Coding

- Implement only the requested feature.
- Follow the approved technology stack.
- Use React and JavaScript for frontend development.
- Use Python and FastAPI for backend development.
- Use PyTorch for supported ML model integration.
- Keep components modular.
- Handle loading, success, and error states.
- Avoid unnecessary dependencies.
- Do not introduce unrelated features.
- Do not invent ML behaviour or evaluation results.

## 23.3 After Coding

Report:

**Feature ID:**  
**Feature Name:**  
**Implementation Status:**  
**Files Created:**  
**Files Modified:**  
**Dependencies Added:**  
**Tests Executed:**  
**Test Results:**  
**Known Limitations:**  
**Remaining Work:**  

Only mark the feature Completed when its acceptance criteria pass.

---

# 24. Final Product Feature Summary

Signova AI will bring together the following capabilities:

1. Camera-based ISL sign recognition.
2. Prediction validation and stabilisation.
3. Sign-to-text conversion for supported vocabulary.
4. Text-to-speech output.
5. Reverse speech-to-text communication.
6. A unified conversation interface.
7. An ISL learning centre.
8. Accessibility settings.
9. Optional user preferences and history.
10. Future dynamic and continuous sign recognition.

The initial product must prioritise a reliable working recognition workflow over a large collection of incomplete features.

**Core Principle: Every feature must solve a clear user problem, have a defined implementation, and be verified before it is considered complete.**