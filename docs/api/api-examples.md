# API endpoint examples

This document contains example API endpoints for the AI Dacha MVP.

## Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "ai-dacha-api"
}
```

## Upload document

```http
POST /documents
Content-Type: multipart/form-data
```

Fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| file | file | yes | PDF document |
| title | string | no | Document title |
| source_type | string | no | Example: `book`, `manual`, `article` |

Example response:

```json
{
  "document_id": 101,
  "status": "uploaded",
  "processing_status": "queued"
}
```

## Get document chunks

```http
GET /documents/{document_id}/chunks
```

Example response:

```json
{
  "document_id": 101,
  "chunks": [
    {
      "chunk_id": 501,
      "page_from": 10,
      "page_to": 11,
      "content": "Text fragment from the document..."
    }
  ]
}
```

## Ask a question

```http
POST /ai/ask
Content-Type: application/json
```

Request:

```json
{
  "question": "Какие растения можно посадить в полутени?",
  "top_k": 5
}
```

Response:

```json
{
  "answer": "В полутени можно рассмотреть...",
  "sources": [
    {
      "document_id": 101,
      "chunk_id": 501,
      "page_from": 10,
      "page_to": 11
    }
  ]
}
```

## Create plant

```http
POST /plants
Content-Type: application/json
```

Request:

```json
{
  "custom_name": "Роза у забора",
  "plant_type": "rose",
  "latitude": 59.15,
  "longitude": 30.15,
  "comment": "Посажена рядом с забором"
}
```

Response:

```json
{
  "plant_id": 1,
  "custom_name": "Роза у забора",
  "geometry": "POINT(30.15 59.15)"
}
```

## Get plants

```http
GET /plants
```

Response:

```json
{
  "items": [
    {
      "plant_id": 1,
      "custom_name": "Роза у забора",
      "plant_type": "rose",
      "geometry": "POINT(30.15 59.15)"
    }
  ]
}
```
