# 1. Primeiro agente: Agent e Runner
# Um Agent combina nome, instruções, modelo e capacidades. O Runner executa o ciclo do agente até obter uma resposta final. Em notebooks, usamos await Runner.run(...); em scripts Python comuns, pode-se criar uma função async main() e chamá-la com asyncio.run(main()).

from agents import Agent, Runner
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "Adicione OPENAI_API_KEY ao arquivo .env na raiz do projeto."
    )

print("Chave configurada com segurança.")

assistente = Agent(
    name="Assistente didático",
    instructions=(
        "Responda em português brasileiro, com linguagem clara e um exemplo curto."
    ),
    model="gpt-4o-mini",
)

#  resultado = await Runner.run(
#     assistente,
#     "Explique recursão em programação em até cinco linhas.",
# )

# print(resultado.final_output)

async def Resultado():
    resultado = await Runner.run(
        assistente,
        "Explique recursão em programação em até cinco linhas.",
    )
    print(resultado.final_output)

# Executa a função assíncrona
asyncio.run(Resultado())