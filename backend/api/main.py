import sys
import os

import uvicorn

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from backend.api import open_dota_router  # Importa seu arquivo de rotas

app = FastAPI(
    title="Dota 2 Build Analyzer",
    description="API para analisar builds de jogadores a partir de partidas do Dota 2",
    version="1.0.0"
)

# Inclui as rotas da API
app.include_router(open_dota_router.router, prefix="/open_dota", tags=["OpenDota"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)