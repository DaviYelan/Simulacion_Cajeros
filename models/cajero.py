import random

class Cajero:
    def __init__(self, tieneExperiencia: bool, service_multiplier: float = 1.0):
        self.experiencia = tieneExperiencia
        self.service_multiplier = service_multiplier

        if self.experiencia:
            self.tiempoEscaneoPorArticulo = 3 * service_multiplier  # segundos por artículo para cajero con experiencia
        else:
            self.tiempoEscaneoPorArticulo = 6 * service_multiplier  # segundos por artículo para cajero sin experiencia
        self.tiempoCobro = random.randint(15, 30) * service_multiplier  # tiempo de cobro aleatorio entre 15 y 30 segundos
    
    def __str__(self):
        experiencia_str = "con experiencia" if self.experiencia else "sin experiencia"
        return f"Cajero {experiencia_str}: Tiempo de escaneo por artículo = {self.tiempoEscaneoPorArticulo}s, Tiempo de cobro = {self.tiempoCobro}s"