import random

class Cajero:
    def __init__(self, tieneExperiencia: bool):
        self.experiencia = tieneExperiencia
        
        if self.experiencia:
            self.tiempoEscaneoPorArticulo = 3  # segundos por artículo para cajero con experiencia
        else:
            self.tiempoEscaneoPorArticulo = 6  # segundos por artículo para cajero sin experiencia
        self.tiempoCobro = random.randint(15, 30)  # tiempo de cobro aleatorio entre 15 y 30 segundos
    
    def __str__(self):
        experiencia_str = "con experiencia" if self.experiencia else "sin experiencia"
        return f"Cajero {experiencia_str}: Tiempo de escaneo por artículo = {self.tiempoEscaneoPorArticulo}s, Tiempo de cobro = {self.tiempoCobro}s"