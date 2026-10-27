
import pytest
from unittest.mock import MagicMock

from src.gerenciador_recursos import GerenciadorRecursosMarte


@pytest.fixture(scope="module")
def parametros_habitat():
    return {
        "oxigenio": 1000.0,
        "agua": 500.0,
        "consumo_oxigenio": 0.84,
        "consumo_agua": 3.0
    }


@pytest.fixture
def gerenciador(parametros_habitat):
    telemetria = MagicMock()

    sistema = GerenciadorRecursosMarte(
        **parametros_habitat,
        telemetria=telemetria
    )

    yield sistema

    # Limpeza após cada teste.
    telemetria.reset_mock()
