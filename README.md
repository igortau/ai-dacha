# AI Dacha

AI Dacha is a personal experimental project focused on combining AI/LLM technologies with geospatial garden management and document-based knowledge retrieval.

Initially, the project started as a local RAG/LLM laboratory for experimenting with:

- PostgreSQL + pgvector;
- local LLM deployment with Ollama;
- PDF ingestion pipelines;
- semantic search;
- OCR processing;
- PostGIS geospatial storage.

Over time, the project evolved into a prototype of an AI-assisted garden management system.

## Main ideas behind the project

The project explores how AI can be integrated into a real information system instead of being used only as a standalone chatbot.

Current experiments include:

- storing plants and their locations on a map;
- processing gardening books and reference PDFs;
- splitting documents into chunks;
- generating embeddings for semantic search;
- storing vectors in PostgreSQL with pgvector;
- using PostGIS for geospatial objects;
- querying local LLM models through Ollama;
- building API endpoints for frontend/mobile clients.

## Current state

Current MVP includes:

- document upload experiments;
- chunk storage in PostgreSQL;
- pgvector semantic search;
- local Ollama integration;
- geospatial storage for plants;
- simple mobile map prototype;
- architecture and data model documentation.

The project is still evolving and many parts are experimental.

## Tested environment

The project is currently tested in a home lab environment using:

- QNAP TS-673A NAS;
- NVIDIA RTX 3090;
- Docker / Portainer;
- Ollama local inference;
- PostgreSQL + pgvector + PostGIS.

## Repository structure

```text
ai-dacha/
├── README.md
├── docker-compose.yml
├── .env.example
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── database/
│   └── requirements/
├── examples/
└── screenshots/

## High-level architecture

flowchart TD
User[User / Mobile App] --> Frontend[Frontend or Mobile UI]
Frontend --> API[FastAPI Backend]

API --> DB[(PostgreSQL)]
DB --> PGVector[pgvector]
DB --> PostGIS[PostGIS]

API --> Ollama[Ollama LLM Service]

PDF[PDF Documents] --> OCR[OCR Worker]
OCR --> Chunker[Document Chunking]
Chunker --> Embedder[Embedding Model]
Embedder --> PGVector

API --> RAG[RAG Retrieval]
RAG --> PGVector
RAG --> Ollama
```

Why PostgreSQL

PostgreSQL was intentionally selected because it allows combining:

relational data;
vector search with pgvector;
geospatial data with PostGIS;

inside a single database engine.

This significantly simplifies the architecture for experimental AI systems.

## Technology stack

| Area | Technology |
|---|---|
| Backend API | FastAPI |
| Database | PostgreSQL |
| Vector search | pgvector |
| Geospatial data | PostGIS |
| LLM runtime | Ollama |
| Embeddings | local embedding model, `nomic-embed-text` |
| OCR / PDF processing | OCR worker service |
| Containerization | Docker / Docker Compose |
| Mobile prototype | Android / map interface |

## Core AI pipeline

```text
PDF document
  ↓
OCR / text extraction
  ↓
Text normalization
  ↓
Chunking
  ↓
Embedding generation
  ↓
Storage in PostgreSQL + pgvector
  ↓
Semantic search
  ↓
Context assembly
  ↓
LLM response generation
```

## Example use cases

### 1. Ask questions about gardening books

User uploads gardening books or reference PDFs.  
The system extracts text, creates chunks, generates embeddings, and allows semantic search over the document base.

Example:

> "Какие растения лучше посадить в полутени рядом с забором?"

The system retrieves relevant chunks from the document base and sends them as context to the LLM.

### 2. Store plants on a garden map

The user can add a plant to a map:

- plant name;
- plant type;
- coordinates;
- comment;
- planting date;
- custom notes.

The geometry is stored in PostGIS.

### 3. Combine plant data and AI recommendations

The system can combine:

- plant location;
- soil or area notes;
- documents from the knowledge base;
- LLM reasoning.

Example:

> "Что можно посадить рядом с розой у забора?"

## API examples

See [`docs/api/api-examples.md`](docs/api/api-examples.md).

## Database model

See [`docs/database/er-diagram.md`](docs/database/er-diagram.md).

## Screenshots

Screenshots should be placed in [`screenshots/`](screenshots/).

Recommended screenshots:

- mobile map with plant marker;
- Swagger / OpenAPI page;
- database table in DBeaver;
- document chunk stored in DB;
- vector column example;
- AI answer from local LLM.

## Status

The project is under active development and is intended to demonstrate:

- system analysis skills;
- data modeling;
- AI/LLM integration;
- document processing pipeline;
- PostgreSQL + pgvector + PostGIS usage;
- API-oriented architecture.

## Roadmap

- [ ] Add real backend source code
- [ ] Add OpenAPI specification
- [ ] Add database migration scripts
- [ ] Add mobile client source code
- [ ] Add screenshots
- [ ] Add demo data
- [ ] Add deployment guide
- [ ] Add automated tests

## Author

Igor Polovitsky  
System Analyst / AI & LLM enthusiast
