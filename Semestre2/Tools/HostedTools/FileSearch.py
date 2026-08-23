# 3.2 FileSearchTool: visão geral
# FileSearchTool realiza busca semântica em documentos previamente indexados em um vector store. O fluxo tem duas partes:
#   1. preparar e enviar os arquivos ao vector store;
#   2. fornecer o ID desse vector store ao agente.
# O exemplo cria um arquivo didático pequeno. Em um projeto real, substitua-o por PDFs, documentos ou textos da sua base de conhecimento.

# Etapa 1 — criar o documento e o vector store
# O cliente OpenAI administra o upload. upload_and_poll aguarda a indexação terminar, evitando que o agente pesquise antes de o conteúdo estar pronto. Execute esta preparação uma vez e reutilize o vector_store.id nas execuções seguintes.

import asyncio
from pathlib import Path
from openai import OpenAI
from agents import Agent, FileSearchTool, Runner
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Adicione OPENAI_API_KEY ao arquivo .env na raiz do projeto."
    )
print("Chave configurada com segurança.")

pasta = Path(__file__).parent / "content"
pasta.mkdir(exist_ok=True)

politica = pasta / "politica.txt"

politica.write_text(
    "Política de trocas da TechMais\n"
    "- Produtos sem defeito podem ser trocados em até 7 dias corridos.\n"
    "- É necessário apresentar o comprovante de compra.\n"
    "- Produtos com defeito passam por avaliação técnica.\n"
    "- O prazo de avaliação técnica é de até 5 dias úteis.\n"
    "- Itens com dano causado por mau uso não são cobertos.\n",
    encoding="utf-8",
)

client = OpenAI()
vector_store = client.vector_stores.create(name="Base de conhecimento TechMais")

with politica.open("rb") as arquivo:
    arquivo_indexado = client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=arquivo,
    )

print("Vector store:", vector_store.id)
print("Status da indexação:", arquivo_indexado.status)

# Etapa 2 — responder com base no documento
# max_num_results limita a quantidade de trechos recuperados. include_search_results=True mantém os resultados da busca na resposta bruta, o que ajuda em auditoria e depuração. As instruções orientam o agente a admitir quando a base não contém a resposta.

agente_documentos = Agent(
    name="Assistente da TechMais",
    instructions=(
        "Responda somente com base nos documentos encontrados. "
        "Informe o documento usado. Se a base não contiver a resposta, diga isso claramente."
    ),
    tools=[
        FileSearchTool(
            vector_store_ids=[vector_store.id],
            max_num_results=5,
            include_search_results=True,
        )
    ],
    model="gpt-4o-mini",
)

async def Resultado_Documentos():
    resultado = await Runner.run(
        agente_documentos,
        """Com quantos dias posso trocar?""",
    )
    print(resultado.final_output)

asyncio.run(Resultado_Documentos())

# Exemplo adicional — comparar duas regras do documento
# Uma boa pergunta de recuperação exige combinar trechos relacionados. Aqui, o agente diferencia troca sem defeito de avaliação de produto defeituoso e evita misturar os dois prazos.
async def Comparacao():
    resultado = await Runner.run(
        agente_documentos,
        "Compare o processo de troca sem defeito com o processo de produto defeituoso. Organize em tabela.",
    )
    print(resultado.final_output)

asyncio.run(Comparacao())

# Exemplo adicional — testar ausência de informação
# Testar perguntas fora da base é uma prática importante. O comportamento esperado é declarar que a informação não foi encontrada, em vez de preencher a lacuna com conhecimento geral ou suposição.
async def Teste_Ausencia():      
    resultado = await Runner.run(
        agente_documentos,
        "Qual é o telefone da loja e qual é o horário de atendimento?",
    )
    print(resultado.final_output)

asyncio.run(Teste_Ausencia())