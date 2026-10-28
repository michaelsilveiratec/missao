import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    navegador = webdriver.Chrome(options=options)
    navegador.implicitly_wait(10)

    yield navegador

    navegador.quit()


def test_pagina_local(driver, tmp_path):
    pagina = tmp_path / "habitat.html"

    pagina.write_text(
        """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head><title>Habitat de Marte</title></head>
        <body>
            <h1 id="status">Sistema ECLSS ativo</h1>
        </body>
        </html>
        """,
        encoding="utf-8"
    )

    driver.get(pagina.as_uri())

    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "status")
            )
        )

        assert elemento.text == "Sistema ECLSS ativo"

    except AssertionError:
        driver.save_screenshot("falha_selenium.png")
        raise