# AI and Machine Learning Development Rules

# Signova AI

These rules apply to all AI and machine learning development in Signova AI, including pretrained model selection, model integration, computer vision, gesture recognition, preprocessing, inference, evaluation, optimisation, and deployment.

The primary objective is to build a reliable Indian Sign Language (ISL) recognition system using suitable pretrained models.

---

## 1. AI/ML Project Overview

**Project:** Signova AI

**Primary Objective:** Recognise supported Indian Sign Language gestures using camera input and convert recognised gestures into readable text and optional speech output.

### Core AI Capabilities

- Camera-based sign gesture recognition.
- Static ISL gesture recognition.
- Dynamic ISL sign recognition, when supported by the selected model.
- Prediction confidence handling.
- Recognition result processing.
- Text output.
- Optional text-to-speech integration.

### Important Scope

Signova AI must distinguish between:

1. Static gesture classification.
2. Dynamic sign recognition.
3. Continuous sign language interpretation.

These are different machine learning tasks.

Do not claim that the application supports complete continuous ISL translation unless the selected model and implemented pipeline genuinely provide that capability.

---

## 2. AI/ML Technology Stack

Use the following technologies where required.

| Category | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Deep Learning | PyTorch |
| Computer Vision | OpenCV |
| Hand Landmark Detection | MediaPipe, when required |
| Numerical Computing | NumPy |
| Data Processing | Pandas |
| Machine Learning Utilities | scikit-learn |
| Model Hosting | Hugging Face, when suitable |
| Model Inference | PyTorch |
| API Integration | FastAPI |
| Testing | Pytest |

### Rules

- Use the existing project environment.
- Check package compatibility before installation.
- Do not introduce unnecessary ML frameworks.
- Do not replace PyTorch without approval.
- Keep model inference separate from backend API routes.
- Use pretrained models wherever possible for the initial prototype.

---

## 3. AI Development Principles

Follow these principles throughout AI development:

1. Prefer verified pretrained models over training from scratch.
2. Prioritise actual ISL support.
3. Verify model architecture before integration.
4. Preserve the original preprocessing pipeline.
5. Maintain correct class labels.
6. Measure actual model performance.
7. Handle uncertain predictions.
8. Avoid unsupported AI claims.
9. Keep model integration reproducible.
10. Document all model limitations.

### Strict Rules

- Never invent model accuracy.
- Never invent model capabilities.
- Never claim a model is pretrained without verifying its checkpoint.
- Never claim real-time inference without measuring it.
- Never treat ASL recognition as ISL recognition.
- Never assume a model supports all ISL signs.
- Never train a new model from scratch unless explicitly approved.

---

## 4. Model Selection Strategy

Model selection must be based on the actual requirements of Signova AI.

Before selecting a model, identify whether the required feature involves:

- Static alphabet recognition.
- Static word or gesture recognition.
- Dynamic word recognition.
- Continuous sign sequence interpretation.

### Model Evaluation Criteria

Evaluate candidate models using:

| Criterion | What to Verify |
|---|---|
| ISL Support | Does the model genuinely support Indian Sign Language? |
| Recognition Type | Static, dynamic, or continuous |
| Model Architecture | CNN, LSTM, Transformer, or other architecture |
| Pretrained Weights | Is a usable checkpoint available? |
| Input Format | Image, landmarks, or video sequence |
| Preprocessing | Resize, normalisation, landmarks, or frame sampling |
| Class Labels | Exact supported signs |
| Model Size | Storage requirements |
| Dependencies | Python and framework compatibility |
| Hardware | CPU, CUDA, and memory requirements |
| Licence | Permitted usage and redistribution |
| Evaluation | Verified metrics and test methodology |

### Selection Rules

- Prefer models with accessible pretrained weights.
- Prefer models with reproducible inference instructions.
- Prefer models with clearly documented preprocessing.
- Prefer models that match the MVP requirements.
- Avoid models with missing checkpoints.
- Avoid models with unclear licences.
- Avoid integrating multiple models without a clear purpose.

Do not select a model only because its GitHub repository has many stars.

---

## 5. ASL vs ISL Verification

This distinction is mandatory.

**ASL:** American Sign Language.

**ISL:** Indian Sign Language.

They are different sign languages and cannot be treated as interchangeable.

### Rules

- Verify the language supported by every candidate model.
- Inspect the training dataset.
- Inspect the class labels.
- Inspect the model documentation.
- Verify the source of pretrained weights.
- Do not use an ASL model as the primary ISL recognition model.
- Do not rename ASL labels and present them as ISL labels.

### Previously Referenced Model

The following model was previously considered:

`prithivMLmods/Alphabet-Sign-Language-Detection`

This is an ASL-oriented alphabet recognition model. It must not be presented as an ISL model.

It may be used for an isolated technical experiment only if clearly labelled as ASL.

---

## 6. Candidate Model Research

Previously discussed candidate repositories include:

### Candidate 1: Indian Sign Language Recognition

Repository:

https://github.com/Dhawal-17/indian_sign_language

Potential use:

- Static ISL alphabet recognition.
- Pretrained image classification, if verified.

Repository-reported architecture and accuracy must be independently checked before use.

### Candidate 2: SignBridge

Repository:

https://github.com/Uni-Creator/signBridge

Model:

https://huggingface.co/Creator-090/isl-swin3d-model

Potential use:

- Dynamic ISL word recognition.
- Video sequence-based recognition.

Repository-reported architecture, class count, and evaluation metrics must be verified from the original source and model files.

### Candidate 3: MediaPipe

Repository:

https://github.com/google-ai-edge/mediapipe

Potential use:

- Hand landmark extraction.
- Pose or landmark preprocessing.
- Input preparation for compatible models.

MediaPipe is a computer vision and landmark-processing framework. It is not, by itself, a complete ISL translation model.

### Candidate Research Rules

Before using any candidate:

1. Inspect the repository.
2. Read the README.
3. Identify the architecture.
4. Locate pretrained weights.
5. Inspect the training configuration if available.
6. Verify the dataset.
7. Verify preprocessing.
8. Check licence.
9. Run inference independently.
10. Record verified limitations.

Do not treat candidate models as approved or integrated until these checks are completed.

---

## 7. Pretrained Model Integration

The initial prototype should prioritise pretrained models.

### Required Integration Workflow

```text
Model Research
      |
      v
Repository Verification
      |
      v
Checkpoint Verification
      |
      v
Dependency Installation
      |
      v
Preprocessing Verification
      |
      v
Independent Inference Test
      |
      v
Output and Label Verification
      |
      v
Backend Integration
      |
      v
Frontend Integration
      |
      v
End-to-End Testing
```

### Integration Rules

- Do not train from scratch by default.
- Do not assume model weights are available.
- Do not assume a GitHub repository is a Python package.
- Do not change the model architecture unnecessarily.
- Do not change checkpoint keys without understanding the architecture.
- Do not replace preprocessing with an unrelated pipeline.
- Do not modify class ordering without verification.
- Do not silently substitute another model if loading fails.

### Independent Testing

Before integrating a model into FastAPI, create a standalone inference test.

The test should verify:

- Model initialisation.
- Checkpoint loading.
- Input dimensions.
- Preprocessing.
- Forward pass.
- Output dimensions.
- Class mapping.
- Prediction generation.

The model must work independently before being connected to the application.

---

## 8. Model Architecture Rules

Understand the selected model architecture before writing integration code.

Possible architectures include:

- CNN.
- MobileNet.
- ResNet.
- Vision Transformer.
- 3D CNN.
- LSTM.
- GRU.
- Transformer Encoder.
- Transformer Decoder.
- Hybrid architectures.

### Rules

- Read the original architecture implementation.
- Match the checkpoint to the correct architecture.
- Preserve expected layer dimensions.
- Understand the model's input and output.
- Avoid rewriting a working architecture without reason.
- Document architecture modifications.
- Test checkpoint compatibility.

### Keypoint-Based Models

Some sign recognition systems use landmark coordinates rather than raw images.

If the selected model expects landmarks:

1. Identify the landmark extraction method.
2. Identify required body and hand landmarks.
3. Verify coordinate ordering.
4. Verify normalisation.
5. Verify sequence length.
6. Verify missing landmark handling.
7. Reproduce the original feature construction.

Do not pass raw camera images directly to a keypoint-based model.

### Image-Based Models

If the model expects images:

1. Verify image dimensions.
2. Verify colour channel ordering.
3. Verify pixel normalisation.
4. Verify image orientation.
5. Verify tensor dimensions.
6. Verify batch dimensions.

Do not pass landmark vectors into an image-based model.

---

## 9. Static Gesture Recognition

Static gesture recognition uses an individual image or frame to classify a sign.

### Potential Pipeline

```text
Camera Frame
     |
     v
Image Validation
     |
     v
Image Preprocessing
     |
     v
Classification Model
     |
     v
Class Probabilities
     |
     v
Prediction Processing
     |
     v
Recognised Sign
```

### Rules

- Use the model's expected image size.
- Apply the original normalisation.
- Preserve the correct class mapping.
- Handle unsupported inputs.
- Handle low-confidence results.
- Avoid displaying repeated predictions unnecessarily.

### Limitations

Static recognition cannot automatically interpret movement-based signs or connected sign sequences.

Do not describe static alphabet recognition as complete ISL translation.

---

## 10. Dynamic Sign Recognition

Dynamic sign recognition requires temporal information.

It may use:

- Video frames.
- Hand landmark sequences.
- Pose sequences.
- Motion features.
- Temporal neural networks.

### Potential Pipeline

```text
Camera Stream
      |
      v
Frame Sampling
      |
      v
Frame or Landmark Extraction
      |
      v
Sequence Preparation
      |
      v
Dynamic Recognition Model
      |
      v
Temporal Prediction
      |
      v
Recognised Sign
```

### Rules

- Preserve frame ordering.
- Match the expected sequence length.
- Follow the model's sampling strategy.
- Handle incomplete sequences.
- Handle missing frames.
- Avoid mixing unrelated sign sequences.
- Verify prediction stability.
- Test with multiple signing examples.

Do not convert a dynamic model into a static classifier without a valid technical reason.

---

## 11. Continuous ISL Interpretation

Continuous sign language interpretation is more complex than isolated sign recognition.

It may require:

- Continuous video processing.
- Sign segmentation.
- Temporal feature extraction.
- Sequence recognition.
- Language modelling.
- Context handling.
- Sentence generation.

### Mandatory Rules

- Do not claim continuous translation unless implemented.
- Do not combine isolated predictions and call them a translated sentence without validation.
- Do not invent grammar or sentence structure.
- Preserve uncertainty when recognition is ambiguous.
- Clearly communicate unsupported signs.
- Document the actual supported recognition scope.

For the MVP, prioritise reliable recognition of a limited set of supported signs over an unverified claim of complete ISL translation.

---

## 12. Computer Vision and MediaPipe Rules

MediaPipe may be used when the selected model requires landmark-based input.

### Rules

- Use the landmark task required by the model.
- Verify the required number of landmarks.
- Preserve landmark ordering.
- Verify coordinate conventions.
- Handle missing or invisible landmarks.
- Match the original preprocessing method.
- Avoid unnecessary landmark extraction.
- Measure landmark processing latency.

### Important

MediaPipe does not automatically understand the meaning of an ISL gesture.

It extracts visual information. A suitable recognition model is still required to classify or interpret that information.

Do not introduce MediaPipe if the selected model uses raw images and does not need landmark extraction.

---

## 13. Dataset Rules

Dataset quality directly affects recognition reliability.

Before using a dataset, document:

- Dataset name.
- Dataset source.
- Licence.
- Sign language.
- Number of classes.
- Number of samples.
- Data format.
- Annotation format.
- Collection method.
- Known limitations.
- Train, validation, and test split strategy.

### Dataset Requirements

- Prefer verified ISL datasets.
- Verify that labels match the actual signs.
- Check for missing annotations.
- Check for corrupted samples.
- Check for duplicate samples.
- Check class imbalance.
- Check signer distribution.
- Avoid mixing ASL and ISL labels.
- Avoid using private recordings without consent.

### Data Leakage Prevention

- Avoid placing near-identical frames from the same recording across training and testing sets.
- Use signer-independent evaluation when possible.
- Keep test data separate from model selection.
- Document the splitting method.

Do not claim generalisation to unseen signers if evaluation does not test it.

---

## 14. Data Preprocessing Rules

Preprocessing must match the model's training pipeline.

Possible operations:

- Image resizing.
- Image normalisation.
- Colour conversion.
- Landmark extraction.
- Landmark normalisation.
- Frame sampling.
- Sequence padding.
- Tensor conversion.
- Invalid sample filtering.

### Strict Rules

- Do not invent normalisation values.
- Do not randomly change image sizes.
- Do not reorder features.
- Do not remove required landmarks.
- Do not change sequence length without checking the model.
- Do not apply training augmentation during normal inference unless specified.
- Keep preprocessing reproducible.

### Reproducibility

Document:

- Input dimensions.
- Colour format.
- Normalisation values.
- Landmark format.
- Sequence length.
- Sampling interval.
- Padding method.
- Output tensor shape.

Create tests for preprocessing independently of the model.

---

## 15. Model Loading and Checkpoint Management

Model loading must be reliable and secure.

### Rules

- Load the model once when practical.
- Use configurable checkpoint paths.
- Validate checkpoint existence.
- Validate architecture compatibility.
- Handle missing weights gracefully.
- Avoid repeated loading per request.
- Keep model configuration documented.
- Do not commit large checkpoints without approval.

### Security

- Prefer Safetensors where supported.
- Avoid loading untrusted pickle-based checkpoints.
- Use `torch.load(..., weights_only=True)` when compatible with the checkpoint format and PyTorch version.
- Inspect third-party model code before executing it.
- Do not download and execute arbitrary scripts.
- Verify file sources and integrity where possible.

### File Organisation

A possible structure:

```text
backend/
├── models/
│   ├── README.md
│   └── .gitkeep
│
├── app/
│   └── ml/
│       ├── model_loader.py
│       ├── preprocessing.py
│       ├── inference.py
│       └── postprocessing.py
│
└── tests/
    └── test_model_inference.py
```

Adapt this structure to the existing repository.

---

## 16. Prediction and Confidence Handling

Raw model output must be processed before returning a prediction to the frontend.

### Responsibilities

- Identify the predicted class.
- Map class indices to labels.
- Calculate confidence when supported.
- Apply an evaluated threshold when appropriate.
- Detect unsupported or uncertain predictions.
- Return a structured result.

### Rules

- Never invent a prediction.
- Never invent a confidence score.
- Never assume model confidence equals actual accuracy.
- Do not present low-confidence output as confirmed.
- Do not use arbitrary confidence thresholds without evaluation.
- Keep thresholds configurable where appropriate.
- Handle unknown signs explicitly.

### Example Result

```json
{
  "label": "Example sign",
  "confidence": 0.91,
  "status": "recognised"
}
```

This is an illustrative structure only. Use it only if the model and backend actually provide these fields.

---

## 17. Model Evaluation

Evaluate every selected model before claiming that it is suitable.

### Classification Metrics

Use appropriate metrics:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Per-class performance.
- Confusion matrix.

For imbalanced classes, do not rely on accuracy alone.

### Dynamic Recognition

Where relevant, evaluate:

- Sequence-level accuracy.
- Word error rate.
- Sign error rate.
- Segmentation quality.
- Per-class recognition performance.

Use metrics that match the actual task.

### Performance Metrics

Measure:

- Model loading time.
- Preprocessing latency.
- Inference latency.
- End-to-end response time.
- Memory usage.
- GPU usage, when available.

### Evaluation Rules

- Document the test dataset.
- Document the evaluation split.
- Document the evaluation method.
- Record actual results.
- Do not copy repository-reported metrics as your own results.
- Do not compare metrics from different datasets as if directly equivalent.
- Never invent benchmark results.

---

## 18. Hardware and Device Compatibility

The application should support practical inference on available hardware.

Possible devices:

- CPU.
- NVIDIA CUDA GPU.

### Rules

- Check CUDA availability.
- Do not assume deployment has a GPU.
- Provide CPU compatibility where practical.
- Check available VRAM.
- Check system RAM.
- Avoid unnecessary model duplication.
- Monitor memory usage.
- Measure actual inference performance.

Example:

```python
import torch


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")
```

### GPU Rules

- Do not assume every PyTorch installation supports CUDA.
- Verify the installed PyTorch build.
- Verify driver compatibility.
- Avoid loading models larger than available memory.
- Use evaluation and inference modes appropriately.

---

## 19. Model Optimisation

Optimise only after establishing a working baseline.

Potential techniques:

- Batch processing.
- Frame sampling.
- Model quantisation.
- Mixed precision, where supported.
- TorchScript, where compatible.
- ONNX export, where useful.
- Efficient image preprocessing.
- Reduced unnecessary data transfer.

### Rules

- Preserve prediction correctness.
- Compare optimised and original outputs.
- Measure performance before and after optimisation.
- Verify hardware compatibility.
- Document any accuracy trade-off.
- Avoid optimisation that makes the MVP less reliable.

Do not introduce complex optimisation techniques without a measured need.

---

## 20. Real-Time Recognition Rules

Real-time recognition should only be implemented when the model and hardware can support it.

### Requirements

- Avoid processing every camera frame unnecessarily.
- Use controlled frame sampling.
- Prevent unbounded processing queues.
- Avoid repeated model initialisation.
- Handle slow inference.
- Keep prediction updates stable.
- Handle camera disconnection.
- Measure actual end-to-end latency.

### Important

A camera preview running smoothly does not prove that AI recognition is running in real time.

Measure model inference and the complete recognition pipeline separately.

---

## 21. Model Service Integration

Keep AI logic modular.

Recommended responsibilities:

| Module | Responsibility |
|---|---|
| `model_loader.py` | Load model architecture and weights |
| `preprocessing.py` | Prepare model input |
| `inference.py` | Execute model inference |
| `postprocessing.py` | Convert raw outputs into predictions |
| `recognition_service.py` | Coordinate recognition operations |

### Rules

- Do not put model code directly inside API routes.
- Do not return raw PyTorch tensors from API endpoints.
- Convert results into serialisable values.
- Handle model loading failures.
- Handle invalid model inputs.
- Keep services independently testable.

---

## 22. Sarvam AI Integration Rules

Sarvam AI may support optional speech and language features in Signova AI.

Possible uses, depending on available provider capabilities:

- Speech-to-text.
- Text-to-speech.
- Supported language processing.

### Important Separation

Sarvam AI is not the ISL gesture recognition model.

Keep these responsibilities separate:

| Component | Responsibility |
|---|---|
| ISL Recognition Model | Recognise supported sign gestures |
| Preprocessing | Prepare camera input |
| Sarvam Speech Services | Supported speech processing |
| Backend | Coordinate application services |
| Frontend | Camera interface and result display |

### Rules

- Verify current Sarvam API documentation.
- Verify supported models and languages.
- Verify input and output formats.
- Keep API keys on the backend.
- Handle provider errors.
- Check usage limits and pricing.
- Do not claim that Sarvam directly translates camera gestures into ISL meaning unless a verified supported service provides that capability.

---

## 23. Testing Rules

Use Pytest for AI/ML testing.

### Model Loading Tests

- Check checkpoint availability.
- Check architecture compatibility.
- Check device selection.
- Check model initialisation.
- Check model evaluation mode.

### Preprocessing Tests

- Check image dimensions.
- Check colour format.
- Check normalisation.
- Check landmark ordering.
- Check sequence dimensions.
- Check invalid input handling.

### Inference Tests

- Check output dimensions.
- Check label mapping.
- Check confidence handling.
- Check unknown input.
- Check inference errors.
- Check CPU execution.
- Check CUDA execution when available.

### Evaluation Tests

- Check metric calculations.
- Check class mapping.
- Check test split integrity.
- Check reproducibility.

### Example Commands

```bash
pytest tests/test_model_inference.py -v
```

Run the actual configured tests. Do not claim success without executing them.

---

## 24. AI/ML Documentation Requirements

Whenever model selection or implementation changes, update relevant documentation.

Relevant files:

- `docs/AI_MODEL_STRATEGY.md`
- `docs/TECH_STACK.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/FEATURES.md`
- `docs/API_DOCUMENTATION.md`
- `docs/TESTING_STRATEGY.md`
- `docs/SECURITY.md`
- `docs/DEPLOYMENT.md`
- `docs/PROGRESS_TRACKER.md`

### Model Documentation Template

For every integrated model, document:

```markdown
## Model Name

### Source
Repository or model URL.

### Sign Language
ISL / ASL / Other.

### Recognition Type
Static / Dynamic / Continuous.

### Architecture
Verified architecture.

### Pretrained Checkpoint
Checkpoint source and format.

### Input
Expected input format and dimensions.

### Preprocessing
Required preprocessing steps.

### Output
Supported labels and output format.

### Dependencies
Required packages and versions.

### Hardware
CPU / CUDA requirements.

### Evaluation
Dataset, split, metrics, and measured results.

### Limitations
Known limitations and unsupported signs.

### Integration Status
Not Started / In Progress / Tested / Integrated.
```

Never mark a model as integrated until inference and application integration have been tested.

---

## 25. Dataset Privacy and Ethical AI

Signova AI is an accessibility project.

Treat sign language data responsibly.

### Rules

- Use datasets with appropriate licences.
- Respect dataset usage restrictions.
- Obtain consent before collecting personal recordings.
- Do not upload private videos without consent.
- Avoid unnecessary personal data collection.
- Avoid identifying individuals from sign recordings.
- Do not claim universal recognition.
- Document known limitations.
- Test with varied signing styles when permitted.
- Avoid making accessibility claims beyond verified capabilities.

### Bias and Reliability

Consider differences in:

- Hand size.
- Skin tone.
- Lighting.
- Camera quality.
- Signing speed.
- Signing style.
- Background.
- Camera angle.
- Left-handed and right-handed signing.

A model should not be described as reliable across all users unless appropriate evaluation supports that claim.

---

## 26. AI Agent Rules for Antigravity

Before making AI/ML changes:

1. Read `AGENTS.md`.
2. Read `docs/AI_MODEL_STRATEGY.md`.
3. Read `docs/SYSTEM_ARCHITECTURE.md`.
4. Read `docs/TECH_STACK.md`.
5. Inspect the existing model implementation.
6. Inspect the checkpoint and configuration.
7. Identify the expected model input and output.
8. Prepare a small implementation plan.
9. Test inference independently.
10. Integrate only after verification.

### Strict Agent Restrictions

- Do not download random models.
- Do not assume GitHub repositories contain pretrained weights.
- Do not use ASL models as ISL models.
- Do not invent model metrics.
- Do not invent class labels.
- Do not change preprocessing without verification.
- Do not retrain models without approval.
- Do not install unnecessary ML libraries.
- Do not add large checkpoints to Git without approval.
- Do not claim continuous ISL translation from static recognition.
- Do not replace a working model without explaining the reason.
- Do not mark untested model integration as complete.

If a model cannot be integrated because its checkpoint, architecture, dependencies, or licence are unavailable, report the blocker and propose verified alternatives.

---

## 27. Definition of Done

An AI/ML task is complete only when:

- [ ] The selected model is verified.
- [ ] ISL support is confirmed.
- [ ] The recognition type is documented.
- [ ] The model architecture is understood.
- [ ] Pretrained weights are available and verified.
- [ ] Preprocessing matches the model requirements.
- [ ] Checkpoint loading works.
- [ ] Inference works independently.
- [ ] Class labels are correctly mapped.
- [ ] Confidence handling is implemented where supported.
- [ ] Relevant tests are executed.
- [ ] Performance is measured where required.
- [ ] Backend integration is tested.
- [ ] Limitations are documented.
- [ ] Relevant documentation is updated.

---

## 28. Final AI/ML Principle

Signova AI must prioritise reliable Indian Sign Language recognition over unnecessary model complexity.

The development priorities are:

1. Verified ISL pretrained model.
2. Correct preprocessing.
3. Reliable model inference.
4. Accurate prediction mapping.
5. Honest confidence handling.
6. Practical performance.
7. Secure model integration.
8. Tested backend and frontend connection.
9. Clear documentation of limitations.

**Build only what the selected model can genuinely support. Accuracy, reliability, accessibility, and honest reporting are more important than claiming advanced AI capabilities.**