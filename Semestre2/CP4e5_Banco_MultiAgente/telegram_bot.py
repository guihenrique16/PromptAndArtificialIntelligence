import truststore

truststore.inject_into_ssl()

import os

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from banco import conversar


load_dotenv()


async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.effective_user.first_name if update.effective_user else "cliente"

    await update.effective_message.reply_text(
        f"Olá, {nome}!\n\n"
        "Sou o Banco Multiagente.\n\n"
        "Posso ajudar você a:\n"
        "• Consultar saldo\n"
        "• Listar, buscar e adicionar contatos PIX\n"
        "• Preparar e realizar PIX\n"
        "• Consultar o histórico de transações\n\n"
        "Use /ajuda para ver exemplos."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Exemplos de mensagens:\n\n"
        "• Qual é meu saldo?\n"
        "• Liste meus contatos.\n"
        "• Busque o contato Ana.\n"
        "• Adicione João com a chave joao@email.com.\n"
        "• Faça um PIX de 50 reais para Ana.\n"
        "• Sim.\n"
        "• Mostre meu histórico de PIX.\n"
        "• Só isso por hoje."
    )


async def receber_mensagem(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    mensagem = update.effective_message
    usuario = update.effective_user

    if mensagem is None or usuario is None or not mensagem.text:
        return

    await mensagem.chat.send_action(ChatAction.TYPING)

    resposta = await conversar(
        user_id=f"telegram_{usuario.id}",
        mensagem=mensagem.text,
    )

    # Limite de mensagens do Telegram: 4096 caracteres.
    for inicio in range(0, len(resposta), 4000):
        await mensagem.reply_text(resposta[inicio:inicio + 4000])


async def erro_telegram(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    print(f"Erro no Telegram: {context.error}")


def criar_app() -> Application:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN não encontrado no arquivo .env."
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", iniciar))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receber_mensagem,
        )
    )
    app.add_error_handler(erro_telegram)

    return app


if __name__ == "__main__":
    print("Bot do Banco Multiagente iniciado.")
    print("Abra o Telegram, envie /start ao bot e faça um teste.")

    app = criar_app()
    app.run_polling(drop_pending_updates=True)