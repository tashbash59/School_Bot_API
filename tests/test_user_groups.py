import pytest
from app.models import user_group

def test_add_user_to_group(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    
    response = client.post("/user-groups/", json=user_group_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["group_id"] == group_id
    assert data["user_role"] == "student"

def test_add_duplicate_user_to_group(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу первый раз
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    # Пытаемся добавить второй раз
    response = client.post("/user-groups/", json=user_group_data)
    assert response.status_code == 400
    assert "already in group" in response.json()["detail"]

def test_read_user_groups(client, test_user_data, test_group_data):
    # Создаем пользователя, группу и связь
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    response = client.get("/user-groups/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id

def test_read_user_groups_by_user(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    response = client.get(f"/user-groups/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["group_id"] == group_id

def test_read_group_users(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    response = client.get(f"/user-groups/group/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id

def test_read_user_group(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    response = client.get(f"/user-groups/{user_id}/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["group_id"] == group_id

def test_update_user_group_role(client, test_user_data, test_group_data):
    # Создаем пользователя
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]

    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]

    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)

    # Обновляем роль - передаем как query параметр
    response = client.put(f"/user-groups/{user_id}/{group_id}?user_role=teacher")
    assert response.status_code == 200
    data = response.json()
    assert data["user_role"] == "teacher"

def test_remove_user_from_group(client, test_user_data, test_group_data):
    # Создаем пользователя и группу
    user_response = client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]
    
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Добавляем пользователя в группу
    user_group_data = {
        "user_id": user_id,
        "group_id": group_id,
        "user_role": "student"
    }
    client.post("/user-groups/", json=user_group_data)
    
    # Удаляем пользователя из группы
    response = client.delete(f"/user-groups/{user_id}/{group_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User removed from group successfully"
    
    # Проверяем, что связь удалена
    response = client.get(f"/user-groups/{user_id}/{group_id}")
    assert response.status_code == 404