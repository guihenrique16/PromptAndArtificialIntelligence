from agents import Agent, Runner, WebSearchTool
import os
from dotenv import load_dotenv
import asyncio

# 3. Hosted tools
# Hosted tools são executadas na infraestrutura da OpenAI. Diferentemente de uma function tool, seu programa não implementa a execução da ferramenta. Elas exigem um modelo OpenAI compatível com a Responses API, caminho usado por padrão pelo SDK para modelos OpenAI.
# Nesta seção veremos WebSearchTool, FileSearchTool e CodeInterpreterTool.

# 3.1 WebSearchTool: informações atuais
# WebSearchTool permite pesquisar informações recentes na web. A instrução exige fontes e datas, reduzindo o risco de apresentar fatos desatualizados como atuais.

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "Adicione OPENAI_API_KEY ao arquivo .env na raiz do projeto."
    )

print("Chave configurada com segurança.")

agente_pesquisa = Agent(
    name="Pesquisador web",
    instructions=(
        "Pesquise a web quando a pergunta depender de informação atual. "
        "Diferencie a data de publicação da data do acontecimento, cite as fontes "
        "e diga quando houver informações conflitantes."
    ),
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o-mini",
)

async def Resultado_Noticia():
    resultado = await Runner.run(
        agente_pesquisa,
        "Pesquise uma notícia recente sobre transporte público em São Paulo e resuma em três tópicos.",
    )
    print(resultado.final_output)

asyncio.run(Resultado_Noticia())