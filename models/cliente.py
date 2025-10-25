import random

class Cliente:
    def __init__(self, numeroArticulos: int):
        self.numeroArticulos = numeroArticulos
        self.tiempoTotal = 0.0

    def __str__(self):
        return (f"Cliente con {self.numeroArticulos} artículos."
                f"{f', Tiempo total en ser atendido: {self.tiempoTotal:.2f}s' if self.tiempoTotal > 0 else ''}")
                