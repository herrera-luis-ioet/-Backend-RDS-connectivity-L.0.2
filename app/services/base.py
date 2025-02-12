from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from app.models.base import BaseModel
from app.schemas.base import BaseCreateSchema, BaseUpdateSchema
from fastapi.exceptions import HTTPException

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)

class BaseCRUDService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> ModelType:
        """Update a record"""
        db_obj = self.get(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Record not found")
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> bool:
        """Delete a record"""
        db_obj = self.get(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Record not found")
        
        db.delete(db_obj)
        db.commit()
        return True