#!/usr/bin/env python3
"""
Script de teste para validar a API Mock Incremental
Execute este script para verificar se a API está funcionando corretamente
"""

import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Health check falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no health check: {e}")

def test_root_endpoint():
    """Testa o endpoint raiz"""
    print("\n🔍 Testando endpoint raiz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Endpoint raiz OK")
            data = response.json()
            print(f"   Mensagem: {data.get('message')}")
            print(f"   Endpoints: {list(data.get('endpoints', {}).keys())}")
        else:
            print(f"❌ Endpoint raiz falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no endpoint raiz: {e}")

def test_issues_endpoint():
    """Testa o endpoint de issues"""
    print("\n🔍 Testando endpoint de issues...")
    
    # Teste 1: Buscar todos os issues
    print("   Teste 1: Buscar todos os issues")
    try:
        response = requests.get(f"{BASE_URL}/api/issues")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retornou {len(data)} issues")
            if data:
                print(f"   📋 Primeiro issue: {data[0]}")
        else:
            print(f"   ❌ Falhou: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Buscar issues com filtro de data
    print("   Teste 2: Buscar issues com filtro de data")
    try:
        params = {
            "updatedAt_min": "2024-01-20T00:00:00",
            "updatedAt_max": "2024-01-25T23:59:59"
        }
        response = requests.get(f"{BASE_URL}/api/issues", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retornou {len(data)} issues no período")
            if data:
                print(f"   📋 Issues no período: {[item['id'] for item in data]}")
        else:
            print(f"   ❌ Falhou: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def test_projects_endpoint():
    """Testa o endpoint de projects"""
    print("\n🔍 Testando endpoint de projects...")
    
    # Teste 1: Buscar todos os projects
    print("   Teste 1: Buscar todos os projects")
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retornou {len(data)} projects")
            if data:
                print(f"   📋 Primeiro project: {data[0]}")
        else:
            print(f"   ❌ Falhou: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Buscar projects com filtro de data
    print("   Teste 2: Buscar projects com filtro de data")
    try:
        params = {
            "updatedAt_min": "2024-01-15T00:00:00",
            "updatedAt_max": "2024-01-20T23:59:59"
        }
        response = requests.get(f"{BASE_URL}/api/projects", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retornou {len(data)} projects no período")
            if data:
                print(f"   📋 Projects no período: {[item['id'] for item in data]}")
        else:
            print(f"   ❌ Falhou: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def test_incremental_scenarios():
    """Testa cenários de incremental refresh"""
    print("\n🔍 Testando cenários de incremental refresh...")
    
    # Simular busca de dados dos últimos 7 dias
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    print(f"   Simulando busca de dados dos últimos 7 dias")
    print(f"   Período: {week_ago.strftime('%Y-%m-%dT%H:%M:%S')} até {today.strftime('%Y-%m-%dT%H:%M:%S')}")
    
    try:
        params = {
            "updatedAt_min": week_ago.strftime("%Y-%m-%dT%H:%M:%S"),
            "updatedAt_max": today.strftime("%Y-%m-%dT%H:%M:%S")
        }
        
        # Teste issues
        response = requests.get(f"{BASE_URL}/api/issues", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Issues recentes: {len(data)} registros")
        
        # Teste projects
        response = requests.get(f"{BASE_URL}/api/projects", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Projects recentes: {len(data)} registros")
            
    except Exception as e:
        print(f"   ❌ Erro no teste incremental: {e}")

def test_deleted_records():
    """Testa se registros deletados são retornados"""
    print("\n🔍 Testando registros deletados...")
    
    try:
        # Buscar todos os issues para verificar se há registros com deletedAt
        response = requests.get(f"{BASE_URL}/api/issues")
        if response.status_code == 200:
            data = response.json()
            deleted_records = [item for item in data if item.get('deletedAt')]
            print(f"   ✅ Encontrados {len(deleted_records)} registros deletados")
            if deleted_records:
                print(f"   📋 IDs deletados: {[item['id'] for item in deleted_records]}")
        
        # Buscar todos os projects para verificar se há registros com deletedAt
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            data = response.json()
            deleted_records = [item for item in data if item.get('deletedAt')]
            print(f"   ✅ Encontrados {len(deleted_records)} registros deletados")
            if deleted_records:
                print(f"   📋 IDs deletados: {[item['id'] for item in deleted_records]}")
                
    except Exception as e:
        print(f"   ❌ Erro no teste de registros deletados: {e}")

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Mock Incremental")
    print("=" * 50)
    
    # Verificar se a API está rodando
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API não está respondendo. Certifique-se de que está rodando com:")
            print("   uvicorn app:app --reload --host 0.0.0.0 --port 8000")
            return
    except Exception as e:
        print("❌ Não foi possível conectar à API. Certifique-se de que está rodando.")
        print(f"   Erro: {e}")
        return
    
    # Executar testes
    test_health_check()
    test_root_endpoint()
    test_issues_endpoint()
    test_projects_endpoint()
    test_incremental_scenarios()
    test_deleted_records()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Se todos os testes passaram, a API está pronta para uso")
    print("2. Configure o Power BI para conectar em http://localhost:8000")
    print("3. Use os endpoints /api/issues e /api/projects")
    print("4. Configure o incremental refresh com os parâmetros updatedAt_min e updatedAt_max")

if __name__ == "__main__":
    main() 