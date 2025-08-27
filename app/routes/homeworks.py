from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.homework import HomeworkModel
from app.schemas.homework import HomeworkCreate, Homework, HomeworkUpdate

router = APIRouter(prefix="/homeworks", tags=["homeworks"])

@router.post(
    "/", 
    response_model=Homework,
    summary="Создать новое домашнее задание",
    description="""
    Создает новое домашнее задание в системе.
    
    **Параметры:**
    - homework: Данные для создания домашнего задания (HomeworkCreate schema)
    
    **Возвращает:**
    - Созданный объект домашнего задания
    
    **Использование:**
    - POST /homeworks/
    - Тело запроса: JSON с данными домашнего задания
    
    **Примечание:**
    Обязательные поля обычно включают title, description, group_id и deadline.
    Проверьте схему HomeworkCreate для точного списка обязательных полей.
    """
)
def create_homework(homework: HomeworkCreate, db: Session = Depends(get_db)):
    db_homework = HomeworkModel(**homework.dict())
    db.add(db_homework)
    db.commit()
    db.refresh(db_homework)
    return db_homework

@router.get(
    "/", 
    response_model=List[Homework],
    summary="Получить список всех домашних заданий",
    description="""
    Возвращает список всех домашних заданий с поддержкой пагинации.
    
    **Параметры запроса:**
    - skip: Количество записей для пропуска (для пагинации)
    - limit: Максимальное количество возвращаемых записей (максимум 100)
    
    **Возвращает:**
    - Список объектов домашних заданий
    
    **Использование:**
    - GET /homeworks/?skip=0&limit=20
    - GET /homeworks/?limit=50
    
    **Примечание:**
    Для получения заданий конкретной группы используйте /homeworks/group/{group_id}
    """
)
def read_homeworks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    homeworks = db.query(HomeworkModel).offset(skip).limit(limit).all()
    return homeworks

@router.get(
    "/{homework_id}", 
    response_model=Homework,
    summary="Получить домашнее задание по ID",
    description="""
    Возвращает информацию о домашнем задании по его внутреннему ID.
    
    **Параметры пути:**
    - homework_id: Внутренний идентификатор домашнего задания в системе
    
    **Возвращает:**
    - Объект домашнего задания с детальной информацией
    
    **Ошибки:**
    - 404: Домашнее задание с указанным ID не найдено
    
    **Использование:**
    - GET /homeworks/123
    - GET /homeworks/45
    
    **Примечание:**
    ID домашнего задания является числовым идентификатором в базе данных.
    """
)
def read_homework(homework_id: int, db: Session = Depends(get_db)):
    db_homework = db.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
    if db_homework is None:
        raise HTTPException(status_code=404, detail="Homework not found")
    return db_homework

@router.get(
    "/group/{group_id}", 
    response_model=List[Homework],
    summary="Получить домашние задания по ID группы",
    description="""
    Возвращает список домашних заданий для конкретной группы.
    
    **Параметры пути:**
    - group_id: Идентификатор группы, для которой нужно получить задания
    
    **Возвращает:"
    - Список объектов домашних заданий, принадлежащих указанной группе
    
    **Использование:**
    - GET /homeworks/group/123
    - GET /homeworks/group/45
    
    **Примечание:**
    Полезно для отображения всех заданий конкретной учебной группы.
    Возвращает как активные, так и завершенные задания.
    """
)
def read_group_homeworks(group_id: int, db: Session = Depends(get_db)):
    homeworks = db.query(HomeworkModel).filter(HomeworkModel.group_id == group_id).all()
    return homeworks

@router.put(
    "/{homework_id}", 
    response_model=Homework,
    summary="Обновить данные домашнего задания",
    description="""
    Обновляет информацию о домашнем задании. Поддерживает частичное обновление - 
    можно передавать только те поля, которые нужно изменить.
    
    **Параметры пути:**
    - homework_id: Внутренний идентификатор домашнего задания для обновления
    
    **Тело запроса:**
    - homework: Данные для обновления (HomeworkUpdate schema)
    
    **Возвращает:**
    - Обновленный объект домашнего задания
    
    **Ошибки:**
    - 404: Домашнее задание с указанным ID не найдено
    
    **Использование:**
    - PUT /homeworks/123
    - Тело запроса: JSON с обновляемыми полями
    
    **Примечание:**
    Часто обновляемые поля: title, description, deadline, is_completed.
    """
)
def update_homework(homework_id: int, homework: HomeworkUpdate, db: Session = Depends(get_db)):
    db_homework = db.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
    if db_homework is None:
        raise HTTPException(status_code=404, detail="Homework not found")
    
    update_data = homework.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_homework, field, value)
    
    db.commit()
    db.refresh(db_homework)
    return db_homework

@router.delete(
    "/{homework_id}",
    summary="Удалить домашнее задание",
    description="""
    Удаляет домашнее задание из системы по его внутреннему ID.
    
    **Внимание:** Эта операция необратима. Все данные домашнего задания будут удалены.
    Убедитесь, что удаление задания не нарушит связанные данные (например, ответы студентов).
    
    **Параметры пути:**
    - homework_id: Внутренний идентификатор домашнего задания для удаления
    
    **Возвращает:**
    - Сообщение об успешном удалении
    
    **Ошибки:**
    - 404: Домашнее задание с указанным ID не найдено
    
    **Использование:**
    - DELETE /homeworks/123
    
    **Примечание:**
    Рекомендуется использовать осторожно, особенно для заданий, на которые уже есть ответы студентов.
    Рассмотрите возможность архивирования вместо полного удаления.
    """
)
def delete_homework(homework_id: int, db: Session = Depends(get_db)):
    db_homework = db.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
    if db_homework is None:
        raise HTTPException(status_code=404, detail="Homework not found")
    
    db.delete(db_homework)
    db.commit()
    return {"message": "Homework deleted successfully"}