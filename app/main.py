from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, groups, homeworks, attachments, user_groups

# Пересоздаем таблицы
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Bot API",
    description="REST API для Telegram бота школы программирования",
    version="1.0.0"
)

# Подключаем роуты
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(homeworks.router)
app.include_router(attachments.router)
app.include_router(user_groups.router)

@app.get("/")
def read_root():
    return {"message": "School Bot API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)