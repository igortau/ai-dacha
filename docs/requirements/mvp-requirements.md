# MVP requirements

## Purpose

Create a minimal public version of the AI Dacha project suitable for portfolio demonstration and technical interviews.

## Functional requirements

### FR-001. Document upload

The system should allow uploading PDF documents.

### FR-002. Document processing

The system should extract text from uploaded PDFs, split text into chunks, and store chunks in the database.

### FR-003. Embedding generation

The system should generate vector embeddings for document chunks.

### FR-004. Semantic search

The system should search relevant chunks by similarity to the user question.

### FR-005. LLM answer generation

The system should generate an answer using retrieved document chunks as context.

### FR-006. Plant catalog

The system should store plants and plant attributes.

### FR-007. Garden map

The system should store plant locations using geospatial data.

## Non-functional requirements

### NFR-001. Local-first deployment

The system should be deployable locally using Docker Compose.

### NFR-002. Modular architecture

Document processing, API, database, and LLM runtime should be separated.

### NFR-003. Explainable AI answers

AI answers should include references to document chunks and pages when possible.

### NFR-004. Data model transparency

The database model should be documented with an ER diagram.

## MVP boundaries

The public MVP does not include:

- real private documents;
- real passwords or tokens;
- private LAN addresses;
- production deployment configuration;
- personal data.
