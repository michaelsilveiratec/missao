import pytest

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
    AguaInsuficienteError,
    NivelEmergenciaInvalidoError
)


def test_calcular_consumo_diario(gerenciador):
    resultado = gerenciador.calcular_consumo_diario(10)

    assert resultado["oxigenio"] == pytest.approx(8.4)
    assert resultado["agua"] == pytest.approx(30.0)


@pytest.mark.parametrize(
    "astronautas, oxigenio, agua",
    [
        (0, 0.0, 0.0),
        (1, 0.84, 3.0),
        (5, 4.2, 15.0),
        (10, 8.4, 30.0)
    ]
)
def test_consumo_parametrizado(
    gerenciador,
    astronautas,
    oxigenio,
    agua
):
    resultado = gerenciador.calcular_consumo_diario(astronautas)

    assert resultado["oxigenio"] == pytest.approx(oxigenio)
    assert resultado["agua"] == pytest.approx(agua)


def test_aplicar_consumo_reduz_estoque(gerenciador):
    resultado = gerenciador.aplicar_consumo(10, dias=1)

    assert gerenciador.oxigenio == pytest.approx(991.6)
    assert gerenciador.agua == pytest.approx(470.0)

    assert resultado["oxigenio_restante"] == pytest.approx(991.6)
    assert resultado["agua_restante"] == pytest.approx(470.0)


def test_validar_estoque_suficiente(gerenciador):
    assert gerenciador.validar_estoque(10, dias=1) is True


def test_oxigenio_insuficiente():
    sistema = GerenciadorRecursosMarte(
        oxigenio=1,
        agua=500
    )

    with pytest.raises(OxigenioInsuficienteError):
        sistema.aplicar_consumo(10)


def test_agua_insuficiente():
    sistema = GerenciadorRecursosMarte(
        oxigenio=1000,
        agua=1
    )

    with pytest.raises(AguaInsuficienteError):
        sistema.aplicar_consumo(1)


@pytest.mark.parametrize("nivel", ["baixo", "medio", "alto", "critico"])
def test_niveis_de_emergencia(gerenciador, nivel):
    resultado = gerenciador.calcular_taxa_emergencia(nivel)

    assert 0 <= resultado <= 1


def test_nivel_de_emergencia_invalido(gerenciador):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.calcular_taxa_emergencia("extremo")


def test_alerta_em_nivel_critico(gerenciador):
    gerenciador.calcular_taxa_emergencia("critico")

    gerenciador.telemetria.disparar_alerta.assert_called_once_with(
        "Nível de emergência elevado no habitat.",
        "critico"
    )


def test_sem_alerta_em_nivel_baixo(gerenciador):
    gerenciador.calcular_taxa_emergencia("baixo")

    gerenciador.telemetria.disparar_alerta.assert_not_called()


def test_racionamento_critico(gerenciador):
    resultado = gerenciador.aplicar_racionamento("critico")

    assert resultado["taxa"] == pytest.approx(0.75)
    assert resultado["consumo_oxigenio"] == pytest.approx(0.21)
    assert resultado["consumo_agua"] == pytest.approx(0.75)


@pytest.mark.parametrize(
    "oxigenio, agua",
    [
        (-1, 100),
        (100, -1),
        (-1, -1)
    ]
)
def test_nao_permite_estoque_negativo(oxigenio, agua):
    with pytest.raises(ValueError):
        GerenciadorRecursosMarte(
            oxigenio=oxigenio,
            agua=agua
        )


def test_nao_permite_consumo_com_astronautas_negativos(gerenciador):
    with pytest.raises(ValueError):
        gerenciador.calcular_consumo_diario(-1)


def test_consumo_nao_altera_estoque_se_faltar_recurso():
    sistema = GerenciadorRecursosMarte(
        oxigenio=100,
        agua=1
    )

    with pytest.raises(AguaInsuficienteError):
        sistema.aplicar_consumo(1)

    assert sistema.oxigenio == 100
    assert sistema.agua == 1