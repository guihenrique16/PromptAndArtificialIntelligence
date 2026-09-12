import asyncio
import os
import unicodedata
from pathlib import Path

from agents import Runner, SQLiteSession
from dotenv import load_dotenv

from agentsBanco import agente_atendimento


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY não encontrada. "
        "Configure a chave no arquivo .env."
    )


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_SESSOES = PASTA_PROJETO / "banco_conversas.db"


def normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()

    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )


def mensagem_de_encerramento(mensagem: str) -> bool:
    frases_encerramento = [
        "sair",
        "encerrar",
        "encerrar atendimento",
        "so isso por hoje",
        "isso e tudo por hoje",
        "era so isso",
        "nao preciso de mais nada",
        "nao preciso de mais nada hoje",
        "obrigado era so isso",
        "obrigada era so isso",
    ]

    return normalizar_texto(mensagem) in frases_encerramento


def obter_sessao(user_id: str) -> SQLiteSession:
    return SQLiteSession(
        session_id=f"banco_{user_id}",
        db_path=str(ARQUIVO_SESSOES),
    )


async def conversar(user_id: str, mensagem: str) -> str:
    """
    Processa uma mensagem vinda do terminal ou do Telegram.
    Cada usuário possui uma sessão de conversa própria.
    """

    if mensagem_de_encerramento(mensagem):
        return (
            "Tudo certo! Obrigado por utilizar o Banco Multiagente. "
            "Até mais!"
        )

    try:
        resultado = await Runner.run(
            agente_atendimento,
            mensagem,
            session=obter_sessao(user_id),
        )

        return str(resultado.final_output)

    except Exception as erro:
        print(f"Erro durante o atendimento: {erro}")

        return (
            "Ocorreu um erro durante o atendimento. "
            "Tente novamente."
        )


async def iniciar_terminal():
    print("=" * 50)
    print("BANCO MULTIAGENTE")
    print("=" * 50)
    print("Digite 'sair' para encerrar.\n")

    while True:
        mensagem = input("Você: ").strip()

        if not mensagem:
            continue

        resposta = await conversar("terminal_cliente", mensagem)

        print(f"\nBanco: {resposta}\n")

        if mensagem_de_encerramento(mensagem):
            break


if __name__ == "__main__":
    asyncio.run(iniciar_terminal())