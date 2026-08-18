from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from pm_workflow.core.entity import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: str) -> ModelType | None:
        return db.get(self.model, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> list[ModelType]:
        return db.query(self.model).limit(limit).offset(offset).all()

    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: str) -> None:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
