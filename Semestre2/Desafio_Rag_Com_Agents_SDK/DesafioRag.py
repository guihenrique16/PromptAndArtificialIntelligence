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

politica = Path("Semestre2/Desafio_Rag_Com_Agents_SDK/manual_do_candidato_2026.pdf")

client = OpenAI()
vector_store = client.vector_stores.create(name="Base de conhecimento Fiap")

with politica.open("rb") as arquivo:
    arquivo_indexado = client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=arquivo,
    )

print("Vector store:", vector_store.id)
print("Status da indexação:", arquivo_indexado.status)



agente_documentos = Agent(
    name="Aura",
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

async def resultado():
    resultadoF = await Runner.run(
        agente_documentos,
        """Qual o valor da inscrição?""",
    )
    print(resultadoF.final_output)  

asyncio.run(resultado())
