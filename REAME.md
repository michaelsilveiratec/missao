# Missão Marte — ECLSS

![Pipeline de testes](https://github.com/michaelsilveiratec/projeto-missao-marte/actions/workflows/pipeline.yml/badge.svg)

Projeto acadêmico de automação de testes do Sistema de Controle Ambiental e Suporte à Vida (ECLSS) de um habitat em Marte.

## Objetivo

Validar o controle de oxigênio e água, o consumo diário, o racionamento, os alertas de emergência e o painel Web por meio de testes automatizados.

## Tecnologias

- Python
- Pytest
- pytest-mock
- pytest-cov
- pytest-bdd
- Selenium WebDriver
- GitHub Actions

## Estrutura do projeto

- `src/`: regras de negócio e serviço de telemetria.
- `tests/`: testes unitários, BDD e E2E.
- `tests/features/`: cenários escritos em Gherkin.
- `web/`: painel Web do habitat.
- `.github/workflows/`: pipeline de integração contínua.

## Pré-requisitos

- Python 3.12 ou compatível.
- Google Chrome ou Chromium para os testes E2E.
- Conexão com a internet para instalar as dependências e, quando necessário, resolver o driver do navegador.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/michaelsilveiratec/projeto-missao-marte.git
cd projeto-missao-marte
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Executar todos os testes

```bash
pytest -v --cov=src --cov-report=term-missing
```

Na última execução local registrada, os 24 testes passaram e a cobertura total foi de 93%.

## Executar categorias separadamente

**Testes de regras de negócio:**

```bash
pytest tests/test_gerenciador.py -v
```

**Testes Web com Selenium:**

```bash
pytest tests/test_selenium_e2e.py -v
```

**Testes BDD:**

```bash
pytest tests/test_bdd.py -v
```

## Evidências de falha

Os testes E2E devem salvar capturas de tela quando ocorre uma falha durante as validações, conforme implementado no código de testes.

## Integração contínua

O GitHub Actions está configurado para executar os testes automaticamente a cada `push` ou `pull_request`, conforme os gatilhos definidos no workflow.

A badge acima indica o estado da última execução do pipeline, quando o repositório e o workflow estão acessíveis.

## Autor

Michael Lucas Ramos da Silveira

Projeto desenvolvido para atividade prática de Qualidade e Automação de Testes de Software.