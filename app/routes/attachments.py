from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.attachment import AttachmentModel
from app.schemas.attachment import AttachmentCreate, Attachment, AttachmentUpdate

router = APIRouter(prefix="/attachments", tags=["attachments"])

@router.post(
    "/",
    response_model=Attachment,
    summary="Создать вложение",
    description="""
    Создает новое вложение в системе.
    
    **Параметры тела:**
    - file_name: Название файла
    - file_path: Путь к файлу
    - file_size: Размер файла в байтах
    - file_type: MIME-тип файла
    - homework_id: ID домашнего задания (опционально)
    - answer_id: ID ответа (опционально)
    
    **Возвращает:**
    - Созданное вложение
    
    **Использование:**
    - POST /attachments/
    
    **Примечание:**
    Вложение должно быть связано либо с домашним заданием, либо с ответом.
    """
)
def create_attachment(attachment: AttachmentCreate, db: Session = Depends(get_db)):
    db_attachment = AttachmentModel(**attachment.dict())
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.get(
    "/",
    response_model=List[Attachment],
    summary="Получить список вложений",
    description="""
    Возвращает список всех вложений с поддержкой пагинации.
    
    **Параметры запроса:**
    - skip: Количество записей для пропуска (по умолчанию 0)
    - limit: Максимальное количество записей для возврата (по умолчанию 100)
    
    **Возвращает:**
    - Список вложений
    
    **Использование:**
    - GET /attachments/
    - GET /attachments/?skip=10&limit=50
    """
)
def read_attachments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attachments = db.query(AttachmentModel).offset(skip).limit(limit).all()
    return attachments

@router.get(
    "/{attachment_id}",
    response_model=Attachment,
    summary="Получить вложение по ID",
    description="""
    Возвращает информацию о конкретном вложении по его идентификатору.
    
    **Параметры пути:**
    - attachment_id: ID вложения
    
    **Возвращает:**
    - Данные вложения
    
    **Ошибки:**
    - 404: Вложение с указанным ID не найдено
    
    **Использование:**
    - GET /attachments/123
    """
)
def read_attachment(attachment_id: int, db: Session = Depends(get_db)):
    db_attachment = db.query(AttachmentModel).filter(AttachmentModel.id == attachment_id).first()
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return db_attachment

@router.get(
    "/homework/{homework_id}",
    response_model=List[Attachment],
    summary="Получить вложения домашнего задания",
    description="""
    Возвращает все вложения, связанные с указанным домашним заданием.
    
    **Параметры пути:**
    - homework_id: ID домашнего задания
    
    **Возвращает:**
    - Список вложений для указанного домашнего задания
    
    **Использование:**
    - GET /attachments/homework/456
    
    **Примечание:"
    Возвращает пустой список, если для задания нет вложений.
    """
)
def read_homework_attachments(homework_id: int, db: Session = Depends(get_db)):
    attachments = db.query(AttachmentModel).filter(AttachmentModel.homework_id == homework_id).all()
    return attachments

@router.put(
    "/{attachment_id}",
    response_model=Attachment,
    summary="Обновить информацию о вложении",
    description="""
    Обновляет информацию о вложении. Можно обновлять только указанные поля.
    
    **Параметры пути:**
    - attachment_id: ID вложения для обновления
    
    **Параметры тела:**
    - file_name: Новое название файла (опционально)
    - file_path: Новый путь к файлу (опционально)
    - file_size: Новый размер файла (опционально)
    - file_type: Новый MIME-тип файла (опционально)
    
    **Возвращает:**
    - Обновленные данные вложения
    
    **Ошибки:**
    - 404: Вложение с указанным ID не найдено
    
    **Использование:**
    - PUT /attachments/123
    
    **Примечание:**
    Использует частичное обновление - только переданные поля будут изменены.
    """
)
def update_attachment(attachment_id: int, attachment: AttachmentUpdate, db: Session = Depends(get_db)):
    db_attachment = db.query(AttachmentModel).filter(AttachmentModel.id == attachment_id).first()
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    update_data = attachment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attachment, field, value)
    
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.delete(
    "/{attachment_id}",
    summary="Удалить вложение",
    description="""
    Удаляет вложение из системы по его ID.
    
    **Внимание:** Эта операция необратима. Файл будет удален из системы.
    Убедитесь, что удаление вложения не нарушит связанные данные.
    
    **Параметры пути:**
    - attachment_id: ID вложения для удаления
    
    **Возвращает:**
    - Сообщение об успешном удалении
    
    **Ошибки:**
    - 404: Вложение с указанным ID не найдено
    
    **Использование:**
    - DELETE /attachments/123
    
    **Примечание:**
    Рекомендуется сначала проверить, не используется ли вложение в важных данных
    перед удалением.
    """
)
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    db_attachment = db.query(AttachmentModel).filter(AttachmentModel.id == attachment_id).first()
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    db.delete(db_attachment)
    db.commit()
    return {"message": "Attachment deleted successfully"}