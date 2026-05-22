# ER diagram

## Conceptual database model

```mermaid
erDiagram
    DOCUMENT ||--o{ DOCUMENT_CHUNK : contains
    DOCUMENT_CHUNK ||--|| DOCUMENT_EMBEDDING : has
    GARDEN ||--o{ USER_PLANT : contains
    USER_PLANT ||--o{ PLANT_LOCATION : has
    PLANT_CATALOG ||--o{ USER_PLANT : describes

    DOCUMENT {
        bigint id PK
        text title
        text source_type
        text file_path
        text processing_status
        timestamp created_at
    }

    DOCUMENT_CHUNK {
        bigint id PK
        bigint document_id FK
        int page_from
        int page_to
        text content
        jsonb metadata
        timestamp created_at
    }

    DOCUMENT_EMBEDDING {
        bigint id PK
        bigint chunk_id FK
        vector embedding
        text embedding_model
        timestamp created_at
    }

    GARDEN {
        bigint id PK
        text name
        text description
        geometry boundary
        timestamp created_at
    }

    PLANT_CATALOG {
        bigint id PK
        text common_name
        text latin_name
        text plant_type
        jsonb attributes
    }

    USER_PLANT {
        bigint id PK
        bigint garden_id FK
        bigint plant_catalog_id FK
        text custom_name
        text comment
        date planting_date
        timestamp created_at
    }

    PLANT_LOCATION {
        bigint id PK
        bigint user_plant_id FK
        geometry geometry
        text location_type
        timestamp created_at
    }
```

## Notes

### DOCUMENT

Stores the original uploaded document.

### DOCUMENT_CHUNK

Stores text fragments extracted from PDF documents.  
A chunk may contain text from one or several pages, therefore `page_from` and `page_to` are stored separately.

### DOCUMENT_EMBEDDING

Stores vector representation of each document chunk.  
The `embedding_model` field is important because embeddings from different models should not be mixed without control.

### GARDEN

Stores the garden or land plot.  
The `boundary` field can store polygon geometry.

### USER_PLANT

Stores a specific plant instance owned by the user.

### PLANT_LOCATION

Stores point, line, or polygon geometry for a plant location.
