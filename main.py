from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/notes",
    tags=["Заметки"],
)

app = FastAPI(
    title="Простое CRUD API для заметок",
    description="Простое API для управления заметками с поддержкой CRUD операций",
    version="0.0.1",
)


@router.post(
    "/",
    response_model=schemas.Note,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заметку",
    description="Создает новую заметку с заголовком и содержимым",
    responses={
        201: {"description": "Заметка успешно создана"},
        422: {"description": "Ошибка валидации данных"}
    }
)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note)


@router.get(
    "/",
    response_model=list[schemas.Note],
    summary="Получить список заметок",
    responses={
        200: {"description": "Список заметок успешно получен"}
    }
)
def read_notes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_notes(db, skip=skip, limit=limit)


@router.get(
    "/{note_id}",
    response_model=schemas.Note,
    summary="Получить заметку по ID",
    responses={
        200: {"description": "Заметка успешно получена"},
        404: {"description": "Заметка не найдена"}
    }
)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Заметка с ID {note_id} не найдена")
    return db_note


@router.put(
    "/{note_id}",
    response_model=schemas.Note,
    summary="Обновить заметку",
    responses={
        200: {"description": "Заметка успешно обновлена"},
        404: {"description": "Заметка не найдена"},
        422: {"description": "Ошибка валидации данных"}
    }
)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.update_note(db, note_id=note_id, note=note)
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Заметка с ID {note_id} не найдена")
    return db_note


@router.delete(
    "/{note_id}",
    response_model=schemas.Note,
    summary="Удалить заметку",
    responses={
        200: {"description": "Заметка успешно удалена"},
        404: {"description": "Заметка не найдена"}
    }
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.delete_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Заметка с ID {note_id} не найдена")
    return db_note

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)