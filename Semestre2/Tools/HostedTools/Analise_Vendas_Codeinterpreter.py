# Exemplo 2 — análise estatística de vendas

# O agente recebe uma pequena série de vendas, calcula estatísticas descritivas e identifica observações acima de média mais um desvio padrão. Pedir método e valores intermediários facilita conferir a resposta.

import asyncio

from agents import Agent, CodeInterpreterTool, Runner
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "Adicione OPENAI_API_KEY ao arquivo .env na raiz do projeto."
    )

print("Chave configurada com segurança.")

agente_calculos = Agent(
    name="Analista quantitativo",
    instructions=(
        "Use o Code Interpreter em todos os cálculos. "
        "Mostre a fórmula, os valores substituídos e o resultado arredondado."
    ),
    tools=[
        CodeInterpreterTool(
            tool_config={
                "type": "code_interpreter",
                "container": {"type": "auto"},
            }
        )
    ],
    model="gpt-4o-mini",
)

vendas = [82, 79, 91, 88, 84, 120, 86, 83, 95, 89, 130, 87]

prompt_analise = (
    f"Analise as vendas semanais: {vendas}\n"
    "1. Calcule média, mediana, desvio padrão amostral e coeficiente de variação.\n"
    "2. Identifique valores acima de média + 1 desvio padrão.\n"
    "3. Explique em linguagem simples o que os resultados sugerem.\n"
    "Use Python e mostre os valores utilizados."
)

async def resultado_analise():
    resultado = await Runner.run(
        agente_calculos,
        prompt_analise,
    )
    print(resultado.final_output)

    resultado.raw_responses[0]

asyncio.run(resultado_analise())


