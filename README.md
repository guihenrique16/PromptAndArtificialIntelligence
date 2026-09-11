# Prompt and Artificial Intelligence

Repositório de estudos práticos da disciplina de **Prompt and Artificial Intelligence**, desenvolvido em Python com a **OpenAI Agents SDK**.

## Conteúdos estudados

* Criação de agentes com `Agent`
* Execução assíncrona com `Runner` e `asyncio`
* Escrita de instruções e prompts
* Uso de variáveis de ambiente com `.env` e `python-dotenv`
* Function tools com `@function_tool`
* Hosted tools: Web Search, File Search e Code Interpreter
* RAG com vector stores
* Handoffs entre agentes especializados
* Persistência de contexto com `SQLiteSession`
* Leitura e alteração de dados em CSV
* Validação e confirmação de operações

## Estrutura

```text
Semestre2/
├── Introducao_Agents_SDK/
├── Tools/
│   ├── FunctionTools/
│   └── HostedTools/
├── Desafio_Rag_Com_Agents_SDK/
└── CP4e5_Banco_MultiAgente/
```

## Projetos

### Introdução ao Agents SDK

Pasta: `Semestre2/Introducao_Agents_SDK`

Primeiro estudo da estrutura de um agente. O exemplo utiliza `Agent`, `Runner`, instruções, `gpt-4o-mini`, `asyncio` e leitura segura da chave de API.

### Function Tools

Pasta: `Semestre2/Tools/FunctionTools`

Agente de clima que usa uma função Python como ferramenta. A aplicação consulta a API Open-Meteo, valida os dados retornados e evita que o modelo invente informações.

Conceitos estudados:

* `@function_tool`
* Type hints e docstrings
* Consumo de APIs externas
* Timeout e tratamento de respostas
* Dados estruturados para agentes

### Hosted Tools

Pasta: `Semestre2/Tools/HostedTools`

Estudos das ferramentas hospedadas pela OpenAI:

| Ferramenta            | Aplicação                                                                |
| --------------------- | ------------------------------------------------------------------------ |
| `WebSearchTool`       | Pesquisa de informações recentes na web, com fontes e datas.             |
| `FileSearchTool`      | Busca semântica em documentos indexados em vector stores.                |
| `CodeInterpreterTool` | Execução de Python em ambiente isolado para cálculos e análise de dados. |

Também foram realizados exemplos de cálculo de *lift* percentual e análise estatística de vendas com média, mediana, desvio padrão e coeficiente de variação.

### Desafio RAG com Agents SDK

Pasta: `Semestre2/Desafio_Rag_Com_Agents_SDK`

Aplicação de RAG usando o arquivo `manual_do_candidato_2026.pdf` como base de conhecimento. O documento é enviado para um vector store, indexado e consultado por um agente.

Conceitos estudados:

* Upload e indexação de documentos
* Vector stores
* Busca semântica com `FileSearchTool`
* Respostas baseadas exclusivamente nos documentos
* Tratamento de perguntas sem resposta na base

### Banco Multiagente

Pasta: `Semestre2/CP4e5_Banco_MultiAgente`

Projeto prático de um banco fictício com três agentes:

* **Agente de Atendimento:** identifica a intenção do cliente e faz o encaminhamento.
* **Agente PIX:** realiza operações relacionadas a saldo, contatos e PIX.
* **Agente de Dúvidas:** responde perguntas sobre conta, cartões, tarifas, saques e PIX.

O projeto usa handoffs entre agentes e `SQLiteSession` para manter o contexto da conversa.

#### Funcionalidades

* Consultar saldo
* Listar, buscar e adicionar contatos PIX
* Preparar PIX com validação de saldo
* Exigir confirmação explícita antes da transferência
* Cancelar PIX pendentes
* Atualizar saldo após a transferência
* Registrar e consultar histórico de transações
* Encerrar o atendimento com mensagens como `sair`, `só isso por hoje` e `era só isso`

#### Dados em CSV

| Arquivo              | Finalidade                             |
| -------------------- | -------------------------------------- |
| `saldo.csv`          | Armazena o saldo do cliente.           |
| `contatos_pix.csv`   | Armazena contatos e chaves PIX.        |
| `transacoes_pix.csv` | Registra as transferências realizadas. |

## Configuração do ambiente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie um arquivo `.env` com:

```env
OPENAI_API_KEY=sua_chave_aqui
```

> Nunca envie o arquivo `.env` para o GitHub.

## Tecnologias utilizadas

* Python
* OpenAI Agents SDK
* OpenAI API
* GPT-4o mini
* Python Dotenv
* Requests
* CSV
* SQLite
* Open-Meteo API

## Autor

**Guilherme Henrique**
Estudante de Ciência da Computação — FIAP
