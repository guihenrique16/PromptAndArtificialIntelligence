import asyncio
import os

from dotenv import load_dotenv
from agents import Runner, SQLiteSession

from agentsBanco import agente_atendimento


load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY não encontrada. "
        "Configure a chave no arquivo .env."
    )


async def main():
    print("=" * 50)
    print("BANCO MULTIAGENTE")
    print("=" * 50)
    print("Digite 'sair' para encerrar.\n")

    # Mantém o contexto da conversa
    session = SQLiteSession(
        "cliente_banco",
        "banco_conversas.db"
    )

    while True:
        mensagem = input("Você: ").strip()

        if mensagem.lower() == "sair":
            print("\nAtendimento encerrado.")
            break

        if not mensagem:
            continue

        try:
            resultado = await Runner.run(
                agente_atendimento,
                mensagem,
                session=session
            )

            print(f"\nBanco: {resultado.final_output}\n")

        except Exception as erro:
            print(f"\nErro durante o atendimento: {erro}\n")


if __name__ == "__main__":
    asyncio.run(main())