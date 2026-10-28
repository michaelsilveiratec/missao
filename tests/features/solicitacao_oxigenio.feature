Feature: Solicitação de oxigênio no habitat de Marte

  Como astronauta
  Quero solicitar oxigênio adicional
  Para manter o habitat em condições seguras

  Scenario: Solicitação normal aprovada
    Given que o habitat possui 100 unidades de oxigênio
    When o astronauta solicita 20 unidades de oxigênio
    Then a solicitação deve ser aprovada
    And o estoque deve ficar com 80 unidades

  Scenario: Solicitação negada por falta de estoque
    Given que o habitat possui 100 unidades de oxigênio
    When o astronauta solicita 150 unidades de oxigênio
    Then a solicitação deve ser negada
    And o estoque deve continuar com 100 unidades

  Scenario: Solicitação em condição de crise
    Given que o habitat possui 100 unidades de oxigênio
    And que o habitat está em nível de emergência critico
    When o astronauta solicita 20 unidades de oxigênio
    Then a solicitação deve ser aprovada
    And o estoque deve ficar com 80 unidades