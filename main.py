from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from Schema.Cliente import ClientSchema
from routes.contas import router as router_contas

app = FastAPI()

# Registrar o router de contas
app.include_router(router_contas)

# Define a rota principal usando decorators parecidos com o Flask
@app.get("/")
def read_root():
    return {"mensagem": "FIAPBANK, API para transações financeiras!"}

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