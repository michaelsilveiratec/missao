from unittest.mock import MagicMock

from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial


def test_enviar_relatorio():
    telemetria = ServicoTelemetriaEspacial()

    resultado = telemetria.enviar_relatorio({
        "oxigenio_restante": 900,
        "agua_restante": 400
    })

    assert resultado is True


def test_disparar_alerta():
    telemetria = ServicoTelemetriaEspacial()

    resultado = telemetria.disparar_alerta(
        "Falha no habitat",
        "critico"
    )

    assert resultado is True


def test_mock_verifica_envio_de_relatorio():
    telemetria = MagicMock()

    sistema = GerenciadorRecursosMarte(
        oxigenio=100,
        agua=100,
        telemetria=telemetria
    )

    sistema.aplicar_consumo(1)

    telemetria.enviar_relatorio.assert_called_once_with({
        "oxigenio_restante": 99.16,
        "agua_restante": 97.0
    })


def test_mock_verifica_alerta():
    telemetria = MagicMock()

    sistema = GerenciadorRecursosMarte(
        telemetria=telemetria
    )

    sistema.calcular_taxa_emergencia("alto")

    telemetria.disparar_alerta.assert_called_once_with(
        "Nível de emergência elevado no habitat.",
        "alto"
    )