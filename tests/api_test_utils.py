"""Utility functions for API testing"""
from typing import Any, Dict, Optional
from fastapi.testclient import TestClient

def create_test_item(
    client: TestClient,
    endpoint: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a test item through the API
    
    Args:
        client: FastAPI test client
        endpoint: API endpoint
        data: Item data to create
        
    Returns:
        Created item data
    """
    response = client.post(endpoint, json=data)
    assert response.status_code == 200
    return response.json()

def get_test_item(
    client: TestClient,
    endpoint: str,
    item_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get a test item through the API
    
    Args:
        client: FastAPI test client
        endpoint: API endpoint
        item_id: ID of the item to get
        
    Returns:
        Item data if found, None if not found
    """
    response = client.get(f"{endpoint}/{item_id}")
    return response.json() if response.status_code == 200 else None

def update_test_item(
    client: TestClient,
    endpoint: str,
    item_id: int,
    data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update a test item through the API
    
    Args:
        client: FastAPI test client
        endpoint: API endpoint
        item_id: ID of the item to update
        data: New item data
        
    Returns:
        Updated item data if successful, None if item not found
    """
    response = client.put(f"{endpoint}/{item_id}", json=data)
    return response.json() if response.status_code == 200 else None

def delete_test_item(
    client: TestClient,
    endpoint: str,
    item_id: int
) -> bool:
    """
    Delete a test item through the API
    
    Args:
        client: FastAPI test client
        endpoint: API endpoint
        item_id: ID of the item to delete
        
    Returns:
        True if deletion was successful, False otherwise
    """
    response = client.delete(f"{endpoint}/{item_id}")
    return response.status_code == 200

def get_all_test_items(
    client: TestClient,
    endpoint: str,
    skip: int = 0,
    limit: int = 100
) -> list:
    """
    Get all test items through the API with pagination
    
    Args:
        client: FastAPI test client
        endpoint: API endpoint
        skip: Number of items to skip
        limit: Maximum number of items to return
        
    Returns:
        List of items
    """
    response = client.get(f"{endpoint}?skip={skip}&limit={limit}")
    return response.json() if response.status_code == 200 else []