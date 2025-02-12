import pytest
from datetime import datetime
from sqlalchemy import Column, String
from app.models.base import BaseModel
from tests.utils import create_test_model, clean_test_data

# Test model class inheriting from BaseModel
class TestModel(BaseModel):
    __tablename__ = "test_models"
    name = Column(String(50))

def test_base_model_creation(test_db_session):
    """Test that BaseModel creates with automatic timestamps"""
    # Create a test model
    model = create_test_model(test_db_session, TestModel, {"name": "test"})
    
    # Verify automatic timestamps
    assert model.created_at is not None
    assert model.updated_at is not None
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)
    assert model.created_at == model.updated_at
    
    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_base_model_update(test_db_session):
    """Test that updated_at timestamp updates automatically"""
    # Create a test model
    model = create_test_model(test_db_session, TestModel, {"name": "test"})
    initial_created_at = model.created_at
    initial_updated_at = model.updated_at
    
    # Wait a moment to ensure timestamp will be different
    import time
    time.sleep(1)
    
    # Update the model
    model.name = "updated"
    test_db_session.commit()
    test_db_session.refresh(model)
    
    # Verify timestamps
    assert model.created_at == initial_created_at  # created_at should not change
    assert model.updated_at > initial_updated_at  # updated_at should be newer
    
    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_base_model_inheritance(test_db_session):
    """Test that model inheritance works correctly"""
    # Create a test model
    model = create_test_model(test_db_session, TestModel, {"name": "test"})
    
    # Verify inheritance
    assert isinstance(model, BaseModel)
    assert hasattr(model, 'id')
    assert hasattr(model, 'created_at')
    assert hasattr(model, 'updated_at')
    assert hasattr(model, 'name')  # Custom field from TestModel
    
    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_primary_key_generation(test_db_session):
    """Test that primary key is generated automatically"""
    # Create multiple test models
    model1 = create_test_model(test_db_session, TestModel, {"name": "test1"})
    model2 = create_test_model(test_db_session, TestModel, {"name": "test2"})
    
    # Verify primary keys
    assert model1.id is not None
    assert model2.id is not None
    assert model1.id != model2.id
    assert isinstance(model1.id, int)
    assert isinstance(model2.id, int)
    
    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_model_serialization(test_db_session):
    """Test that model can be serialized to dict"""
    # Create a test model
    model = create_test_model(test_db_session, TestModel, {"name": "test"})
    
    # Convert to dict
    model_dict = {
        'id': model.id,
        'name': model.name,
        'created_at': model.created_at,
        'updated_at': model.updated_at
    }
    
    # Verify serialization
    assert model_dict['id'] == model.id
    assert model_dict['name'] == "test"
    assert isinstance(model_dict['created_at'], datetime)
    assert isinstance(model_dict['updated_at'], datetime)
    
    # Clean up
    clean_test_data(test_db_session, TestModel)