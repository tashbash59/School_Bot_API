import pytest
from app.models import group

def test_create_group(client, test_group_data):
    response = client.post("/groups/", json=test_group_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_group_data["name"]
    assert data["description"] == test_group_data["description"]
    assert "id" in data

def test_create_duplicate_group(client, test_group_data):
    # Создаем первую группу
    client.post("/groups/", json=test_group_data)
    
    # Пытаемся создать дубликат
    response = client.post("/groups/", json=test_group_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_groups(client, test_group_data):
    # Создаем группу
    client.post("/groups/", json=test_group_data)
    
    response = client.get("/groups/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_group_data["name"]

def test_read_group(client, test_group_data):
    # Создаем группу
    create_response = client.post("/groups/", json=test_group_data)
    group_id = create_response.json()["id"]
    
    response = client.get(f"/groups/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group_id
    assert data["name"] == test_group_data["name"]

def test_read_nonexistent_group(client):
    response = client.get("/groups/999")
    assert response.status_code == 404

def test_update_group(client, test_group_data):
    # Создаем группу
    create_response = client.post("/groups/", json=test_group_data)
    group_id = create_response.json()["id"]
    
    # Обновляем
    update_data = {"name": "Updated Group", "description": "Updated description"}
    response = client.put(f"/groups/{group_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Group"
    assert data["description"] == "Updated description"

def test_delete_group(client, test_group_data):
    # Создаем группу
    create_response = client.post("/groups/", json=test_group_data)
    group_id = create_response.json()["id"]
    
    # Удаляем
    response = client.delete(f"/groups/{group_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Group deleted successfully"
    
    # Проверяем, что группа удалена
    response = client.get(f"/groups/{group_id}")
    assert response.status_code == 404