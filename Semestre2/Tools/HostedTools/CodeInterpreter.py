# 3.3 CodeInterpreterTool: visão geral

# CodeInterpreterTool permite ao modelo escrever e executar Python em um contêiner isolado. É útil para cálculos, estatística, transformação de dados e geração de gráficos. Com container={"type": "auto"}, a infraestrutura cria o ambiente automaticamente para a execução.

# O resultado deve ser verificado: executar código reduz erros aritméticos, mas não garante que o método estatístico escolhido seja adequado.

# Exemplo 1 — cálculo verificável
# As instruções obrigam o agente a usar Python e apresentar fórmula, substituição e resultado. Isso torna o raciocínio numérico mais auditável para os alunos.

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

async def resultado_calculos():
    resultado = await Runner.run(
        agente_calculos,
        "Uma loja vendeu 128 unidades contra um concorrente que vendeu 80. Calcule o lift percentual.",
    )
    print(resultado.final_output)

asyncio.run(resultado_calculos())