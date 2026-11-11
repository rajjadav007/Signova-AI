# Database Schema

## Signova AI

**Project:** Signova AI  
**Database:** PostgreSQL  
**Status:** Planned, optional for MVP  
**Version:** 1.0

---

# 1. Overview

This document defines the proposed database structure for Signova AI.

The database may support:

- User accounts.
- Recognition history.
- Saved predictions.
- Model information.
- User preferences.
- Application activity records.

The initial MVP does not require persistent database storage. Recognition should work directly through the FastAPI backend and AI inference pipeline.

PostgreSQL can be introduced when persistent features are implemented.

## 1.1 Database Strategy

| Feature | MVP requirement |
|---|---|
| Live sign recognition | No database required |
| Model inference | No database required |
| Text output | No database required |
| Text-to-speech | No database required |
| User accounts | Future feature |
| Recognition history | Future feature |
| Saved translations | Future feature |
| User preferences | Future feature |
| Model registry | Initially configuration-based |

**Important:** Do not introduce database dependencies into the recognition pipeline unless a real requirement exists.

---

# 2. Database Technology

| Component | Technology |
|---|---|
| Database | PostgreSQL |
| Query layer | SQLAlchemy |
| Migrations | Alembic |
| Data validation | Pydantic |
| Backend | FastAPI |
| Primary key | UUID |
| Timestamp | TIMESTAMPTZ |

---

# 3. Entity Relationship Overview

The planned database contains four main entities:

1. Users
2. Recognition History
3. AI Models
4. User Preferences

Relationship overview:

```text
USERS
  |
  | 1
  |
  | N
RECOGNITION_HISTORY
  |
  | N
  |
  | 1
AI_MODELS


USERS
  |
  | 1
  |
  | 1
USER_PREFERENCES
```

A user can have multiple recognition records.

Each recognition record can reference the model used for inference.

Each user can have one preference record.

---

# 4. Database Tables

## 4.1 Users

**Table:** `users`

Stores registered user information if authentication is introduced.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | User identifier |
| `email` | VARCHAR(255) | Unique, Not Null | User email |
| `display_name` | VARCHAR(100) | Nullable | Display name |
| `password_hash` | TEXT | Nullable | Hashed password, if locally managed |
| `is_active` | BOOLEAN | Default TRUE | Account status |
| `created_at` | TIMESTAMPTZ | Not Null | Account creation time |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update time |

Notes:

- Never store plain-text passwords.
- If external authentication is used, store the external provider's user identifier instead of managing passwords locally.
- Authentication is not required for the initial MVP.

## 4.2 AI Models

**Table:** `ai_models`

Stores metadata about evaluated and integrated AI models.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Model identifier |
| `model_key` | VARCHAR(100) | Unique, Not Null | Internal model key |
| `name` | VARCHAR(255) | Not Null | Model name |
| `version` | VARCHAR(50) | Nullable | Model version |
| `task_type` | VARCHAR(50) | Not Null | Recognition task |
| `architecture` | VARCHAR(100) | Nullable | Model architecture |
| `checkpoint_reference` | TEXT | Nullable | Checkpoint identifier or reference |
| `model_status` | VARCHAR(30) | Not Null | Model evaluation status |
| `license` | VARCHAR(100) | Nullable | Model licence |
| `created_at` | TIMESTAMPTZ | Not Null | Record creation time |

Possible `task_type` values:

- `static_sign`
- `dynamic_sign`
- `pose_to_text`
- `continuous_translation`

Possible `model_status` values:

- `research`
- `experimental`
- `available`
- `unavailable`
- `rejected`

The iSign T5 candidate should initially be recorded as `experimental`.

Model weights must remain in local or external model storage. Do not store checkpoint binaries in PostgreSQL.

## 4.3 Recognition History

**Table:** `recognition_history`

Stores recognition results when users choose to save their history.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Recognition record ID |
| `user_id` | UUID | Foreign Key, Nullable | User who initiated recognition |
| `model_id` | UUID | Foreign Key, Nullable | Model used |
| `input_type` | VARCHAR(30) | Not Null | Image, video, or landmarks |
| `recognition_type` | VARCHAR(50) | Not Null | Recognition task |
| `recognized_text` | TEXT | Nullable | Generated or recognised text |
| `confidence` | REAL | Nullable | Confidence when supported |
| `processing_time_ms` | INTEGER | Nullable | Inference duration |
| `status` | VARCHAR(30) | Not Null | Recognition result status |
| `created_at` | TIMESTAMPTZ | Not Null | Recognition time |

Notes:

- `user_id` is nullable to support anonymous recognition if history saving is enabled.
- `model_id` is nullable for results that cannot be linked to a registered model record.
- Confidence must only be stored when the model provides a meaningful confidence value.
- Do not store raw webcam footage by default.
- Recognition history should only be saved with user consent.

## 4.4 User Preferences

**Table:** `user_preferences`

Stores user-specific application settings.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Preference record ID |
| `user_id` | UUID | Unique, Foreign Key | User identifier |
| `speech_enabled` | BOOLEAN | Default TRUE | Enable speech output |
| `speech_rate` | REAL | Default 1.0 | Speech playback rate |
| `save_history` | BOOLEAN | Default FALSE | Save recognition history |
| `theme` | VARCHAR(20) | Default `system` | Interface theme |
| `created_at` | TIMESTAMPTZ | Not Null | Creation time |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update time |

Possible theme values:

- `light`
- `dark`
- `system`

Preferences are optional and should only be introduced when user accounts are implemented.

---

# 5. Relationships

| Parent table | Child table | Relationship |
|---|---|---|
| `users` | `recognition_history` | One-to-many |
| `ai_models` | `recognition_history` | One-to-many |
| `users` | `user_preferences` | One-to-one |

Foreign key behaviour:

- Deleting a user should delete their preferences.
- Recognition history should follow the application's retention and privacy policy.
- Model records referenced by recognition history should not be deleted casually.
- Prefer marking obsolete models as unavailable rather than deleting their records.

---

# 6. PostgreSQL SQL Schema

The following SQL represents the proposed future database structure.

It is not required for the initial MVP.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    password_hash TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ai_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_key VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    task_type VARCHAR(50) NOT NULL,
    architecture VARCHAR(100),
    checkpoint_reference TEXT,
    model_status VARCHAR(30) NOT NULL DEFAULT 'research',
    license VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE recognition_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    model_id UUID REFERENCES ai_models(id) ON DELETE SET NULL,
    input_type VARCHAR(30) NOT NULL,
    recognition_type VARCHAR(50) NOT NULL,
    recognized_text TEXT,
    confidence REAL,
    processing_time_ms INTEGER,
    status VARCHAR(30) NOT NULL DEFAULT 'completed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL
        REFERENCES users(id) ON DELETE CASCADE,
    speech_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    speech_rate REAL NOT NULL DEFAULT 1.0,
    save_history BOOLEAN NOT NULL DEFAULT FALSE,
    theme VARCHAR(20) NOT NULL DEFAULT 'system',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# 7. Indexing Strategy

Indexes should be added when persistent database features are implemented.

```sql
CREATE INDEX idx_recognition_user_id
ON recognition_history(user_id);

CREATE INDEX idx_recognition_model_id
ON recognition_history(model_id);

CREATE INDEX idx_recognition_created_at
ON recognition_history(created_at DESC);

CREATE INDEX idx_ai_models_status
ON ai_models(model_status);
```

These indexes support:

- Retrieving a user's recognition history.
- Filtering recognition records by model.
- Sorting history by date.
- Finding available or experimental models.

---

# 8. Data Validation Rules

The backend should validate all values before database insertion.

| Field | Validation |
|---|---|
| Email | Valid email format |
| Model key | Non-empty identifier |
| Task type | Allowed task value |
| Input type | Supported input type |
| Confidence | Nullable, within 0 to 1 when applicable |
| Processing time | Non-negative integer |
| Speech rate | Positive number within configured limits |
| Theme | `light`, `dark`, or `system` |
| Model status | Allowed status value |

Database constraints should reinforce application-level validation.

---

# 9. Data Privacy and Retention

Signova AI processes camera input, which may contain sensitive personal information.

Privacy requirements:

- Do not save webcam frames automatically.
- Do not save raw video by default.
- Save recognition history only when enabled by the user.
- Avoid storing unnecessary personal information.
- Protect account information.
- Hash locally managed passwords securely.
- Provide a way to delete saved recognition history.
- Apply an appropriate retention policy.
- Do not store API keys in database records.

---

# 10. Database Integration Architecture

When database functionality is introduced:

```text
React Frontend
      |
      v
FastAPI Backend
      |
      +------------------+
      |                  |
      v                  v
AI Service          Database Service
      |                  |
      v                  v
Model Inference     PostgreSQL
      |                  |
      +--------+---------+
               |
               v
         API Response
```

The AI inference pipeline must continue to work independently of PostgreSQL.

A database outage should not prevent basic recognition when the feature does not require persistent storage.

---

# 11. Implementation Phases

| Phase | Database work | Priority |
|---|---|---|
| MVP | No database required | Current |
| Phase 2 | PostgreSQL setup | Optional |
| Phase 2 | SQLAlchemy and Alembic | Optional |
| Phase 3 | User authentication | Future |
| Phase 3 | Recognition history | Future |
| Phase 3 | User preferences | Future |
| Phase 4 | Model metadata persistence | Future |

Do not implement all database tables before the corresponding application features exist.

---

# 12. Development Rules

1. Keep the AI inference pipeline independent of the database.
2. Use PostgreSQL only when persistent storage is required.
3. Use UUID identifiers.
4. Use UTC-aware timestamps.
5. Never store plain-text passwords.
6. Never store raw webcam footage by default.
7. Validate data before insertion.
8. Use database migrations for schema changes.
9. Avoid storing model checkpoint binaries in PostgreSQL.
10. Follow user consent and data retention requirements.
11. Do not create unnecessary tables.
12. Keep database access inside a dedicated service or repository layer.

---

# 13. Final Database Strategy

The initial Signova AI hackathon MVP should run without PostgreSQL.

The priority is to complete the following:

1. FastAPI backend.
2. Pretrained ISL model integration.
3. Image, video, or landmark inference as supported.
4. Frontend integration.
5. Text and speech output.

PostgreSQL should be introduced only when features such as user accounts, saved recognition history, or persistent preferences are required.

**Database decision:** PostgreSQL is the planned future database, not an MVP dependency.