# 2. Function tools
# Uma function tool transforma uma função Python em uma ferramenta que o modelo pode escolher e chamar. Type hints e docstrings são importantes porque ajudam o SDK a gerar o esquema da ferramenta e explicam ao modelo quando e como utilizá-la.

# 2.1 Exemplo: consulta de clima com validação
# O agente não deve inventar dados meteorológicos. A ferramenta consulta uma API externa, usa timeout, valida a resposta e devolve dados estruturados. O modelo fica responsável por converter a pergunta em uma chamada e explicar o resultado ao usuário.

import requests
from agents import Agent, Runner, function_tool
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

@function_tool
def consultar_clima(cidade: str) -> dict:
    """Obtém o clima atual de uma cidade usando a API Open-Meteo."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": cidade, "count": 1, "language": "pt", "format": "json"},
        timeout=15,
    )
    geo.raise_for_status()
    locais = geo.json().get("results", [])
    if not locais:
        return {"erro": f"Cidade não encontrada: {cidade}"}

    local = locais[0]
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": local["latitude"],
            "longitude": local["longitude"],
            "current": "temperature_2m,apparent_temperature,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=15,
    )
    clima.raise_for_status()
    atual = clima.json()["current"]

    return {
        "cidade": local["name"],
        "estado": local.get("admin1"),
        "temperatura_c": atual["temperature_2m"],
        "sensacao_c": atual["apparent_temperature"],
        "vento_kmh": atual["wind_speed_10m"],
        "horario_local": atual["time"],
    }


agente_clima = Agent(
    name="Agente de clima",
    instructions=(
        "Use consultar_clima para perguntas meteorológicas. "
        "Informe a cidade, o horário dos dados e as unidades. Não invente valores."
    ),
    tools=[consultar_clima],
    model="gpt-4o-mini",
)

async def resultado_clima():
    resultado = await Runner.run(agente_clima, "Como está o clima agora em Recife?")
    print(resultado.final_output)


asyncio.run(resultado_clima())