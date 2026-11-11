# Security Development Rules

## Signova AI

**Project:** Signova AI  
**Security Scope:** Frontend, Backend, AI/ML, Data, and Deployment  
**Backend:** Python + FastAPI  
**Frontend:** React + JavaScript + Vite  
**AI Framework:** PyTorch

---

# 1. Core Security Principles

All development must follow these principles:

1. Protect user privacy.
2. Never expose secrets or credentials.
3. Validate all external input.
4. Use secure file handling.
5. Protect camera and media data.
6. Restrict API access appropriately.
7. Keep dependencies updated.
8. Avoid unnecessary data collection.
9. Handle errors without exposing internal details.
10. Never compromise security for convenience.

---

# 2. User Privacy and Camera Security

Camera access is a sensitive feature of Signova AI.

### Requirements

- Request camera permission only after user interaction.
- Clearly indicate when the camera is active.
- Provide an option to stop the camera.
- Stop all camera tracks when the camera is stopped.
- Stop camera tracks when the relevant component unmounts.
- Do not record or store video by default.
- Do not send camera footage to external services without explicit approval.
- Send only the data required by the recognition model.
- Do not log raw images, videos, or landmarks containing user data.

### Privacy Rule

Camera data must be processed only for the requested recognition task.

Do not introduce background recording or hidden media collection.

---

# 3. API Security

All backend endpoints must validate incoming requests.

### Requirements

- Validate request bodies using Pydantic.
- Validate uploaded files.
- Restrict supported file formats.
- Apply reasonable upload size limits.
- Handle malformed requests safely.
- Use suitable HTTP status codes.
- Avoid exposing internal server details.
- Add rate limiting when required by deployment conditions.

Never trust frontend validation as the only security layer.

---

# 4. CORS Security

Configure Cross-Origin Resource Sharing carefully.

### Development

Allow only the required local frontend origin.

```text
http://localhost:5173
```

### Production

- Allow only approved production domains.
- Avoid wildcard origins.
- Restrict HTTP methods.
- Restrict request headers.
- Do not enable credential sharing unnecessarily.

Keep allowed origins in backend configuration.

---

# 5. Secrets and Environment Variables

Never hardcode secrets in source code.

Sensitive configuration includes:

- API keys.
- Database passwords.
- Authentication secrets.
- Private service tokens.
- External provider credentials.

### Requirements

- Use environment variables.
- Keep `.env` out of Git.
- Provide `.env.example` without real credentials.
- Never expose backend secrets through frontend code.
- Never commit credentials in documentation or logs.
- Rotate credentials if they are accidentally exposed.

### Frontend Rule

Vite variables beginning with `VITE_` are exposed to browser code.

Never store private credentials in `VITE_` variables.

---

# 6. File Upload Security

If image or video upload is implemented:

- Validate file size.
- Validate file extension.
- Validate MIME type.
- Do not trust the original filename.
- Generate safe temporary filenames.
- Store temporary files outside public directories.
- Prevent path traversal.
- Delete temporary files after processing.
- Reject unsupported or malformed files.
- Avoid executing uploaded content.

Do not permanently store uploaded media unless a clearly approved feature requires it.

---

# 7. AI Model Security

AI model files and inference pipelines must be handled carefully.

### Model Files

- Download models from trusted sources.
- Verify model repository identity.
- Review model licences.
- Avoid loading untrusted model files.
- Keep checkpoints outside Git.
- Restrict write access to model directories.
- Avoid exposing local model paths through APIs.

### PyTorch Security

- Prefer safer model formats where supported.
- Do not load untrusted pickle-based checkpoints.
- Use `weights_only=True` when compatible with the checkpoint and installed PyTorch version.
- Do not disable model-loading safety checks without a documented reason.
- Review custom model-loading code before execution.

### Inference Security

- Validate all model inputs.
- Restrict input dimensions and sequence lengths.
- Apply reasonable processing limits.
- Handle malformed landmarks.
- Avoid unrestricted resource consumption.
- Never execute user-provided code or model instructions.

---

# 8. Dataset Security and Licensing

Before using any dataset:

- Verify its source.
- Review its licence.
- Check usage restrictions.
- Avoid downloading unknown executable files.
- Preserve original data.
- Restrict access to local datasets.
- Do not upload restricted datasets to public repositories.

Public availability does not automatically mean unrestricted usage.

Respect attribution, non-commercial, and share-alike requirements where applicable.

---

# 9. Frontend Security

The React frontend must follow these rules:

- Avoid unsafe HTML rendering.
- Do not use `dangerouslySetInnerHTML` unless strictly necessary and safely sanitised.
- Validate data received from the backend.
- Do not expose private configuration.
- Avoid storing sensitive information in browser storage.
- Handle API errors safely.
- Use HTTPS in production.
- Do not include secrets in client-side source code.
- Avoid untrusted external scripts.

Use normal React rendering for recognition output.

Do not execute or interpret model predictions as HTML or JavaScript.

---

# 10. Authentication and Authorisation

Authentication is not required for the initial MVP unless explicitly approved.

If authentication is added later:

- Use a trusted authentication mechanism.
- Never store plaintext passwords.
- Validate authentication tokens on the backend.
- Protect private endpoints.
- Apply suitable session expiration.
- Restrict access to user-specific records.
- Do not rely on frontend-only access checks.

Do not add authentication or user accounts without a product requirement.

---

# 11. Database Security

PostgreSQL is optional for the initial MVP.

If introduced:

- Keep credentials in environment variables.
- Use parameterised queries or a suitable ORM.
- Restrict database permissions.
- Validate stored data.
- Avoid storing raw camera footage.
- Protect personal information.
- Use migrations for schema changes.
- Do not expose database errors to users.
- Back up data securely when persistent storage is required.

Basic sign recognition must not depend on a database.

---

# 12. Error Handling and Logging

### Error Handling

- Return safe and understandable error messages.
- Do not expose stack traces.
- Do not reveal internal paths.
- Do not expose environment variables.
- Do not reveal database credentials.
- Handle unexpected exceptions safely.

### Logging

Log useful technical events:

- Application startup.
- Model loading status.
- API failures.
- Processing errors.
- Unexpected exceptions.

Never log:

- Passwords.
- API keys.
- Authentication tokens.
- Raw camera footage.
- Sensitive user data.
- Unnecessary request payloads.

---

# 13. Dependency Security

All project dependencies must be reviewed.

### Requirements

- Install packages from trusted sources.
- Avoid unnecessary dependencies.
- Check package maintenance and compatibility.
- Review security advisories.
- Avoid installing unknown scripts.
- Pin important dependency versions where practical.
- Review major version upgrades before applying them.

Do not run downloaded scripts without inspecting their source.

---

# 14. Network and Deployment Security

For production deployment:

- Use HTTPS.
- Configure secure CORS policies.
- Keep secrets on the backend.
- Restrict public API access where appropriate.
- Apply request size limits.
- Configure suitable timeouts.
- Avoid exposing internal development ports.
- Keep debug mode disabled.
- Use secure environment configuration.
- Monitor application errors.

Do not expose development tools or debug endpoints publicly.

---

# 15. Resource Protection

AI inference can consume significant CPU, GPU, and memory resources.

Requirements:

- Limit upload sizes.
- Limit video duration where applicable.
- Restrict frame counts.
- Validate sequence lengths.
- Avoid unlimited concurrent inference.
- Handle GPU memory errors.
- Set suitable request timeouts.
- Prevent repeated model loading.
- Avoid unrestricted background processing.

Do not allow one request to consume unlimited system resources.

---

# 16. Security Testing

Test the following areas:

| Area | Security Test |
|---|---|
| API | Invalid request validation |
| Uploads | Unsupported file rejection |
| CORS | Unapproved origin rejection |
| Secrets | No credentials in frontend or Git |
| Camera | Permission and cleanup behaviour |
| AI Models | Untrusted checkpoint handling |
| Database | Query safety |
| Errors | No internal details exposed |
| Dependencies | Known vulnerability checks |
| Deployment | HTTPS and debug configuration |

Security testing must be performed before production deployment.

---

# 17. Security Incident Handling

If a security issue is discovered:

1. Stop the affected operation if necessary.
2. Identify the affected component.
3. Avoid exposing additional user data.
4. Preserve relevant technical logs without collecting sensitive content.
5. Fix the root cause.
6. Rotate exposed credentials.
7. Test the fix.
8. Document the issue and resolution.

Do not hide security failures or claim they are resolved without verification.

---

# 18. Strict Rules for Antigravity

Before making security-related changes:

1. Inspect the existing implementation.
2. Read `SECURITY.md`.
3. Read `backend-rules.md`.
4. Read `frontend-rules.md`.
5. Reuse existing security controls.
6. Do not weaken existing protections.
7. Do not expose credentials.
8. Do not delete security configuration without approval.
9. Do not install untrusted dependencies.
10. Do not add unnecessary authentication.
11. Do not store camera data without approval.
12. Do not load untrusted model checkpoints.
13. Do not claim security testing passed without running it.
14. Keep code, comments, and tests in English.
15. Update relevant documentation when security behaviour changes.

If a security requirement is unclear, report the risk before implementing a potentially unsafe change.

---

# 19. Final Security Goal

Signova AI must protect user privacy, camera data, application credentials, model files, and backend resources.

Security must be part of every development phase.

**Never sacrifice user privacy or application security to make a feature appear functional.**