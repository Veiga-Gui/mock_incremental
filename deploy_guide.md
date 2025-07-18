# 🚀 Guia de Deploy - API Mock Incremental

## 📋 Pré-requisitos
- Conta no GitHub (gratuita)
- Conta no Railway (gratuita)

## 🔧 Passo a Passo - Deploy no Railway

### 1. Preparar o Repositório
```bash
# Inicializar git (se ainda não foi feito)
git init
git add .
git commit -m "Initial commit - API Mock Incremental"

# Criar repositório no GitHub
# 1. Vá para github.com
# 2. Clique em "New repository"
# 3. Nome: mock-incremental-api
# 4. Deixe público
# 5. NÃO inicialize com README
# 6. Clique em "Create repository"

# Conectar ao GitHub
git remote add origin https://github.com/SEU_USUARIO/mock-incremental-api.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Railway
1. **Acesse**: [railway.app](https://railway.app)
2. **Faça login** com GitHub
3. **Clique** em "New Project"
4. **Selecione** "Deploy from GitHub repo"
5. **Escolha** o repositório `mock-incremental-api`
6. **Clique** em "Deploy Now"

### 3. Configurar Variáveis (Opcional)
- Railway detectará automaticamente que é uma aplicação Python
- Os arquivos `requirements.txt`, `Procfile` e `runtime.txt` já estão configurados

### 4. Acessar a API
- Após o deploy, Railway fornecerá uma URL como: `https://mock-incremental-api-production-xxxx.up.railway.app`
- Teste: `https://sua-url.railway.app/health`

## 🧪 Testar a API Online

### Endpoints Disponíveis:
```
https://sua-url.railway.app/
https://sua-url.railway.app/health
https://sua-url.railway.app/api/issues
https://sua-url.railway.app/api/projects
```

### Exemplos de Uso:
```
# Todos os issues
https://sua-url.railway.app/api/issues

# Issues com filtro
https://sua-url.railway.app/api/issues?updatedAt_min=2024-01-20T00:00:00

# Projects com filtro
https://sua-url.railway.app/api/projects?updatedAt_min=2024-01-15T00:00:00
```

## 🔄 Atualizar Dados (Opcional)

Para atualizar os dados CSV online:
1. **Vá** para o projeto no Railway
2. **Clique** em "Variables"
3. **Adicione** variáveis de ambiente se necessário
4. **Redeploy** se precisar atualizar os CSVs

## 📊 Usar no Power BI

### URL da API:
```
https://sua-url.railway.app/api/issues
https://sua-url.railway.app/api/projects
```

### M Code para Power BI:
```m
let
    Source = Json.Document(Web.Contents("https://sua-url.railway.app/api/issues")),
    #"Converted to Table" = Table.FromRecords(Source),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{
        {"id", type text},
        {"updatedAt", type datetime},
        {"deletedAt", type datetime},
        {"text", type text},
        {"priority", type text},
        {"status", type text}
    })
in
    #"Changed Type"
```

## 🆓 Plano Gratuito do Railway
- **500 horas/mês** de execução
- **1GB** de RAM
- **1GB** de storage
- **Perfeito** para testes e desenvolvimento

## 🔍 Troubleshooting

### Erro de Deploy:
- Verifique se todos os arquivos estão no repositório
- Confirme se `requirements.txt` está correto
- Verifique os logs no Railway

### API não responde:
- Verifique se o deploy foi concluído
- Teste o endpoint `/health` primeiro
- Verifique os logs no Railway

### CORS Issues:
- A API já está configurada com CORS liberado
- Se houver problemas, verifique se a URL está correta

## 🎯 Próximos Passos
1. Deploy no Railway
2. Teste os endpoints
3. Configure no Power BI
4. Teste o incremental refresh no Power BI Service 