import random

class Cliente:
    def __init__(self, numeroArticulos: int):
        self.numeroArticulos = numeroArticulos # 1-50 artículos
        self.tiempoTotal = 0.0  # Tiempo total en ser atendido, inicializado en 0.0 segundos

    def __str__(self):
        return (f"Cliente con {self.numeroArticulos} artículos."
                f"{f', Tiempo total en ser atendido: {self.tiempoTotal:.2f}s' if self.tiempoTotal > 0 else ''}")
                