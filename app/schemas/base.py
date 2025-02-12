from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseSchema(BaseModel):
    """
    Base Pydantic schema with common configuration
    """
    model_config = ConfigDict(from_attributes=True)

class BaseResponseSchema(BaseSchema):
    """
    Base schema for all response models
    """
    id: int
    created_at: datetime
    updated_at: datetime

class BaseCreateSchema(BaseSchema):
    """
    Base schema for create operations
    """
    pass

class BaseUpdateSchema(BaseSchema):
    """
    Base schema for update operations
    """
    pass