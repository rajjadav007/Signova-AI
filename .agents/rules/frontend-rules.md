# Frontend Development Rules

## Signova AI

**Project:** Signova AI  
**Frontend Framework:** React  
**Language:** JavaScript ES6+  
**Build Tool:** Vite  
**Styling:** CSS  
**Backend:** Python + FastAPI  
**API Communication:** Fetch API or Axios

---

# 1. Core Frontend Principles

All frontend development must follow these rules:

1. Use React with JavaScript.
2. Use Vite as the build tool.
3. Use `.jsx` for React components.
4. Use `.js` for JavaScript utility modules.
5. Do not introduce TypeScript.
6. Keep components reusable and focused.
7. Separate UI, business logic, and API communication.
8. Keep the interface responsive and accessible.
9. Handle loading, success, empty, and error states.
10. Do not create fake AI predictions or hardcoded recognition results.

---

# 2. Technology Rules

| Area | Technology |
|---|---|
| UI Framework | React |
| Language | JavaScript ES6+ |
| Build Tool | Vite |
| Styling | CSS |
| API Communication | Fetch API or Axios |
| Camera | Browser MediaDevices API |
| Speech Output | Browser SpeechSynthesis API |
| Testing | Vitest + React Testing Library |

Do not add another frontend framework or state-management library without a clear requirement.

---

# 3. Frontend Architecture

Use a modular component-based structure.

Suggested structure:

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── camera/
│   │   │   ├── CameraPreview.jsx
│   │   │   └── CameraControls.jsx
│   │   ├── recognition/
│   │   │   ├── RecognitionPanel.jsx
│   │   │   └── RecognitionResult.jsx
│   │   ├── speech/
│   │   │   └── SpeechControls.jsx
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   └── Footer.jsx
│   │   └── common/
│   │       ├── Button.jsx
│   │       ├── Card.jsx
│   │       └── StatusIndicator.jsx
│   ├── pages/
│   │   └── Home.jsx
│   ├── services/
│   │   └── api.js
│   ├── hooks/
│   ├── context/
│   ├── utils/
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
├── index.html
└── package.json
```

This is a suggested structure. Inspect the existing repository and reuse existing files before creating new ones.

---

# 4. React Component Rules

- Use functional components.
- Use React Hooks where appropriate.
- Keep components small and focused.
- Avoid unnecessary component nesting.
- Reuse common UI components.
- Keep camera logic separate from recognition logic.
- Keep speech logic separate from recognition logic.
- Avoid putting the entire application in `App.jsx`.
- Use meaningful component and variable names.

Do not create a separate component for every small HTML element unless reuse or clarity justifies it.

---

# 5. JavaScript Rules

- Use modern JavaScript ES6+.
- Use `const` by default.
- Use `let` only when reassignment is required.
- Use clear variable and function names.
- Use `async/await` for asynchronous operations.
- Handle rejected promises.
- Avoid unnecessary global variables.
- Avoid deeply nested callbacks.
- Keep utility functions reusable.
- Do not use TypeScript syntax.

All frontend source code must use `.js` and `.jsx` files.

---

# 6. API Integration Rules

The frontend must communicate with FastAPI through service modules.

Example structure:

```text
src/
└── services/
    ├── api.js
    ├── healthService.js
    └── recognitionService.js
```

### Requirements

- Keep API calls outside presentation components where practical.
- Use a central API base URL.
- Use environment variables for backend URLs.
- Handle network failures.
- Handle non-success HTTP responses.
- Validate response data before using it.
- Avoid duplicate API logic.
- Do not hardcode prediction responses.

Example environment variable:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Example API service:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`);

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}
```

Do not expose secrets in frontend environment variables.

Only variables intended to be public should use the `VITE_` prefix.

---

# 7. Camera Integration Rules

Use the browser MediaDevices API for camera access.

### Requirements

- Request camera access only after user interaction.
- Handle permission denial.
- Handle missing cameras.
- Handle camera startup errors.
- Display the live camera stream.
- Stop camera tracks when the camera is stopped.
- Clean up streams when the component unmounts.
- Avoid creating multiple unnecessary camera streams.

### Important

The frontend is responsible for browser camera access.

The backend receives only the input required for recognition.

Do not assume that every AI model accepts raw camera frames. Check the selected model's input requirements before implementing frame submission.

---

# 8. Recognition Integration Rules

The frontend must display actual backend predictions.

### Requirements

- Show recognition status.
- Show processing feedback.
- Display returned prediction text.
- Handle empty predictions.
- Handle unsupported inputs.
- Handle backend failures.
- Avoid showing stale results as new predictions.
- Do not invent confidence scores.
- Do not combine isolated predictions and describe them as continuous ISL translation.

The UI must reflect the actual capabilities of the connected model.

---

# 9. Speech Output Rules

Use the browser SpeechSynthesis API for basic text-to-speech.

### Requirements

- Speak only available recognition text.
- Provide a stop action.
- Handle unsupported browser functionality.
- Prevent repeated speech requests from overlapping unexpectedly.
- Show the current speech status.
- Cancel speech when appropriate during component cleanup.

Speech output is not the same as sign language recognition. Keep the two features separate.

---

# 10. State Management Rules

Use React state and hooks for local UI state.

Examples:

- Camera active or inactive.
- Recognition loading.
- Current prediction.
- API connection status.
- Speech playing or stopped.
- Error messages.

### Requirements

- Keep state close to the component that uses it.
- Lift state only when multiple components need it.
- Avoid unnecessary global state.
- Avoid duplicated state.
- Do not store values that can be derived from existing state.
- Clean up event listeners and media resources.

Do not introduce Redux or another state library unless the application genuinely requires it.

---

# 11. UI/UX Rules

Follow `UI_UX_GUIDELINES.md`.

The interface must be:

- Clean.
- Modern.
- Minimal.
- Responsive.
- Accessible.
- Consistent.

Use the established white and teal visual identity.

Prioritise:

1. Camera preview.
2. Recognition controls.
3. Recognition result.
4. Speech controls.
5. System and model status.

Avoid unnecessary dashboard elements or decorative sections that distract from recognition.

---

# 12. Responsive Design Rules

Support:

- Desktop.
- Tablet.
- Mobile.

### Requirements

- Use flexible layouts.
- Use CSS Grid and Flexbox where appropriate.
- Avoid fixed widths that break smaller screens.
- Prevent horizontal overflow.
- Keep camera controls accessible.
- Make result text readable.
- Test important screen sizes.

Do not hide essential recognition controls on mobile.

---

# 13. Accessibility Rules

- Use semantic HTML.
- Add labels to form controls.
- Add accessible names to icon buttons.
- Support keyboard navigation.
- Maintain visible focus states.
- Use sufficient colour contrast.
- Provide meaningful error messages.
- Avoid colour-only status indicators.
- Respect reduced-motion preferences.
- Ensure interactive elements have suitable touch targets.

Accessibility must be considered during development, not added only at the end.

---

# 14. Error and Loading States

Every asynchronous action must provide feedback.

### Loading

Show a clear loading indicator during API requests and recognition.

### Success

Display the actual returned result.

### Empty

Explain when no recognition result is available.

### Error

Show a short, useful message.

### Offline

Indicate when the backend cannot be reached.

Do not expose internal server errors or stack traces to users.

---

# 15. Performance Rules

- Avoid unnecessary React re-renders.
- Avoid unnecessary API requests.
- Process camera frames at a controlled rate.
- Release media streams when no longer needed.
- Avoid loading unnecessary libraries.
- Optimise images and static assets.
- Use memoisation only when it provides a real benefit.
- Avoid blocking the main UI thread with expensive processing.

Do not send every camera frame to the backend without considering the model's processing requirements and system performance.

---

# 16. Security and Privacy Rules

- Do not store camera footage by default.
- Do not expose backend secrets.
- Do not trust frontend validation alone.
- Avoid unsafe HTML rendering.
- Use HTTPS in production.
- Do not log sensitive user media.
- Handle API errors safely.
- Request only necessary browser permissions.

The application must clearly communicate when the camera is active.

---

# 17. Testing Rules

Use Vitest and React Testing Library.

Test:

- Component rendering.
- Button interactions.
- Camera permission states.
- Camera cleanup.
- API success responses.
- API failure responses.
- Recognition loading states.
- Recognition result display.
- Speech controls.
- Responsive behaviour where practical.
- Accessibility basics.

Mock browser APIs and backend requests where needed.

Do not report mocked API tests as real backend or AI model validation.

---

# 18. Dependency Rules

- Keep dependencies minimal.
- Check existing packages before installing new ones.
- Avoid duplicate libraries.
- Use compatible package versions.
- Do not install a UI library without a clear need.
- Keep package scripts organised.
- Verify the build after dependency changes.

Do not replace existing working tools without a technical reason.

---

# 19. Development Workflow

Follow this order:

### Phase 1: Frontend Foundation

- Set up React and Vite.
- Configure CSS.
- Create the main application layout.
- Add reusable UI components.

### Phase 2: Camera Interface

- Implement camera permission handling.
- Display the camera preview.
- Add start and stop controls.
- Handle camera errors.

### Phase 3: Backend Connection

- Configure the API base URL.
- Create service modules.
- Connect health endpoints.
- Handle loading and network errors.

### Phase 4: Recognition Interface

- Connect supported prediction endpoints.
- Send compatible input.
- Display actual predictions.
- Handle unsupported model capabilities.

### Phase 5: Speech Output

- Add SpeechSynthesis support.
- Add speak and stop controls.
- Handle browser compatibility.

### Phase 6: Testing and Polish

- Test important interactions.
- Test responsive layouts.
- Check accessibility.
- Verify production build.

---

# 20. Strict Rules for Antigravity

Before making frontend changes:

1. Inspect the existing frontend structure.
2. Read `UI_UX_GUIDELINES.md`.
3. Read `TECH_STACK.md`.
4. Read the API documentation.
5. Reuse existing components and services.
6. Do not create duplicate files.
7. Do not introduce TypeScript.
8. Do not hardcode fake recognition results.
9. Do not assume unsupported AI capabilities.
10. Do not change backend contracts without agreement.
11. Do not delete existing files without approval.
12. Do not install unnecessary dependencies.
13. Do not claim features work without testing them.
14. Keep code, comments, and tests in English.
15. Update relevant documentation when implementation changes.

If a backend endpoint or AI model is not ready, build an honest loading, unavailable, or error state instead of simulating a successful result.

---

# 21. Final Frontend Goal

The Signova AI frontend must provide a smooth and accessible experience for capturing signing input, displaying genuine recognition results, and converting available text into speech.

**The frontend must reflect the real backend and AI capabilities. It must never hide model limitations behind fake UI behaviour.**