# Signova AI: Database Schema

## 1. Overview

This document defines the database architecture and schema for Signova AI.

Signova AI uses PostgreSQL as its relational database for managing user accounts, preferences, conversation sessions, recognised text, and optional learning progress.

The database is designed to support the application's future expansion without making database storage a requirement for the initial AI recognition pipeline.

### Database Objectives

- Store user information securely.
- Manage user preferences.
- Maintain conversation sessions.
- Store recognised text when users opt in.
- Maintain conversation message history.
- Support learning resources and progress.
- Maintain data relationships and integrity.
- Support future application expansion.
- Minimise unnecessary personal data collection.

### Technology

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational database |
| SQLAlchemy | Python ORM |
| Alembic | Database migrations |
| Pydantic | Request and response validation |
| UUID | Record identifiers |
| FastAPI | Backend integration |

---

# 2. Database Design Principles

The database will follow these principles:

### 2.1 Data Integrity

- Use primary keys.
- Use foreign keys.
- Apply unique constraints.
- Apply appropriate NOT NULL constraints.
- Validate relationships.
- Prevent orphan records.

### 2.2 Security

- Never store plaintext passwords.
- Protect user-owned records.
- Keep credentials outside source code.
- Avoid storing raw camera footage.
- Avoid storing raw audio unless explicitly required.
- Use secure database connections in production.

### 2.3 Scalability

- Use UUID identifiers.
- Add indexes for frequently queried fields.
- Separate user, conversation, and message data.
- Avoid unnecessary duplicated information.
- Use pagination for history endpoints.

### 2.4 Privacy

- Store only necessary information.
- Provide history deletion.
- Define data retention policies.
- Request consent before storing conversation content.
- Do not store camera images or video by default.

---

# 3. Database Architecture

The application follows a modular database architecture.

```text
FastAPI Backend
      |
      v
Database Service
      |
      v
SQLAlchemy ORM
      |
      v
PostgreSQL
      |
      ├── users
      |
      ├── user_preferences
      |
      ├── conversations
      |
      ├── messages
      |
      ├── model_registry
      |
      ├── recognition_logs (Optional)
      |
      ├── learning_resources
      |
      └── user_learning_progress
```

### Database Responsibilities

| Module | Responsibility |
|---|---|
| Users | Account information |
| User Preferences | Application preferences |
| Conversations | Communication sessions |
| Messages | Text and recognition results |
| Model Registry | Approved model metadata |
| Recognition Logs | Optional technical monitoring |
| Learning Resources | ISL learning content |
| Learning Progress | User learning activity |

Not all tables need to be created in the initial development phase.

---

# 4. Database Configuration

### Database Name

```text
signova_ai
```

### Development Connection

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/signova_ai
```

Use actual local database credentials in the private `.env` file.

### Production Connection

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/signova_ai
```

Production credentials must be provided by the selected hosting platform.

### Database Rules

- Never commit `.env`.
- Use `.env.example` for configuration templates.
- Use a separate development database.
- Use a separate production database.
- Use migrations for schema changes.
- Do not modify production tables manually without a migration plan.

---

# 5. Entity Relationship Diagram

The following diagram represents the proposed relationships.

```mermaid
erDiagram
    USERS ||--o| USER_PREFERENCES : has
    USERS ||--o{ CONVERSATIONS : creates
    CONVERSATIONS ||--o{ MESSAGES : contains
    USERS ||--o{ RECOGNITION_LOGS : generates
    USERS ||--o{ USER_LEARNING_PROGRESS : tracks
    LEARNING_RESOURCES ||--o{ USER_LEARNING_PROGRESS : records
    MODEL_REGISTRY ||--o{ RECOGNITION_LOGS : uses

    USERS {
        UUID id PK
        VARCHAR email UK
        VARCHAR password_hash
        VARCHAR display_name
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    USER_PREFERENCES {
        UUID id PK
        UUID user_id FK
        VARCHAR theme
        VARCHAR preferred_language
        BOOLEAN speech_enabled
        TIMESTAMP updated_at
    }

    CONVERSATIONS {
        UUID id PK
        UUID user_id FK
        VARCHAR conversation_type
        VARCHAR source_language
        VARCHAR target_language
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    MESSAGES {
        UUID id PK
        UUID conversation_id FK
        VARCHAR message_type
        TEXT content
        VARCHAR language_code
        JSONB metadata
        TIMESTAMP created_at
    }

    MODEL_REGISTRY {
        UUID id PK
        VARCHAR model_name
        VARCHAR model_version
        VARCHAR recognition_type
        VARCHAR status
        TIMESTAMP created_at
    }

    RECOGNITION_LOGS {
        UUID id PK
        UUID user_id FK
        UUID model_id FK
        VARCHAR prediction_label
        FLOAT confidence
        INTEGER processing_time_ms
        TIMESTAMP created_at
    }

    LEARNING_RESOURCES {
        UUID id PK
        VARCHAR title
        VARCHAR category
        TEXT description
        VARCHAR resource_type
        BOOLEAN is_published
        TIMESTAMP created_at
    }

    USER_LEARNING_PROGRESS {
        UUID id PK
        UUID user_id FK
        UUID resource_id FK
        VARCHAR status
        TIMESTAMP completed_at
    }
```

The relationship diagram describes the intended logical design. Optional tables can be introduced later.

---

# 6. Table 1: Users

**Table name:** `users`

Purpose: Store user account information.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | User identifier |
| `email` | VARCHAR(255) | Unique, Not Null | User email |
| `password_hash` | TEXT | Nullable | Password hash if local authentication is used |
| `display_name` | VARCHAR(100) | Nullable | User display name |
| `auth_provider` | VARCHAR(50) | Nullable | Authentication provider |
| `created_at` | TIMESTAMPTZ | Not Null | Account creation |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update |

### SQL

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash TEXT,

    display_name VARCHAR(100),

    auth_provider VARCHAR(50),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Rules

- Email must be unique.
- Passwords must never be stored in plaintext.
- Use a secure password hashing algorithm if local authentication is implemented.
- External authentication credentials should be handled by the selected identity provider.
- Do not store unnecessary personal information.

If an external identity provider is used, its stable subject identifier should also be stored and uniquely constrained.

---

# 7. Table 2: User Preferences

**Table name:** `user_preferences`

Purpose: Store individual application preferences.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Preference identifier |
| `user_id` | UUID | Foreign Key, Unique | User identifier |
| `theme` | VARCHAR(20) | Not Null | Light or dark theme |
| `preferred_language` | VARCHAR(20) | Not Null | Preferred language code |
| `speech_enabled` | BOOLEAN | Not Null | Speech preference |
| `history_enabled` | BOOLEAN | Not Null | History preference |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update |

### SQL

```sql
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID UNIQUE NOT NULL
        REFERENCES users(id) ON DELETE CASCADE,

    theme VARCHAR(20) NOT NULL DEFAULT 'light'
        CHECK (theme IN ('light', 'dark', 'system')),

    preferred_language VARCHAR(20) NOT NULL DEFAULT 'en-IN',

    speech_enabled BOOLEAN NOT NULL DEFAULT TRUE,

    history_enabled BOOLEAN NOT NULL DEFAULT FALSE,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Rules

- One user has one preference record.
- Theme must be supported.
- Language codes must be validated by the backend.
- Preference changes should update `updated_at`.
- Users must only modify their own preferences.

---

# 8. Table 3: Conversations

**Table name:** `conversations`

Purpose: Store communication session metadata.

A conversation represents one communication session between users or communication modes.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Conversation identifier |
| `user_id` | UUID | Foreign Key | Session owner |
| `conversation_type` | VARCHAR(50) | Not Null | Communication mode |
| `source_language` | VARCHAR(30) | Nullable | Source language |
| `target_language` | VARCHAR(30) | Nullable | Target language |
| `status` | VARCHAR(20) | Not Null | Session status |
| `created_at` | TIMESTAMPTZ | Not Null | Creation time |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update |

### SQL

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id) ON DELETE CASCADE,

    conversation_type VARCHAR(50) NOT NULL
        CHECK (
            conversation_type IN (
                'sign_to_text',
                'sign_to_speech',
                'voice_to_text',
                'multimodal'
            )
        ),

    source_language VARCHAR(30),

    target_language VARCHAR(30),

    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (
            status IN (
                'active',
                'completed',
                'cancelled'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Rules

- Every conversation belongs to a user.
- Conversation ownership must be validated.
- Session status must be valid.
- Only permitted session information should be stored.
- Raw camera video must not be stored by default.

---

# 9. Table 4: Messages

**Table name:** `messages`

Purpose: Store individual messages and text outputs inside conversations.

### Supported Message Types

- `sign_recognition`
- `speech_transcription`
- `translation`
- `text`
- `system`

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Message identifier |
| `conversation_id` | UUID | Foreign Key | Parent conversation |
| `message_type` | VARCHAR(50) | Not Null | Message category |
| `content` | TEXT | Not Null | Message text |
| `language_code` | VARCHAR(30) | Nullable | Language code |
| `metadata` | JSONB | Nullable | Additional structured information |
| `created_at` | TIMESTAMPTZ | Not Null | Message time |

### SQL

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    conversation_id UUID NOT NULL
        REFERENCES conversations(id) ON DELETE CASCADE,

    message_type VARCHAR(50) NOT NULL
        CHECK (
            message_type IN (
                'sign_recognition',
                'speech_transcription',
                'translation',
                'text',
                'system'
            )
        ),

    content TEXT NOT NULL,

    language_code VARCHAR(30),

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Example Message Metadata

```json
{
  "model_name": "isl_static_recognition",
  "model_version": "1.0",
  "confidence": 0.94,
  "recognition_type": "static"
}
```

This metadata is illustrative. Only include fields actually returned by the relevant service.

### Rules

- Every message belongs to a conversation.
- Store recognised text, not raw video frames.
- Store confidence only when available.
- Avoid placing sensitive personal information in metadata.
- Validate the message type.
- Apply history retention rules.

---

# 10. Table 5: Model Registry

**Table name:** `model_registry`

Purpose: Maintain metadata about the AI models used by Signova AI.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Model identifier |
| `model_name` | VARCHAR(150) | Not Null | Model name |
| `model_version` | VARCHAR(50) | Not Null | Model version |
| `recognition_type` | VARCHAR(30) | Not Null | Static or dynamic |
| `architecture` | VARCHAR(100) | Nullable | Architecture |
| `status` | VARCHAR(30) | Not Null | Model status |
| `created_at` | TIMESTAMPTZ | Not Null | Registration time |

### SQL

```sql
CREATE TABLE model_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    model_name VARCHAR(150) NOT NULL,

    model_version VARCHAR(50) NOT NULL,

    recognition_type VARCHAR(30) NOT NULL
        CHECK (
            recognition_type IN (
                'static',
                'dynamic',
                'continuous'
            )
        ),

    architecture VARCHAR(100),

    status VARCHAR(30) NOT NULL DEFAULT 'research'
        CHECK (
            status IN (
                'research',
                'tested',
                'approved',
                'deprecated'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (model_name, model_version)
);
```

### Rules

- Register only identifiable model versions.
- Distinguish research models from approved models.
- Do not store checkpoint binary files in PostgreSQL.
- Store checkpoint metadata or a controlled storage reference separately.
- Record model licence and source in the project documentation or extend the registry when model governance requires it.

---

# 11. Table 6: Recognition Logs

**Table name:** `recognition_logs`

Purpose: Store optional technical information about recognition requests.

This table is useful for monitoring model performance and diagnosing issues.

It is optional and should not be enabled by default if it collects more user data than necessary.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Log identifier |
| `user_id` | UUID | Nullable Foreign Key | User identifier |
| `model_id` | UUID | Foreign Key | Model used |
| `prediction_label` | VARCHAR(100) | Nullable | Predicted label |
| `confidence` | DOUBLE PRECISION | Nullable | Prediction confidence |
| `processing_time_ms` | INTEGER | Nullable | Inference duration |
| `status` | VARCHAR(30) | Not Null | Recognition status |
| `created_at` | TIMESTAMPTZ | Not Null | Log time |

### SQL

```sql
CREATE TABLE recognition_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    model_id UUID NOT NULL
        REFERENCES model_registry(id) ON DELETE RESTRICT,

    prediction_label VARCHAR(100),

    confidence DOUBLE PRECISION
        CHECK (
            confidence IS NULL OR
            confidence BETWEEN 0 AND 1
        ),

    processing_time_ms INTEGER
        CHECK (
            processing_time_ms IS NULL OR
            processing_time_ms >= 0
        ),

    status VARCHAR(30) NOT NULL
        CHECK (
            status IN (
                'recognised',
                'uncertain',
                'unknown',
                'failed'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Rules

- Do not store raw image or video data in this table.
- Avoid unnecessary user identifiers.
- Store only fields required for monitoring.
- Apply a retention period.
- Do not use recognition logs as training data without appropriate consent and governance.

---

# 12. Table 7: Learning Resources

**Table name:** `learning_resources`

Purpose: Store verified ISL learning content.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Resource identifier |
| `title` | VARCHAR(200) | Not Null | Resource title |
| `category` | VARCHAR(100) | Nullable | Resource category |
| `description` | TEXT | Nullable | Resource description |
| `resource_type` | VARCHAR(30) | Not Null | Resource type |
| `content_url` | TEXT | Nullable | Resource location |
| `is_published` | BOOLEAN | Not Null | Publishing status |
| `created_at` | TIMESTAMPTZ | Not Null | Creation time |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update |

### SQL

```sql
CREATE TABLE learning_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(200) NOT NULL,

    category VARCHAR(100),

    description TEXT,

    resource_type VARCHAR(30) NOT NULL
        CHECK (
            resource_type IN (
                'sign',
                'video',
                'article',
                'course',
                'external_link'
            )
        ),

    content_url TEXT,

    is_published BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Rules

- Only publish verified educational content.
- Validate external links.
- Respect content licences.
- Ensure sign descriptions are accurate.
- Do not present ASL learning content as ISL learning content.

---

# 13. Table 8: User Learning Progress

**Table name:** `user_learning_progress`

Purpose: Track learning progress when the learning centre is implemented.

### Columns

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Progress identifier |
| `user_id` | UUID | Foreign Key | User identifier |
| `resource_id` | UUID | Foreign Key | Learning resource |
| `status` | VARCHAR(30) | Not Null | Learning status |
| `completed_at` | TIMESTAMPTZ | Nullable | Completion time |
| `created_at` | TIMESTAMPTZ | Not Null | Creation time |
| `updated_at` | TIMESTAMPTZ | Not Null | Last update |

### SQL

```sql
CREATE TABLE user_learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id) ON DELETE CASCADE,

    resource_id UUID NOT NULL
        REFERENCES learning_resources(id) ON DELETE CASCADE,

    status VARCHAR(30) NOT NULL DEFAULT 'not_started'
        CHECK (
            status IN (
                'not_started',
                'in_progress',
                'completed'
            )
        ),

    completed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (user_id, resource_id)
);
```

### Rules

- One user should have one progress record per learning resource.
- Progress must belong to the authenticated user.
- Only published resources should be available for normal learning activity.
- Completion timestamps should be recorded when a resource is completed.

---

# 14. Database Relationships

| Parent Table | Child Table | Relationship |
|---|---|---|
| users | user_preferences | One-to-One |
| users | conversations | One-to-Many |
| conversations | messages | One-to-Many |
| users | recognition_logs | One-to-Many |
| model_registry | recognition_logs | One-to-Many |
| users | user_learning_progress | One-to-Many |
| learning_resources | user_learning_progress | One-to-Many |

### Relationship Rules

- Deleting a user deletes their preferences and conversations.
- Deleting a conversation deletes its messages.
- Deleting a learning resource removes associated progress records.
- Model registry records referenced by recognition logs should not be deleted casually.
- Recognition log ownership can be anonymised by setting the user reference to NULL when a user is deleted.

---

# 15. Database Indexing Strategy

Indexes improve query performance for commonly accessed records.

### Recommended Indexes

```sql
CREATE INDEX idx_conversations_user_id
ON conversations(user_id);

CREATE INDEX idx_conversations_created_at
ON conversations(created_at DESC);

CREATE INDEX idx_messages_conversation_id
ON messages(conversation_id);

CREATE INDEX idx_messages_created_at
ON messages(created_at DESC);

CREATE INDEX idx_recognition_logs_user_id
ON recognition_logs(user_id);

CREATE INDEX idx_recognition_logs_model_id
ON recognition_logs(model_id);

CREATE INDEX idx_recognition_logs_created_at
ON recognition_logs(created_at DESC);

CREATE INDEX idx_learning_resources_category
ON learning_resources(category);

CREATE INDEX idx_learning_resources_published
ON learning_resources(is_published);

CREATE INDEX idx_learning_progress_user_id
ON user_learning_progress(user_id);
```

### Indexing Rules

- Index frequently filtered columns.
- Index foreign keys used in joins and lookups.
- Avoid unnecessary indexes.
- Review query performance before adding more indexes.
- Use `EXPLAIN ANALYZE` for important database queries.

---

# 16. Database Constraints

Use database constraints to protect data integrity.

### Required Constraints

- Unique email.
- Unique model name and version.
- Unique user preference per user.
- Unique learning progress per user and resource.
- Valid theme values.
- Valid conversation types.
- Valid message types.
- Valid status values.
- Confidence between 0 and 1.
- Non-negative processing time.
- Valid foreign key references.

Validation should exist at both the application and database levels where appropriate.

---

# 17. Data Retention and Privacy

Signova AI processes camera, audio, and communication data. Database storage must follow privacy-first principles.

### 17.1 Camera Data

- Do not store raw camera footage by default.
- Process camera frames for recognition only.
- Do not save images automatically.
- Require clear consent for any future image storage.

### 17.2 Audio Data

- Do not store raw audio by default.
- Store transcription text only when history is enabled.
- Explain when external speech services process audio.
- Avoid unnecessary audio retention.

### 17.3 Conversation Data

- Store history only when the feature is enabled.
- Provide a clear deletion option.
- Restrict access to the owner.
- Apply a documented retention policy.

### 17.4 Recognition Logs

- Keep only required technical information.
- Avoid unnecessary personal identifiers.
- Define a retention period.
- Do not reuse logs as training data without appropriate consent.

### 17.5 Suggested Retention Policy

These are initial policy recommendations and must be reviewed before production.

| Data | Suggested Policy |
|---|---|
| User account | Until account deletion |
| User preferences | Until account deletion |
| Conversation text | Only when history is enabled, with a documented retention period |
| Raw camera video | Not stored by default |
| Raw audio | Not stored by default |
| Recognition logs | Short, documented retention period |
| Learning progress | Until account deletion or user-requested deletion |

---

# 18. SQLAlchemy Model Structure

Recommended backend structure:

```text
backend/app/database/
├── connection.py
├── base.py
├── models/
│   ├── user.py
│   ├── user_preferences.py
│   ├── conversation.py
│   ├── message.py
│   ├── model_registry.py
│   ├── recognition_log.py
│   ├── learning_resource.py
│   └── learning_progress.py
│
└── repositories/
    ├── user_repository.py
    ├── conversation_repository.py
    ├── message_repository.py
    └── learning_repository.py
```

Create only the models required for the current implementation.

### Example SQLAlchemy Base

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

### Example Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
```

### Example Database Dependency

```python
from app.database.connection import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Production configuration must also consider connection pool limits and the selected PostgreSQL hosting provider.

---

# 19. Database Migration Strategy

Use Alembic for database schema migrations.

### Initial Setup

```bash
pip install sqlalchemy alembic psycopg[binary]
```

Initialise Alembic:

```bash
alembic init migrations
```

Generate a migration:

```bash
alembic revision --autogenerate -m "create initial schema"
```

Apply migrations:

```bash
alembic upgrade head
```

Check migration history:

```bash
alembic history
```

Rollback one revision when appropriate:

```bash
alembic downgrade -1
```

### Migration Rules

- Every schema change must have a migration.
- Review autogenerated migrations before applying them.
- Never run destructive migrations without a backup and review.
- Test migrations on a development database first.
- Keep migration files in Git.
- Do not use automatic table creation as the production migration strategy.

---

# 20. Database API Integration

The FastAPI backend should access the database through repositories and services.

### Example Conversation Flow

```text
Frontend
   |
   v
POST /api/v1/conversations
   |
   v
FastAPI Route
   |
   v
Pydantic Validation
   |
   v
Conversation Service
   |
   v
Conversation Repository
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
```

### API to Database Mapping

| API Endpoint | Database Tables |
|---|---|
| `POST /conversations` | conversations |
| `GET /conversations` | conversations |
| `GET /conversations/{id}` | conversations, messages |
| `DELETE /conversations/{id}` | conversations, messages |
| `GET /users/me/preferences` | user_preferences |
| `PUT /users/me/preferences` | user_preferences |
| Recognition logging | recognition_logs |
| Learning resources | learning_resources |
| Learning progress | user_learning_progress |

### Rules

- Routes must not contain raw SQL queries.
- Use service and repository layers.
- Validate user ownership.
- Use database transactions where necessary.
- Avoid returning database models directly to the frontend.
- Use Pydantic response schemas.

---

# 21. Database Testing Strategy

Use Pytest with an isolated test database.

### User Tests

- Create user.
- Duplicate email.
- Invalid user data.
- Delete user.
- User preference creation.

### Conversation Tests

- Create conversation.
- List conversations.
- Retrieve conversation.
- Delete conversation.
- Create message.
- Delete conversation and verify message cascade.
- Prevent cross-user access.

### Model Registry Tests

- Register model.
- Duplicate model version.
- Update model status.
- Prevent invalid recognition type.

### Recognition Log Tests

- Store valid prediction metadata.
- Reject confidence outside valid range.
- Reject negative processing time.
- Verify optional user relationship.

### Learning Tests

- Create learning resource.
- Update resource status.
- Record progress.
- Prevent duplicate progress records.
- Verify user ownership.

### Migration Tests

- Apply initial migration.
- Upgrade schema.
- Verify expected tables and constraints.
- Test rollback where supported.

### Testing Rules

- Do not run destructive tests against production.
- Use isolated test data.
- Reset test state between relevant tests.
- Test database constraints.
- Record actual test results.

---

# 22. Backup and Recovery

Production database backups are important for protecting user and application data.

### Requirements

- Use scheduled backups.
- Protect backup files.
- Restrict backup access.
- Encrypt backups where supported.
- Define a recovery process.
- Test restoration periodically.
- Avoid committing backups to Git.

The backup frequency and retention period must match the actual hosting and data-retention requirements.

---

# 23. Performance Optimisation

### Database Performance

- Add indexes for common queries.
- Use pagination.
- Avoid loading unnecessary columns.
- Use efficient relationships.
- Avoid N+1 query problems.
- Use connection pooling.
- Monitor slow queries.

### Message History

For conversation history:

- Retrieve messages by conversation.
- Order messages by creation time.
- Use pagination for large histories.
- Avoid loading every message at once.

### Growth Strategy

If the application grows:

- Review query execution plans.
- Add indexes based on real workloads.
- Consider archiving old technical logs.
- Review connection pool settings.
- Consider table partitioning only when data volume justifies it.

Do not add Redis or other infrastructure unless an actual performance requirement exists.

---

# 24. Initial Database Implementation Priority

Not every table is required for the first working prototype.

| Priority | Table | Phase |
|---|---|---|
| Critical if accounts are required | users | Authentication |
| Critical if preferences are stored | user_preferences | Settings |
| High if history is enabled | conversations | Communication history |
| High if history is enabled | messages | Communication history |
| Medium | model_registry | Model governance |
| Optional | recognition_logs | Monitoring |
| Future | learning_resources | Learning centre |
| Future | user_learning_progress | Learning centre |

### Recommended Initial Approach

For the first recognition prototype:

1. Run the verified ISL model.
2. Build the FastAPI inference endpoints.
3. Connect the React frontend.
4. Verify the complete recognition workflow.
5. Introduce PostgreSQL when persistent user data or history is required.

Database setup must not block the initial ML inference milestone.

---

# 25. Definition of Done

A database feature is complete only when:

1. Its data requirements are documented.
2. Its table structure is defined.
3. Primary and foreign keys are configured.
4. Required constraints are applied.
5. SQLAlchemy models are implemented.
6. Alembic migration is created.
7. Database operations are tested.
8. Access controls are verified.
9. Retention and deletion behaviour are documented.
10. Relevant API integration is tested.

A table that exists without working application logic is not a completed feature.

---

# 26. Instructions for Antigravity

Before implementing any database functionality:

1. Read `AGENTS.md`.
2. Read `docs/PRD.md`.
3. Read `docs/PROJECT_OVERVIEW.md`.
4. Read `docs/FEATURES.md`.
5. Read `docs/TECH_STACK.md`.
6. Read `docs/SYSTEM_ARCHITECTURE.md`.
7. Read `docs/API_DOCUMENTATION.md`.
8. Read this `docs/DATABASE_SCHEMA.md`.
9. Read `docs/PHASE_ROADMAP.md`.
10. Inspect the existing backend and database code.

### Development Rules

- Use PostgreSQL.
- Use SQLAlchemy.
- Use Alembic for migrations.
- Use UUID primary keys.
- Use foreign key constraints.
- Keep database logic separate from API routes.
- Validate user ownership.
- Do not store raw camera video by default.
- Do not store raw audio by default.
- Never store plaintext passwords.
- Do not create unnecessary tables.
- Do not add Redis or other infrastructure without approval.
- Test all database changes.
- Update documentation after schema changes.

### Completion Report

After each database task, provide:

- Tables created or modified.
- SQLAlchemy models implemented.
- Migration files created.
- Relationships and constraints.
- Indexes added.
- API integration completed.
- Tests executed.
- Actual test results.
- Security and privacy considerations.
- Known limitations.
- Recommended next task.

---

# 27. Final Database Strategy

Signova AI will use PostgreSQL as an optional persistence layer around its AI recognition and communication services.

The implementation order is:

1. Finalise database requirements.
2. Configure PostgreSQL.
3. Set up SQLAlchemy.
4. Configure Alembic.
5. Implement user and preference tables if accounts are required.
6. Implement conversation and message tables if history is enabled.
7. Add model registry and optional recognition logs.
8. Add learning resources and progress when the learning centre is implemented.
9. Test relationships, constraints, and deletion behaviour.
10. Review security, backups, and retention.

**Final Goal:** Maintain a secure, reliable, and extensible database that supports Signova AI's communication features while protecting user privacy and keeping the core ISL recognition pipeline independent of persistent storage.