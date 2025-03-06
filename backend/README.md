# Agent Framework Backend Server

This directory contains a FastAPI-based backend server that integrates with the agent framework. The server provides API endpoints for interacting with agents like the Weather Vibes Agent.

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- The main agent_framework package

## Installation

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   This will install FastAPI, Uvicorn, and reference the main project as a dependency.

3. If you're working in a virtual environment (recommended), activate it before installing:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

## Running the Server

Start the backend server by running:

```
python run.py
```

Alternatively, you can use Uvicorn directly:

```
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

The server will start on port 5000, which is where the frontend expects to find it.

## API Endpoints

Once the server is running, you can access the following endpoints:

- **GET /health**: Simple health check to verify the server is running
- **POST /api/weather**: Get weather information for a location
  - Request body: `{"location": "City, Country"}`
- **POST /api/weather-vibes**: Get a recommended YouTube video based on the weather
  - Request body: `{"location": "City, Country"}`

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## Integration with Agent Framework

This backend server integrates with the agent framework by:

1. Importing agent functionality from the main project
2. Creating API endpoints that utilize agent capabilities
3. Providing a web interface to the agent's tools

## Troubleshooting

- If you encounter a "Module not found" error, ensure you've installed all dependencies and that the main agent_framework package is in your Python path.
- For port conflicts, change the port in `run.py` and update the frontend configuration accordingly.

