from pydantic import BaseModel, Field

class ContaSchema(BaseModel):
    agencia: str = Field(..., min_length=4, max_length=5, description="Número da agência (ex: 0001)")
    numero: str = Field(..., min_length=5, max_length=10, description="Número da conta corrente")
    saldo: float = Field(default=0.0, ge=0.0, description="Saldo inicial da conta (não pode ser negativo)")
    id_cliente: int = Field(..., description="ID único do cliente associado a esta conta")