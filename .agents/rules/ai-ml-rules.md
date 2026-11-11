# AI/ML Development Rules

## Signova AI

**Project:** Signova AI  
**Domain:** Indian Sign Language Recognition  
**AI Framework:** PyTorch  
**Backend:** Python 3.11 + FastAPI  
**Development Approach:** Pretrained Models First, Local Development First

---

# 1. Core AI/ML Principles

All AI/ML development must follow these principles:

1. Prefer existing pretrained models over training from scratch.
2. Do not assume a model supports Indian Sign Language without verification.
3. Keep model loading, preprocessing, inference, and postprocessing separate.
4. Preserve the original model architecture and expected input format.
5. Validate model compatibility before integrating it into the application.
6. Never generate fake predictions or hardcode recognition results.
7. Keep AI modules independent from frontend and API implementation.
8. Document known model limitations.
9. Prefer reproducible experiments.
10. Do not claim model accuracy without evaluation evidence.

---

# 2. Sign Language Rules

Signova AI focuses on **Indian Sign Language (ISL)**.

Antigravity must follow these rules:

- Do not treat American Sign Language (ASL) as ISL.
- Do not present ASL alphabet recognition as ISL translation.
- Do not assume signs are identical across different sign languages.
- Do not claim support for all ISL vocabulary.
- Do not claim continuous sentence translation when only isolated signs are recognised.
- Distinguish isolated sign recognition from continuous sign language recognition.
- Consider hand movements, body pose, and facial expressions when the selected model requires them.

Any model's supported sign language and vocabulary must be checked before integration.

---

# 3. Pretrained Model Rules

## 3.1 Model Selection

Before selecting a model, verify:

- Supported sign language.
- Supported vocabulary.
- Input type.
- Output format.
- Model architecture.
- Required preprocessing.
- Dataset used.
- Training and evaluation details.
- Model licence.
- Hardware requirements.
- Inference dependencies.

Do not select a model based only on its name or model card title.

## 3.2 Model Compatibility

A model must be classified according to its actual input requirements.

| Model Type | Expected Input |
|---|---|
| Image Classification | Individual images |
| Video Classification | Video frames or clips |
| Landmark Classification | Extracted landmarks |
| Pose-to-Text | Pose or landmark sequences |
| Continuous Sign Translation | Temporal sign sequences |

Do not pass raw webcam frames into a model that expects pose landmarks.

Do not pass landmarks into a model that expects images.

## 3.3 Model Integration

Before integration:

1. Inspect the model repository.
2. Read the original documentation.
3. Inspect the inference implementation.
4. Identify the expected input dimensions.
5. Identify normalization requirements.
6. Identify checkpoint and tokenizer requirements.
7. Run a standalone inference test.
8. Record the test result.
9. Integrate only after compatibility is established.

Never modify the original model architecture just to make an incompatible input work without a documented technical reason.

---

# 4. Model Architecture Rules

Keep model-related code modular.

Suggested structure:

```text
ai/
├── preprocessing/
│   ├── image_preprocessing.py
│   ├── video_preprocessing.py
│   └── landmark_preprocessing.py
│
├── pose_extraction/
│   └── pose_extractor.py
│
├── inference/
│   ├── model_loader.py
│   └── predictor.py
│
├── model_adapters/
│   ├── base_adapter.py
│   └── isign_adapter.py
│
├── postprocessing/
│   └── prediction_formatter.py
│
└── config/
    └── model_config.py
```

This is a suggested structure. Reuse existing modules where possible.

### Architecture Requirements

- Model loading must be separate from prediction.
- Preprocessing must be separate from inference.
- Each model must have its own adapter when input or output formats differ.
- Configuration must not be scattered across files.
- API routes must not contain model implementation logic.
- Frontend code must not contain AI model logic.

---

# 5. Preprocessing Rules

Preprocessing is a critical part of model compatibility.

Antigravity must:

1. Reproduce the preprocessing used by the original model.
2. Preserve landmark ordering.
3. Preserve expected coordinate formats.
4. Apply the correct normalization.
5. Maintain expected input dimensions.
6. Handle missing or invalid landmarks.
7. Validate input shape before inference.
8. Avoid silently changing input values.
9. Keep preprocessing deterministic where possible.

### Landmark Processing

When a model uses MediaPipe landmarks:

- Verify which MediaPipe solution is required.
- Verify which landmarks are used.
- Verify landmark ordering.
- Verify coordinate dimensions.
- Verify whether body pose, left hand, right hand, or facial landmarks are required.
- Verify how missing landmarks are represented.
- Verify whether temporal information is required.

Do not assume that all landmark-based models use the same format.

---

# 6. iSign T5 Model Rules

The `manavdhamecha77/iSign-t5-pose-to-text` model is an experimental candidate for Signova AI.

It must not be treated as a verified production model until compatibility and performance are tested.

### Important Requirements

- Treat it as a pose-to-text model.
- Do not assume it accepts raw images or webcam frames.
- Inspect the original inference implementation.
- Verify the selected checkpoint configuration.
- Verify expected pose dimensions.
- Verify landmark ordering.
- Verify normalization and motion processing.
- Verify tokenizer and output generation settings.
- Use the matching preprocessing pipeline.

### Checkpoint Selection

The model repository describes multiple checkpoint variants.

Do not assume their input dimensions or configurations are interchangeable.

Verify the exact configuration of the selected checkpoint before inference.

### Validation

Test the model using compatible samples from its intended dataset or another verified compatible source.

Record:

- Input sample.
- Expected output.
- Predicted output.
- Input shape.
- Preprocessing configuration.
- Inference time.
- Observed errors.

A prediction on an unrelated dataset is not sufficient to establish model accuracy or failure.

---

# 7. Model Loading Rules

Model loading must happen separately from individual prediction requests.

Requirements:

- Load the model during application startup or through a controlled lazy-loading mechanism.
- Avoid loading model weights for every request.
- Check whether the model files exist.
- Validate checkpoint compatibility.
- Handle missing dependencies.
- Handle CPU and CUDA devices.
- Provide clear model status.
- Release resources safely during shutdown where applicable.

The application must not crash silently when model loading fails.

---

# 8. Hardware and Device Rules

Primary development environment:

- Windows.
- Python 3.11.
- NVIDIA GPU with 4 GB VRAM.
- Local development first.

### Device Selection

Use automatic device selection:

1. Check whether CUDA is available.
2. Use a compatible GPU when available.
3. Fall back to CPU when necessary.
4. Log the selected device.

Example:

```python
import torch

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {DEVICE}")
```

### GPU Rules

- Do not assume CUDA is available.
- Verify the installed PyTorch build.
- Do not assume the system's CUDA driver version equals the PyTorch CUDA runtime version.
- Monitor GPU memory.
- Avoid loading multiple large models unnecessarily.
- Use smaller checkpoints when appropriate.
- Handle CUDA out-of-memory errors.

If local execution is not practical, Kaggle can be used as a fallback for experiments.

Do not move the entire development workflow to Kaggle without a clear reason.

---

# 9. Inference Rules

Every prediction request must follow a controlled pipeline:

```text
Input
  |
  v
Input Validation
  |
  v
Preprocessing
  |
  v
Model Inference
  |
  v
Postprocessing
  |
  v
Output Validation
  |
  v
Prediction Result
```

### Requirements

- Validate input before inference.
- Check model availability.
- Use the correct preprocessing pipeline.
- Run inference using the selected device.
- Use evaluation mode for inference.
- Disable gradient calculation when appropriate.
- Handle inference exceptions.
- Validate model output.
- Return structured results.

Never return a successful prediction when inference has failed.

---

# 10. Continuous Recognition Rules

Isolated sign recognition and continuous sign recognition are different tasks.

### Isolated Recognition

- Processes one sign or a defined short sample.
- Produces an individual sign prediction.
- Does not automatically provide sentence-level translation.

### Continuous Recognition

- Processes a sequence of signs.
- Requires temporal information.
- May require segmentation and sequence modelling.
- Must handle transitions between signs.
- May require language-level postprocessing.

Antigravity must not combine isolated predictions and describe the result as reliable continuous ISL translation.

Continuous recognition should be implemented only when a compatible model and suitable evaluation data are available.

---

# 11. Dataset Rules

Before using a dataset, verify:

- Dataset source.
- Sign language.
- Vocabulary.
- Annotation format.
- Number of samples.
- Video or image format.
- Landmark availability.
- Train, validation, and test splits.
- Licence and usage restrictions.

### Dataset Handling

- Do not modify original datasets.
- Keep raw datasets separate from processed data.
- Do not commit large datasets to Git.
- Avoid downloading huge archives without checking available storage.
- Preserve original annotations.
- Record preprocessing steps.
- Keep train and test data separate.

### Dataset Licence

Respect the dataset licence.

For example, datasets under `CC-BY-NC-SA-4.0` must be handled according to their non-commercial and share-alike conditions.

Do not assume that a publicly downloadable dataset is unrestricted for commercial use.

---

# 12. Model Evaluation Rules

Every model must be evaluated before being considered suitable for the application.

### Evaluation Metrics

Select metrics based on the model task.

| Metric | Purpose |
|---|---|
| Accuracy | Overall classification correctness |
| Precision | Correctness of positive predictions |
| Recall | Coverage of actual positive samples |
| F1-score | Balance between precision and recall |
| Confusion Matrix | Class-level prediction errors |
| BLEU / ROUGE | Possible text-generation evaluation |
| Inference Time | Prediction speed |
| Memory Usage | Hardware requirements |

Not every metric applies to every model.

For sequence translation, use suitable sequence-level evaluation methods rather than relying only on classification accuracy.

### Evaluation Requirements

- Use compatible test data.
- Avoid evaluating only on training samples.
- Keep test samples separate.
- Record the model checkpoint.
- Record preprocessing configuration.
- Save evaluation results.
- Report limitations.
- Do not invent evaluation metrics.

---

# 13. Backend Integration Rules

AI modules must remain independent from FastAPI routes.

Recommended flow:

```text
FastAPI Route
    |
    v
AI Service
    |
    v
Model Adapter
    |
    v
Preprocessing
    |
    v
Model Inference
    |
    v
Postprocessing
    |
    v
Structured Response
```

### Backend Requirements

- Use separate AI service modules.
- Validate API inputs.
- Return structured JSON.
- Handle model loading errors.
- Handle inference errors.
- Avoid blocking unrelated API routes.
- Add suitable request limits.
- Keep model configuration outside route files.

The backend must report whether the AI model is available.

---

# 14. Error Handling Rules

Handle the following conditions:

- Model file missing.
- Invalid checkpoint.
- Unsupported input format.
- Incorrect input dimensions.
- Missing landmarks.
- Invalid landmark values.
- Camera input unavailable.
- CUDA unavailable.
- GPU memory exhausted.
- Inference timeout.
- Model output invalid.
- Model dependency missing.

Errors must be understandable and must not expose sensitive internal details.

Do not convert an error into a fake prediction.

---

# 15. Performance Rules

Optimise only after measuring actual performance.

Priorities:

1. Avoid repeated model loading.
2. Avoid unnecessary frame processing.
3. Use suitable image or video sizes.
4. Avoid unnecessary memory copies.
5. Use GPU acceleration when supported.
6. Process frames at a controlled rate.
7. Keep inference and API response handling efficient.
8. Monitor memory usage.

Do not sacrifice prediction correctness for speed without measuring the impact.

---

# 16. Testing Rules

Every AI module must have tests where practical.

Required testing areas:

- Model loading.
- Input validation.
- Preprocessing.
- Landmark extraction.
- Input shape validation.
- Inference.
- Postprocessing.
- API integration.
- Error handling.
- CPU execution.
- CUDA execution when available.

Use mock models for API tests when actual model weights are unavailable.

Do not report mock-model tests as real AI model validation.

---

# 17. Model and File Management

Keep large model files outside Git.

Recommended approach:

```text
models/
├── README.md
├── checkpoints/
└── configs/
```

### Rules

- Do not commit large checkpoints.
- Do not commit downloaded model caches.
- Do not delete existing weights without inspecting them.
- Keep download instructions documented.
- Store model paths in configuration.
- Never hardcode private tokens.
- Do not upload restricted datasets or weights without checking their licences.

Use `.gitignore` for local model files and temporary experiment outputs.

---

# 18. AI/ML Development Workflow

Follow this implementation order:

### Phase 1: Research

- Identify candidate pretrained models.
- Verify ISL support.
- Inspect model architecture.
- Inspect input requirements.
- Check model licence.

### Phase 2: Standalone Testing

- Download a suitable checkpoint.
- Set up the environment.
- Test model loading.
- Test preprocessing.
- Run standalone inference.
- Record results.

### Phase 3: Evaluation

- Use compatible samples.
- Compare predictions with ground truth.
- Record relevant metrics.
- Identify limitations.

### Phase 4: Modular Integration

- Create or reuse a model adapter.
- Implement model loading.
- Implement preprocessing.
- Implement inference.
- Implement postprocessing.

### Phase 5: Backend Integration

- Connect the AI service to FastAPI.
- Add validation.
- Add error handling.
- Test API responses.

### Phase 6: Frontend Integration

- Connect the frontend to the backend.
- Send supported inputs.
- Display actual predictions.
- Show processing and error states.

---

# 19. Strict Rules for Antigravity

Before changing AI/ML code:

1. Inspect the existing project structure.
2. Read the relevant model documentation.
3. Check existing preprocessing and inference code.
4. Reuse working implementations.
5. Avoid duplicate modules.
6. Do not delete datasets, checkpoints, or experiments without approval.
7. Do not change model architecture without a clear reason.
8. Do not invent model capabilities.
9. Do not generate fake predictions.
10. Do not claim successful testing without running it.
11. Do not install unnecessary dependencies.
12. Keep code modular and maintainable.
13. Keep project files and comments in English.
14. Update relevant documentation when implementation changes.

If model compatibility is uncertain, stop and report the uncertainty instead of silently implementing an assumption.

---

# 20. Final AI/ML Goal

The AI system must provide genuine, testable ISL recognition capabilities.

The priority is:

1. Correct model selection.
2. Verified input compatibility.
3. Correct preprocessing.
4. Reliable inference.
5. Honest evaluation.
6. Modular backend integration.
7. Practical performance.

**Correctness and verified ISL support are more important than adding unsupported features or making inaccurate claims.**