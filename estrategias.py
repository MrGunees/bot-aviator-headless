class Estrategia15x:
    def analisar(self, historico):
        if len(historico) >= 3 and all(v < 1.5 for v in historico[-3:]):
            return "📢 Entrada Estratégia 15x detectada!"
        return None

class Estrategia10x:
    def analisar(self, historico):
        if historico and historico[-1] >= 10:
            return "🚀 Vela >=10x detectada!"
        return None