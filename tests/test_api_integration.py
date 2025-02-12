"""Integration tests for API endpoints"""
import pytest
from fastapi import status
from app.models.base import BaseModel
from app.schemas.base import BaseCreateSchema, BaseUpdateSchema

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "RDS Connectivity API is running"}

class TestBaseCRUDEndpoints:
    """Test suite for base CRUD endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self, client, test_db_session):
        """Setup test data"""
        self.client = client
        self.db = test_db_session
        # Example endpoint prefix for testing
        self.endpoint = "/api/v1/items"
    
    def test_create_item(self):
        """Test creating a new item"""
        data = {"name": "test_item", "description": "test description"}
        response = self.client.post(self.endpoint, json=data)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["name"] == data["name"]
        assert result["description"] == data["description"]
        assert "id" in result
    
    def test_get_item(self):
        """Test getting an item by ID"""
        # Create test item
        item = BaseModel()
        self.db.add(item)
        self.db.commit()
        
        response = self.client.get(f"{self.endpoint}/{item.id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == item.id
    
    def test_get_all_items(self):
        """Test getting all items"""
        # Create test items
        items = [BaseModel() for _ in range(3)]
        for item in items:
            self.db.add(item)
        self.db.commit()
        
        response = self.client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) >= len(items)
    
    def test_update_item(self):
        """Test updating an item"""
        # Create test item
        item = BaseModel()
        self.db.add(item)
        self.db.commit()
        
        update_data = {"name": "updated_item", "description": "updated description"}
        response = self.client.put(f"{self.endpoint}/{item.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["name"] == update_data["name"]
        assert result["description"] == update_data["description"]
    
    def test_delete_item(self):
        """Test deleting an item"""
        # Create test item
        item = BaseModel()
        self.db.add(item)
        self.db.commit()
        
        response = self.client.delete(f"{self.endpoint}/{item.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Record deleted successfully"}
        
        # Verify item is deleted
        get_response = self.client.get(f"{self.endpoint}/{item.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_nonexistent_item(self):
        """Test getting a nonexistent item"""
        response = self.client.get(f"{self.endpoint}/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_nonexistent_item(self):
        """Test updating a nonexistent item"""
        update_data = {"name": "updated_item", "description": "updated description"}
        response = self.client.put(f"{self.endpoint}/999999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_item(self):
        """Test deleting a nonexistent item"""
        response = self.client.delete(f"{self.endpoint}/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
