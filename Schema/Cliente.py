from pydantic import BaseModel, Field

class ClientSchema(BaseModel):
    id_cliente: int = Field(..., description="ID único do cliente associado a esta conta")
    nome_completo: str = Field(..., description="Nome completo do Cliente")
    idade: int = Field(..., description="Idade do Cliente (minimo 14)")
    telefone: str = Field(..., description="Numero do Cliente (minimo 14)")