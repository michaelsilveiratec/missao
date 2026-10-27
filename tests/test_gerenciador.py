
import pytest

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
    AguaInsuficienteError,
    NivelEmergenciaInvalidoError
)


@pytest.mark.parametrize(
    "astronautas, oxigenio_esperado, agua_esperada",
    [
        (1, 0.84, 3.0),
        (2, 1.68, 6.0),
        (4, 3.36, 12.0),
        (6, 5.04, 18.0)
    ]
)
def test_consumo_diario(
    gerenciador,
    astronautas,
    oxigenio_esperado,
    agua_esperada
):
    resultado = gerenciador.calcular_consumo_diario(astronautas)

    assert resultado["oxigenio"] == pytest.approx(
        oxigenio_esperado
    )
    assert resultado["agua"] == pytest.approx(agua_esperada)


@pytest.mark.parametrize(
    "astronautas, dias",
    [
        (1, 1),
        (4, 7),
        (6, 25)
    ]
)
def test_validar_estoque(gerenciador, astronautas, dias):
    assert gerenciador.validar_estoque(astronautas, dias)


def test_consumo_reduz_estoque(gerenciador):
    resultado = gerenciador.aplicar_consumo(2, 1)

    assert resultado["oxigenio_restante"] == pytest.approx(998.32)
    assert resultado["agua_restante"] == pytest.approx(494.0)

    gerenciador.telemetria.enviar_relatorio.assert_called_once_with({
        "oxigenio_restante": pytest.approx(998.32),
        "agua_restante": pytest.approx(494.0)
    })


def test_oxigenio_insuficiente():
    sistema = GerenciadorRecursosMarte(
        oxigenio=1,
        agua=100
    )

    with pytest.raises(OxigenioInsuficienteError):
        sistema.aplicar_consumo(2)


def test_agua_insuficiente():
    sistema = GerenciadorRecursosMarte(
        oxigenio=100,
        agua=1
    )

    with pytest.raises(AguaInsuficienteError):
        sistema.aplicar_consumo(1)


@pytest.mark.parametrize(
    "nivel, taxa_esperada",
    [
        ("baixo", 0.10),
        ("medio", 0.25),
        ("alto", 0.50),
        ("critico", 0.75)
    ]
)
def test_taxa_emergencia(gerenciador, nivel, taxa_esperada):
    taxa = gerenciador.calcular_taxa_emergencia(nivel)

    assert taxa == pytest.approx(taxa_esperada)


def test_nivel_emergencia_invalido(gerenciador):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.calcular_taxa_emergencia("extremo")


def test_alerta_emergencia_critica(gerenciador):
    gerenciador.calcular_taxa_emergencia("critico")

    gerenciador.telemetria.disparar_alerta.assert_called_once_with(
        "Nível de emergência elevado no habitat.",
        "critico"
    )


def test_emergencia_baixa_nao_dispara_alerta(gerenciador):
    gerenciador.calcular_taxa_emergencia("baixo")

    gerenciador.telemetria.disparar_alerta.assert_not_called()


def test_racionamento(gerenciador):
    resultado = gerenciador.aplicar_racionamento("alto")

    assert resultado["taxa"] == pytest.approx(0.50)
    assert resultado["consumo_oxigenio"] == pytest.approx(0.42)
    assert resultado["consumo_agua"] == pytest.approx(1.5)


def test_numero_negativo_de_astronautas(gerenciador):
    with pytest.raises(ValueError):
        gerenciador.calcular_consumo_diario(-1)
