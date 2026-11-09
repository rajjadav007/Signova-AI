# Signova AI: Testing Strategy

## 1. Overview

This document defines the testing strategy for Signova AI.

Signova AI is an AI-powered accessibility platform designed to recognise Indian Sign Language (ISL) gestures and support communication through text and speech.

Testing is essential to ensure that the application is:

- Functionally correct.
- Reliable during real-time recognition.
- Accurate within the supported sign vocabulary.
- Secure and privacy-conscious.
- Responsive across devices.
- Compatible with the selected AI models.
- Stable during API communication.
- Accessible and easy to use.

The testing process covers the complete application, including frontend, backend, ML inference, database, and external speech services.

---

# 2. Testing Objectives

The primary objectives are:

1. Verify that every implemented feature works correctly.
2. Validate the ISL recognition pipeline.
3. Measure model performance using appropriate evaluation metrics.
4. Test communication between frontend and backend.
5. Verify real-time recognition behaviour.
6. Validate Sarvam AI integrations.
7. Identify errors before deployment.
8. Test application security and privacy.
9. Measure inference latency and application responsiveness.
10. Ensure a consistent user experience.

### Testing Principles

- Test actual implementation, not planned features.
- Use reproducible test cases.
- Never invent model accuracy or performance results.
- Separate software bugs from model limitations.
- Test both successful and unsuccessful scenarios.
- Record actual test results.
- Protect real user data.
- Fix critical issues before deployment.

---

# 3. Testing Scope

Testing is divided into eight major areas.

| Testing Area | Purpose |
|---|---|
| Frontend Testing | Verify React components and interactions |
| Backend Testing | Verify FastAPI services and business logic |
| ML Testing | Evaluate ISL recognition models |
| API Testing | Verify request and response behaviour |
| WebSocket Testing | Verify real-time communication |
| Database Testing | Verify data integrity and operations |
| Integration Testing | Verify communication between modules |
| System Testing | Verify the complete application |

Additional testing includes security, accessibility, compatibility, and performance.

---

# 4. Testing Architecture

```text
                  Signova AI
                      |
          ┌───────────┴───────────┐
          |                       |
       Frontend                 Backend
          |                       |
          v                       v
    React Component         FastAPI Testing
       Testing                    |
          |                       v
          |                  API Testing
          |                       |
          |              ┌────────┴────────┐
          |              |                 |
          |              v                 v
          |         ML Testing        Database Testing
          |              |
          |              v
          |        Model Evaluation
          |              |
          └──────────────┴──────────────┐
                                       |
                                       v
                               Integration Testing
                                       |
                                       v
                                  E2E Testing
                                       |
                                       v
                                Deployment Testing
```

---

# 5. Testing Technology Stack

| Technology | Purpose |
|---|---|
| Pytest | Python unit and integration tests |
| FastAPI TestClient | Backend API testing |
| HTTPX | HTTP and asynchronous API testing |
| Vitest | Frontend unit testing |
| React Testing Library | React component testing |
| Playwright | Browser end-to-end testing |
| Ruff | Python linting |
| ESLint | JavaScript linting |
| PostgreSQL Test Database | Database testing |
| Python logging | Test and runtime diagnostics |
| GitHub Actions | Automated CI testing |

Use only the tools required by the implemented features.

---

# 6. Frontend Testing

## 6.1 Objectives

Frontend testing verifies that the React application behaves correctly and provides a consistent user experience.

### Components to Test

- Landing page.
- Navigation.
- Dashboard.
- Camera interface.
- Recognition interface.
- Prediction result display.
- Text output.
- Speech controls.
- Language selector.
- Conversation interface.
- Settings.
- Error messages.
- Loading indicators.

## 6.2 Component Testing

Verify:

- Components render correctly.
- Props are handled correctly.
- Buttons trigger expected actions.
- Forms validate user input.
- Loading states display correctly.
- Error messages are visible.
- Empty states are handled.
- Components remain responsive.

### Example Test

```javascript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { RecognitionStatus } from "./RecognitionStatus";

describe("RecognitionStatus", () => {
  it("displays the recognition status", () => {
    render(
      <RecognitionStatus status="recognised" />
    );

    expect(
      screen.getByText(/recognised/i)
    ).toBeInTheDocument();
  });
});
```

This example assumes the component and its test dependencies have been implemented.

## 6.3 Camera Testing

Test the following scenarios:

| Test Case | Expected Result |
|---|---|
| Camera permission granted | Camera starts |
| Camera permission denied | Clear error appears |
| Camera unavailable | Fallback message appears |
| Camera stopped | Video stream is released |
| Camera switched | Correct device is selected |
| Page unmounted | Camera tracks are stopped |
| Invalid frame | Frame is rejected safely |

### Camera Requirements

- Request permission only when needed.
- Display a clear camera status.
- Handle browser permission errors.
- Stop camera tracks when the feature closes.
- Do not capture frames without user consent.

## 6.4 Recognition Interface Testing

Verify:

- Prediction appears after a valid response.
- Confidence is displayed only when available.
- Unknown predictions are handled.
- Uncertain predictions are not shown as confirmed signs.
- Repeated predictions do not unnecessarily duplicate text.
- Pause and resume controls work.
- Camera disconnection is handled.
- Recognition errors do not crash the interface.

## 6.5 Frontend Accessibility Testing

Verify:

- Buttons have meaningful labels.
- Inputs have accessible labels.
- Keyboard navigation works.
- Focus indicators are visible.
- Text contrast is sufficient.
- Status updates are accessible to assistive technology.
- Screen readers can understand important controls.
- Colour is not the only way to communicate status.

---

# 7. Backend Testing

## 7.1 Objectives

Backend testing verifies that FastAPI routes, services, validation, and business logic behave correctly.

### Modules to Test

- Health service.
- Recognition service.
- Model loading service.
- Image preprocessing.
- Video processing.
- Speech service.
- Translation service.
- Conversation service.
- Authentication.
- Database repositories.

## 7.2 Unit Testing

Unit tests verify individual functions independently.

### Example

```python
def test_validate_language_code():
    from app.services.speech_service import (
        validate_language_code,
    )

    assert validate_language_code("en-IN") is True
```

This test assumes that the function is implemented with the stated contract.

### Unit Test Requirements

- Test valid inputs.
- Test invalid inputs.
- Test missing values.
- Test boundary conditions.
- Test expected exceptions.
- Mock external services.
- Keep tests independent.

## 7.3 Service Testing

| Service | Test |
|---|---|
| Recognition | Valid prediction output |
| Preprocessing | Correct model input |
| Model Loader | Successful checkpoint loading |
| Speech | TTS response handling |
| STT | Audio transcription handling |
| Translation | Language validation |
| Conversation | Session creation |
| Database | Record creation and retrieval |

## 7.4 Error Handling Tests

Test:

- Invalid request.
- Missing required fields.
- Unsupported file.
- Model unavailable.
- Inference failure.
- External API timeout.
- Database connection failure.
- Authentication failure.

Expected behaviour:

- Return a meaningful error.
- Use the correct status code.
- Do not expose internal stack traces.
- Do not crash unrelated requests.

---

# 8. Machine Learning Testing

<badge color="success">Critical Testing Area</badge>

ML testing is one of the most important parts of Signova AI.

A working application does not automatically mean that the ISL recognition model is accurate.

The model must be evaluated independently before integration and again after integration.

## 8.1 Model Verification

Before testing a pretrained model, verify:

- Repository source.
- Model architecture.
- Checkpoint availability.
- Model licence.
- Dataset provenance.
- Supported sign vocabulary.
- Input image or video format.
- Expected input dimensions.
- Preprocessing requirements.
- Output class labels.
- Dependencies.
- Hardware requirements.

### Model Verification Checklist

| Requirement | Expected Result |
|---|---|
| Checkpoint | Loads successfully |
| Architecture | Matches checkpoint |
| Input shape | Matches model requirements |
| Preprocessing | Reproduces training pipeline |
| Class labels | Verified |
| Inference | Runs successfully |
| Licence | Reviewed |
| Dataset | Identified |
| Hardware | Tested |
| Output | Valid and interpretable |

Do not integrate an unverified checkpoint into the production inference service.

## 8.2 Static Sign Recognition Testing

Static recognition evaluates individual signs or hand configurations.

Test:

- Every supported class.
- Different hand positions.
- Different lighting conditions.
- Different backgrounds.
- Different camera distances.
- Left and right hand variations where supported.
- Partially obscured hands.
- Invalid inputs.
- Unsupported signs.

### Example Test Dataset

```text
ml/datasets/
├── test/
│   ├── class_1/
│   ├── class_2/
│   ├── class_3/
│   └── ...
```

The actual dataset structure must match the selected model's requirements.

## 8.3 Dynamic Sign Recognition Testing

Dynamic recognition evaluates signs that depend on movement over time.

Test:

- Correct frame sequence.
- Incorrect frame sequence.
- Different movement speeds.
- Different starting positions.
- Different sequence lengths.
- Missing frames.
- Camera interruptions.
- Similar-looking signs.
- Unseen or unsupported signs.

A dynamic model must be evaluated using complete temporal sequences.

Do not evaluate it as a collection of unrelated static images unless that is the model's intended input method.

## 8.4 Continuous Sign Language Testing

Continuous ISL interpretation is a more advanced capability.

It may require:

- Continuous video understanding.
- Word boundary detection.
- Temporal segmentation.
- Contextual sentence interpretation.
- Non-manual cues.
- Facial expressions.
- Spatial and grammatical information.

Testing must use appropriately annotated continuous ISL data.

A static alphabet classifier must never be described as a continuous ISL translation model.

## 8.5 Model Evaluation Metrics

Use the following metrics where applicable.

### Accuracy

Measures the percentage of correct predictions.

\[
Accuracy = \frac{Correct\ Predictions}{Total\ Predictions}
\]

### Precision

Measures how many positive predictions are correct.

\[
Precision = \frac{TP}{TP+FP}
\]

### Recall

Measures how many actual positive samples are correctly identified.

\[
Recall = \frac{TP}{TP+FN}
\]

### F1 Score

Balances precision and recall.

\[
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
\]

### Additional Metrics

| Metric | Purpose |
|---|---|
| Accuracy | Overall correctness |
| Precision | Prediction reliability |
| Recall | Ability to identify supported classes |
| Macro F1 | Balanced class-level performance |
| Weighted F1 | Performance weighted by class frequency |
| Confusion Matrix | Class-level errors |
| Top-1 Accuracy | Most likely class correctness |
| Top-5 Accuracy | Correct class within top five, when applicable |
| Inference Latency | Time required for inference |
| Throughput | Samples processed per unit time |

Do not rely on accuracy alone, especially when the dataset has class imbalance.

## 8.6 Confusion Matrix

Use a confusion matrix to identify classes that the model frequently confuses.

```python
from sklearn.metrics import confusion_matrix

actual = [0, 1, 2, 1, 0]
predicted = [0, 1, 1, 1, 0]

matrix = confusion_matrix(
    actual,
    predicted,
)

print(matrix)
```

The values above are illustrative test data, not Signova AI model results.

## 8.7 Dataset Splitting

Use separate training, validation, and test data where model training or fine-tuning is performed.

Recommended approach:

| Dataset | Purpose |
|---|---|
| Training | Model learning |
| Validation | Model selection and tuning |
| Test | Final evaluation |

### Important Rules

- Avoid duplicate images across splits.
- Avoid leakage between training and test data.
- Prefer signer-independent evaluation when signer identities are available.
- Keep test data separate during model selection.
- Document dataset sources.
- Check class imbalance.
- Record the dataset version.

A random image split may overestimate real-world performance when the same signer or recording session appears across multiple splits.

## 8.8 Unknown Sign Testing

The system must handle signs outside its supported vocabulary.

Test:

- Unknown gestures.
- No hand visible.
- Multiple hands.
- Blurred input.
- Low lighting.
- Incorrect hand orientation.
- Ambiguous signs.

Expected result:

- Return `unknown` or `uncertain` when appropriate.
- Do not invent a valid sign.
- Do not present low-confidence predictions as confirmed translations.

Confidence thresholds must be calibrated using validation data, not selected only because they look good in a demo.

## 8.9 Model Reproducibility

For every model evaluation, record:

- Model name.
- Model version.
- Checkpoint identifier.
- Dataset version.
- Dataset split.
- Preprocessing configuration.
- Evaluation script version.
- Hardware.
- Python and PyTorch versions.
- Random seed where relevant.
- Actual evaluation metrics.

Store evaluation reports in:

```text
ml/evaluation/
├── reports/
├── confusion_matrices/
├── metrics/
└── benchmark_results/
```

---

# 9. API Testing

API testing verifies communication between frontend and backend.

Use FastAPI TestClient or HTTPX.

## 9.1 Health API

Endpoint:

```http
GET /health
```

Test:

- Successful response.
- Correct status code.
- Correct response format.
- Backend unavailable scenario.

## 9.2 Image Prediction API

Endpoint:

```http
POST /api/v1/ai/predict/image
```

Test:

| Test Case | Expected Result |
|---|---|
| Valid image | Prediction response |
| Invalid image | 400 error |
| Unsupported format | 415 error |
| Oversized file | 413 error |
| Missing file | 422 error |
| Invalid model ID | Validation error |
| Model unavailable | 503 error |
| Inference failure | Controlled error |
| Low confidence | Uncertain status |

## 9.3 Video Prediction API

Endpoint:

```http
POST /api/v1/ai/predict/video
```

Test:

- Valid video.
- Invalid video.
- Unsupported format.
- Oversized video.
- Invalid frame sequence.
- Missing dynamic model.
- Processing failure.

## 9.4 Speech API

Test:

- Valid TTS request.
- Empty text.
- Unsupported language.
- Valid STT audio.
- Invalid audio.
- Translation request.
- External API failure.
- External API timeout.

## 9.5 Conversation API

Test:

- Create session.
- Retrieve session.
- List sessions.
- Delete session.
- Invalid session ID.
- Unauthenticated access.
- Cross-user access.

## 9.6 API Contract Testing

Verify that:

- Request fields match the documentation.
- Response fields match the documentation.
- Status codes are correct.
- Validation errors are consistent.
- Optional fields behave correctly.
- Binary responses use the correct content type.

The actual API contract must remain synchronised with `docs/API_DOCUMENTATION.md`.

---

# 10. WebSocket Testing

WebSocket testing verifies real-time recognition.

### Endpoint

```text
ws://localhost:8000/api/v1/ai/predict/stream
```

### Test Cases

| Test Case | Expected Result |
|---|---|
| Successful connection | Connection established |
| Invalid configuration | Error returned |
| Valid frame | Prediction returned |
| Invalid frame | Controlled error |
| Oversized frame | Rejected |
| Unknown model | Error returned |
| Stop message | Session stopped |
| Client disconnect | Resources released |
| Inference failure | Error returned |
| Excessive frame rate | Rate limit applied |

### Performance Testing

Measure:

- Frame transmission time.
- Backend preprocessing time.
- Model inference time.
- Response transmission time.
- End-to-end latency.
- Dropped frames.
- Queue size.

Do not confuse model inference time with total user-perceived response time.

### WebSocket Stability

Test:

- Repeated connection and disconnection.
- Long-running sessions.
- Network interruptions.
- Browser tab closure.
- Backend restart.
- Multiple concurrent clients.

---

# 11. Database Testing

Database testing verifies PostgreSQL data integrity and application access controls.

### Tables to Test

- `users`
- `user_preferences`
- `conversations`
- `messages`
- `model_registry`
- `recognition_logs`
- `learning_resources`
- `user_learning_progress`

### Test Cases

| Test | Expected Result |
|---|---|
| Create user | User record created |
| Duplicate email | Constraint violation |
| Create preferences | Preference saved |
| Create conversation | Session saved |
| Create message | Message linked correctly |
| Delete conversation | Messages deleted |
| Invalid foreign key | Database rejects record |
| Invalid confidence | Database rejects value |
| Duplicate progress | Constraint violation |
| Delete user | Configured cascade behaviour |

### Database Requirements

- Use a separate test database.
- Verify foreign key relationships.
- Verify constraints.
- Test migrations.
- Test transaction rollback.
- Verify deletion behaviour.
- Test access restrictions.

Never run destructive database tests against production.

---

# 12. Integration Testing

Integration testing verifies that multiple application modules work together.

### 12.1 Frontend and Backend

Verify:

- React sends correct API requests.
- FastAPI receives valid requests.
- Responses update the interface.
- Loading states work.
- Errors are displayed correctly.

### 12.2 Backend and ML Model

Verify:

- Model loads successfully.
- Correct preprocessing is applied.
- Input reaches the model correctly.
- Output is converted into the documented response schema.
- Unknown and uncertain outputs are handled.

### 12.3 Backend and Sarvam AI

Verify:

- Credentials are read securely.
- Requests use the correct external API contract.
- Supported languages are handled.
- Audio and text responses are processed correctly.
- Rate limits and timeouts are handled.

Use mocked responses for normal automated tests and controlled real API tests for integration verification.

### 12.4 Backend and Database

Verify:

- Records are saved correctly.
- Relationships are valid.
- Transactions work.
- User access is enforced.
- Deletion policies work.

---

# 13. End-to-End Testing

End-to-end testing verifies the complete user journey in a browser.

Use Playwright.

## 13.1 Main User Journey

```text
Open Signova AI
       |
       v
Navigate to Recognition
       |
       v
Grant Camera Permission
       |
       v
Start Camera
       |
       v
Present Supported ISL Sign
       |
       v
Capture Frame or Sequence
       |
       v
Send to Backend
       |
       v
Run ML Inference
       |
       v
Receive Prediction
       |
       v
Display Recognised Text
       |
       v
Generate Speech (Optional)
       |
       v
Play Audio
```

This journey must only include recognition modes that are actually implemented.

## 13.2 E2E Test Scenarios

| Scenario | Expected Result |
|---|---|
| Open landing page | Page loads |
| Navigate to recognition | Recognition page opens |
| Allow camera | Camera starts |
| Deny camera | Error appears |
| Submit valid input | Prediction displayed |
| Submit invalid input | Error displayed |
| Receive uncertain prediction | Uncertainty displayed |
| Generate speech | Audio is returned |
| Play audio | Audio plays |
| Stop recognition | Camera and connection stop |

## 13.3 E2E Testing Rules

- Use controlled test data.
- Mock external services where appropriate.
- Use a test backend.
- Avoid depending on unpredictable real-world camera conditions.
- Verify the full application flow.
- Record screenshots or traces for failed tests when useful.

---

# 14. Sarvam AI Integration Testing

Sarvam AI supports speech and language features around Signova AI.

Test each selected capability independently.

### Text-to-Speech

- Valid text.
- Supported language.
- Unsupported language.
- Invalid speaker.
- Empty input.
- API timeout.
- Invalid credentials.
- Audio response validation.

### Speech-to-Text

- Valid audio.
- Empty audio.
- Unsupported format.
- Unsupported language.
- No speech detected.
- External API failure.

### Translation

- Valid source language.
- Valid target language.
- Unsupported language.
- Empty text.
- Long text.
- External API failure.

### Important Rules

- Verify the current Sarvam API documentation before implementation.
- Do not assume every language or model is supported.
- Keep API keys on the backend.
- Do not make live paid API calls in every unit test.
- Record real integration results separately.
- Handle provider rate limits and service interruptions.

---

# 15. Security Testing

Security testing ensures that Signova AI protects user information and application resources.

## 15.1 Authentication

Test:

- Valid login.
- Invalid login.
- Expired token.
- Missing token.
- Invalid token.
- Protected endpoint access.

## 15.2 Authorisation

Test:

- User accessing their own conversation.
- User attempting to access another user's conversation.
- User updating their own preferences.
- User attempting to modify another user's data.

Expected result: Unauthorised access is rejected.

## 15.3 File Upload Security

Test:

- Invalid file extensions.
- Incorrect file content.
- Oversized files.
- Corrupted files.
- Unexpected filenames.
- Malformed payloads.

Validate file contents and decoding, not only the filename.

## 15.4 API Security

Test:

- CORS configuration.
- Rate limiting.
- Input validation.
- SQL injection resistance.
- Authentication enforcement.
- Sensitive error exposure.
- Secret management.

## 15.5 Privacy Testing

Verify:

- Camera access requires permission.
- Microphone access requires permission.
- Raw video is not stored by default.
- Raw audio is not stored by default.
- Conversation history follows user preferences.
- Data deletion works.
- External service processing is disclosed.

---

# 16. Accessibility Testing

Signova AI is an accessibility-focused product. Its interface must be usable by people with different abilities.

### Accessibility Requirements

- Keyboard-accessible controls.
- Screen reader support.
- Proper semantic HTML.
- Clear form labels.
- Visible focus states.
- Sufficient text contrast.
- Readable typography.
- Clear error messages.
- Captions or text alternatives for audio content.
- Accessible status announcements.

### Camera Interface

- Provide clear camera instructions.
- Show camera permission status.
- Avoid relying only on visual indicators.
- Provide text-based recognition results.
- Provide accessible controls for starting and stopping recognition.

### Speech Interface

- Provide text alternatives for generated audio.
- Provide replay controls.
- Clearly indicate audio playback state.
- Avoid automatic audio playback without user action.

### Testing Standard

Use WCAG 2.2 AA as the accessibility target.

Automated accessibility checks are useful, but they do not replace manual keyboard and screen reader testing.

---

# 17. Performance Testing

Performance testing evaluates the application's speed, stability, and resource consumption.

## 17.1 Frontend Performance

Measure:

- Initial page load.
- Route navigation.
- Component rendering.
- Camera startup.
- API response handling.
- Memory usage.
- UI responsiveness.

## 17.2 Backend Performance

Measure:

- API response time.
- Model loading time.
- Preprocessing time.
- Inference time.
- Database query time.
- WebSocket latency.
- Concurrent request handling.

## 17.3 ML Performance

Measure:

- Model loading time.
- Inference latency.
- CPU usage.
- GPU usage.
- GPU memory usage.
- RAM consumption.
- Batch throughput where relevant.

Test on the actual target hardware.

A model that runs on a development GPU may behave differently on a CPU-only production server.

## 17.4 Real-Time Recognition Performance

Measure the complete pipeline:

```text
Camera Capture
      |
      v
Frame Processing
      |
      v
Network Transfer
      |
      v
Backend Preprocessing
      |
      v
ML Inference
      |
      v
Response Transfer
      |
      v
Frontend Update
```

Record the latency of each stage.

## 17.5 Performance Targets

The following are initial engineering targets, not verified results or guaranteed requirements.

| Metric | Initial Target |
|---|---|
| Backend health response | Under 500 ms |
| Simple API response | Under 1 second |
| Recognition feedback | Under 1.5 seconds where hardware permits |
| Frontend interaction | Responsive without blocking |
| WebSocket connection | Stable during normal sessions |
| Memory usage | Within deployment limits |
| Error handling | No application crash |

The final targets must be adjusted after measuring the selected model and deployment environment.

---

# 18. Compatibility Testing

Test Signova AI across supported browsers and devices.

### Browsers

- Google Chrome.
- Microsoft Edge.
- Mozilla Firefox.
- Safari.

### Devices

- Desktop.
- Laptop.
- Tablet.
- Smartphone.

### Compatibility Checks

- Camera permissions.
- Microphone permissions.
- WebSocket support.
- Audio playback.
- Responsive layout.
- File upload.
- Browser media APIs.
- WebRTC-related behaviour if introduced.

Test actual device behaviour rather than assuming that every browser handles camera and audio access identically.

---

# 19. Regression Testing

Regression testing verifies that new changes do not break existing features.

Run regression tests after:

- ML model replacement.
- Model preprocessing changes.
- Backend API changes.
- WebSocket changes.
- Frontend redesign.
- Database migrations.
- Sarvam integration updates.
- Dependency upgrades.

### Regression Checklist

- [ ] Landing page works.
- [ ] Navigation works.
- [ ] Camera access works.
- [ ] Recognition works.
- [ ] Prediction output is correct.
- [ ] Unknown sign handling works.
- [ ] Speech output works if implemented.
- [ ] API requests work.
- [ ] Database operations work if enabled.
- [ ] No major console errors.
- [ ] No backend crashes.

---

# 20. Test Directory Structure

Recommended project structure:

```text
signova-ai/
│
├── frontend/
│   └── src/
│       └── features/
│
├── backend/
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_ai.py
│       ├── test_speech.py
│       ├── test_conversations.py
│       ├── test_websocket.py
│       └── test_database.py
│
├── ml/
│   ├── evaluation/
│   │   ├── evaluate_model.py
│   │   ├── metrics.py
│   │   ├── confusion_matrix.py
│   │   └── reports/
│   │
│   └── tests/
│       ├── test_preprocessing.py
│       ├── test_model_loading.py
│       ├── test_inference.py
│       └── test_prediction_output.py
│
├── frontend/
│   └── tests/
│       ├── components/
│       └── services/
│
└── tests/
    ├── e2e/
    │   ├── landing.spec.js
    │   ├── recognition.spec.js
    │   └── communication.spec.js
    │
    ├── integration/
    └── security/
```

Keep frontend tests inside the existing frontend structure. Avoid creating duplicate frontend directories when implementing this layout.

---

# 21. Test Execution Commands

## 21.1 Backend Tests

Install testing dependencies:

```bash
pip install pytest pytest-cov httpx
```

Run all backend tests:

```bash
pytest backend/tests -v
```

Run tests with coverage:

```bash
pytest backend/tests --cov=backend/app --cov-report=term-missing
```

## 21.2 ML Tests

```bash
pytest ml/tests -v
```

## 21.3 Frontend Tests

Install dependencies:

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

Run frontend tests:

```bash
npm run test
```

## 21.4 E2E Tests

Install Playwright:

```bash
npm install -D @playwright/test
```

Install browser dependencies:

```bash
npx playwright install
```

Run E2E tests:

```bash
npx playwright test
```

## 21.5 Python Code Quality

```bash
ruff check backend ml
```

## 21.6 JavaScript Code Quality

```bash
npm run lint
```

Commands must match the actual scripts configured in the project.

---

# 22. Continuous Integration

Use GitHub Actions to automate repeatable tests.

### CI Workflow

```text
Developer Push
      |
      v
GitHub Repository
      |
      v
GitHub Actions
      |
      ├── Install Dependencies
      |
      ├── Python Lint
      |
      ├── Backend Tests
      |
      ├── ML Unit Tests
      |
      ├── Frontend Lint
      |
      ├── Frontend Tests
      |
      └── Build Frontend
              |
              v
        Test Report
```

### CI Requirements

- Run tests on pull requests.
- Run tests on important branches.
- Use dependency caching where appropriate.
- Store test reports.
- Keep secrets in GitHub Actions secrets.
- Avoid requiring paid external API calls.
- Avoid downloading large model checkpoints during every CI run.

### Example GitHub Actions Workflow

Create:

`.github/workflows/tests.yml`

```yaml
name: Signova AI Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov httpx ruff

      - name: Run lint
        run: ruff check backend

      - name: Run backend tests
        run: pytest backend/tests -v

  frontend-tests:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: frontend

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "24"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Run frontend lint
        run: npm run lint

      - name: Run frontend tests
        run: npm run test

      - name: Build frontend
        run: npm run build
```

This workflow assumes that the corresponding scripts and dependency files exist. Adjust the commands to match the actual repository.

ML integration tests requiring large checkpoints or a GPU should run in a separate controlled workflow or environment.

---

# 23. Test Data Management

Test data must be organised and controlled.

### Recommended Structure

```text
tests/
├── fixtures/
│   ├── images/
│   ├── videos/
│   ├── audio/
│   └── json/
│
├── mock_data/
│   ├── predictions.json
│   ├── conversations.json
│   └── speech_responses.json
│
└── reports/
```

### Test Data Rules

- Use legally permitted datasets.
- Respect dataset licences.
- Avoid personal user data.
- Use synthetic data where possible.
- Keep test data separate from production data.
- Do not commit private API responses or credentials.
- Document the source of test datasets.

---

# 24. Bug Reporting and Issue Management

Every discovered issue should be documented.

### Bug Report Format

```text
Title:
Short description:

Module:
Frontend / Backend / ML / Database / API

Severity:
Critical / High / Medium / Low

Steps to Reproduce:
1.
2.
3.

Expected Result:

Actual Result:

Environment:

Logs or Screenshots:

Suggested Fix:
```

### Severity Levels

| Severity | Description |
|---|---|
| Critical | Application unusable or serious security issue |
| High | Major feature broken |
| Medium | Feature works incorrectly in some cases |
| Low | Minor visual or usability issue |

### Bug Fix Process

1. Reproduce the issue.
2. Identify the responsible module.
3. Find the root cause.
4. Implement a fix.
5. Add a regression test.
6. Run relevant tests.
7. Verify the fix.
8. Update the issue.

---

# 25. Testing Reports

Every important testing milestone should produce a report.

### Report Structure

```text
Signova AI Testing Report

Date:

Application Version:

Model Name:

Model Version:

Dataset Version:

Environment:

Hardware:

Testing Category:

Total Tests:

Passed:

Failed:

Skipped:

Metrics:

Known Issues:

Limitations:

Conclusion:
```

### ML Evaluation Report

Include:

- Dataset name and version.
- Number of test samples.
- Supported classes.
- Class distribution.
- Accuracy.
- Precision.
- Recall.
- Macro F1.
- Weighted F1.
- Confusion matrix.
- Inference latency.
- Hardware information.
- Evaluation limitations.

### Reporting Rules

- Report actual results only.
- Never invent test outcomes.
- Separate model metrics from application performance.
- Document failed tests.
- Explain limitations.
- Do not claim production readiness based only on passing unit tests.

---

# 26. Definition of Done

A feature is considered tested only when:

1. Requirements are documented.
2. Test cases are defined.
3. Positive scenarios pass.
4. Negative scenarios are tested.
5. Relevant unit tests pass.
6. Integration tests pass.
7. Error handling is verified.
8. Security requirements are reviewed.
9. Regression tests pass.
10. Actual results are documented.

### ML Feature Definition of Done

An ML feature is complete only when:

1. The model source and licence are reviewed.
2. The checkpoint loads successfully.
3. Preprocessing is verified.
4. Supported labels are verified.
5. Inference works.
6. Unknown and uncertain inputs are tested.
7. Evaluation data is documented.
8. Relevant metrics are calculated.
9. Latency is measured.
10. Model limitations are documented.

---

# 27. Testing Roadmap

| Phase | Testing Activity | Expected Result |
|---|---|---|
| Phase 0 | Test environment setup | Testing tools configured |
| Phase 1 | Model verification tests | Pretrained model validated |
| Phase 2 | ML inference tests | Prediction pipeline verified |
| Phase 3 | Backend unit and API tests | API behaviour verified |
| Phase 4 | Frontend component tests | UI behaviour verified |
| Phase 5 | Camera and WebSocket tests | Real-time communication verified |
| Phase 6 | Recognition output tests | Text construction verified |
| Phase 7 | Sarvam integration tests | Speech features verified |
| Phase 8 | Reverse communication tests | Voice workflow verified |
| Phase 9 | Database and security tests | Persistence and access verified |
| Phase 10 | E2E, performance, and deployment tests | Release readiness assessed |

Testing should begin early and continue throughout development, not only at the end.

---

# 28. Instructions for Antigravity

Before implementing tests:

1. Read `AGENTS.md`.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read `docs/FEATURES.md`.
5. Read `docs/TECH_STACK.md`.
6. Read `docs/SYSTEM_ARCHITECTURE.md`.
7. Read `docs/AI_MODEL_STRATEGY.md`.
8. Read `docs/PHASE_ROADMAP.md`.
9. Read `docs/API_DOCUMENTATION.md`.
10. Read `docs/DATABASE_SCHEMA.md`.
11. Read this `docs/TESTING_STRATEGY.md`.
12. Inspect the existing source code and test configuration.

### Development Rules

- Use Pytest for Python tests.
- Use Vitest for frontend unit tests.
- Use React Testing Library for component tests.
- Use Playwright for browser E2E tests.
- Mock external APIs during unit tests.
- Keep test data separate from production data.
- Test actual model inference separately from mocked inference.
- Do not invent model predictions or evaluation metrics.
- Do not silently skip failing tests.
- Do not weaken tests just to make the pipeline pass.
- Do not run destructive tests against production.
- Keep tests focused and reproducible.
- Update tests whenever application behaviour changes.

### Completion Report

After every testing task, provide:

- Test files created or modified.
- Features covered.
- Test commands executed.
- Actual pass and fail counts.
- Skipped tests and reasons.
- Coverage results, if measured.
- Model metrics, if evaluated.
- Known failures.
- Recommended fixes.
- Remaining testing work.

---

# 29. Final Testing Strategy

Signova AI will follow a continuous testing approach.

The recommended order is:

1. Verify the development environment.
2. Test the pretrained ISL model independently.
3. Validate image and video preprocessing.
4. Test the inference pipeline.
5. Test FastAPI endpoints.
6. Test React components.
7. Test camera integration.
8. Test WebSocket recognition.
9. Test sign-to-text output.
10. Test Sarvam AI speech features.
11. Test database operations when persistence is enabled.
12. Perform security and accessibility checks.
13. Perform end-to-end testing.
14. Measure performance on target hardware.
15. Verify deployment behaviour.

**Final Goal:** Ensure Signova AI delivers reliable, secure, and measurable ISL recognition and communication features through continuous testing, transparent evaluation, and documented quality standards.