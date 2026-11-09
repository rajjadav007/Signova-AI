# Security Development Rules

# Signova AI

These rules apply to all security-related development across the Signova AI frontend, backend, AI/ML pipeline, APIs, database, external services, and deployment environments.

The primary objective is to protect users, their data, camera access, application credentials, and AI model assets.

Security and privacy must be considered throughout development, not added only before deployment.

---

## 1. Security Principles

All development must follow these principles:

1. Privacy by default.
2. Minimum data collection.
3. Secure credential management.
4. Explicit camera and microphone permissions.
5. Secure API communication.
6. Input validation.
7. Safe AI model loading.
8. Controlled data storage.
9. Least-privilege access.
10. Secure error handling.
11. Dependency security.
12. Transparent external service usage.

### Mandatory Rules

- Never expose secrets in frontend code.
- Never commit credentials.
- Never collect unnecessary personal information.
- Never record camera footage without clear user consent.
- Never trust client-side validation alone.
- Never load untrusted model checkpoints.
- Never expose internal server errors.
- Never store sensitive data without a clear requirement.

---

## 2. Security Technology Stack

Use the following security practices with the existing project stack.

| Area | Security Requirement |
|---|---|
| Frontend | Secure React implementation |
| Backend | FastAPI validation and controlled access |
| Authentication | Secure authentication when required |
| API | HTTPS and request validation |
| Database | Restricted access and secure credentials |
| AI Models | Verified model sources and safe checkpoint loading |
| Secrets | Environment variables |
| Dependencies | Version control and vulnerability checks |
| Deployment | Secure environment configuration |
| Testing | Security and privacy tests |

Do not introduce additional security tools without a clear requirement.

---

## 3. Camera and Microphone Privacy

Camera access is a core feature of Signova AI.

The application must respect the user's control over camera and microphone access.

### Camera Rules

- Request permission only when camera functionality is needed.
- Start camera access only after an appropriate user action.
- Show a visible camera-active state.
- Provide a clear stop-camera action.
- Handle denied permissions.
- Handle unavailable cameras.
- Stop all active media tracks when the camera is stopped.
- Stop media tracks when the relevant component is unmounted.
- Do not access cameras in the background without a clear user-approved feature.

### Microphone Rules

If speech functionality requires microphone access:

- Request microphone permission explicitly.
- Explain why microphone access is needed.
- Show when microphone capture is active.
- Provide a stop-recording action.
- Stop microphone tracks when recording ends.
- Do not record audio in the background without explicit consent.

### Recording Rules

- Do not record video by default.
- Do not persist raw camera recordings by default.
- Do not upload video or audio without user consent.
- Do not send recordings to third-party services without explaining the purpose.
- Delete temporary files when they are no longer needed.
- Never use camera or microphone access for unrelated purposes.

### Important

Camera permission from the browser is not permission to store or share the user's recordings.

---

## 4. Personal Data Protection

Collect only information necessary for the requested functionality.

### Potential Data Categories

| Data | Security Requirement |
|---|---|
| Camera frames | Process for recognition, avoid persistence by default |
| Microphone input | Use only for requested speech features |
| Recognised text | Store only when required and permitted |
| User account data | Protect with authentication and access controls |
| Preferences | Store only necessary settings |
| Recognition history | Require a clear purpose and user consent |
| API credentials | Keep exclusively on the backend |

### Rules

- Do not collect unnecessary personal information.
- Avoid storing raw video and audio.
- Avoid storing biometric information unnecessarily.
- Do not expose user-specific records to other users.
- Provide clear information about data collection.
- Define retention periods for stored data.
- Delete data when no longer needed, subject to applicable legal requirements.
- Do not use personal recordings to train models without appropriate consent and permissions.

---

## 5. Environment Variables and Secret Management

All private credentials must be stored securely.

### Examples of Secrets

- Sarvam AI API key.
- Database credentials.
- Authentication secrets.
- Access tokens.
- Third-party service credentials.
- Deployment credentials.

### Mandatory Rules

- Never hardcode API keys.
- Never place private credentials in React components.
- Never expose private credentials through `VITE_` environment variables.
- Never commit `.env` files.
- Never print secrets in logs.
- Never include credentials in screenshots or public issues.
- Use hosting-provider secret management for production.
- Rotate credentials if they are exposed.

### Example `.env.example`

```env
APP_ENV=development

FRONTEND_URL=http://localhost:5173

DATABASE_URL=

SARVAM_API_KEY=

SECRET_KEY=

MODEL_PATH=
```

These are example variables only. Use the actual configuration required by the application.

### Git Protection

Ensure `.gitignore` includes:

```gitignore
.env
.env.*
!.env.example

venv/
.venv/

__pycache__/
*.pyc

node_modules/
dist/

*.log

*.pt
*.pth
*.ckpt
*.pkl
*.pickle
```

Model checkpoints should only be ignored if the repository uses external model storage or another approved approach. Do not accidentally exclude required, intentionally tracked model assets.

---

## 6. Frontend Security Rules

The React frontend must not be treated as a trusted environment.

### Rules

- Never store private API keys in frontend code.
- Never store passwords in local storage.
- Avoid storing sensitive authentication tokens in browser storage.
- Do not render untrusted HTML.
- Avoid unsafe DOM manipulation.
- Validate data received from the backend.
- Use HTTPS in production.
- Avoid exposing internal backend errors.
- Do not place secrets in URLs.
- Avoid unnecessary browser permissions.

### Cross-Site Scripting (XSS)

- Use React's normal escaping behaviour.
- Avoid `dangerouslySetInnerHTML`.
- If HTML rendering is genuinely required, use a trusted sanitisation approach.
- Never insert unsanitised user input into HTML.
- Validate content received from external services.

### Content Security

Use an appropriate Content Security Policy in production.

Restrict:

- Script sources.
- Image sources.
- API connections.
- Font sources.
- Frame sources.
- Other resource origins.

Configure the policy to match the actual application. Do not break required camera, API, or asset functionality.

---

## 7. Backend Security Rules

The FastAPI backend must validate and protect every incoming request.

### Rules

- Validate all request data.
- Use Pydantic schemas.
- Restrict request sizes.
- Validate uploaded files.
- Use controlled error responses.
- Avoid exposing stack traces.
- Restrict CORS origins.
- Apply rate limits where appropriate.
- Protect sensitive endpoints.
- Avoid trusting client-provided user identifiers.
- Use HTTPS in production.

### Input Validation

Validate:

- Data types.
- Required fields.
- File sizes.
- Image formats.
- Image dimensions.
- Text lengths.
- Query parameters.
- Request payload structure.

Do not assume that frontend validation makes backend validation unnecessary.

### Error Handling

Never return:

- Internal stack traces.
- Database credentials.
- File system paths.
- API keys.
- Authentication secrets.
- Internal model configuration.

Log useful diagnostic information securely on the backend.

---

## 8. API Security

All API communication must follow secure practices.

### API Rules

- Use HTTPS in production.
- Validate request bodies.
- Validate query parameters.
- Use appropriate HTTP methods.
- Use appropriate HTTP status codes.
- Restrict access to protected resources.
- Apply rate limits where necessary.
- Configure request timeouts.
- Reject malformed requests.
- Avoid unnecessary API permissions.

### CORS

Configure CORS using approved frontend origins.

Example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

This is a development-oriented example. Adjust the configuration to the actual authentication method and production domains.

Do not use unrestricted wildcard origins with credentials.

### Rate Limiting

Consider rate limits for:

- Recognition requests.
- Image uploads.
- Speech generation.
- Authentication endpoints.
- Other resource-intensive operations.

Use limits appropriate to the actual application workload.

Do not introduce unnecessary infrastructure just to implement rate limiting.

---

## 9. Authentication and Authorisation

Authentication should be implemented only when required by the approved product scope.

### If Authentication Is Implemented

- Use a trusted authentication approach.
- Never store plaintext passwords.
- Use an appropriate password hashing algorithm.
- Validate tokens on protected endpoints.
- Apply appropriate token expiration.
- Protect user-specific resources.
- Enforce ownership checks.
- Use secure cookie settings when cookie-based authentication is used.
- Implement logout and token invalidation appropriately.

### Authorisation Rules

- Do not trust user IDs supplied by the frontend.
- Verify access to every user-specific resource.
- Prevent users from accessing another user's history or preferences.
- Apply least-privilege access.
- Do not expose administrative functions to normal users.

Do not introduce authentication solely for appearance or architectural complexity.

---

## 10. Database Security

PostgreSQL is optional and should only be introduced when persistent storage is needed.

### Database Rules

- Store credentials in environment variables.
- Restrict database network access.
- Use separate development and production databases.
- Validate database input.
- Use parameterised queries or safe ORM operations.
- Avoid dynamically constructed SQL from untrusted input.
- Use database transactions where appropriate.
- Apply least-privilege database permissions.
- Keep database migrations controlled.
- Back up important production data securely.

### Sensitive Data

- Do not store raw camera recordings by default.
- Do not store unnecessary biometric information.
- Avoid storing unnecessary recognition history.
- Protect user-specific records.
- Apply retention and deletion policies.

### Database Error Handling

Never expose:

- SQL queries containing sensitive values.
- Database connection strings.
- Database passwords.
- Internal schema details that should remain private.
- Raw database stack traces.

---

## 11. AI Model and Checkpoint Security

AI model integration introduces additional security risks.

### Model Source Verification

Before downloading a model:

1. Verify the original repository.
2. Check the model owner.
3. Check the model licence.
4. Inspect the model files.
5. Check available checkpoint formats.
6. Review model-loading code.
7. Check dependencies.
8. Verify that the model supports ISL.
9. Avoid executing unknown scripts.
10. Document the source.

### Checkpoint Security

- Prefer Safetensors where supported.
- Avoid untrusted pickle-based checkpoints.
- Use `torch.load(..., weights_only=True)` when compatible with the checkpoint and PyTorch version.
- Verify checkpoint compatibility.
- Avoid arbitrary checkpoint downloads at runtime.
- Do not execute checkpoint contents as code.
- Keep model paths configurable.
- Restrict write access to model directories.

### Model Integrity

Where possible:

- Record the model source.
- Record the model version.
- Record the checkpoint hash.
- Verify the checkpoint before loading.
- Keep model metadata documented.

Never claim a checkpoint is safe simply because it is hosted on GitHub or Hugging Face.

---

## 12. AI Prediction and User Safety

Recognition results must be presented responsibly.

### Rules

- Do not invent predictions.
- Do not invent confidence scores.
- Do not present uncertain predictions as confirmed.
- Do not hide recognition failures.
- Do not claim complete ISL interpretation when only limited signs are supported.
- Handle unsupported signs explicitly.
- Document known model limitations.

### Accessibility Considerations

- Make uncertainty understandable.
- Avoid misleading users with incorrect output.
- Do not imply that the application replaces a qualified human interpreter.
- Do not claim universal accuracy.
- Explain the supported sign vocabulary where appropriate.

---

## 13. External Service Security

Signova AI may use external services such as Sarvam AI for supported speech and language functionality.

### Rules

- Use official provider documentation.
- Keep API credentials on the backend.
- Verify supported endpoints.
- Verify request and response formats.
- Use network timeouts.
- Handle provider errors.
- Check pricing and usage limits.
- Avoid sending unnecessary user data.
- Use only the data required for the requested service.
- Review provider data retention and privacy policies.

### Important

Do not send camera footage, audio, or personal information to external services unless the feature genuinely requires it and the user has been informed.

Sarvam AI must not be treated as the ISL gesture recognition model unless a verified service explicitly supports that task.

---

## 14. File Upload Security

If image or video uploads are supported:

- Validate file type.
- Validate actual file contents.
- Restrict file size.
- Restrict image dimensions.
- Use safe temporary storage.
- Generate safe filenames.
- Avoid trusting original filenames.
- Prevent path traversal.
- Reject corrupted files.
- Remove temporary files after processing.
- Avoid permanent storage unless required.

Never execute uploaded files.

Never trust a file merely because its extension is `.jpg`, `.png`, or `.mp4`.

---

## 15. WebSocket Security

If real-time recognition uses WebSockets:

- Validate connection origins.
- Authenticate connections when required.
- Validate incoming messages.
- Limit message size.
- Limit connection rates.
- Handle disconnects safely.
- Prevent unbounded queues.
- Avoid logging sensitive frame data.
- Close connections properly.
- Prevent unauthorised access to user-specific sessions.

Do not introduce WebSockets unless they are required by the actual recognition workflow.

---

## 16. Dependency and Supply Chain Security

Third-party dependencies can introduce vulnerabilities.

### Rules

- Install packages from trusted sources.
- Check package maintenance.
- Review package licences.
- Avoid unnecessary dependencies.
- Keep lockfiles committed.
- Review dependency updates.
- Remove unused packages.
- Avoid installing unknown GitHub scripts directly.
- Check for known vulnerabilities.

### Frontend

Use the existing npm lockfile and inspect dependencies before upgrading.

### Backend

Use the project's existing Python dependency management approach.

Do not upgrade major versions without checking compatibility with FastAPI, PyTorch, OpenCV, and the selected model.

---

## 17. Logging and Monitoring Security

Logs must support debugging without exposing sensitive information.

### Safe Events to Log

- Application startup and shutdown.
- API request completion.
- Model loading status.
- Recognition processing status.
- External provider failures.
- Authentication failures.
- Unexpected server errors.

### Never Log

- API keys.
- Passwords.
- Access tokens.
- Session secrets.
- Raw camera frames.
- Private audio recordings.
- Full sensitive request payloads.
- Database credentials.

Use appropriate log levels.

Avoid verbose debug logging in production.

---

## 18. Deployment Security

Before production deployment, verify:

- HTTPS is enabled.
- Environment variables are configured.
- Debug mode is disabled.
- CORS uses approved origins.
- API secrets are not exposed.
- Database access is restricted.
- Model files come from verified sources.
- Upload limits are configured.
- Request timeouts are configured.
- Logs do not contain secrets.
- Dependencies are reviewed.
- Health checks do not expose sensitive information.

### Hosting Rules

- Never assume a hosting provider offers GPU support.
- Do not expose private storage.
- Do not store credentials in deployment configuration files committed to Git.
- Verify model storage persistence.
- Check service access controls.
- Review hosting costs and usage limits.

Follow `docs/DEPLOYMENT.md`.

---

## 19. Git and Repository Security

Keep the repository free from secrets and sensitive files.

### Never Commit

- `.env` files.
- API keys.
- Passwords.
- Private tokens.
- Database dumps containing personal information.
- Raw user recordings.
- Private datasets.
- Unapproved model checkpoints.
- Private certificates.
- Deployment credentials.

### Git Rules

- Review staged files before committing.
- Use `.gitignore`.
- Check commit history for accidental secrets.
- Do not force-push without approval.
- Do not rewrite shared Git history without approval.
- Rotate exposed credentials immediately.

Example:

```bash
git status
git diff
git diff --cached
```

If a secret is committed, removing it from the latest file is not enough. Revoke or rotate the exposed credential and follow the repository's incident response process.

---

## 20. Security Testing

Security requirements must be tested.

### Frontend Security

- Untrusted input rendering.
- Camera permission handling.
- Microphone permission handling.
- Secret exposure checks.
- Authentication state handling, if implemented.
- Secure production configuration.

### Backend Security

- Invalid request validation.
- Oversized upload rejection.
- Unsupported file rejection.
- CORS configuration.
- Authentication checks, if implemented.
- Authorisation checks, if implemented.
- Rate limiting, if implemented.
- Safe error responses.

### AI Security

- Untrusted checkpoint rejection.
- Missing model handling.
- Invalid model input handling.
- Checkpoint compatibility.
- Temporary file cleanup.

### Database Security

- Access control.
- Credential handling.
- User data isolation.
- Safe query handling.
- Migration safety.

Do not claim a security test passed unless it was executed.

---

## 21. Security Incident Handling

If a security issue is discovered:

1. Stop the affected operation if necessary.
2. Identify the affected component.
3. Determine what data or credentials may be exposed.
4. Revoke or rotate compromised credentials.
5. Restrict affected access.
6. Preserve relevant safe diagnostic logs.
7. Fix the underlying vulnerability.
8. Add regression tests.
9. Update relevant documentation.
10. Report the actual impact and resolution.

Do not hide or misrepresent security incidents.

Do not publish exposed credentials in issue reports or pull requests.

---

## 22. AI Agent Security Rules

When working as Antigravity or another coding agent:

- Read the root `AGENTS.md`.
- Read `docs/SECURITY.md`.
- Inspect existing security controls before changing them.
- Never print environment variable values containing secrets.
- Never expose credentials in frontend code.
- Never disable validation to make a feature work.
- Never weaken CORS or authentication without approval.
- Never remove security checks without approval.
- Never download and execute unknown scripts.
- Never load untrusted model checkpoints.
- Never collect camera or microphone data without the required permission.
- Never store raw recordings by default.
- Never mark security checks as passed without testing.

If a security requirement conflicts with a requested feature, explain the risk and propose a safer implementation.

---

## 23. Security Definition of Done

A security-related task is complete only when:

- [ ] The security requirement is understood.
- [ ] Existing controls have been inspected.
- [ ] The implementation follows least-privilege principles.
- [ ] User data is protected.
- [ ] Secrets are not exposed.
- [ ] Camera and microphone permissions are respected.
- [ ] Inputs are validated.
- [ ] Errors do not reveal sensitive information.
- [ ] Relevant security tests are executed.
- [ ] Documentation is updated.
- [ ] Remaining risks are documented.

---

## 24. Final Security Principle

Signova AI must protect users while providing accessible sign language recognition.

Prioritise:

1. User privacy.
2. Camera and microphone control.
3. Secure API communication.
4. Safe AI model integration.
5. Credential protection.
6. Secure data handling.
7. Responsible prediction output.
8. Reliable deployment.

**Security must never be sacrificed to make a feature appear functional. Build Signova AI with privacy, transparency, and user trust as core requirements.**