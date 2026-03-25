from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TipoPagamento(str, Enum):
    PIX = "PIX"
    CREDITO = "Credito"


class PagamentoCreate(BaseModel):
    cliente_id: str
    codigo: str
    valor_total: float = Field(gt=0)
    tipo: TipoPagamento
    parcelas: int = Field(ge=1)
    data_pagamento: date


class PagamentoResponse(BaseModel):
    id: UUID
    cliente_id: str
    cliente_email: str
    codigo: str
    valor_total: float
    tipo: str
    parcelas: int
    valor_parcela: float
    data_pagamento: date

    class Config:
        from_attributes = True
