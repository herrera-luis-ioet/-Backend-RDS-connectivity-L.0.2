from typing import Any, Dict, Type, TypeVar
from sqlalchemy.orm import Session
from app.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

def create_test_model(
    db: Session,
    model_class: Type[T],
    data: Dict[str, Any] = None
) -> T:
    """
    Creates a test model instance with given data
    
    Args:
        db: Database session
        model_class: Model class to create
        data: Dictionary of model attributes
        
    Returns:
        Created model instance
    """
    if data is None:
        data = {}
    
    model = model_class(**data)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def clean_test_data(db: Session, model_class: Type[BaseModel]) -> None:
    """
    Cleans up test data for a given model
    
    Args:
        db: Database session
        model_class: Model class to clean up
    """
    db.query(model_class).delete()
    db.commit()

def assert_model_attrs(model: BaseModel, expected_data: Dict[str, Any]) -> None:
    """
    Asserts that model attributes match expected values
    
    Args:
        model: Model instance to check
        expected_data: Dictionary of expected attribute values
    """
    for key, value in expected_data.items():
        assert getattr(model, key) == value, f"Model attribute '{key}' does not match expected value"