# RotaFácil API - Sistema de Gerenciamento de Transporte Escolar

## 📋 Descrição

API RESTful desenvolvida com FastAPI e MongoDB para gerenciamento de transporte escolar. O sistema utiliza um modelo não relacional orientado a documentos, explorando as vantagens do MongoDB como flexibilidade de esquema, embedding de dados e operações de agregação complexas.

## 🏗️ Arquitetura

### Modelo de Dados MongoDB

- **alunos**: Usuario + Aluno embutidos (1:1)
- **motoristas**: Usuario + Motorista embutidos (1:1)
- **veiculos**: Coleção independente
- **rotas**: Rota + Pontos de Parada embutidos (1:N)
- **viagens**: Referenciando outras entidades (1:N)
- **frequencias**: Linking collection para relação N:N

### Estratégias de Modelagem

- **Embedding**: Para relacionamentos "contém" ou "um-para-poucos"
- **Referencing**: Para relacionamentos "um-para-muitos" ou "muitos-para-muitos"
- **Linking Collection**: Para relações N:N complexas

## 🚀 Tecnologias

- **Python 3.9+**
- **FastAPI** - Framework web
- **MongoDB** - Banco de dados NoSQL
- **Motor** - Driver assíncrono para MongoDB
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📦 Instalação

### Pré-requisitos

1. Python 3.9 ou superior
2. MongoDB instalado e rodando
3. Git

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd ProjetoDePersistencia
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Edite o arquivo config.env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=rotafacil
   ```

5. **Inicie o MongoDB**
   ```bash
   # Certifique-se de que o MongoDB está rodando
   mongod
   ```

6. **Execute a aplicação**
   ```bash
   python main.py
   ```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Funcionalidades Implementadas

### F1: Inserir uma entidade
- `POST /api/v1/alunos/`
- `POST /api/v1/motoristas/`
- `POST /api/v1/veiculos/`
- `POST /api/v1/rotas/`
- `POST /api/v1/viagens/`

### F2: Listar todas as entidades
- `GET /api/v1/alunos/`
- `GET /api/v1/motoristas/`
- `GET /api/v1/veiculos/`
- `GET /api/v1/rotas/`
- `GET /api/v1/viagens/`

### F3: CRUD completo
- `GET /api/v1/{entidade}/{id}` - Buscar por ID
- `PUT /api/v1/{entidade}/{id}` - Atualizar
- `DELETE /api/v1/{entidade}/{id}` - Deletar

### F4: Mostrar quantidade de entidades
- `GET /api/v1/{entidade}/quantidade/total`

### F5: Implementar paginação
- `GET /api/v1/{entidade}/pagina/?page=0&limit=10`

### F6: Filtrar por atributos
- `GET /api/v1/{entidade}/buscar/?parametro=valor`
- `GET /api/v1/{entidade}/buscar/texto/?texto=termo`

### F7: Consultas Complexas (Agregação MongoDB)

#### Viagens Detalhadas
```bash
GET /api/v1/viagens/{id}/detalhes
```
Retorna viagem com dados completos do motorista, veículo e rota.

#### Alunos de uma Viagem
```bash
GET /api/v1/viagens/{id}/alunos
```
Lista todos os alunos que embarcaram em uma viagem específica.

#### Estatísticas por Período
```bash
GET /api/v1/viagens/estatisticas/periodo/?data_inicio=2024-01-01&data_fim=2024-12-31
```

#### Estatísticas de Veículos
```bash
GET /api/v1/veiculos/estatisticas/
```

## 📊 Exemplos de Uso

### Criar um Veículo
```bash
curl -X POST "http://localhost:8000/api/v1/veiculos/" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC1234",
    "modelo": "Ônibus Escolar",
    "capacidade_passageiros": 30,
    "status_manutencao": "Disponível",
    "adaptado_pcd": false,
    "ano_fabricacao": 2020
  }'
```

### Criar uma Rota
```bash
curl -X POST "http://localhost:8000/api/v1/rotas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_rota": "Rota Centro",
    "descricao": "Rota que atende o centro da cidade",
    "turno": "Manhã",
    "ativa": true,
    "pontos_de_parada": [
      {
        "nome_ponto": "Ponto Central",
        "endereco": "Rua Principal, 123",
        "lat": -3.1190,
        "lon": -60.0217,
        "ordem": 1
      },
      {
        "nome_ponto": "Escola",
        "endereco": "Av. Educação, 456",
        "lat": -3.1200,
        "lon": -60.0220,
        "ordem": 2
      }
    ]
  }'
```

### Consulta Complexa - Viagem Detalhada
```bash
curl "http://localhost:8000/api/v1/viagens/{viagem_id}/detalhes"
```

## 🔍 Endpoints Especiais

### Veículos
- `GET /api/v1/veiculos/disponiveis/` - Veículos disponíveis
- `GET /api/v1/veiculos/adaptados-pcd/` - Veículos adaptados para PCD

### Rotas
- `GET /api/v1/rotas/ativas/` - Rotas ativas
- `GET /api/v1/rotas/turno/{turno}` - Rotas por turno
- `GET /api/v1/rotas/mais-pontos/` - Rotas ordenadas por número de pontos

### Alunos
- `GET /api/v1/alunos/necessidades-especiais/` - Alunos com necessidades especiais
- `GET /api/v1/alunos/ponto-embarque/{ponto_id}` - Alunos por ponto de embarque

### Motoristas
- `GET /api/v1/motoristas/ativos/` - Motoristas ativos
- `GET /api/v1/motoristas/inativos/` - Motoristas inativos

### Viagens
- `GET /api/v1/viagens/status/{status}` - Viagens por status
- `GET /api/v1/viagens/hoje/` - Viagens de hoje
- `GET /api/v1/viagens/motorista/{motorista_id}` - Viagens por motorista
- `GET /api/v1/viagens/rota/{rota_id}` - Viagens por rota

## 🗄️ Estrutura do Projeto

```
ProjetoDePersistencia/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── config.py
│   ├── database.py
│   ├── models/
│   │   └── pydantic_models.py
│   ├── routers/
│   │   ├── router_aluno.py
│   │   ├── router_motorista.py
│   │   ├── router_veiculo.py
│   │   ├── router_rota.py
│   │   └── router_viagem.py
│   └── services/
│       └── crud_services.py
├── config.env
├── main.py
├── requirements.txt
├── start.py
├── start_backend.py
├── exemplos_uso.py
└── README.md
```

## 🧪 Testes

Para testar a API, você pode usar:

1. **Swagger UI**: Acesse `http://localhost:8000/docs`
2. **curl**: Use os exemplos acima
3. **Postman**: Importe os endpoints
4. **Insomnia**: Configure as requisições
5. **Script de exemplo**: Execute `python exemplos_uso.py`

## 🔧 Configuração de Desenvolvimento

### Variáveis de Ambiente
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=rotafacil
```

### Logs
A aplicação gera logs detalhados durante a execução. Monitore o console para informações sobre:
- Conexão com MongoDB
- Operações de banco de dados
- Erros e exceções

## 🚀 Deploy

### Produção
1. Configure as variáveis de ambiente para produção
2. Use um servidor WSGI como Gunicorn
3. Configure um proxy reverso (Nginx)
4. Configure SSL/TLS
5. Configure backups do MongoDB

### Docker (Opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Licença

Este projeto foi desenvolvido como parte de um trabalho acadêmico sobre persistência de dados.

## 👥 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação da API
- Verifique os logs da aplicação 