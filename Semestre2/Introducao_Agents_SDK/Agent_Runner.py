from agents import Agent, Runner
import asyncio

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

async def main():
    resultado = await Runner.run(
        assistente,
        "Explique recursão em programação em até cinco linhas.",
    )
    print(resultado.final_output)

# Executa a função assíncrona
asyncio.run(main())