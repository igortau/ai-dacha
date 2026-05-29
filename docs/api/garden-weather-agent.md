# Garden Weather Agent

## Purpose

The Garden Weather Agent provides plant-specific recommendations based on:

* current weather measurements;
* weather forecast;
* user garden inventory;
* local LLM reasoning.

The agent combines structured PostgreSQL data with AI-generated recommendations.

---

## Endpoint

```http
POST /garden/ask
```

---

## Example Request

```json
{
  "question": "Нужно ли сегодня поливать розу у забора?"
}
```

---

## Processing Pipeline

```text
User Question
      ↓
Plant Matching
      ↓
Plant Context
      ↓
Weather Context
      ↓
Forecast Context
      ↓
Ollama LLM
      ↓
Response Generation
```

---

## Data Sources

### Garden Database

Tables:

```text
garden.user_plants
garden.plant_locations
catalog.plants_catalog
```

Used for:

* plant identification;
* plant metadata;
* location information;
* planting dates and notes.

### Weather Database

Tables:

```text
weather.netatmo_current_measurements
weather.weather_forecast
```

Used for:

* current weather conditions;
* humidity;
* temperature;
* pressure;
* rain;
* wind;
* weather forecast.

---

## Plant Matching

Before sending a request to the LLM, the agent searches for relevant plants.

Example:

Question:

```text
Нужно ли сегодня поливать розу у забора?
```

Matched plant:

```text
Роза у забора
```

This reduces unnecessary context and improves answer quality.

---

## Example Implementation

```python
matched_plants = find_relevant_plants(
    request.question,
    plants
)

prompt = f"""
Question:
{request.question}

Plants:
{json.dumps(matched_plants)}

Current weather:
{json.dumps(current)}

Forecast:
{json.dumps(forecast)}
"""

answer = ask_ollama(prompt)
```

---

## Example Response

```json
{
  "agent_type": "garden_weather_agent",
  "matched_plants_count": 1,
  "plants_sent_to_llm": 1,
  "current_weather_used": true,
  "forecast_hours_used": 24
}
```

---

## Current Capabilities

* plant-specific watering recommendations;
* weather-based recommendations;
* wind risk assessment;
* frost warnings;
* plant context selection;
* local LLM inference using Ollama.

---

## Future Improvements

* Frost Alert Agent
* Irrigation Agent
* Plant Disease Agent
* Soil Sensor Integration
* Risk Assessment Agent
* Multi-Agent Garden Workflow

```
```
