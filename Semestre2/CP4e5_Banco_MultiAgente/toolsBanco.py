import csv
from datetime import datetime
from pathlib import Path

from agents import function_tool


ID_CLIENTE = "1"

PASTA_DATA = Path(__file__).parent / "data"
ARQUIVO_SALDO = PASTA_DATA / "saldo.csv"
ARQUIVO_CONTATOS = PASTA_DATA / "contatos_pix.csv"
ARQUIVO_TRANSACOES = PASTA_DATA / "transacoes_pix.csv"

pix_pendente = None


def ler_csv(caminho: Path) -> list[dict]:
    with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def escrever_csv(caminho: Path, campos: list[str], dados: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)


def obter_saldo() -> float:
    dados = ler_csv(ARQUIVO_SALDO)

    for cliente in dados:
        if cliente["id_cliente"] == ID_CLIENTE:
            return float(cliente["saldo"])

    raise ValueError("Cliente não encontrado no arquivo saldo.csv.")


def atualizar_saldo(novo_saldo: float) -> None:
    dados = ler_csv(ARQUIVO_SALDO)

    for cliente in dados:
        if cliente["id_cliente"] == ID_CLIENTE:
            cliente["saldo"] = f"{novo_saldo:.2f}"
            break

    escrever_csv(
        ARQUIVO_SALDO,
        ["id_cliente", "nome", "saldo"],
        dados
    )


def encontrar_contato_exato(nome: str) -> dict | None:
    contatos = ler_csv(ARQUIVO_CONTATOS)

    for contato in contatos:
        if (
            contato["id_cliente"] == ID_CLIENTE
            and contato["nome_contato"].lower() == nome.lower()
        ):
            return contato

    return None


@function_tool
def consultar_saldo() -> str:
    """
    Consulta o saldo disponível da conta do cliente.
    """

    saldo = obter_saldo()
    return f"Saldo disponível: R$ {saldo:.2f}"


@function_tool
def listar_contatos() -> str:
    """
    Lista todos os contatos PIX cadastrados pelo cliente.
    """

    contatos = ler_csv(ARQUIVO_CONTATOS)

    contatos_cliente = [
        contato
        for contato in contatos
        if contato["id_cliente"] == ID_CLIENTE
    ]

    if not contatos_cliente:
        return "Você não possui contatos PIX cadastrados."

    resultado = "Contatos PIX cadastrados:\n"

    for indice, contato in enumerate(contatos_cliente, start=1):
        resultado += (
            f"{indice}. {contato['nome_contato']} - "
            f"Chave PIX: {contato['chave_pix']}\n"
        )

    return resultado


@function_tool
def buscar_contato(nome: str) -> str:
    """
    Busca contatos PIX pelo nome ou por parte do nome informado.
    """

    contatos = ler_csv(ARQUIVO_CONTATOS)

    encontrados = [
        contato
        for contato in contatos
        if (
            contato["id_cliente"] == ID_CLIENTE
            and nome.lower() in contato["nome_contato"].lower()
        )
    ]

    if not encontrados:
        return f"Nenhum contato encontrado para: {nome}."

    resultado = "Contato(s) encontrado(s):\n"

    for contato in encontrados:
        resultado += (
            f"- {contato['nome_contato']} | "
            f"Chave PIX: {contato['chave_pix']}\n"
        )

    return resultado


@function_tool
def adicionar_contato(nome: str, chave_pix: str) -> str:
    """
    Adiciona um novo contato PIX com nome e chave PIX.
    """

    nome = nome.strip()
    chave_pix = chave_pix.strip()

    if not nome or not chave_pix:
        return "Erro: informe o nome e a chave PIX do novo contato."

    contatos = ler_csv(ARQUIVO_CONTATOS)

    for contato in contatos:
        if (
            contato["id_cliente"] == ID_CLIENTE
            and contato["nome_contato"].lower() == nome.lower()
        ):
            return (
                f"Erro: o contato '{contato['nome_contato']}' "
                "já está cadastrado."
            )

        if (
            contato["id_cliente"] == ID_CLIENTE
            and contato["chave_pix"].lower() == chave_pix.lower()
        ):
            return "Erro: essa chave PIX já está cadastrada."

    contatos.append(
        {
            "id_cliente": ID_CLIENTE,
            "nome_contato": nome,
            "chave_pix": chave_pix,
        }
    )

    escrever_csv(
        ARQUIVO_CONTATOS,
        ["id_cliente", "nome_contato", "chave_pix"],
        contatos
    )

    return (
        "Contato adicionado com sucesso!\n"
        f"Nome: {nome}\n"
        f"Chave PIX: {chave_pix}"
    )


@function_tool
def preparar_pix(nome: str, valor: float) -> str:
    """
    Prepara um PIX para confirmação, mas não realiza a transferência.
    """

    global pix_pendente

    if valor <= 0:
        return "Erro: o valor do PIX deve ser maior que zero."

    destinatario = encontrar_contato_exato(nome)

    if destinatario is None:
        return (
            f"Erro: o contato '{nome}' não foi encontrado. "
            "Use buscar_contato ou listar_contatos."
        )

    saldo = obter_saldo()

    if valor > saldo:
        return "Erro: saldo insuficiente para realizar o PIX."

    pix_pendente = {
        "destinatario": destinatario["nome_contato"],
        "chave_pix": destinatario["chave_pix"],
        "valor": valor,
    }

    return (
        "PIX preparado para confirmação.\n"
        f"Destinatário: {destinatario['nome_contato']}\n"
        f"Chave PIX: {destinatario['chave_pix']}\n"
        f"Valor: R$ {valor:.2f}\n"
        "Aguardando confirmação do cliente."
    )


@function_tool
def realizar_pix() -> str:
    """
    Realiza o PIX pendente somente após a confirmação explícita do cliente.
    Atualiza saldo.csv e registra a transação em transacoes_pix.csv.
    """

    global pix_pendente

    if pix_pendente is None:
        return "Não existe nenhum PIX pendente para realizar."

    saldo = obter_saldo()
    valor = pix_pendente["valor"]

    if valor > saldo:
        pix_pendente = None
        return "Erro: saldo insuficiente para realizar o PIX."

    novo_saldo = saldo - valor
    atualizar_saldo(novo_saldo)

    transacoes = ler_csv(ARQUIVO_TRANSACOES)

    proximo_id = 1
    if transacoes:
        proximo_id = max(
            int(transacao["id_transacao"])
            for transacao in transacoes
        ) + 1

    transacoes.append(
        {
            "id_transacao": str(proximo_id),
            "id_cliente": ID_CLIENTE,
            "destinatario": pix_pendente["destinatario"],
            "chave_pix": pix_pendente["chave_pix"],
            "valor": f"{valor:.2f}",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )

    escrever_csv(
        ARQUIVO_TRANSACOES,
        [
            "id_transacao",
            "id_cliente",
            "destinatario",
            "chave_pix",
            "valor",
            "data",
        ],
        transacoes
    )

    resultado = (
        "PIX realizado com sucesso!\n"
        f"Destinatário: {pix_pendente['destinatario']}\n"
        f"Chave PIX: {pix_pendente['chave_pix']}\n"
        f"Valor: R$ {valor:.2f}\n"
        f"Novo saldo: R$ {novo_saldo:.2f}"
    )

    pix_pendente = None

    return resultado


@function_tool
def cancelar_pix() -> str:
    """
    Cancela um PIX que está aguardando confirmação.
    """

    global pix_pendente

    if pix_pendente is None:
        return "Não existe nenhum PIX pendente para cancelar."

    pix_pendente = None

    return "PIX cancelado com sucesso."


@function_tool
def consultar_historico() -> str:
    """
    Lista as transações PIX realizadas pelo cliente.
    """

    transacoes = ler_csv(ARQUIVO_TRANSACOES)

    transacoes_cliente = [
        transacao
        for transacao in transacoes
        if transacao["id_cliente"] == ID_CLIENTE
    ]

    if not transacoes_cliente:
        return "Nenhuma transação PIX foi realizada."

    resultado = "Histórico de PIX:\n"

    for transacao in transacoes_cliente:
        resultado += (
            f"{transacao['id_transacao']}. "
            f"{transacao['destinatario']} - "
            f"R$ {float(transacao['valor']):.2f} - "
            f"{transacao['data']}\n"
        )

    return resultado