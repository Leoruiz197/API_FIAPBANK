from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

class ContaSchema(BaseModel):
    agencia: str = Field(..., min_length=4, max_length=5, description="Número da agência (ex: 0001)")
    numero: str = Field(..., min_length=5, max_length=10, description="Número da conta corrente")
    saldo: float = Field(default=0.0, ge=0.0, description="Saldo inicial da conta (não pode ser negativo)")
    id_cliente: int = Field(..., description="ID único do cliente associado a esta conta")

class ClientSchema(BaseModel):
    id_cliente: int = Field(..., description="ID único do cliente associado a esta conta")
    nome_completo: str = Field(..., description="Nome completo do Cliente")
    idade: int = Field(..., description="Idade do Cliente (minimo 14)")
    telefone: str = Field(..., description="Numero do Cliente (minimo 14)")

banco_dados_fake = []

app = FastAPI()

# Define a rota principal usando decorators parecidos com o Flask
@app.get("/")
def read_root():
    return {"mensagem": "FIAPBANK, API para transações financeiras!"}

@app.get("/contas", summary="Buscar conta por agência e número")
def read_conta(agencia: str, numero: str):
    
    # Percorre o nosso "banco de dados" procurando a combinação exata
    for conta in banco_dados_fake:
        if conta["agencia"] == agencia and conta["numero"] == numero:
            return {
                "mensagem": "Conta encontrada com sucesso!",
                "dados_da_conta": conta
            }
            
    # Se percorrer toda a lista e não encontrar nada, lança um erro 404 (Not Found)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Conta com a agência {agencia} e número {numero} não foi encontrada."
    )

@app.post("/contas/create", status_code=status.HTTP_201_CREATED, summary="Criar uma nova conta bancária")
def criar_conta(conta: ContaSchema):
    # Aqui você inseriria a lógica para salvar no banco de dados real (ex: MySQL, PostgreSQL)
    
    # Validação simples para evitar contas duplicadas na nossa lista fake
    for c in banco_dados_fake:
        if c["agencia"] == conta.agencia and c["numero"] == conta.numero:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Esta conta já está cadastrada nesta agência."
            )
    
    # Converte o objeto do Pydantic para um dicionário Python comum
    nova_conta = conta.model_dump()
    banco_dados_fake.append(nova_conta)
    
    return {
        "mensagem": "Conta criada com sucesso!",
        "dados_da_conta": nova_conta
    }

# Rota de exemplo recebendo um parâmetro na URL e uma query string opcional
@app.get("/itens/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "busca": q}

clientes_lista = []

@app.post("/clientes/create", status_code=status.HTTP_201_CREATED, summary="Criar uma nova conta bancária")
def criar_cliente(clientes: ClientSchema):
    for c in clientes_lista:
        if c["id_cliente"] == clientes.id_cliente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Cliente já cadastrato"
            )
        
        if clientes.idade < 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Idade abaixo da minima, volte em {14 - clientes.idade} anos"
            )
    
    novo_cliente = clientes.model_dump()
    clientes_lista.append(novo_cliente)
    
    return {
        "mensagem": "Cliente criado com sucesso!",
        "cliente_data": novo_cliente
    }        


@app.get("/clientes/{id}", summary="Buscar cliente por id")
def read_cliente(id: int):
    
    for cliente in clientes_lista:
        if cliente["id_cliente"] == id:
            return {
                "mensagem": "Cliente encontrado!",
                "cliente_data": cliente
            }
            
    # Se percorrer toda a lista e não encontrar nada, lança um erro 404 (Not Found)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cliente com id {id} nao localizado"
    )