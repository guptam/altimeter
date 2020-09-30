# pylint: disable=too-few-public-methods
"""Pydantic Status schemas"""
from pydantic import BaseModel


class Status(BaseModel):
    """Status schema"""

    status: str
