# Frontend Development Rules

# Signova AI

These rules apply to all frontend development, UI implementation, component creation, styling, routing, state management, and API integration in Signova AI.

The goal is to maintain a clean, responsive, accessible, and maintainable React application.

---

## 1. Frontend Technology Stack

Use the following technologies:

| Category | Technology |
|---|---|
| Framework | React |
| Language | JavaScript (ES6+) |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Routing | React Router |
| Icons | Lucide React |
| API Communication | Fetch API or Axios |
| Testing | Vitest |
| Component Testing | React Testing Library |
| E2E Testing | Playwright |

### Strict Rules

- Use JavaScript, not TypeScript.
- Use React functional components.
- Use React Hooks.
- Use Vite for the frontend build.
- Use Tailwind CSS for styling.
- Reuse shadcn/ui components where appropriate.
- Use Lucide React for icons.
- Do not introduce another frontend framework.
- Do not migrate to Next.js without approval.

---

## 2. Project Structure

Follow the existing frontend structure.

A recommended structure is:

```text
frontend/
├── public/
│   └── assets/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── common/
│   │   ├── layout/
│   │   └── recognition/
│   │
│   ├── pages/
│   │
│   ├── layouts/
│   │
│   ├── hooks/
│   │
│   ├── services/
│   │   ├── api.js
│   │   └── recognitionService.js
│   │
│   ├── context/
│   │
│   ├── utils/
│   │
│   ├── constants/
│   │
│   ├── styles/
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── tests/
├── .env.example
├── index.html
├── package.json
└── vite.config.js
```

This is a recommended structure, not a requirement to create every directory immediately.

### Structure Rules

- Keep page components inside `pages/`.
- Keep reusable components inside `components/`.
- Keep API communication inside `services/`.
- Keep reusable React hooks inside `hooks/`.
- Keep shared constants inside `constants/`.
- Keep general helper functions inside `utils/`.
- Keep global styles inside `styles/`.
- Avoid putting the entire application inside `App.jsx`.
- Do not create duplicate directories with similar responsibilities.

---

## 3. Naming Conventions

Use consistent naming throughout the frontend.

| Element | Convention | Example |
|---|---|---|
| React Components | PascalCase | `CameraPreview.jsx` |
| Pages | PascalCase | `Dashboard.jsx` |
| Hooks | camelCase with `use` | `useCamera.js` |
| Services | camelCase | `recognitionService.js` |
| Utilities | camelCase | `formatPrediction.js` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL` |
| CSS Classes | Tailwind utilities | `flex items-center` |

Use meaningful names.

Avoid:

```javascript
const x = {};
const d = [];
function fn() {}
```

Prefer:

```javascript
const recognitionResult = {};
const predictionHistory = [];

function formatRecognitionResult() {}
```

---

## 4. React Component Rules

### Component Design

- Use functional components.
- Keep components focused on one responsibility.
- Prefer reusable components.
- Keep business logic outside large UI components.
- Avoid deeply nested JSX.
- Avoid unnecessary component abstractions.
- Use props to share data between components.
- Use state only when necessary.

Example:

```jsx
function RecognitionResult({ prediction, confidence }) {
  return (
    <section>
      <h2>Recognition Result</h2>

      <p>{prediction || "No sign detected"}</p>

      {confidence !== null && (
        <p>Confidence: {confidence}%</p>
      )}
    </section>
  );
}

export default RecognitionResult;
```

### React Hooks

Use hooks correctly:

- `useState`
- `useEffect`
- `useCallback`
- `useMemo`
- `useRef`
- Custom hooks when useful

Rules:

- Never call hooks conditionally.
- Never call hooks inside loops.
- Clean up event listeners and subscriptions.
- Clean up camera streams when components unmount.
- Avoid unnecessary effects.
- Avoid storing values in state when they can be calculated.

---

## 5. UI Design Rules

Signova AI must have a modern, clean, accessible, and professional interface.

### Design Principles

- Minimal and clean layouts.
- Consistent spacing.
- Clear typography.
- Good colour contrast.
- Responsive components.
- Clear visual hierarchy.
- Consistent border radius.
- Subtle transitions.
- Useful empty states.
- Clear loading indicators.

### Avoid

- Excessive gradients.
- Excessive shadows.
- Too many colours.
- Unnecessary animations.
- Cluttered layouts.
- Inconsistent spacing.
- Random font combinations.
- Decorative elements that reduce readability.

### Design Consistency

Before creating new UI components:

1. Check existing components.
2. Check the current design system.
3. Reuse existing styles.
4. Follow the project's UI guidelines.
5. Avoid introducing a second design system.

Follow `docs/UI_UX_GUIDELINES.md`.

---

## 6. Tailwind CSS Rules

Use Tailwind CSS for component styling.

Example:

```jsx
<div className="flex min-h-screen items-center justify-center p-6">
  <div className="w-full max-w-4xl rounded-xl border p-6">
    <h1 className="text-2xl font-semibold">
      Signova AI
    </h1>
  </div>
</div>
```

### Rules

- Prefer utility classes.
- Keep class names readable.
- Reuse common design patterns.
- Avoid excessive arbitrary values.
- Use the project's existing colour tokens.
- Use responsive breakpoints appropriately.
- Avoid unnecessary inline styles.
- Do not mix multiple styling frameworks.

If a class combination becomes difficult to maintain, extract a reusable component or use an appropriate helper already present in the project.

---

## 7. shadcn/ui Rules

Use shadcn/ui components where they improve consistency and accessibility.

Examples:

- Button
- Card
- Dialog
- Dropdown Menu
- Input
- Label
- Select
- Tabs
- Tooltip
- Alert
- Badge
- Skeleton
- Toast or Sonner, depending on the existing setup

### Rules

- Reuse installed components.
- Follow existing component conventions.
- Do not repeatedly install duplicate UI components.
- Customise components using project design tokens.
- Preserve keyboard accessibility.
- Do not replace an existing component without a clear reason.

---

## 8. Routing Rules

Use React Router.

### Rules

- Keep route definitions organised.
- Use meaningful route paths.
- Separate page components from reusable UI components.
- Handle unknown routes.
- Protect authenticated routes only when authentication is implemented.
- Avoid unnecessary nested routes.

Example:

```jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

Adapt the example to the actual application routes.

---

## 9. State Management Rules

Start with React's built-in state management.

Use:

- `useState` for local component state.
- `useContext` for shared state when appropriate.
- Custom hooks for reusable stateful logic.

Do not introduce Redux, Zustand, or another state library unless the application genuinely needs it.

### Rules

- Keep state as close as practical to where it is used.
- Avoid unnecessary global state.
- Avoid duplicating the same state in multiple places.
- Keep derived values out of state where possible.
- Handle asynchronous state carefully.

---

## 10. API Integration Rules

All backend communication must go through the service layer.

Recommended structure:

```text
src/
└── services/
    ├── api.js
    └── recognitionService.js
```

### API Rules

- Do not hardcode backend URLs throughout components.
- Use environment variables for API configuration.
- Handle network errors.
- Handle loading states.
- Validate response assumptions.
- Use consistent error messages.
- Avoid duplicate API requests.
- Never expose private API keys in frontend code.

Example:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function recogniseSign(imageBlob) {
  if (!API_BASE_URL) {
    throw new Error("API base URL is not configured.");
  }

  const formData = new FormData();
  formData.append("image", imageBlob);

  const response = await fetch(
    `${API_BASE_URL}/recognition/predict`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error("Sign recognition request failed.");
  }

  return response.json();
}
```

This is an example only. Confirm the actual backend endpoint and request format before implementing it.

---

## 11. Camera Integration Rules

Camera functionality is a core part of Signova AI.

### Camera Requirements

- Use the browser MediaDevices API.
- Request camera permission through a clear user action.
- Handle denied permissions.
- Handle unavailable cameras.
- Provide start and stop controls.
- Display a camera preview.
- Clean up media tracks when the camera stops.
- Handle component unmounting.
- Do not access the camera without user permission.

Example:

```javascript
async function startCamera(videoElement) {
  if (!navigator.mediaDevices?.getUserMedia) {
    throw new Error("Camera access is not supported.");
  }

  const stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
  });

  videoElement.srcObject = stream;

  return stream;
}

function stopCamera(stream) {
  stream?.getTracks().forEach((track) => track.stop());
}
```

Use the appropriate React hook or component lifecycle to manage the stream safely.

### Camera Privacy

- Do not record video by default.
- Do not upload camera footage without consent.
- Do not leave camera streams running after the user stops recognition.
- Make camera activity visible to the user.

---

## 12. Recognition Interface Rules

The recognition interface must clearly communicate the current application state.

### Required States

| State | UI Behaviour |
|---|---|
| Idle | Show instructions and start action |
| Permission Required | Explain camera permission |
| Camera Active | Show live camera preview |
| Processing | Show processing indicator |
| Prediction Available | Display recognised output |
| Low Confidence | Indicate uncertain prediction |
| No Sign Detected | Show helpful guidance |
| Error | Display a clear error message |

### Prediction Display

- Display the recognised label clearly.
- Show confidence only when the backend supplies a valid confidence value.
- Do not invent confidence scores.
- Do not display unsupported labels.
- Avoid repeated duplicate results where appropriate.
- Provide a clear way to reset or start another recognition.

### Important

The frontend must reflect the actual capability of the connected model.

If the backend supports only alphabet recognition, do not display the result as a complete ISL sentence translation.

---

## 13. Speech Output Rules

Speech output is optional and should be implemented only when supported by the backend or an approved speech service.

### Requirements

- Provide a clear speak button.
- Allow users to stop speech where supported.
- Handle unavailable speech services.
- Do not block recognised text when speech fails.
- Avoid automatically speaking every repeated prediction.
- Do not expose provider API keys in the browser.

The frontend must not claim that speech output is available until the corresponding feature is implemented.

---

## 14. Accessibility Rules

Accessibility is a core requirement of Signova AI.

Follow these practices:

- Use semantic HTML.
- Provide accessible labels.
- Use keyboard-accessible controls.
- Maintain sufficient colour contrast.
- Provide visible focus states.
- Avoid colour-only status indicators.
- Use appropriate ARIA attributes when necessary.
- Support screen readers.
- Use readable font sizes.
- Provide understandable error messages.

Test the interface with keyboard navigation and relevant accessibility tools.

---

## 15. Responsive Design Rules

The application must support:

- Desktop.
- Laptop.
- Tablet.
- Mobile devices.

Use Tailwind responsive breakpoints.

Example:

```jsx
<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  {/* Responsive content */}
</div>
```

### Requirements

- Avoid horizontal overflow.
- Keep camera preview usable on smaller screens.
- Ensure buttons remain easy to tap.
- Keep text readable.
- Adapt navigation for smaller screens.
- Test the layout at different viewport sizes.

---

## 16. Loading and Error States

Every asynchronous feature must provide feedback.

Examples:

- Camera initialisation.
- Backend requests.
- Recognition processing.
- Speech generation.
- Model availability checks.

Use consistent loading indicators and error messages.

Do not leave users with a blank screen when something fails.

Do not expose raw backend stack traces or sensitive technical information in the UI.

---

## 17. Performance Rules

- Avoid unnecessary component re-renders.
- Use `useMemo` and `useCallback` only when useful.
- Avoid processing every video frame without need.
- Use suitable frame sampling based on model requirements.
- Avoid unnecessary image conversions.
- Revoke temporary object URLs when no longer needed.
- Clean up event listeners and camera streams.
- Avoid loading large assets unnecessarily.
- Keep initial page loading fast.

Measure performance before making claims about improvements.

---

## 18. Environment Variables

Use Vite environment variables for frontend configuration.

Example `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Rules

- Only expose values that are safe for browser access.
- Never store private API keys in `VITE_` variables.
- Never commit real `.env` files.
- Keep `.env.example` updated.
- Do not hardcode production service URLs in components.

---

## 19. Testing Rules

Use the project's configured testing tools.

### Required Testing Areas

- Component rendering.
- User interactions.
- Camera permission handling.
- Camera start and stop.
- API request handling.
- Loading states.
- Error states.
- Recognition result rendering.
- Responsive layouts.
- Accessibility.

### Example Commands

Check the scripts in `package.json` before running:

```bash
npm run lint
npm run test
npm run build
```

Do not report tests as passed unless they have actually been executed.

---

## 20. Security Rules

- Never expose backend credentials.
- Never expose Sarvam API keys.
- Validate data received from the backend.
- Avoid rendering untrusted HTML.
- Do not use unsafe DOM manipulation.
- Use secure production connections.
- Restrict browser camera access to user-approved actions.
- Avoid storing sensitive user information unnecessarily.
- Follow the project's `docs/SECURITY.md`.

---

## 21. Documentation Rules

When frontend implementation changes, update relevant documentation.

Examples:

- `docs/FEATURES.md`
- `docs/UI_UX_GUIDELINES.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/API_DOCUMENTATION.md`
- `docs/TESTING_STRATEGY.md`
- `docs/PROGRESS_TRACKER.md`

Do not document unimplemented features as completed.

---

## 22. Frontend Definition of Done

A frontend task is complete only when:

- [ ] The feature is implemented.
- [ ] Existing functionality still works.
- [ ] Components follow project conventions.
- [ ] JavaScript is used instead of TypeScript.
- [ ] Responsive behaviour is checked.
- [ ] Accessibility is considered.
- [ ] Loading and error states are handled.
- [ ] API integration uses the actual backend contract.
- [ ] Relevant tests are executed.
- [ ] Build succeeds.
- [ ] Documentation is updated where necessary.

---

## 23. Final Rule

Build the Signova AI frontend with a clear focus on accessibility, usability, reliability, and maintainability.

**Prioritise a working camera-to-recognition experience over decorative UI features.**

Never create a frontend feature that pretends to work when the required backend or AI model functionality does not exist.