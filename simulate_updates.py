#!/usr/bin/env python3
"""
Script para simular atualizações nos dados CSV
Este script adiciona novos registros e atualiza existentes para testar o incremental refresh
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def add_new_issues():
    """Adiciona novos issues ao CSV"""
    print("📝 Adicionando novos issues...")
    
    # Ler dados existentes
    df = pd.read_csv("issues.csv")
    
    # Gerar novos IDs
    max_id = df['id'].astype(int).max()
    new_ids = range(max_id + 1, max_id + 6)
    
    # Dados de exemplo para novos issues
    new_issues = []
    current_time = datetime.now()
    
    for i, new_id in enumerate(new_ids):
        # Criar data de atualização (últimas 24 horas)
        hours_ago = random.randint(1, 24)
        updated_at = current_time - timedelta(hours=hours_ago)
        
        issues_data = [
            {
                'id': str(new_id),
                'updatedAt': updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'deletedAt': '',
                'text': f'Novo issue {new_id} - {["Bug crítico", "Melhoria", "Feature", "Documentação", "Teste"][i]}',
                'priority': random.choice(['high', 'medium', 'low']),
                'status': random.choice(['open', 'in_progress', 'closed'])
            }
        ]
        new_issues.extend(issues_data)
    
    # Adicionar novos registros
    new_df = pd.DataFrame(new_issues)
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    # Salvar
    updated_df.to_csv("issues.csv", index=False)
    print(f"✅ Adicionados {len(new_issues)} novos issues")
    
    return new_issues

def update_existing_issues():
    """Atualiza issues existentes"""
    print("🔄 Atualizando issues existentes...")
    
    # Ler dados existentes
    df = pd.read_csv("issues.csv")
    
    # Selecionar alguns issues para atualizar (excluindo os deletados)
    non_deleted = df[df['deletedAt'] == ''].copy()
    if len(non_deleted) > 0:
        # Selecionar 3 issues aleatórios para atualizar
        to_update = non_deleted.sample(min(3, len(non_deleted)))
        
        current_time = datetime.now()
        
        for idx in to_update.index:
            # Atualizar updatedAt para agora
            df.loc[idx, 'updatedAt'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            
            # Atualizar status ou texto
            if random.choice([True, False]):
                df.loc[idx, 'status'] = random.choice(['open', 'in_progress', 'closed'])
            else:
                df.loc[idx, 'text'] = df.loc[idx, 'text'] + ' - ATUALIZADO'
        
        # Salvar
        df.to_csv("issues.csv", index=False)
        print(f"✅ Atualizados {len(to_update)} issues existentes")
        
        return to_update['id'].tolist()
    
    return []

def simulate_soft_delete():
    """Simula soft delete de alguns issues"""
    print("🗑️ Simulando soft delete...")
    
    # Ler dados existentes
    df = pd.read_csv("issues.csv")
    
    # Selecionar issues não deletados
    non_deleted = df[df['deletedAt'] == ''].copy()
    if len(non_deleted) > 0:
        # Selecionar 1 issue para deletar
        to_delete = non_deleted.sample(min(1, len(non_deleted)))
        
        current_time = datetime.now()
        
        for idx in to_delete.index:
            # Marcar como deletado
            df.loc[idx, 'deletedAt'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            df.loc[idx, 'updatedAt'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            df.loc[idx, 'status'] = 'deleted'
        
        # Salvar
        df.to_csv("issues.csv", index=False)
        print(f"✅ Soft delete aplicado em {len(to_delete)} issue(s)")
        
        return to_delete['id'].tolist()
    
    return []

def add_new_projects():
    """Adiciona novos projetos ao CSV"""
    print("📝 Adicionando novos projetos...")
    
    # Ler dados existentes
    df = pd.read_csv("projects.csv")
    
    # Gerar novos IDs
    max_id = df['id'].astype(int).max()
    new_ids = range(max_id + 1, max_id + 4)
    
    # Dados de exemplo para novos projetos
    new_projects = []
    current_time = datetime.now()
    
    project_names = [
        "Sistema de Analytics",
        "App de Gestão Financeira", 
        "Portal de Vendas"
    ]
    
    descriptions = [
        "Dashboard avançado de analytics",
        "Aplicativo para controle financeiro",
        "Portal integrado de vendas"
    ]
    
    owners = ["Ana Silva", "Carlos Santos", "Maria Costa"]
    
    for i, new_id in enumerate(new_ids):
        # Criar data de atualização (últimas 24 horas)
        hours_ago = random.randint(1, 24)
        updated_at = current_time - timedelta(hours=hours_ago)
        
        projects_data = {
            'id': str(new_id),
            'updatedAt': updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
            'deletedAt': '',
            'name': project_names[i],
            'description': descriptions[i],
            'status': 'active',
            'owner': owners[i]
        }
        new_projects.append(projects_data)
    
    # Adicionar novos registros
    new_df = pd.DataFrame(new_projects)
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    # Salvar
    updated_df.to_csv("projects.csv", index=False)
    print(f"✅ Adicionados {len(new_projects)} novos projetos")
    
    return new_projects

def update_existing_projects():
    """Atualiza projetos existentes"""
    print("🔄 Atualizando projetos existentes...")
    
    # Ler dados existentes
    df = pd.read_csv("projects.csv")
    
    # Selecionar alguns projetos para atualizar (excluindo os deletados)
    non_deleted = df[df['deletedAt'] == ''].copy()
    if len(non_deleted) > 0:
        # Selecionar 2 projetos aleatórios para atualizar
        to_update = non_deleted.sample(min(2, len(non_deleted)))
        
        current_time = datetime.now()
        
        for idx in to_update.index:
            # Atualizar updatedAt para agora
            df.loc[idx, 'updatedAt'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            
            # Atualizar status ou descrição
            if random.choice([True, False]):
                df.loc[idx, 'status'] = random.choice(['active', 'inactive'])
            else:
                df.loc[idx, 'description'] = df.loc[idx, 'description'] + ' - ATUALIZADO'
        
        # Salvar
        df.to_csv("projects.csv", index=False)
        print(f"✅ Atualizados {len(to_update)} projetos existentes")
        
        return to_update['id'].tolist()
    
    return []

def main():
    """Executa todas as simulações"""
    print("🚀 Iniciando simulação de atualizações de dados")
    print("=" * 50)
    
    # Simular atualizações nos issues
    new_issues = add_new_issues()
    updated_issues = update_existing_issues()
    deleted_issues = simulate_soft_delete()
    
    print()
    
    # Simular atualizações nos projects
    new_projects = add_new_projects()
    updated_projects = update_existing_projects()
    
    print("\n" + "=" * 50)
    print("✅ Simulação concluída!")
    print("\n📊 Resumo das alterações:")
    print(f"   Issues adicionados: {len(new_issues)}")
    print(f"   Issues atualizados: {len(updated_issues)}")
    print(f"   Issues deletados: {len(deleted_issues)}")
    print(f"   Projetos adicionados: {len(new_projects)}")
    print(f"   Projetos atualizados: {len(updated_projects)}")
    
    print("\n🧪 Próximos passos para testar:")
    print("1. Execute o Power BI e conecte à API")
    print("2. Configure o incremental refresh")
    print("3. Execute o refresh e verifique se apenas os dados novos/atualizados foram carregados")
    print("4. Verifique se os registros deletados ainda aparecem (soft delete)")

if __name__ == "__main__":
    main() 