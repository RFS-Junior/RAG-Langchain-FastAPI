# LangChain Fast API

## Visão Geral

Este projeto implementa uma API usando FastAPI para gerenciar serviços, com funcionalidades para buscar serviços com base em perguntas utilizando LangChain e Qdrant para indexação, além de permitir a adição de exemplos de serviços à coleção Qdrant.

## Funcionalidades Principais

- **Busca de Serviços**: Utiliza LangChain e Qdrant para retornar serviços com base em perguntas fornecidas.
- **Adição de Exemplos**: Permite adicionar novos serviços à coleção Qdrant para indexação e pesquisa.
- **Suporte a Fases de Serviço**: Cada serviço pode ter várias fases, permitindo uma descrição detalhada do ciclo de vida.

## Pré-requisitos

- Python 3.7 ou superior instalado
- Pacotes especificados em `requirements.txt`
- Variáveis de ambiente configuradas (veja seção de Configuração)

## Instalação

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

Antes de iniciar a aplicação, configure as variáveis de ambiente necessárias. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
QDRANT_URL=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=nome-da-sua-colecao
```

Substitua os valores acima conforme sua configuração do Qdrant.

## Uso

1. **Inicie o Servidor FastAPI:**

   ```bash
   uvicorn main:app --reload
   ```

2. **Documentação da API:**

   Acesse `http://localhost:8000/docs` no seu navegador para ver a documentação interativa da API. Lá você pode testar os endpoints diretamente.

## Exemplos de Uso

### Busca de Serviço

**Endpoint:** `POST /search_service`

```json
{
  "question": "Como eu faço para enviar um pacote?"
}
```

### Adição de Exemplos

**Endpoint:** `POST /add_examples`

```json
[
  {
    "name": "Nome do Serviço",
    "description": "Descrição detalhada do serviço",
    "phases": ["Fase 1", "Fase 2"]
  }
]
```

## Contato

- Ronivaldo Júnior
- juniorferreira59@outlook.com

Conecte-se comigo no LinkedIn: [Ronivaldo Júnior](https://www.linkedin.com/in/ronivaldo-junior/)