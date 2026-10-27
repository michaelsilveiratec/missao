
import pytest

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    navegador = webdriver.Chrome(options=options)
    navegador.implicitly_wait(0)

    try:
        yield navegador
    finally:
        navegador.quit()


@pytest.fixture
def painel(driver):
    caminho = (
        Path(__file__).resolve().parents[1]
        / "web"
        / "painel.html"
    )

    driver.get(caminho.as_uri())
    return driver


def salvar_evidencia(painel, nome):
    pasta = Path("evidencias")
    pasta.mkdir(exist_ok=True)
    painel.save_screenshot(str(pasta / nome))


def test_solicitacao_oxigenio_aprovada(painel):
    try:
        campo = painel.find_element(By.ID, "quantidade")
        campo.send_keys("100")

        painel.find_element(
            By.CSS_SELECTOR,
            "#formulario button[type='submit']"
        ).click()

        WebDriverWait(painel, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "mensagem"),
                "Solicitação aprovada"
            )
        )

        assert painel.find_element(By.ID, "oxigenio").text == "900"

        assert "Solicitação aprovada" in painel.find_element(
            By.ID, "mensagem"
        ).text

    except Exception:
        salvar_evidencia(
            painel,
            "falha_solicitacao_aprovada.png"
        )
        raise


def test_solicitacao_acima_do_estoque(painel):
    try:
        campo = painel.find_element(By.ID, "quantidade")
        campo.send_keys("2000")

        painel.find_element(
            By.CSS_SELECTOR,
            "#formulario button[type='submit']"
        ).click()

        WebDriverWait(painel, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "mensagem"),
                "oxigênio insuficiente"
            )
        )

        assert painel.find_element(By.ID, "oxigenio").text == "1000"

    except Exception:
        salvar_evidencia(
            painel,
            "falha_estoque_insuficiente.png"
        )
        raise
