
class ServicoTelemetriaEspacial:
    def enviar_relatorio(self, relatorio):
        """Envia o relatório para a estação terrestre."""
        print(f"Relatório enviado à Terra: {relatorio}")
        return True

    def disparar_alerta(self, mensagem, nivel):
        """Envia um alerta de emergência."""
        print(f"ALERTA {nivel}: {mensagem}")
        return True
