class ServicoTelemetriaEspacial:

    def enviar_relatorio(self, relatorio):
        """Simula o envio de relatório para a Terra."""
        print(f"Relatório enviado à Terra: {relatorio}")
        return True

    def disparar_alerta(self, mensagem, nivel):
        """Simula o envio de um alerta de emergência."""
        print(f"ALERTA {nivel}: {mensagem}")
        return True