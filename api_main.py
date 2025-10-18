from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from coleta.local_Coleta import carregarArquivoLoc
from analise.dadosFormatar import formatar_colunas
from pydantic import BaseModel
from typing import Dict, Any
from analise.dadosAPI import carregarAPI

app = FastAPI(
    title="AxiomaPy API",
    description="Uma API para coleta, processamento e análise de dados.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à AxiomaPy API!"}

# Novo endpoint para upload de arquivos
@app.post("/data/upload-local/")
async def upload_local_file(file: UploadFile = File(...)):
    # Salva o arquivo temporariamente para que a função original possa lê-lo
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Usa a sua função original para carregar o arquivo em um DataFrame
    df = carregarArquivoLoc(temp_file_path)

    if df is None:
        raise HTTPException(status_code=400, detail="Não foi possível processar o arquivo.")

    # Converte o DataFrame para JSON e retorna
    # orient='records' transforma o DF em uma lista de dicionários
    return df.to_dict(orient='records')

# Endpoint para buscar dados de uma API externa
class APIParams(BaseModel):
    params: Dict[str, Any]

# Endpoint para buscar dados de uma API externa
@app.post("/data/load-from-api/{api_name}")
def load_from_external_api(api_name: str, api_params: APIParams):
    # A função carregarAPI precisa ser refatorada para não usar 'input()' (já refatorada)
    # Ela deve receber o nome da API e os parâmetros diretamente.

    from utils.leitorAPIconfig import carregar_configuracoes_api
    from coleta.api_Coleta import APIDados

    configs = carregar_configuracoes_api()
    if api_name not in configs:
        raise HTTPException(status_code=404, detail=f"API '{api_name}' não configurada.")

    api_config = configs[api_name]
    api_client = APIDados(api_config)

    # Atribui os parâmetros recebidos na requisição
    api_client.params = api_params.params

    df = api_client.consultar_dataframe()

    if df is None:
        raise HTTPException(status_code=500, detail="Falha ao coletar dados da API externa.")

    return df.to_dict(orient='records')