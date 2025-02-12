from fastapi import FastAPI, Depends
from config import Settings
from app.database import init_db, get_db
from sqlalchemy.orm import Session

# Initialize FastAPI app and database
app = FastAPI(
    title="RDS Connectivity API",
    description="API service with RDS connectivity",
    version="0.1.0"
)

# Load configuration and initialize database
settings = Settings()
init_db()

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
