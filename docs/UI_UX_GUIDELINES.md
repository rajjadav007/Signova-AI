# UI/UX Guidelines

## Signova AI

**Project:** Signova AI  
**Application Type:** Web Application  
**Frontend:** React + JavaScript + Vite  
**Styling:** CSS  
**Design Approach:** Modern, Minimal, Accessible  
**Primary Focus:** Indian Sign Language Recognition

---

# 1. Design Vision

Signova AI should provide a clean, modern, accessible, and easy-to-use interface.

The design must make the sign recognition process simple and understandable, even for users who are not technically experienced.

The interface should prioritise:

- Clear camera interaction.
- Easy-to-read recognition results.
- Visible system status.
- Accessible controls.
- Minimal distractions.
- Responsive layouts.
- Consistent visual design.

The interface should feel like a professional AI accessibility product rather than a generic dashboard.

---

# 2. Design Principles

### 2.1 Simplicity

- Keep the interface clean.
- Avoid unnecessary sections.
- Use clear labels.
- Make important actions easy to find.

### 2.2 Accessibility

- Use readable font sizes.
- Maintain sufficient colour contrast.
- Provide clear button labels.
- Support keyboard navigation.
- Do not communicate status using colour alone.
- Provide visible focus indicators.

### 2.3 Consistency

- Use consistent spacing.
- Maintain a clear typography system.
- Reuse common components.
- Keep button and card styles consistent.

### 2.4 Responsiveness

- Support desktop, tablet, and mobile screens.
- Prevent horizontal overflow.
- Keep camera controls accessible on smaller screens.
- Adapt layouts without hiding important functionality.

---

# 3. Visual Identity

## Design Direction

Recommended visual style:

- Modern AI product.
- Minimal interface.
- Soft backgrounds.
- Clean cards.
- Rounded corners.
- Subtle shadows.
- Clear typography.
- Professional accessibility-focused appearance.

## Colour Palette

Use a white and teal visual identity.

| Colour | Suggested Value | Usage |
|---|---|---|
| Primary Teal | `#0F766E` | Main actions |
| Dark Teal | `#115E59` | Hover and emphasis |
| Light Teal | `#CCFBF1` | Highlight backgrounds |
| Background | `#F8FAFC` | Main page background |
| Surface | `#FFFFFF` | Cards and panels |
| Primary Text | `#0F172A` | Headings |
| Secondary Text | `#64748B` | Supporting text |
| Border | `#E2E8F0` | Card and input borders |
| Success | `#16A34A` | Successful operations |
| Warning | `#D97706` | Warnings |
| Error | `#DC2626` | Errors |

Use colour consistently. Do not use too many accent colours.

---

# 4. Typography

Use a clean and readable font.

Recommended fonts:

- Inter
- Geist Sans
- DM Sans

### Typography Scale

| Element | Suggested Size |
|---|---|
| Main Heading | 32px to 40px |
| Section Heading | 22px to 28px |
| Card Heading | 18px to 20px |
| Body Text | 14px to 16px |
| Supporting Text | 12px to 14px |
| Button Text | 14px to 16px |

Use appropriate font weights and line heights.

Avoid overly decorative fonts for important information.

---

# 5. Application Layout

The main application should contain the following sections:

```text
Signova AI
│
├── Header
│   ├── Logo
│   ├── Navigation
│   └── Accessibility Controls
│
├── Main Workspace
│   ├── Welcome Section
│   ├── Camera Panel
│   ├── Recognition Controls
│   └── Recognition Results
│
├── Speech Controls
│
└── Footer
```

Keep the main recognition workspace as the visual focus.

---

# 6. Header and Navigation

### Header Elements

- Signova AI logo.
- Product name.
- Main navigation.
- Optional accessibility settings.

### Design Rules

- Keep the header simple.
- Use a consistent height.
- Make navigation easy to understand.
- Keep the logo visually clear.
- Avoid excessive navigation items.

---

# 7. Camera Interface

The camera interface is one of the most important parts of Signova AI.

### Required Elements

- Camera preview.
- Camera permission status.
- Start camera button.
- Stop camera button.
- Recognition status.
- Camera error messages.

### Camera States

| State | UI Behaviour |
|---|---|
| Initial | Show camera start action |
| Permission Required | Explain camera permission |
| Camera Active | Display live preview |
| Camera Stopped | Show inactive state |
| Permission Denied | Display helpful instructions |
| Camera Unavailable | Show an error message |
| Processing | Display processing indicator |

### Camera Design Rules

- Maintain a suitable aspect ratio.
- Keep the signing area visible.
- Avoid covering the user's hands with controls.
- Use a clear camera border.
- Provide visible start and stop controls.
- Show useful feedback when the camera is unavailable.

Do not start camera access automatically without user interaction.

---

# 8. Recognition Interface

The recognition interface must clearly communicate the current processing state.

### Required Elements

- Recognition status.
- Processing indicator.
- Recognised text.
- Prediction confidence, only if provided by the model.
- Error or uncertain prediction message.

### Recognition States

| State | Display |
|---|---|
| Ready | Ready to recognise |
| Processing | Processing signing input |
| Success | Prediction available |
| Uncertain | Could not confidently recognise |
| Error | Recognition failed |
| Model Unavailable | Model is not available |

### Design Rules

- Make recognised text easy to read.
- Use a clear result area.
- Avoid displaying fabricated predictions.
- Do not display confidence values unless the model provides meaningful confidence information.
- Distinguish recognition errors from unsupported signs.

---

# 9. Recognition Result Card

The result card should be visually prominent.

### Suggested Content

```text
Recognition Result

Recognised Text
------------------------------
[ Model prediction appears here ]

[ Copy Text ]  [ Speak ]
```

### Requirements

- Display actual model output.
- Support longer text without breaking the layout.
- Provide copy functionality if implemented.
- Provide speech playback controls.
- Show an appropriate empty state.
- Avoid displaying old predictions as current results.

---

# 10. Text-to-Speech Interface

Speech controls should be simple and easy to use.

### Required Controls

- Speak.
- Stop.
- Speech status.
- Optional voice selection.

### Speech States

| State | Display |
|---|---|
| Idle | Ready to speak |
| Speaking | Speech playing |
| Stopped | Speech stopped |
| Unsupported | Speech unavailable |

### Design Rules

- Use recognisable control icons.
- Provide accessible labels.
- Disable controls when no text is available.
- Clearly indicate when speech is playing.
- Handle unsupported browser functionality.

---

# 11. Buttons and Interactive Elements

Use consistent button styles.

### Primary Button

Used for important actions such as starting the camera or recognition.

### Secondary Button

Used for actions such as stopping, copying, or resetting.

### Disabled Button

Used when an action is unavailable.

### Button Rules

- Use clear action labels.
- Provide hover and focus states.
- Provide visible disabled states.
- Avoid tiny click targets.
- Prevent accidental repeated actions.

Recommended minimum touch target: approximately 44 × 44 CSS pixels.

---

# 12. Cards and Containers

Use cards to organise related information.

Recommended cards:

- Camera card.
- Recognition result card.
- Model status card.
- Speech control card.

### Card Styling

- White background.
- Subtle border.
- Rounded corners.
- Light shadow where useful.
- Consistent internal spacing.

Avoid excessive card nesting.

---

# 13. Icons and Visual Elements

Use a consistent icon library such as Lucide.

Recommended icons:

| Purpose | Icon |
|---|---|
| Camera | Camera |
| Start | Play |
| Stop | Square |
| Speech | Volume 2 |
| Copy | Copy |
| Success | Check Circle |
| Error | Alert Circle |
| Settings | Settings |

Icons must have accessible labels when they communicate an action.

Do not use icons alone when their meaning may be unclear.

---

# 14. Responsive Design

The application must support:

- Desktop.
- Tablet.
- Mobile.

### Desktop

- Main workspace can use a two-column layout.
- Camera and results can appear side by side.
- Keep the recognition controls close to the camera.

### Tablet

- Reduce spacing.
- Maintain readable content.
- Adjust camera and result panel widths.

### Mobile

- Use a single-column layout.
- Keep camera preview prominent.
- Place controls within easy reach.
- Avoid horizontal scrolling.
- Ensure result text remains readable.

---

# 15. Accessibility Requirements

Signova AI is an accessibility-focused application.

Follow these requirements:

- Use semantic HTML.
- Provide accessible names for controls.
- Support keyboard navigation.
- Maintain visible focus states.
- Use sufficient text contrast.
- Avoid colour-only status indicators.
- Provide clear error messages.
- Use appropriate ARIA attributes when needed.
- Ensure controls work with screen readers.
- Respect reduced-motion preferences.

Do not make the interface dependent on animations to communicate important information.

---

# 16. Loading, Empty, and Error States

Every important interaction should have clear feedback.

### Loading State

Show a spinner or progress indicator while processing.

### Empty State

Explain what the user needs to do when no recognition result exists.

### Error State

Display a short and helpful error message.

### Model Status

Show whether the AI model is available.

Avoid exposing internal stack traces or technical server details in the UI.

---

# 17. Animation and Microinteractions

Use subtle animations only where they improve usability.

Suitable animations:

- Button hover transitions.
- Card appearance.
- Camera activation feedback.
- Loading indicators.
- Recognition result updates.

Avoid:

- Excessive motion.
- Distracting background effects.
- Long transitions.
- Animations that delay important actions.

Respect the user's reduced-motion settings.

---

# 18. Frontend Component Structure

Use reusable React components with JavaScript and JSX.

Suggested structure:

```text
frontend/src/
├── components/
│   ├── camera/
│   │   ├── CameraPreview.jsx
│   │   └── CameraControls.jsx
│   ├── recognition/
│   │   ├── RecognitionPanel.jsx
│   │   └── RecognitionResult.jsx
│   ├── speech/
│   │   └── SpeechControls.jsx
│   ├── layout/
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   └── common/
│       ├── Button.jsx
│       ├── Card.jsx
│       └── StatusIndicator.jsx
├── pages/
│   └── Home.jsx
├── services/
│   └── api.js
├── hooks/
├── context/
├── styles/
├── App.jsx
└── main.jsx
```

This is a suggested structure. Reuse existing components where possible rather than creating duplicates.

---

# 19. UI Development Rules

Antigravity must follow these rules when implementing the frontend:

1. Use React with JavaScript.
2. Use `.jsx` for React components.
3. Use `.js` for JavaScript utility modules.
4. Do not introduce TypeScript.
5. Use reusable components.
6. Keep API logic inside service modules.
7. Keep camera logic separate from presentation components.
8. Keep speech logic separate from recognition logic.
9. Use consistent CSS variables for design tokens.
10. Avoid unnecessary dependencies.
11. Do not hardcode fake AI predictions.
12. Show real backend responses.
13. Handle loading, empty, and error states.
14. Test responsive layouts.
15. Follow accessibility requirements.

---

# 20. Final UI/UX Goal

The final Signova AI interface should be:

- Modern.
- Minimal.
- Professional.
- Accessible.
- Responsive.
- Easy to understand.
- Focused on sign recognition.

The camera experience and recognition result must remain the primary focus.

The design should help users understand what the system is doing, what it has recognised, and when speech output is available.