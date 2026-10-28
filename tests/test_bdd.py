import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError
)


scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto_solicitacao():
    return {
        "sistema": None,
        "aprovada": False
    }


@given(
    parsers.parse(
        "que o habitat possui {quantidade:d} unidades de oxigênio"
    ),
    target_fixture="contexto_solicitacao"
)
def habitat_com_oxigenio(quantidade):
    sistema = GerenciadorRecursosMarte(
        oxigenio=quantidade,
        agua=500,
        consumo_oxigenio=1,
        consumo_agua=0
    )

    return {
        "sistema": sistema,
        "aprovada": False
    }


@given(
    "que o habitat está em nível de emergência critico"
)
def nivel_emergencia_critico(contexto_solicitacao):
    contexto_solicitacao["sistema"].calcular_taxa_emergencia("critico")


@when(
    parsers.parse(
        "o astronauta solicita {quantidade:d} unidades de oxigênio"
    )
)
def astronauta_solicita_oxigenio(
    contexto_solicitacao,
    quantidade
):
    sistema = contexto_solicitacao["sistema"]

    try:
        if sistema.oxigenio < quantidade:
            raise OxigenioInsuficienteError(
                "Estoque de oxigênio insuficiente."
            )

        sistema.oxigenio -= quantidade
        contexto_solicitacao["aprovada"] = True

    except OxigenioInsuficienteError:
        contexto_solicitacao["aprovada"] = False


@then("a solicitação deve ser aprovada")
def solicitacao_aprovada(contexto_solicitacao):
    assert contexto_solicitacao["aprovada"] is True


@then("a solicitação deve ser negada")
def solicitacao_negada(contexto_solicitacao):
    assert contexto_solicitacao["aprovada"] is False


@then(
    parsers.parse(
        "o estoque deve ficar com {quantidade:d} unidades"
    )
)
def estoque_final(contexto_solicitacao, quantidade):
    assert contexto_solicitacao["sistema"].oxigenio == quantidade


@then(
    parsers.parse(
        "o estoque deve continuar com {quantidade:d} unidades"
    )
)
def estoque_continuou(contexto_solicitacao, quantidade):
    assert contexto_solicitacao["sistema"].oxigenio == quantidade