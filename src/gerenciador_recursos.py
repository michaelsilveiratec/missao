
from src.servico_telemetria import ServicoTelemetriaEspacial


class OxigenioInsuficienteError(Exception):
    pass


class AguaInsuficienteError(Exception):
    pass


class NivelEmergenciaInvalidoError(Exception):
    pass


class GerenciadorRecursosMarte:
    def __init__(
        self,
        oxigenio=1000.0,
        agua=500.0,
        consumo_oxigenio=0.84,
        consumo_agua=3.0,
        telemetria=None
    ):
        self.oxigenio = float(oxigenio)
        self.agua = float(agua)
        self.consumo_oxigenio = float(consumo_oxigenio)
        self.consumo_agua = float(consumo_agua)
        self.telemetria = (
            telemetria or ServicoTelemetriaEspacial()
        )

        if min(
            self.oxigenio,
            self.agua,
            self.consumo_oxigenio,
            self.consumo_agua
        ) < 0:
            raise ValueError("Os valores não podem ser negativos.")

    def calcular_consumo_diario(self, astronautas):
        if astronautas < 0:
            raise ValueError("Número de astronautas inválido.")

        return {
            "oxigenio": astronautas * self.consumo_oxigenio,
            "agua": astronautas * self.consumo_agua
        }

    def validar_estoque(self, astronautas, dias=1):
        if astronautas < 0 or dias < 0:
            raise ValueError("Astronautas e dias devem ser válidos.")

        consumo = self.calcular_consumo_diario(astronautas)

        oxigenio_necessario = consumo["oxigenio"] * dias
        agua_necessaria = consumo["agua"] * dias

        if self.oxigenio < oxigenio_necessario:
            raise OxigenioInsuficienteError(
                "Estoque de oxigênio insuficiente."
            )

        if self.agua < agua_necessaria:
            raise AguaInsuficienteError(
                "Estoque de água insuficiente."
            )

        return True

    def aplicar_consumo(self, astronautas, dias=1):
        self.validar_estoque(astronautas, dias)

        consumo = self.calcular_consumo_diario(astronautas)

        gasto_oxigenio = consumo["oxigenio"] * dias
        gasto_agua = consumo["agua"] * dias

        self.oxigenio -= gasto_oxigenio
        self.agua -= gasto_agua

        self.telemetria.enviar_relatorio({
            "oxigenio_restante": self.oxigenio,
            "agua_restante": self.agua
        })

        return {
            "oxigenio_restante": self.oxigenio,
            "agua_restante": self.agua
        }

    def calcular_taxa_emergencia(self, nivel):
        taxas = {
            "baixo": 0.10,
            "medio": 0.25,
            "alto": 0.50,
            "critico": 0.75
        }

        if nivel not in taxas:
            raise NivelEmergenciaInvalidoError(
                f"Nível de emergência inválido: {nivel}"
            )

        taxa = taxas[nivel]

        if nivel in ("alto", "critico"):
            self.telemetria.disparar_alerta(
                "Nível de emergência elevado no habitat.",
                nivel
            )

        return taxa

    def aplicar_racionamento(self, nivel):
        taxa = self.calcular_taxa_emergencia(nivel)

        return {
            "taxa": taxa,
            "consumo_oxigenio": self.consumo_oxigenio * (1 - taxa),
            "consumo_agua": self.consumo_agua * (1 - taxa)
        }
