from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging
import time
from config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Create SQLAlchemy base class for models
Base = declarative_base()

# Configure database engine with connection pooling
def create_db_engine():
    """
    Creates and configures the SQLAlchemy engine with connection pooling
    """
    return create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,  # Maximum number of connections in the pool
        max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
        pool_timeout=30,  # Timeout for getting a connection from the pool
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_pre_ping=True,  # Enable connection health checks
        echo=settings.DEBUG  # SQL query logging
    )

# Initialize engine with retry logic
def get_engine(max_retries: int = 3, retry_delay: int = 5):
    """
    Attempts to create database engine with retry logic
    """
    for attempt in range(max_retries):
        try:
            engine = create_db_engine()
            # Test the connection
            engine.connect()
            logger.info("Successfully connected to the database")
            return engine
        except OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to connect to database after {max_retries} attempts")
                raise
            logger.warning(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

# Create engine instance
engine = get_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Generator:
    """
    Context manager for database sessions
    
    Yields:
        Session: Database session
    
    Example:
        with get_db() as db:
            db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all defined tables
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully initialized database tables")
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise