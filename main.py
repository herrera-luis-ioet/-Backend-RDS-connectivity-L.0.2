from fastapi import FastAPI
from config import Settings

# Initialize FastAPI app
app = FastAPI(
    title="RDS Connectivity API",
    description="API service with RDS connectivity",
    version="0.1.0"
)

# Load configuration
settings = Settings()

@app.get("/")
async def root():
    """
    Root endpoint to verify API is running
    """
    return {"message": "RDS Connectivity API is running"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)