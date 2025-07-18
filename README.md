# Mock API Incremental para Power BI

Este projeto implementa uma API mock para testar o incremental refresh no Power BI, simulando cenários reais de atualização de dados.

## 📁 Estrutura do Projeto

```
mock_incremental/
├── app.py              # API FastAPI principal
├── issues.csv          # Dados de issues/tickets
├── projects.csv        # Dados de projetos
├── requirements.txt    # Dependências Python
└── README.md          # Esta documentação
```

## 🚀 Instalação e Execução

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a API
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📊 Endpoints Disponíveis

### Endpoint Raiz
- **GET** `/` - Informações da API

### Endpoints de Dados
- **GET** `/api/issues` - Lista de issues/tickets
- **GET** `/api/projects` - Lista de projetos

### Endpoint de Health Check
- **GET** `/health` - Status da API

## 🔍 Parâmetros de Filtro

Ambos os endpoints aceitam filtros por `updatedAt`:

- `updatedAt_min` (opcional): Data mínima inclusiva (formato ISO: `2024-01-15T10:30:00`)
- `updatedAt_max` (opcional): Data máxima exclusiva (formato ISO: `2024-01-16T10:30:00`)

### Exemplos de Uso

```bash
# Buscar todos os issues
GET http://localhost:8000/api/issues

# Buscar issues atualizados após 2024-01-20
GET http://localhost:8000/api/issues?updatedAt_min=2024-01-20T00:00:00

# Buscar issues em um período específico
GET http://localhost:8000/api/issues?updatedAt_min=2024-01-20T00:00:00&updatedAt_max=2024-01-25T23:59:59

# Buscar projects atualizados em janeiro
GET http://localhost:8000/api/projects?updatedAt_min=2024-01-01T00:00:00&updatedAt_max=2024-02-01T00:00:00
```

## 📈 Configuração no Power BI

### 1. Conectar à API
1. No Power BI Desktop, vá em **Obter Dados** → **Web**
2. Digite a URL: `http://localhost:8000/api/issues`
3. Clique em **OK**

### 2. Configurar Incremental Refresh
1. Selecione a tabela importada
2. Vá em **Propriedades da Tabela**
3. Configure o **Incremental Refresh**:
   - **Atualizar dados nos últimos**: 7 dias
   - **Arquivar dados nos últimos**: 30 dias
   - **Detectar alterações de dados**: Sim
   - **Campo de detecção**: `updatedAt`

### 3. M Code para Incremental Refresh

```m
let
    Source = Json.Document(Web.Contents("http://localhost:8000/api/issues", [
        Query=[
            #"updatedAt_min"=DateTime.ToText(DateTime.LocalNow() - #duration(7,0,0,0), "yyyy-MM-ddTHH:mm:ss"),
            #"updatedAt_max"=DateTime.ToText(DateTime.LocalNow(), "yyyy-MM-ddTHH:mm:ss")
        ]
    ])),
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

## 🧪 Testando Cenários

### 1. Adicionar Novos Registros
Edite os arquivos CSV e adicione novos registros com `updatedAt` atual:

```csv
16,2024-02-08T14:30:00,,Novo bug reportado,high,open
```

### 2. Atualizar Registros Existentes
Modifique o campo `updatedAt` de registros existentes:

```csv
1,2024-02-08T15:45:00,,Bug no login - CORRIGIDO,high,closed
```

### 3. Simular Soft Delete
Adicione uma data no campo `deletedAt`:

```csv
5,2024-02-08T16:20:00,2024-02-08T16:20:00,Corrigir layout,medium,deleted
```

### 4. Testar Incremental Refresh
1. Execute o refresh no Power BI
2. Verifique se apenas os registros modificados foram atualizados
3. Confirme que registros deletados (com `deletedAt`) ainda aparecem

## 📋 Estrutura dos Dados

### Issues CSV
- `id`: Identificador único
- `updatedAt`: Data/hora da última atualização (ISO 8601)
- `deletedAt`: Data/hora da exclusão (vazio se não deletado)
- `text`: Descrição do issue
- `priority`: Prioridade (high/medium/low)
- `status`: Status (open/in_progress/closed)

### Projects CSV
- `id`: Identificador único
- `updatedAt`: Data/hora da última atualização (ISO 8601)
- `deletedAt`: Data/hora da exclusão (vazio se não deletado)
- `name`: Nome do projeto
- `description`: Descrição do projeto
- `status`: Status (active/inactive)
- `owner`: Responsável pelo projeto

## 🔧 Personalização

### Adicionar Novos Campos
1. Edite os arquivos CSV adicionando novas colunas
2. A API automaticamente retornará todos os campos

### Modificar Filtros
1. Edite a função `filter_by_updatedAt` em `app.py`
2. Adicione novos parâmetros de filtro conforme necessário

### Alterar Formato de Data
1. Modifique os exemplos de data nos parâmetros Query
2. Ajuste a função de filtro se necessário

## 🐛 Troubleshooting

### CORS Errors
- Verifique se o CORS está configurado corretamente
- Em produção, especifique apenas os domínios necessários

### Erro de Conexão
- Confirme se a API está rodando em `http://localhost:8000`
- Verifique se não há firewall bloqueando a porta

### Dados Não Atualizam
- Confirme se o `updatedAt` está no formato correto (ISO 8601)
- Verifique se os filtros estão sendo aplicados corretamente

## 📝 Logs

A API gera logs detalhados para debug:
- Requisições recebidas
- Filtros aplicados
- Quantidade de registros retornados
- Erros encontrados

## 🔒 Segurança

⚠️ **Atenção**: Esta é uma API mock para desenvolvimento. Em produção:
- Implemente autenticação
- Configure CORS adequadamente
- Use HTTPS
- Implemente rate limiting
- Valide inputs adequadamente 