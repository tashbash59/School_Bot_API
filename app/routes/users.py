from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import UserModel
from app.schemas.user import UserCreate, User, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/", 
    response_model=User,
    summary="Создать нового пользователя",
    description="""
    Создает нового пользователя в системе.
    
    **Проверяет наличие пользователя с таким telegram_id** перед созданием.
    Если пользователь с указанным telegram_id уже существует, возвращает ошибку 400.
    
    **Параметры:**
    - user: Данные для создания пользователя (UserCreate schema)
    
    **Возвращает:**
    - Созданный объект пользователя
    
    **Ошибки:**
    - 400: Пользователь с таким telegram_id уже существует
    """
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким telegram_id
    db_user = db.query(UserModel).filter(UserModel.telegram_id == user.telegram_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get(
    "/", 
    response_model=List[User],
    summary="Получить список пользователей",
    description="""
    Возвращает список всех пользователей с поддержкой пагинации.
    
    **Параметры запроса:**
    - skip: Количество записей для пропуска (для пагинации)
    - limit: Максимальное количество возвращаемых записей (максимум 100)
    
    **Возвращает:**
    - Список объектов пользователей
    
    **Использование:**
    - GET /users/?skip=0&limit=20
    """
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get(
    "/{user_id}", 
    response_model=User,
    summary="Получить пользователя по ID",
    description="""
    Возвращает информацию о пользователе по его внутреннему ID.
    
    **Параметры пути:"
    - user_id: Внутренний идентификатор пользователя в системе
    
    **Возвращает:**
    - Объект пользователя
    
    **Ошибки:**
    - 404: Пользователь с указанным ID не найден
    
    **Использование:**
    - GET /users/123
    """
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get(
    "/telegram/{telegram_id}", 
    response_model=User,
    summary="Получить пользователя по Telegram ID",
    description="""
    Возвращает информацию о пользователе по его Telegram ID.
    Полезно для интеграции с Telegram ботами.
    
    **Параметры пути:**
    - telegram_id: Идентификатор пользователя в Telegram
    
    **Возвращает:**
    - Объект пользователя
    
    **Ошибки:**
    - 404: Пользователь с указанным Telegram ID не найден
    
    **Использование:**
    - GET /users/telegram/123456789
    """
)
def read_user_by_telegram(telegram_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put(
    "/{user_id}", 
    response_model=User,
    summary="Обновить данные пользователя",
    description="""
    Обновляет информацию о пользователе. Поддерживает частичное обновление - 
    можно передавать только те поля, которые нужно изменить.
    
    **Параметры пути:**
    - user_id: Внутренний идентификатор пользователя для обновления
    
    **Тело запроса:**
    - user: Данные для обновления (UserUpdate schema)
    
    **Возвращает:**
    - Обновленный объект пользователя
    
    **Ошибки:**
    - 404: Пользователь с указанным ID не найден
    
    **Использование:**
    - PUT /users/123
    """
)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete(
    "/{user_id}",
    summary="Удалить пользователя",
    description="""
    Удаляет пользователя из системы по его внутреннему ID.
    
    **Внимание:** Эта операция необратима. Все данные пользователя будут удалены.
    
    **Параметры пути:**
    - user_id: Внутренний идентификатор пользователя для удаления
    
    **Возвращает:**
    - Сообщение об успешном удалении
    
    **Ошибки:**
    - 404: Пользователь с указанным ID не найден
    
    **Использование:**
    - DELETE /users/123
    """
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}