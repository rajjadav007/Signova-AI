# Security Policy and Guidelines

**Project:** Signova AI  
**Document:** Security Guidelines  
**File:** `docs/SECURITY.md`  
**Status:** Development Guidelines  
**Version:** 1.0

---

## 1. Purpose

This document defines the security requirements and development practices for Signova AI.

Signova AI processes camera input, hand gestures, sign-language recognition results, and optional speech input and output. Security and privacy must be considered throughout the application.

The objectives are to:

- Protect user information and application data.
- Secure camera and microphone access.
- Prevent unauthorised access to APIs and user accounts.
- Protect AI models, checkpoints, and dependencies.
- Secure communication between frontend and backend.
- Protect database credentials and external API keys.
- Reduce risks during development and deployment.

Security must be implemented gradually according to the project's development phase.

## 2. Security Principles

Follow these principles throughout development:

| Principle | Requirement |
|---|---|
| Privacy first | Collect only the data required for application functionality. |
| User consent | Request permission before accessing camera or microphone. |
| Least privilege | Give users and services only the access they need. |
| Secure by default | Keep sensitive features disabled until explicitly enabled. |
| Data minimisation | Avoid unnecessary storage of personal information. |
| Secure communication | Use HTTPS and secure WebSocket connections in production. |
| Input validation | Validate all incoming API and user inputs. |
| Secret protection | Never expose private credentials in frontend code. |
| Transparency | Explain how camera, microphone, and external AI services are used. |

## 3. Security Scope

The following application components are covered:

1. React frontend.
2. Python FastAPI backend.
3. AI and machine learning inference pipeline.
4. Camera and microphone processing.
5. WebSocket communication.
6. PostgreSQL database, if enabled.
7. Sarvam AI integration.
8. Authentication and user management, if enabled.
9. Deployment infrastructure.
10. Third-party packages and pretrained models.

## 4. Threat Model

The application must consider the following potential security threats.

| Threat | Possible Impact | Required Protection |
|---|---|---|
| Unauthorised API access | Exposure or misuse of application functionality | Authentication and authorisation where required |
| API key exposure | Misuse of external AI services | Server-side secret management |
| Malicious file upload | Server-side attacks or resource exhaustion | File validation and upload limits |
| Unauthorised camera access | Privacy violation | Explicit browser permission |
| Unauthorised microphone access | Privacy violation | Explicit browser permission |
| WebSocket abuse | Resource exhaustion or unauthorised access | Authentication, validation, and rate limits |
| SQL injection | Unauthorised database operations | Parameterised queries and ORM |
| Cross-site scripting | Malicious browser-side code execution | Safe rendering and input handling |
| Model file compromise | Arbitrary code execution or incorrect inference | Trusted model sources and file verification |
| Dependency vulnerability | Application compromise | Dependency scanning and updates |
| Data leakage | Exposure of personal information | Data minimisation and access control |
| Denial of service | Application becomes unavailable | Request limits and resource controls |

This threat model is a starting point. Update it when new features or external integrations are introduced.

## 5. Data Classification

Classify application data before deciding how it should be stored or processed.

| Data Type | Classification | Handling |
|---|---|---|
| Camera frames | Sensitive | Process temporarily, do not store by default |
| Microphone recordings | Sensitive | Process temporarily, do not store by default |
| Recognised sign text | User data | Store only when necessary and with appropriate consent |
| Conversation history | User data | Restrict access to the account owner |
| Email address | Personal information | Store securely when authentication requires it |
| Password hash | Highly sensitive | Use a secure password hashing algorithm |
| API credentials | Secret | Store only in backend environment variables or secret manager |
| Model checkpoints | Application assets | Verify their origin and integrity |
| Application logs | Operational data | Avoid personal content and secrets |

### 5.1 Data Minimisation

- Collect only the information needed for the requested feature.
- Do not collect personal information for analytics without a clear purpose.
- Do not store raw camera frames or audio recordings by default.
- Avoid collecting location information unless a feature genuinely requires it.
- Do not store unnecessary device information.
- Do not expose private information through API responses.

## 6. Camera and Microphone Privacy

Camera and microphone access are important parts of Signova AI.

These features must remain under the user's control.

### 6.1 Permission Handling

- Request camera permission only when the user starts the sign recognition feature.
- Request microphone permission only when the user starts a speech feature.
- Explain why permission is required.
- Handle permission denial gracefully.
- Never attempt to bypass browser permission controls.
- Show a clear camera or microphone active state.
- Provide an option to stop the camera or microphone immediately.

### 6.2 Camera Security

Implementation requirements:

- Use the browser MediaDevices API.
- Use HTTPS in production because browser camera access requires a secure context.
- Request only the required video stream.
- Stop all active media tracks when the user stops recognition or leaves the relevant page.
- Release camera resources when components unmount.
- Avoid recording or saving video unless a separate feature explicitly requires it.
- Do not send camera frames to external services unless the feature requires it and the user has been informed.

Example:

```javascript
const stream = await navigator.mediaDevices.getUserMedia({
  video: true,
  audio: false,
});

// Stop camera when recognition ends.
stream.getTracks().forEach((track) => track.stop());
```

### 6.3 Microphone Security

- Request microphone access only when needed.
- Explain whether audio is processed locally or sent to an external service.
- Stop microphone tracks after processing.
- Avoid retaining audio recordings by default.
- Do not send audio to Sarvam AI without user action and appropriate disclosure.
- Handle microphone permission errors safely.

### 6.4 Media Retention

Default policy:

| Media | Default Storage |
|---|---|
| Camera frames | Not stored |
| Live camera stream | Not stored |
| Microphone audio | Not stored |
| Temporary processing frames | Deleted after processing |
| Temporary audio files | Deleted after processing |
| Recognised text | Stored only if required and enabled |

If media storage is introduced in the future, implement explicit consent, access controls, retention periods, and deletion functionality.

## 7. API Security

The backend uses FastAPI to handle application requests and AI inference.

Every API endpoint must validate incoming data.

### 7.1 Input Validation

- Use Pydantic schemas for request validation.
- Validate required fields and data types.
- Apply maximum request sizes.
- Reject unexpected or malformed input.
- Validate image, video, and audio inputs before processing.
- Avoid trusting frontend validation alone.

Example:

```python
from pydantic import BaseModel, Field

class RecognitionRequest(BaseModel):
    model_name: str = Field(min_length=1, max_length=100)
    confidence_threshold: float = Field(
        ge=0.0,
        le=1.0
    )
```

### 7.2 Authentication

If authentication is implemented:

- Use a trusted authentication provider or a secure backend authentication system.
- Never store plaintext passwords.
- Use Argon2id or another appropriately configured password hashing algorithm.
- Use secure session handling.
- Set cookies to `HttpOnly`, `Secure`, and an appropriate `SameSite` value when cookie-based sessions are used.
- Validate authentication tokens on protected endpoints.
- Apply token expiry and revocation where supported.
- Never expose access tokens in URLs.

Authentication should be introduced only when account-based features require it.

### 7.3 Authorisation

Authentication confirms who the user is. Authorisation determines what the user can access.

Requirements:

- Users must access only their own private data.
- Verify ownership before reading, modifying, or deleting records.
- Do not rely on frontend route protection alone.
- Protect administrative endpoints separately.
- Use role-based access only when the application genuinely requires different roles.

### 7.4 Rate Limiting

Protect expensive endpoints against abuse.

Apply reasonable limits to:

- AI inference requests.
- Image and video uploads.
- Audio processing.
- Authentication attempts.
- WebSocket connections.
- External AI provider requests.

Use configurable limits based on endpoint cost and deployment capacity.

Return HTTP `429 Too Many Requests` when appropriate.

For a multi-instance deployment, use a shared rate-limit store if required. Do not introduce Redis into the MVP unless the deployment architecture needs it.

### 7.5 Error Handling

- Return clear and safe error messages.
- Do not expose stack traces in production.
- Do not return database connection details.
- Do not reveal internal filesystem paths.
- Do not expose API credentials or access tokens.
- Log technical details securely on the backend.

## 8. File Upload Security

Signova AI may process images, video, or audio files.

All uploaded files must be treated as untrusted input.

### 8.1 Validation Requirements

Validate:

- Allowed file formats.
- Actual file content, not only the filename extension.
- MIME type and file signature where applicable.
- Maximum file size.
- Image and video dimensions.
- Audio duration.
- Decoding success.
- Number of frames or processing duration.

### 8.2 Safe File Processing

- Generate server-side temporary filenames.
- Never use user-provided filenames as filesystem paths.
- Prevent path traversal attacks.
- Store temporary files outside publicly accessible directories.
- Restrict file permissions.
- Delete temporary files after processing.
- Do not execute uploaded files.
- Apply processing timeouts.
- Avoid loading extremely large files entirely into memory.

### 8.3 Upload Limits

Define configurable limits for:

- Maximum image size.
- Maximum video size.
- Maximum audio size.
- Maximum video duration.
- Maximum image dimensions.
- Maximum number of frames.

These limits must be based on the actual model and hosting capacity.

Do not advertise unsupported upload sizes in the frontend.

## 9. WebSocket Security

WebSockets may be used for real-time sign recognition.

Secure the connection before accepting incoming data.

Requirements:

- Use `wss://` in production.
- Validate the connection origin.
- Authenticate connections when accessing protected functionality.
- Apply connection and message rate limits.
- Limit incoming message sizes.
- Validate every received message.
- Apply idle connection timeouts.
- Limit simultaneous connections where necessary.
- Close invalid or unauthorised connections.
- Release resources when a connection closes.
- Avoid logging raw video frames or audio content.

Example endpoint:

```text
wss://api.example.com/api/v1/ai/predict/stream
```

The example domain is illustrative. Use the actual deployed backend URL.

## 10. AI Model and Checkpoint Security

Pretrained models are a core part of Signova AI.

Model files and external repositories must be treated as untrusted until verified.

### 10.1 Trusted Sources

Prefer:

- Official GitHub repositories.
- Official Hugging Face model pages.
- Maintainer-provided releases.
- Models with clear documentation and licensing.

Before integrating a model, verify:

1. Repository ownership and source.
2. Model architecture.
3. Checkpoint origin.
4. Input dimensions and preprocessing.
5. Output labels and class mapping.
6. Dataset information.
7. Model licence.
8. Dependency requirements.
9. Inference compatibility.
10. Hardware and memory requirements.

### 10.2 Checkpoint Safety

- Never load untrusted PyTorch pickle checkpoints.
- Prefer `safetensors` when supported.
- When using PyTorch checkpoints, prefer safe loading options such as `weights_only=True` where compatible.
- Verify model file hashes when the publisher provides trusted checksums.
- Store checkpoints in controlled directories.
- Do not allow users to upload model files for automatic execution.
- Do not execute scripts from an unknown model repository without inspection.

Example:

```python
import torch

checkpoint = torch.load(
    "model_weights.pt",
    map_location="cpu",
    weights_only=True
)
```

This example is suitable only for compatible checkpoint formats. Verify the expected checkpoint structure before loading.

### 10.3 Model Inference Safety

- Validate model input shapes.
- Validate input data types.
- Reject invalid or excessively large inputs.
- Handle model loading failures safely.
- Set inference timeouts where practical.
- Prevent unlimited concurrent inference jobs.
- Avoid exposing internal model filesystem paths.
- Handle low-confidence and unknown predictions instead of presenting unreliable results as certain.

### 10.4 Model Licence

Before using a pretrained model:

- Review its licence.
- Check whether commercial or public deployment is permitted.
- Follow attribution requirements.
- Review dataset usage restrictions.
- Document the model source and licence in `docs/AI_MODEL_STRATEGY.md`.

Do not assume that a publicly available model is free for every type of use.

## 11. Sarvam AI Integration Security

Sarvam AI may be used for supported speech and language features.

The integration must protect user data and API credentials.

### 11.1 API Key Protection

- Store Sarvam API keys on the backend.
- Never place API keys in frontend source code.
- Never expose API keys through React environment variables.
- Never commit API keys to GitHub.
- Use environment variables or a secure secret manager.
- Rotate exposed or compromised keys.
- Restrict access to production credentials.

Example backend environment variable:

```env
SARVAM_API_KEY=your_private_api_key
```

The value above is a placeholder. Never commit actual credentials.

### 11.2 External Data Processing

Before sending audio or text to an external provider:

- Explain what information will be sent.
- Explain the purpose of processing.
- Obtain appropriate user consent.
- Send only the data needed for the requested operation.
- Avoid sending unnecessary personal information.
- Review the provider's current privacy and retention policies.

Do not claim that external processing is private, temporary, or automatically deleted unless the provider's documented terms support that claim.

### 11.3 Failure Handling

- Handle provider timeouts.
- Handle authentication failures.
- Handle rate-limit responses.
- Avoid exposing provider credentials in error messages.
- Do not retry requests indefinitely.
- Provide a clear message when a speech feature is temporarily unavailable.

## 12. Frontend Security

The frontend uses React and JavaScript.

Follow these practices:

### 12.1 XSS Protection

- Avoid rendering untrusted HTML.
- Do not use `dangerouslySetInnerHTML` with untrusted content.
- Render user-provided text as normal React text.
- Sanitize content if HTML rendering is genuinely required.
- Avoid unsafe URL handling.

### 12.2 Environment Variables

Vite exposes variables prefixed with `VITE_` to frontend code.

Never place private credentials in frontend environment variables.

Safe example:

```env
VITE_API_BASE_URL=https://api.example.com
```

Unsafe example:

```env
VITE_SARVAM_API_KEY=private-secret-key
```

The frontend should communicate with the backend, and the backend should communicate with Sarvam AI.

### 12.3 HTTPS

- Use HTTPS in production.
- Do not send authentication tokens through insecure connections.
- Use secure WebSocket connections in production.
- Redirect HTTP traffic to HTTPS where supported.

### 12.4 Content Security Policy

Configure a Content Security Policy (CSP) at the deployment layer.

Start with a policy that restricts:

- Script sources.
- Style sources.
- Image sources.
- Connection sources.
- Object sources.
- Frame sources.

Allow only the external services and resources required by the application.

Test the policy against the actual frontend before enforcing it.

### 12.5 Browser Permissions

- Request permissions only when needed.
- Handle denied permissions.
- Stop camera and microphone tracks after use.
- Avoid unexpected permission prompts.
- Keep the user informed about active media access.

## 13. CORS and CSRF Protection

### 13.1 CORS

Configure FastAPI CORS with explicitly allowed frontend origins.

Example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],
    allow_headers=[
        "Authorization",
        "Content-Type"
    ],
)
```

This is a development example.

In production:

- Replace localhost with the actual frontend origin.
- Do not use wildcard origins with credentials.
- Allow only the methods and headers required.
- Review WebSocket origin validation separately.

### 13.2 CSRF

If authentication uses cookies:

- Apply CSRF protection to state-changing requests.
- Configure suitable `SameSite` cookie settings.
- Validate request origins where appropriate.
- Use CSRF tokens when required by the authentication architecture.

If bearer tokens are used instead, assess the associated storage and XSS risks.

## 14. Database Security

If PostgreSQL is enabled, follow these rules.

### 14.1 Database Access

- Use a dedicated application database account.
- Do not use PostgreSQL superuser credentials in the application.
- Restrict database network access.
- Apply least-privilege permissions.
- Use parameterised queries or SQLAlchemy ORM.
- Keep database credentials outside source code.

### 14.2 Database Credentials

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/signova_db
```

Use placeholders in `.env.example`.

Never commit a real production database URL.

### 14.3 Data Protection

- Restrict access to conversation history.
- Store password hashes, never plaintext passwords.
- Protect personal information.
- Use encrypted connections to remote databases.
- Enable encryption at rest through the hosting provider where available.
- Define retention and deletion policies.
- Avoid storing raw camera and microphone data by default.

### 14.4 Backups

- Create regular database backups when persistent data is used.
- Restrict backup access.
- Protect backup files with encryption.
- Test database restoration.
- Do not store backups in public directories.
- Define a reasonable backup retention period.

### 14.5 Data Deletion

If users can create accounts or save conversation history:

- Provide a way to delete their stored information.
- Verify ownership before deletion.
- Delete associated records according to the retention policy.
- Document any backups or external records that cannot be deleted immediately.
- Avoid retaining deleted data longer than necessary.

## 15. Logging and Monitoring

Logs help diagnose issues, but must not expose private information.

### 15.1 Safe Logging

Log:

- Request identifiers.
- API endpoint names.
- Response status codes.
- Processing duration.
- Model version.
- Non-sensitive application errors.
- System health information.

Do not log:

- API keys.
- Passwords.
- Authentication tokens.
- Raw audio recordings.
- Raw video frames.
- Full private conversation content.
- Database credentials.
- Sensitive personal information.

### 15.2 Monitoring

Monitor:

- Backend availability.
- API error rates.
- Inference failures.
- Memory usage.
- CPU and GPU usage.
- Request volume.
- External provider failures.
- WebSocket connection failures.

Monitoring must not become a reason to collect unnecessary user data.

## 16. Dependency and Package Security

The project uses JavaScript and Python dependencies.

### 16.1 JavaScript

- Review dependencies before installation.
- Prefer actively maintained packages.
- Avoid unnecessary dependencies.
- Review package permissions and install scripts.
- Keep `package-lock.json` committed.
- Run dependency audits regularly.

Useful command:

```bash
npm audit
```

Review reported vulnerabilities before applying automatic fixes.

### 16.2 Python

- Keep `requirements.txt` updated.
- Pin or constrain dependency versions appropriately.
- Avoid installing packages from unknown sources.
- Review package maintainers and release history.
- Scan dependencies for known vulnerabilities.

Useful command:

```bash
pip install pip-audit
pip-audit
```

### 16.3 Dependency Updates

- Update vulnerable dependencies.
- Test updates before merging.
- Avoid blindly upgrading all packages during hackathon development.
- Remove unused packages.
- Document important dependency changes.

## 17. Environment and Secret Management

Maintain separate environments for development and production.

Recommended files:

```text
signova-ai/
├── .env
├── .env.example
├── .gitignore
├── frontend/
└── backend/
```

### 17.1 `.gitignore`

Ensure sensitive files are excluded:

```gitignore
# Environment files
.env
.env.*
!.env.example

# Python
__pycache__/
*.pyc
.venv/
venv/

# Node
node_modules/
dist/

# Model checkpoints
*.pt
*.pth
*.ckpt
*.pkl

# Temporary uploads
uploads/
temp/
tmp/

# Logs
*.log

# IDE and system files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Important:

- Add model files to Git only when their size and licence permit it.
- Do not ignore a model checkpoint if the project intentionally uses Git LFS or another approved model-storage process.
- Verify `.gitignore` before the first commit.
- If a secret is committed accidentally, revoke or rotate it immediately. Removing it from the latest commit does not guarantee that it is gone from Git history.

### 17.2 Environment Variables

Keep separate credentials for:

- Local development.
- Testing.
- Production.

Never reuse a public demo credential as a production secret.

## 18. Deployment Security

Before deploying Signova AI:

### 18.1 Frontend

- Enable HTTPS.
- Configure a suitable CSP.
- Keep private keys out of frontend builds.
- Remove development-only debugging output.
- Configure production API URLs.
- Review third-party scripts and dependencies.

### 18.2 Backend

- Disable debug mode.
- Restrict CORS.
- Protect API credentials.
- Configure request limits.
- Validate uploads.
- Use secure database connections.
- Configure health checks.
- Restrict access to administrative endpoints.

### 18.3 Hosting

Before selecting a hosting provider, verify:

- Python version support.
- Available RAM and CPU.
- GPU availability if required.
- Model checkpoint size limits.
- Request timeouts.
- WebSocket support.
- Temporary storage limits.
- Persistent storage availability.
- Deployment and bandwidth costs.

Do not assume that a frontend hosting provider can run the Python ML backend.

### 18.4 Production Configuration

Example backend configuration:

```env
APP_ENV=production
DEBUG=false
DATABASE_URL=your_secure_database_url
SARVAM_API_KEY=your_private_api_key
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

All values are examples. Use the hosting provider's secret management system for production credentials.

## 19. CI/CD Security

Automated workflows must not expose credentials.

Requirements:

- Store CI secrets in GitHub Actions secrets.
- Never print secrets in workflow logs.
- Restrict workflow permissions.
- Pin third-party GitHub Actions to trusted versions or commit SHAs where practical.
- Run automated tests before deployment.
- Run dependency security checks.
- Protect production deployment credentials.
- Require review before sensitive production changes.

Suggested CI security checks:

```text
1. Python dependency audit
2. JavaScript dependency audit
3. Python linting
4. Frontend linting
5. Backend unit tests
6. Frontend tests
7. Production build
8. Secret scanning
```

Do not deploy automatically when critical security checks fail.

## 20. Privacy and External Services

Signova AI may interact with external services such as Sarvam AI.

The application must clearly explain:

- Which features use external services.
- What data is sent.
- Why the data is sent.
- Whether the feature can work without external processing.
- Where users can disable optional processing.
- Any relevant third-party privacy and retention terms.

Do not make unsupported claims about regulatory compliance, data residency, encryption, or provider retention.

## 21. Security Testing Strategy

Security testing should be included throughout development.

| Test Area | What to Verify |
|---|---|
| Authentication | Invalid credentials and expired tokens are rejected |
| Authorisation | Users cannot access another user's records |
| API validation | Invalid inputs are rejected |
| File uploads | Unsupported and oversized files are rejected |
| Camera | Permission denial and camera cleanup work |
| Microphone | Permission denial and microphone cleanup work |
| WebSocket | Invalid connections and oversized messages are rejected |
| Database | Queries are parameterised |
| Secrets | Credentials are absent from frontend builds and Git |
| XSS | Untrusted content cannot execute as HTML or JavaScript |
| CORS | Unauthorised origins are rejected |
| Rate limiting | Excessive requests are limited |
| Model security | Untrusted checkpoint loading is prevented |
| Logging | Private media and credentials are not recorded |

### 21.1 Manual Security Checklist

Before a release, verify:

- [ ] No private API key exists in frontend code.
- [ ] No real credentials are committed to GitHub.
- [ ] HTTPS is enabled in production.
- [ ] Camera permission is requested only when needed.
- [ ] Microphone permission is requested only when needed.
- [ ] Media streams stop correctly.
- [ ] Raw media is not stored by default.
- [ ] Uploaded files are validated.
- [ ] API request limits are configured.
- [ ] CORS uses approved origins.
- [ ] WebSocket messages are validated.
- [ ] Database access is restricted.
- [ ] User records have ownership checks.
- [ ] Model sources and licences are reviewed.
- [ ] Untrusted pickle checkpoints are not loaded.
- [ ] Logs do not contain private data.
- [ ] Dependencies have been reviewed.
- [ ] Production debug mode is disabled.

## 22. Security Incident Response

If a security issue is discovered, follow this process.

### Step 1: Identify

- Record what happened.
- Identify affected services and data.
- Determine whether credentials or personal information were exposed.

### Step 2: Contain

- Disable affected endpoints if necessary.
- Revoke compromised credentials.
- Restrict access to affected systems.
- Stop unsafe processing jobs.

### Step 3: Investigate

- Review application logs.
- Identify the cause.
- Determine the impact.
- Check whether user information was affected.

### Step 4: Fix

- Apply the required security patch.
- Update vulnerable dependencies.
- Rotate compromised secrets.
- Add tests to prevent recurrence.

### Step 5: Recover

- Restore services safely.
- Verify application functionality.
- Check system health.
- Monitor for repeated activity.

### Step 6: Document

Record:

- Incident date.
- Affected components.
- Root cause.
- Impact.
- Corrective action.
- Preventive measures.

If user data or credentials may have been exposed, follow the applicable notification and response requirements.

## 23. Development Security Rules for Antigravity

Antigravity and AI coding agents must follow these rules when working on Signova AI.

### General Rules

1. Read `AGENTS.md` before implementing a feature.
2. Read the relevant documentation in `docs/`.
3. Inspect existing code before modifying it.
4. Do not introduce unnecessary security dependencies.
5. Do not hardcode credentials or private configuration.
6. Do not expose backend secrets to frontend code.
7. Validate all external inputs.
8. Follow existing authentication and authorisation patterns.
9. Use secure error handling.
10. Do not store raw camera or microphone media by default.

### Backend Rules

- Use Pydantic validation.
- Use parameterised database queries.
- Protect private endpoints.
- Validate uploaded media.
- Apply request and processing limits.
- Handle errors without exposing internal details.
- Verify model checkpoint sources.
- Keep external API credentials on the backend.

### Frontend Rules

- Use browser permission controls for camera and microphone.
- Stop media tracks after use.
- Do not store private credentials in Vite variables.
- Avoid unsafe HTML rendering.
- Show clear permission and privacy messages.
- Handle API errors safely.

### AI Model Rules

- Do not download unknown checkpoints blindly.
- Review model repositories and licences.
- Prefer safe model formats.
- Do not execute untrusted repository scripts.
- Validate model inputs and outputs.
- Do not present low-confidence predictions as certain results.

### Required Completion Report

After implementing a security-related task, Antigravity must report:

1. Files created or modified.
2. Security measures implemented.
3. Tests executed.
4. Actual test results.
5. Known security limitations.
6. Remaining security risks.
7. Documentation updated.

Never claim that a security feature is complete unless it has been implemented and tested.

## 24. Security Implementation Roadmap

Security should be implemented in phases rather than delaying the MVP with unnecessary complexity.

| Phase | Security Work |
|---|---|
| Project foundation | `.gitignore`, `.env.example`, secret protection |
| AI model integration | Trusted model sources, checkpoint validation |
| Backend development | Input validation, safe error handling |
| Frontend development | Camera and microphone consent, media cleanup |
| API integration | CORS, API validation, request limits |
| Real-time recognition | WebSocket validation, connection limits |
| Speech integration | Server-side Sarvam credentials, provider privacy disclosure |
| Database integration | Access control, ownership checks, secure credentials |
| Authentication | Password hashing or trusted authentication provider |
| Deployment | HTTPS, production secrets, debug disabled |
| Final testing | Security checks, dependency audits, incident readiness |

## 25. MVP Security Requirements

The following requirements are mandatory for the initial prototype:

- [ ] Protect API keys and environment variables.
- [ ] Keep Sarvam credentials on the backend.
- [ ] Use HTTPS in production.
- [ ] Request camera and microphone permission only when needed.
- [ ] Stop media tracks after use.
- [ ] Avoid storing raw video and audio by default.
- [ ] Validate API requests.
- [ ] Validate uploaded media.
- [ ] Apply basic request limits.
- [ ] Configure appropriate CORS origins.
- [ ] Verify pretrained model sources.
- [ ] Avoid unsafe checkpoint loading.
- [ ] Prevent sensitive information from appearing in logs.
- [ ] Handle errors safely.

Advanced authentication, account management, audit logging, and database security should be implemented when those features are introduced.

## 26. Final Security Policy

Security and privacy are continuous responsibilities in Signova AI.

Every new feature must be reviewed for:

1. Data collection.
2. User permission.
3. External service usage.
4. API security.
5. Storage requirements.
6. Access control.
7. Error handling.
8. Testing requirements.

The project must prioritise user privacy, secure AI model integration, and safe handling of camera and microphone data.

**Important:** This document defines development requirements. It does not certify Signova AI as secure, compliant, or independently audited. Security claims must be based on implemented controls and verified testing.