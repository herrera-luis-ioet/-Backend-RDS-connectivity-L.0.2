import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.base import BaseSchema, BaseResponseSchema, BaseCreateSchema, BaseUpdateSchema
from app.models.base import BaseModel
from sqlalchemy import Column, String
from tests.utils import create_test_model, clean_test_data

# Test model and schema classes
class TestModel(BaseModel):
    __tablename__ = "test_models"
    name = Column(String(50))

class TestResponseSchema(BaseResponseSchema):
    name: str

class TestCreateSchema(BaseCreateSchema):
    name: str

class TestUpdateSchema(BaseUpdateSchema):
    name: str | None = None

def test_base_schema_validation():
    """Test base schema validation rules"""
    class TestSchema(BaseSchema):
        name: str
        age: int | None = None

    # Test valid data
    valid_data = {"name": "test"}
    schema = TestSchema(**valid_data)
    assert schema.name == "test"
    assert schema.age is None

    # Test invalid data type
    with pytest.raises(ValidationError) as exc_info:
        TestSchema(name=123)  # name should be string
    assert "Input should be a string" in str(exc_info.value)

def test_base_response_schema_validation(test_db_session):
    """Test response schema validation with model data"""
    # Create test model
    model = create_test_model(
        test_db_session,
        TestModel,
        {"name": "test"}
    )

    # Test schema creation from model
    response_schema = TestResponseSchema.model_validate(model)
    assert response_schema.id == model.id
    assert response_schema.name == model.name
    assert response_schema.created_at == model.created_at
    assert response_schema.updated_at == model.updated_at

    # Test invalid data
    with pytest.raises(ValidationError):
        TestResponseSchema(
            id="invalid",  # id should be integer
            name="test",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_base_create_schema_validation():
    """Test create schema validation"""
    # Test valid data
    valid_data = {"name": "test"}
    schema = TestCreateSchema(**valid_data)
    assert schema.name == "test"

    # Test missing required field
    with pytest.raises(ValidationError) as exc_info:
        TestCreateSchema()
    assert "Field required" in str(exc_info.value)

def test_base_update_schema_validation():
    """Test update schema validation with optional fields"""
    # Test with all fields
    schema = TestUpdateSchema(name="test")
    assert schema.name == "test"

    # Test with no fields (all optional)
    schema = TestUpdateSchema()
    assert schema.name is None

def test_model_to_schema_conversion(test_db_session):
    """Test conversion from model instance to schema"""
    # Create test model
    model = create_test_model(
        test_db_session,
        TestModel,
        {"name": "test"}
    )

    # Convert to response schema
    schema = TestResponseSchema.model_validate(model)

    # Verify conversion
    assert schema.id == model.id
    assert schema.name == model.name
    assert schema.created_at == model.created_at
    assert schema.updated_at == model.updated_at

    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_schema_to_model_conversion(test_db_session):
    """Test conversion from schema to model attributes"""
    # Create schema instance
    create_schema = TestCreateSchema(name="test")

    # Create model using schema data
    model = create_test_model(
        test_db_session,
        TestModel,
        create_schema.model_dump()
    )

    # Verify conversion
    assert model.name == create_schema.name

    # Test update schema conversion
    update_schema = TestUpdateSchema(name="updated")
    for key, value in update_schema.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
    test_db_session.commit()
    test_db_session.refresh(model)

    # Verify update
    assert model.name == "updated"

    # Clean up
    clean_test_data(test_db_session, TestModel)

def test_schema_validation_error_handling():
    """Test schema validation error handling"""
    # Test multiple validation errors
    with pytest.raises(ValidationError) as exc_info:
        TestResponseSchema(
            id="invalid",  # should be integer
            name=123,  # should be string
            created_at="invalid",  # should be datetime
            updated_at="invalid"  # should be datetime
        )
    
    errors = exc_info.value.errors()
    assert len(errors) > 0  # Multiple validation errors
    
    # Verify error messages are descriptive
    error_messages = [error["msg"] for error in errors]
    assert any("Input should be a valid integer" in msg for msg in error_messages)
    assert any("Input should be a valid datetime" in msg for msg in error_messages)