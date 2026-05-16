from fastapi import APIRouter, HTTPException, status
from Schema.Conta import ContaSchema

router = APIRouter()
banco_dados_fake = []


@router.get("/contas", summary="Buscar conta por agência e número")
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

@router.post("/contas/create", status_code=status.HTTP_201_CREATED, summary="Criar uma nova conta bancária")
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
