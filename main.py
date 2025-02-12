from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from app.database import init_db, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Initialize FastAPI app and database
app = FastAPI(
    title="RDS Connectivity API",
    description="API service with RDS connectivity",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for database errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"message": "Database error occurred", "detail": str(exc)},
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
