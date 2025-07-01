from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(title="F1 Data API")


# Define the root endpoint
@app.get("/")
async def root() -> dict:
    """
    Root endpoint to check if the F1 Dashboard Backend is running.

    Returns:
        dict: A message confirming the server is up and running.
    """
    return {"message": "F1 Dashboard Backend Running"}
