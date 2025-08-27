from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user_group import UserGroupModel
from app.schemas.user_group import UserGroupCreate, UserGroup

router = APIRouter(prefix="/user-groups", tags=["user_groups"])

@router.post(
    "/",
    response_model=UserGroup,
    summary="Добавить пользователя в группу",
    description="""
    Создает связь между пользователем и группой с указанной ролью.
    
    **Параметры тела:**
    - user_id: ID пользователя
    - group_id: ID группы
    - user_role: Роль пользователя в группе
    
    **Возвращает:**
    - Созданную связь пользователь-группа
    
    **Ошибки:**
    - 400: Пользователь уже находится в этой группе
    
    **Использование:**
    - POST /user-groups/
    """
)
def add_user_to_group(user_group: UserGroupCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже такая связь
    db_user_group = db.query(UserGroupModel).filter(
        UserGroupModel.user_id == user_group.user_id,
        UserGroupModel.group_id == user_group.group_id
    ).first()
    
    if db_user_group:
        raise HTTPException(status_code=400, detail="User already in group")
    
    db_user_group = UserGroupModel(**user_group.dict())
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group

@router.get(
    "/",
    response_model=List[UserGroup],
    summary="Получить все связи пользователей и групп",
    description="""
    Возвращает список всех связей между пользователями и группами с пагинации.
    
    **Параметры запроса:**
    - skip: Количество записей для пропуска (по умолчанию 0)
    - limit: Максимальное количество записей для возврата (по умолчанию 100)
    
    **Возвращает:**
    - Список связей пользователь-группа
    
    **Использование:**
    - GET /user-groups/
    - GET /user-groups/?skip=10&limit=50
    """
)
def read_user_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_groups = db.query(UserGroupModel).offset(skip).limit(limit).all()
    return user_groups

@router.get(
    "/user/{user_id}",
    response_model=List[UserGroup],
    summary="Получить группы пользователя",
    description="""
    Возвращает все группы, в которых состоит указанный пользователь.
    
    **Параметры пути:**
    - user_id: ID пользователя
    
    **Возвращает:"
    - Список связей пользователь-группа для указанного пользователя
    
    **Ошибки:**
    - 404: Пользователь не найден (если нет ни одной связи)
    
    **Использование:**
    - GET /user-groups/user/123
    """
)
def read_user_groups_by_user(user_id: int, db: Session = Depends(get_db)):
    user_groups = db.query(UserGroupModel).filter(UserGroupModel.user_id == user_id).all()
    return user_groups

@router.get(
    "/group/{group_id}",
    response_model=List[UserGroup],
    summary="Получить пользователей группы",
    description="""
    Возвращает всех пользователей, состоящих в указанной группе.
    
    **Параметры пути:**
    - group_id: ID группы
    
    **Возвращает:**
    - Список связей пользователь-группа для указанной группы
    
    **Ошибки:**
    - 404: Группа не найдена (если нет ни одного пользователя)
    
    **Использование:**
    - GET /user-groups/group/456
    """
)
def read_group_users(group_id: int, db: Session = Depends(get_db)):
    user_groups = db.query(UserGroupModel).filter(UserGroupModel.group_id == group_id).all()
    return user_groups

@router.get(
    "/{user_id}/{group_id}",
    response_model=UserGroup,
    summary="Получить конкретную связь пользователь-группа",
    description="""
    Возвращает информацию о конкретной связи между пользователем и группой.
    
    **Параметры пути:**
    - user_id: ID пользователя
    - group_id: ID группы
    
    **Возвращает:**
    - Связь пользователь-группа
    
    **Ошибки:**
    - 404: Пользователь не найден в указанной группе
    
    **Использование:**
    - GET /user-groups/123/456
    """
)
def read_user_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    user_group = db.query(UserGroupModel).filter(
        UserGroupModel.user_id == user_id,
        UserGroupModel.group_id == group_id
    ).first()
    
    if user_group is None:
        raise HTTPException(status_code=404, detail="User not found in group")
    
    return user_group

@router.put(
    "/{user_id}/{group_id}",
    response_model=UserGroup,
    summary="Изменить роль пользователя в группе",
    description="""
    Обновляет роль пользователя в указанной группе.
    
    **Параметры пути:**
    - user_id: ID пользователя
    - group_id: ID группы
    
    **Параметры тела:**
    - user_role: Новая роль пользователя в группе
    
    **Возвращает:**
    - Обновленную связь пользователь-группа
    
    **Ошибки:**
    - 404: Пользователь не найден в указанной группе
    
    **Использование:**
    - PUT /user-groups/123/456
    """
)
def update_user_group_role(user_id: int, group_id: int, user_role: str, db: Session = Depends(get_db)):
    user_group = db.query(UserGroupModel).filter(
        UserGroupModel.user_id == user_id,
        UserGroupModel.group_id == group_id
    ).first()
    
    if user_group is None:
        raise HTTPException(status_code=404, detail="User not found in group")
    
    user_group.user_role = user_role
    db.commit()
    db.refresh(user_group)
    return user_group

@router.delete(
    "/{user_id}/{group_id}",
    summary="Удалить пользователя из группы",
    description="""
    Удаляет связь между пользователем и группой.
    
    **Внимание:** Эта операция удаляет пользователя из группы.
    Убедитесь, что это не нарушит функциональность системы.
    
    **Параметры пути:**
    - user_id: ID пользователя для удаления из группы
    - group_id: ID группы
    
    **Возвращает:**
    - Сообщение об успешном удалении
    
    **Ошибки:**
    - 404: Пользователь не найден в указанной группе
    
    **Использование:"
    - DELETE /user-groups/123/456
    
    **Примечание:**
    Удаление пользователя из группы может повлиять на его доступ к материалам
    и функциональности, связанной с этой группе.
    """
)
def remove_user_from_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    user_group = db.query(UserGroupModel).filter(
        UserGroupModel.user_id == user_id,
        UserGroupModel.group_id == group_id
    ).first()
    
    if user_group is None:
        raise HTTPException(status_code=404, detail="User not found in group")
    
    db.delete(user_group)
    db.commit()
    return {"message": "User removed from group successfully"}