from agents import function_tool
import databaseBanco


@function_tool
def consultar_saldo() -> str:
    """
    Consulta o saldo atual da conta do cliente.
    """

    return (
        f"Saldo disponível: "
        f"R$ {databaseBanco.conta['saldo']:.2f}"
    )


@function_tool
def buscar_destinatario(nome: str) -> str:
    """
    Busca um destinatário na lista de contatos pelo nome.
    """

    for contato in databaseBanco.contatos:
        if contato["nome"].lower() == nome.lower():
            return (
                f"Destinatário encontrado: {contato['nome']} | "
                f"Chave PIX: {contato['chave_pix']}"
            )

    return f"Destinatário '{nome}' não encontrado."


@function_tool
def preparar_pix(nome: str, valor: float) -> str:
    """
    Prepara um PIX para confirmação do cliente.
    Não realiza a transferência.
    """

    if valor <= 0:
        return "Erro: o valor do PIX deve ser maior que zero."

    destinatario = None

    for contato in databaseBanco.contatos:
        if contato["nome"].lower() == nome.lower():
            destinatario = contato
            break

    if destinatario is None:
        return f"Erro: destinatário '{nome}' não encontrado."

    if valor > databaseBanco.conta["saldo"]:
        return "Erro: saldo insuficiente para realizar o PIX."

    databaseBanco.pix_pendente = {
        "nome": destinatario["nome"],
        "chave_pix": destinatario["chave_pix"],
        "valor": valor,
    }

    return (
        "PIX preparado para confirmação.\n"
        f"Destinatário: {destinatario['nome']}\n"
        f"Chave PIX: {destinatario['chave_pix']}\n"
        f"Valor: R$ {valor:.2f}\n"
        "Aguardando confirmação do cliente."
    )


@function_tool
def realizar_pix() -> str:
    """
    Realiza o PIX pendente após confirmação do cliente.
    """

    if databaseBanco.pix_pendente is None:
        return "Não existe nenhum PIX pendente."

    pix = databaseBanco.pix_pendente

    if pix["valor"] > databaseBanco.conta["saldo"]:
        databaseBanco.pix_pendente = None
        return "Erro: saldo insuficiente para realizar o PIX."

    databaseBanco.conta["saldo"] -= pix["valor"]

    transacao = {
        "tipo": "PIX",
        "destinatario": pix["nome"],
        "chave_pix": pix["chave_pix"],
        "valor": pix["valor"],
    }

    databaseBanco.historico.append(transacao)

    databaseBanco.pix_pendente = None

    return (
        "PIX realizado com sucesso!\n"
        f"Destinatário: {pix['nome']}\n"
        f"Chave PIX: {pix['chave_pix']}\n"
        f"Valor: R$ {pix['valor']:.2f}\n"
        f"Novo saldo: R$ {databaseBanco.conta['saldo']:.2f}"
    )


@function_tool
def cancelar_pix() -> str:
    """
    Cancela um PIX que esteja aguardando confirmação.
    """

    if databaseBanco.pix_pendente is None:
        return "Não existe nenhum PIX pendente para cancelar."

    databaseBanco.pix_pendente = None

    return "PIX cancelado com sucesso."


@function_tool
def consultar_historico() -> str:
    """
    Consulta o histórico de transações realizadas.
    """

    if not databaseBanco.historico:
        return "Nenhuma transação foi realizada."

    resultado = "Histórico de transações:\n"

    for i, transacao in enumerate(
        databaseBanco.historico,
        start=1
    ):
        resultado += (
            f"{i}. {transacao['tipo']} - "
            f"{transacao['destinatario']} - "
            f"R$ {transacao['valor']:.2f}\n"
        )

    return resultado