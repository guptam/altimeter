"""Base pydantic altimeter model"""
from pydantic import BaseModel


class BaseAltiModel(BaseModel):
    """Base pydantic altimeter model"""

    class Config:
        """Pydantic config"""

        allow_mutation = False
        extra = "forbid"
        arbitrary_types_allowed = True
