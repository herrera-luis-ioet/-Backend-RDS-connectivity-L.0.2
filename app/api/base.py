from typing import Generic, TypeVar, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.base import BaseCRUDService
from app.schemas.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseResponseSchema)

class BaseCRUDRouter(Generic[CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """
    Base router class for CRUD operations
    """
    def __init__(
        self,
        service: BaseCRUDService,
        create_schema: type[CreateSchemaType],
        update_schema: type[UpdateSchemaType],
        response_schema: type[ResponseSchemaType],
        prefix: str,
        tags: List[str]
    ):
        self.service = service
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self._register_routes()

    def _register_routes(self):
        """Register all CRUD routes"""
        
        @self.router.get("/{id}", response_model=self.response_schema)
        async def get_by_id(id: int, db: Session = Depends(get_db)):
            """Get a record by ID"""
            result = self.service.get(db, id)
            if not result:
                raise HTTPException(status_code=404, detail="Record not found")
            return result

        @self.router.get("/", response_model=List[self.response_schema])
        async def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            """Get all records with pagination"""
            return self.service.get_all(db, skip=skip, limit=limit)

        @self.router.post("/", response_model=self.response_schema)
        async def create(obj_in: CreateSchemaType, db: Session = Depends(get_db)):
            """Create a new record"""
            return self.service.create(db, obj_in)

        @self.router.put("/{id}", response_model=self.response_schema)
        async def update(id: int, obj_in: UpdateSchemaType, db: Session = Depends(get_db)):
            """Update a record"""
            return self.service.update(db, id, obj_in)

        @self.router.delete("/{id}")
        async def delete(id: int, db: Session = Depends(get_db)):
            """Delete a record"""
            self.service.delete(db, id)
            return {"message": "Record deleted successfully"}