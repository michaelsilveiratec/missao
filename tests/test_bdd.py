
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError
)

scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto():
    return {}


@given(
    parsers.parse(
        "que o habitat possui {estoque:d} unidades de oxigênio"
    )
)
def habitat_com_estoque(contexto, estoque):
    contexto["sistema"] = GerenciadorRecursosMarte(
        oxigenio=estoque,
        agua=500
    )
    contexto["aprovada"] = None
    contexto["quantidade"] = None


@given("que o habitat está em nível de emergência critico")
def habitat_em_crise(contexto):
    contexto["sistema"].calcular_taxa_emergencia("critico")


@when(
    parsers.parse(
        "o astronauta solicita {quantidade:d} unidades de oxigênio"
    )
)
def solicitar_oxigenio(contexto, quantidade):
    sistema = contexto["sistema"]
    contexto["quantidade"] = quantidade

    try:
        if quantidade > sistema.oxigenio:
            raise OxigenioInsuficienteError(
                "Estoque insuficiente"
            )

        sistema.oxigenio -= quantidade
        contexto["aprovada"] = True

    except OxigenioInsuficienteError:
        contexto["aprovada"] = False


@then("a solicitação deve ser aprovada")
def solicitacao_aprovada(contexto):
    assert contexto["aprovada"] is True


@then("a solicitação deve ser negada")
def solicitacao_negada(contexto):
    assert contexto["aprovada"] is False


@then(
    parsers.parse(
        "o estoque deve ficar com {estoque:d} unidades"
    )
)
def conferir_estoque(contexto, estoque):
    assert contexto["sistema"].oxigenio == estoque


@then(
    parsers.parse(
        "o estoque deve continuar com {estoque:d} unidades"
    )
)
def conferir_estoque_preservado(contexto, estoque):
    assert contexto["sistema"].oxigenio == estoque
