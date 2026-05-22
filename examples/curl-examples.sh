#!/usr/bin/env bash

BASE_URL="http://localhost:8000"

echo "Health check"
curl -X GET "$BASE_URL/health"

echo "Ask AI"
curl -X POST "$BASE_URL/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Какие растения можно посадить в полутени?",
    "top_k": 5
  }'

echo "Create plant"
curl -X POST "$BASE_URL/plants" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_name": "Роза у забора",
    "plant_type": "rose",
    "latitude": 59.15,
    "longitude": 30.15,
    "comment": "Посажена рядом с забором"
  }'

echo "Get plants"
curl -X GET "$BASE_URL/plants"
