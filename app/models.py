import uuid
from datetime import date

from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(String, nullable=False)
    cliente_email = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    valor_total = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)  # PIX ou Credito
    parcelas = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)
    data_pagamento = Column(Date, nullable=False, default=date.today)
