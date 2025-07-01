from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes

# Create the FastAPI application instance
app = FastAPI(title="F1 Data API")
app.include_router(routes.router, prefix="/api")

# Allow requests from Vite dev server (React)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add middleware for CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root endpoint
@app.get("/")
async def root() -> dict:
    """
    Root endpoint to check if the F1 Dashboard Backend is running.

    Returns:
        dict: A message confirming the server is up and running.
    """
    return {"message": "F1 Dashboard Backend Running"}
