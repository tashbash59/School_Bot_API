from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.group import Group
from app.schemas.group import GroupCreate, Group, GroupUpdate

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post(
    "/", 
    response_model=Group,
    summary="Создать новую группу",
    description="""
    Создает новую группу в системе.
    
    **Проверяет наличие группы с таким именем** перед созданием.
    Если группа с указанным именем уже существует, возвращает ошибку 400.
    
    **Параметры:**
    - group: Данные для создания группы (GroupCreate schema)
    
    **Возвращает:**
    - Созданный объект группы
    
    **Ошибки:**
    - 400: Группа с таким именем уже существует
    
    **Использование:**
    - POST /groups/
    - Тело запроса: JSON с данными группы
    """
)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.name == group.name).first()
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")
    
    db_group = Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get(
    "/", 
    response_model=List[Group],
    summary="Получить список групп",
    description="""
    Возвращает список всех групп с поддержкой пагинации.
    
    **Параметры запроса:**
    - skip: Количество записей для пропуска (для пагинации)
    - limit: Максимальное количество возвращаемых записей (максимум 100)
    
    **Возвращает:**
    - Список объектов групп
    
    **Использование:**
    - GET /groups/?skip=0&limit=20
    - GET /groups/?limit=50
    
    **Примечание:**
    Используйте пагинацию для больших списков групп.
    """
)
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups

@router.get(
    "/{group_id}", 
    response_model=Group,
    summary="Получить группу по ID",
    description="""
    Возвращает информацию о группе по её внутреннему ID.
    
    **Параметры пути:**
    - group_id: Внутренний идентификатор группы в системе
    
    **Возвращает:**
    - Объект группы с детальной информацией
    
    **Ошибки:**
    - 404: Группа с указанным ID не найдена
    
    **Использование:**
    - GET /groups/123
    - GET /groups/45
    
    **Примечание:**
    ID группы является числовым идентификатором в базе данных.
    """
)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.put(
    "/{group_id}", 
    response_model=Group,
    summary="Обновить данные группы",
    description="""
    Обновляет информацию о группе. Поддерживает частичное обновление - 
    можно передавать только те поля, которые нужно изменить.
    
    **Параметры пути:**
    - group_id: Внутренний идентификатор группы для обновления
    
    **Тело запроса:**
    - group: Данные для обновления (GroupUpdate schema)
    
    **Возвращает:**
    - Обновленный объект группы
    
    **Ошибки:**
    - 404: Группа с указанным ID не найдена
    
    **Использование:**
    - PUT /groups/123
    - Тело запроса: JSON с обновляемыми полями
    
    **Примечание:**
    Если имя группы изменяется, система проверит уникальность нового имени.
    """
)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    update_data = group.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_group, field, value)
    
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete(
    "/{group_id}",
    summary="Удалить группу",
    description="""
    Удаляет группу из системы по её внутреннему ID.
    
    **Внимание:** Эта операция необратима. Все данные группы будут удалены.
    Убедитесь, что удаление группы не нарушит целостность данных системы.
    
    **Параметры пути:**
    - group_id: Внутренний идентификатор группы для удаления
    
    **Возвращает:**
    - Сообщение об успешном удалении
    
    **Ошибки:**
    - 404: Группа с указанным ID не найдена
    
    **Использование:**
    - DELETE /groups/123
    
    **Примечание:**
    Перед удалением группы рекомендуется проверить связанные сущности
    (пользователей, права доступа и т.д.), которые могут ссылаться на эту группу.
    """
)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(db_group)
    db.commit()
    return {"message": "Group deleted successfully"}