from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mock API Incremental - Power BI",
    description="API para testar incremental refresh no Power BI",
    version="1.0.0"
)

# Configurar CORS para permitir acesso do Power BI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique apenas os domínios necessários
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def filter_by_updatedAt(df: pd.DataFrame, updatedAt_min: Optional[str], updatedAt_max: Optional[str]) -> pd.DataFrame:
    """
    Filtra o DataFrame por intervalo de updatedAt
    """
    if updatedAt_min:
        logger.info(f"Filtrando por updatedAt >= {updatedAt_min}")
        df = df[df["updatedAt"] >= updatedAt_min]
    
    if updatedAt_max:
        logger.info(f"Filtrando por updatedAt < {updatedAt_max}")
        df = df[df["updatedAt"] < updatedAt_max]
    
    return df

@app.get("/")
def read_root():
    """
    Endpoint raiz com informações da API
    """
    return {
        "message": "Mock API Incremental para Power BI",
        "endpoints": {
            "issues": "/api/issues",
            "projects": "/api/projects"
        },
        "usage": "Use os parâmetros updatedAt_min e updatedAt_max para filtros incrementais"
    }

@app.get("/api/issues")
def get_issues(
    updatedAt_min: Optional[str] = Query(None, description="Data mínima (inclusiva) - formato ISO: 2024-01-15T10:30:00"),
    updatedAt_max: Optional[str] = Query(None, description="Data máxima (exclusiva) - formato ISO: 2024-01-16T10:30:00")
):
    """
    Retorna issues com filtro opcional por updatedAt
    """
    try:
        logger.info(f"Buscando issues - min: {updatedAt_min}, max: {updatedAt_max}")
        
        # Ler CSV
        df = pd.read_csv("issues.csv", dtype=str)
        
        # Aplicar filtros
        df = filter_by_updatedAt(df, updatedAt_min, updatedAt_max)
        
        # Converter para dict e substituir NaN por string vazia
        result = df.fillna("").to_dict(orient="records")
        
        logger.info(f"Retornando {len(result)} issues")
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar issues: {str(e)}")
        return []

@app.get("/api/projects")
def get_projects(
    updatedAt_min: Optional[str] = Query(None, description="Data mínima (inclusiva) - formato ISO: 2024-01-10T08:00:00"),
    updatedAt_max: Optional[str] = Query(None, description="Data máxima (exclusiva) - formato ISO: 2024-01-11T08:00:00")
):
    """
    Retorna projects com filtro opcional por updatedAt
    """
    try:
        logger.info(f"Buscando projects - min: {updatedAt_min}, max: {updatedAt_max}")
        
        # Ler CSV
        df = pd.read_csv("projects.csv", dtype=str)
        
        # Aplicar filtros
        df = filter_by_updatedAt(df, updatedAt_min, updatedAt_max)
        
        # Converter para dict e substituir NaN por string vazia
        result = df.fillna("").to_dict(orient="records")
        
        logger.info(f"Retornando {len(result)} projects")
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar projects: {str(e)}")
        return []

@app.get("/health")
def health_check():
    """
    Endpoint de health check
    """
    return {"status": "healthy", "message": "API funcionando normalmente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 