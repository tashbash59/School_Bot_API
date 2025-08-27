import pytest

def test_create_attachment(client, test_attachment_data, test_group_data, test_homework_data):
    # Сначала создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    assert group_response.status_code == 200
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    assert homework_response.status_code == 200
    homework_id = homework_response.json()["id"]
    
    # Создаем вложение
    attachment_data = test_attachment_data.copy()
    attachment_data["homework_id"] = homework_id
    
    response = client.post("/attachments/", json=attachment_data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == attachment_data["file_name"]
    assert "id" in data

def test_read_attachments(client, test_attachment_data, test_group_data, test_homework_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    homework_id = homework_response.json()["id"]
    
    # Создаем вложение
    attachment_data = test_attachment_data.copy()
    attachment_data["homework_id"] = homework_id
    client.post("/attachments/", json=attachment_data)
    
    response = client.get("/attachments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["file_name"] == attachment_data["file_name"]

def test_read_attachment(client, test_attachment_data, test_group_data, test_homework_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    homework_id = homework_response.json()["id"]
    
    # Создаем вложение
    attachment_data = test_attachment_data.copy()
    attachment_data["homework_id"] = homework_id
    create_response = client.post("/attachments/", json=attachment_data)
    attachment_id = create_response.json()["id"]
    
    response = client.get(f"/attachments/{attachment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == attachment_id
    assert data["file_name"] == attachment_data["file_name"]

def test_read_nonexistent_attachment(client):
    response = client.get("/attachments/999")
    assert response.status_code == 404

def test_read_homework_attachments(client, test_attachment_data, test_group_data, test_homework_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    homework_id = homework_response.json()["id"]
    
    # Создаем несколько вложений для одного homework
    attachment_data1 = test_attachment_data.copy()
    attachment_data1["homework_id"] = homework_id
    
    attachment_data2 = test_attachment_data.copy()
    attachment_data2["file_name"] = "test2.txt"
    attachment_data2["homework_id"] = homework_id
    
    client.post("/attachments/", json=attachment_data1)
    client.post("/attachments/", json=attachment_data2)
    
    response = client.get(f"/attachments/homework/{homework_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_attachment(client, test_attachment_data, test_group_data, test_homework_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    homework_id = homework_response.json()["id"]
    
    # Создаем вложение
    attachment_data = test_attachment_data.copy()
    attachment_data["homework_id"] = homework_id
    create_response = client.post("/attachments/", json=attachment_data)
    attachment_id = create_response.json()["id"]
    
    # Обновляем
    update_data = {"caption": "str"}
    response = client.put(f"/attachments/{attachment_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["caption"] == "str"

def test_delete_attachment(client, test_attachment_data, test_group_data, test_homework_data):
    # Создаем группу
    group_response = client.post("/groups/", json=test_group_data)
    group_id = group_response.json()["id"]
    
    # Создаем домашнее задание
    homework_data = test_homework_data.copy()
    homework_data["group_id"] = group_id
    homework_response = client.post("/homeworks/", json=homework_data)
    homework_id = homework_response.json()["id"]
    
    # Создаем вложение
    attachment_data = test_attachment_data.copy()
    attachment_data["homework_id"] = homework_id
    create_response = client.post("/attachments/", json=attachment_data)
    attachment_id = create_response.json()["id"]
    
    # Удаляем
    response = client.delete(f"/attachments/{attachment_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Attachment deleted successfully"
    
    # Проверяем, что вложение удалено
    response = client.get(f"/attachments/{attachment_id}")
    assert response.status_code == 404

def test_create_attachment_without_homework_id(client, test_attachment_data):
    # Пытаемся создать вложение без homework_id (должно работать, если answer_id есть)
    attachment_data = test_attachment_data.copy()
    attachment_data.pop("homework_id", None)
    attachment_data.pop("answer_id", None)
    
    response = client.post("/attachments/", json=attachment_data)
    # Должна быть ошибка, так как нужно либо homework_id, либо answer_id
    assert response.status_code in [400, 422]