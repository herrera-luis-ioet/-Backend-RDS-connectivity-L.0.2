import pytest
from datetime import datetime
from sqlalchemy import Column, String
from pydantic import BaseModel as PydanticBaseModel
from app.models.base import BaseModel
from app.schemas.base import BaseCreateSchema, BaseUpdateSchema
from app.services.base import BaseCRUDService

# Test Model
class TestModel(BaseModel):
    __tablename__ = "test_items"
    name = Column(String(50), nullable=False)

# Test Schemas
class TestCreateSchema(BaseCreateSchema):
    name: str

class TestUpdateSchema(BaseUpdateSchema):
    name: str | None = None

# Test Service
class TestService(BaseCRUDService[TestModel, TestCreateSchema, TestUpdateSchema]):
    def __init__(self):
        super().__init__(TestModel)

@pytest.fixture
def test_service():
    return TestService()

@pytest.fixture
def test_item(test_db_session):
    item = TestModel(name="test_item")
    test_db_session.add(item)
    test_db_session.commit()
    test_db_session.refresh(item)
    return item

def test_create_item(test_db_session, test_service):
    # Test creating a new item
    create_data = TestCreateSchema(name="new_item")
    item = test_service.create(test_db_session, create_data)
    
    assert item.id is not None
    assert item.name == "new_item"
    assert isinstance(item.created_at, datetime)
    assert isinstance(item.updated_at, datetime)

def test_get_item(test_db_session, test_service, test_item):
    # Test getting an item by ID
    retrieved_item = test_service.get(test_db_session, test_item.id)
    
    assert retrieved_item is not None
    assert retrieved_item.id == test_item.id
    assert retrieved_item.name == test_item.name

def test_get_nonexistent_item(test_db_session, test_service):
    # Test getting a non-existent item
    retrieved_item = test_service.get(test_db_session, 999)
    assert retrieved_item is None

def test_get_all_items(test_db_session, test_service):
    # Create multiple items
    items = [
        TestModel(name=f"item_{i}")
        for i in range(3)
    ]
    for item in items:
        test_db_session.add(item)
    test_db_session.commit()

    # Test getting all items
    retrieved_items = test_service.get_all(test_db_session)
    assert len(retrieved_items) == 3
    
    # Test pagination
    paginated_items = test_service.get_all(test_db_session, skip=1, limit=1)
    assert len(paginated_items) == 1
    assert paginated_items[0].name == "item_1"

def test_update_item(test_db_session, test_service, test_item):
    # Test updating an item
    update_data = TestUpdateSchema(name="updated_item")
    updated_item = test_service.update(test_db_session, test_item.id, update_data)
    
    assert updated_item.id == test_item.id
    assert updated_item.name == "updated_item"
    assert updated_item.updated_at > test_item.created_at

def test_update_nonexistent_item(test_db_session, test_service):
    # Test updating a non-existent item
    update_data = TestUpdateSchema(name="updated_item")
    with pytest.raises(HTTPException) as exc_info:
        test_service.update(test_db_session, 999, update_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Record not found"

def test_partial_update_item(test_db_session, test_service, test_item):
    # Test partial update (not updating all fields)
    original_name = test_item.name
    update_data = TestUpdateSchema()  # No fields set
    updated_item = test_service.update(test_db_session, test_item.id, update_data)
    
    assert updated_item.id == test_item.id
    assert updated_item.name == original_name  # Name should not change

def test_delete_item(test_db_session, test_service, test_item):
    # Test deleting an item
    result = test_service.delete(test_db_session, test_item.id)
    assert result is True
    
    # Verify item is deleted
    deleted_item = test_service.get(test_db_session, test_item.id)
    assert deleted_item is None

def test_delete_nonexistent_item(test_db_session, test_service):
    # Test deleting a non-existent item
    with pytest.raises(HTTPException) as exc_info:
        test_service.delete(test_db_session, 999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Record not found"