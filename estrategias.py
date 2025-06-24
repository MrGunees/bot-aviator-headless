import time

class Estrategia15x:
    def __init__(self):
        self.losses = 0
        self.pausado_ate = None

    def analisar(self, historico):
        if self.pausado_ate and time.time() < self.pausado_ate:
            return None

        ultimos = historico[-3:]
        if len(ultimos) < 3:
            return None

        if all(v < 1.5 for v in ultimos):
            self.losses += 1
            if self.losses >= 2:
                self.pausado_ate = time.time() + 2 * 3600
                return "⚠️ Estratégia pausada após 2 ciclos de loss. Retomando em 2 horas."
            return "🎯 Entrada após 3 velas <1.5x"
        elif ultimos[-1] >= 1.5:
            self.losses = 0
        return None

class Estrategia10x:
    def __init__(self):
        self.contagem = 0

    def analisar(self, historico):
        if len(historico) < 1:
            return None

        if historico[-1] >= 10:
            self.contagem += 1
            return f"🔥 Vela >=10x detectada! Contagem atual: {self.contagem}"
        return None
