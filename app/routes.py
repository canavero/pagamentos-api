from typing import Optional
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pagamento
from app.schemas import PagamentoCreate, PagamentoResponse

router = APIRouter()

USERS_API_URL = "http://18.228.48.67/users"


@router.get("/pagamento", response_model=list[PagamentoResponse])
def listar_pagamentos(cliente_id: Optional[str] = None, db: Session = Depends(get_db)):
    if cliente_id:
        pagamentos = db.query(Pagamento).filter(Pagamento.cliente_id == cliente_id).all()
    else:
        pagamentos = db.query(Pagamento).all()
    return pagamentos


@router.delete("/pagamento/{pagamento_id}")
def deletar_pagamento(pagamento_id: UUID, db: Session = Depends(get_db)):
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento nao encontrado")
    db.delete(pagamento)
    db.commit()
    return {"message": "Pagamento deletado com sucesso"}


@router.post("/pagamento", response_model=PagamentoResponse, status_code=201)
def criar_pagamento(dados: PagamentoCreate, db: Session = Depends(get_db)):
    # Validar cliente na API externa
    response = httpx.get(f"{USERS_API_URL}/{dados.cliente_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    response.raise_for_status()

    usuario = response.json()
    cliente_email = usuario["email"]

    # Calcular valor da parcela
    valor_parcela = round(dados.valor_total / dados.parcelas, 2)

    pagamento = Pagamento(
        cliente_id=dados.cliente_id,
        cliente_email=cliente_email,
        codigo=dados.codigo,
        valor_total=dados.valor_total,
        tipo=dados.tipo.value,
        parcelas=dados.parcelas,
        valor_parcela=valor_parcela,
        data_pagamento=dados.data_pagamento,
    )

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento
