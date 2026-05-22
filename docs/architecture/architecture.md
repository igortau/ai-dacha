# Architecture

## Context

AI Dacha is a local-first AI system for garden management and document-based knowledge retrieval.

The system combines several subsystems:

1. API backend
2. PostgreSQL database
3. PostGIS geospatial storage
4. pgvector semantic search
5. OCR worker
6. Embedding generation
7. Ollama LLM runtime
8. Mobile or web client

## Main flow: document processing

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI Backend
    participant OCR as OCR Worker
    participant EMB as Embedding Service
    participant DB as PostgreSQL + pgvector
    participant LLM as Ollama

    U->>API: Upload PDF
    API->>DB: Create document record
    API->>OCR: Send document for processing
    OCR->>OCR: Extract text
    OCR->>OCR: Split text into chunks
    OCR->>EMB: Generate embeddings
    EMB-->>OCR: Return vectors
    OCR->>DB: Save chunks + embeddings

    U->>API: Ask question
    API->>EMB: Generate question embedding
    API->>DB: Search similar chunks
    DB-->>API: Return relevant chunks
    API->>LLM: Send prompt + context
    LLM-->>API: Return answer
    API-->>U: Show AI answer
```

## Main flow: plant on map

```mermaid
sequenceDiagram
    participant U as User
    participant APP as Mobile App
    participant API as FastAPI Backend
    participant DB as PostgreSQL + PostGIS

    U->>APP: Tap on map
    APP->>APP: Open plant form
    U->>APP: Enter plant data
    APP->>API: POST /plants
    API->>DB: Save plant
    API->>DB: Save geometry POINT
    API-->>APP: Return created plant
    APP-->>U: Show marker on map
```
