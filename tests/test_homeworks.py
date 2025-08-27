import pytest
from app.models import homework

def test_create_homework(client, test_homework_data, test_group_data):
    # Сначала создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    
    response = client.post("/homeworks/", json=homework_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == homework_data["title"]
    assert data["group_id"] == group_id
    assert "id" in data

def test_read_homeworks(client, test_homework_data, test_group_data):
    # Создаем группу и домашнее задание
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    client.post("/homeworks/", json=homework_data)
    
    response = client.get("/homeworks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == homework_data["title"]

def test_read_homework(client, test_homework_data, test_group_data):
    # Создаем группу и домашнее задание
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    create_response = client.post("/homeworks/", json=homework_data)
    homework_id = create_response.json()["id"]
    
    response = client.get(f"/homeworks/{homework_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == homework_id
    assert data["title"] == homework_data["title"]

def test_read_group_homeworks(client, test_homework_data, test_group_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашние задания для группы
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    client.post("/homeworks/", json=homework_data)
    
    # Создаем другое домашнее задание с другим названием
    homework_data2 = homework_data.copy()
    homework_data2["title"] = "Another Homework"
    client.post("/homeworks/", json=homework_data2)
    
    response = client.get(f"/homeworks/group/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_homework(client, test_homework_data, test_group_data):
    # Создаем группу и домашнее задание
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    create_response = client.post("/homeworks/", json=homework_data)
    homework_id = create_response.json()["id"]
    
    # Обновляем
    update_data = {"title": "Updated Homework", "description": "Updated description"}
    response = client.put(f"/homeworks/{homework_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Homework"
    assert data["description"] == "Updated description"

def test_delete_homework(client, test_homework_data, test_group_data):
    # Создаем группу и домашнее задание
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    create_response = client.post("/homeworks/", json=homework_data)
    homework_id = create_response.json()["id"]
    
    # Удаляем
    response = client.delete(f"/homeworks/{homework_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Homework deleted successfully"
    
    # Проверяем, что домашнее задание удалено
    response = client.get(f"/homeworks/{homework_id}")
    assert response.status_code == 404