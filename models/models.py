from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class Service(BaseModel):
    """Informação sobre um serviço."""
    name: str = Field(description="Nome do serviço")
    description: str = Field(description="Descrição do serviço")
    phases: List[str]