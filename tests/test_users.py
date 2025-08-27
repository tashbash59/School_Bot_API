import pytest
from app.models import user

def test_create_user(client, test_user_data):
    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["telegram_id"] == test_user_data["telegram_id"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data

def test_create_duplicate_user(client, test_user_data):
    # Создаем первого пользователя
    client.post("/users/", json=test_user_data)
    
    # Пытаемся создать дубликат
    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_users(client, test_user_data):
    # Создаем пользователя
    client.post("/users/", json=test_user_data)
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["telegram_id"] == test_user_data["telegram_id"]

def test_read_user(client, test_user_data):
    # Создаем пользователя
    create_response = client.post("/users/", json=test_user_data)
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["telegram_id"] == test_user_data["telegram_id"]

def test_read_user_by_telegram(client, test_user_data):
    # Создаем пользователя
    client.post("/users/", json=test_user_data)
    
    response = client.get(f"/users/telegram/{test_user_data['telegram_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["telegram_id"] == test_user_data["telegram_id"]

def test_read_nonexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == 404

def test_update_user(client, test_user_data):
    # Создаем пользователя
    create_response = client.post("/users/", json=test_user_data)
    user_id = create_response.json()["id"]
    
    # Обновляем
    update_data = {"username": "updateduser", "full_name": "Updated"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["full_name"] == "Updated"

def test_delete_user(client, test_user_data):
    # Создаем пользователя
    create_response = client.post("/users/", json=test_user_data)
    user_id = create_response.json()["id"]
    
    # Удаляем
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    
    # Проверяем, что пользователь удален
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404