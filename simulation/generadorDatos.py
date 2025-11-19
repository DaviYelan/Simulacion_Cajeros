import random
from models.cliente import Cliente
from models.cajero import Cajero

class GeneradorDatos:
    def __init__(self):
        pass
    
    def generaClientes(self, numeroClientes: int, sesgo_express: bool = True):
        clientes = []
        for _ in range(numeroClientes):
            if sesgo_express:

                if random.random() < 0.50:
                    numeroArticulos = random.randint(1, 10)
                else:
                    numeroArticulos = random.randint(11, 50)
            else:
                numeroArticulos = random.randint(1, 50)
            
            cliente = Cliente(numeroArticulos)
            clientes.append(cliente)
        return clientes


        
    def generarCajeros(self, numeroCajeros : int, service_multiplier: float = 1.0):
        cajeros = [] #lista vacia para almacenar cajeros
        for _ in range(numeroCajeros):
            experienciaAleatoria = random.choice([True, False]) #generamos experiencia aleatoria
            cajero = Cajero(experienciaAleatoria, service_multiplier) #creamos instancia de cajero con experiencia aleatoria
            cajeros.append(cajero) #agregamos cajero a la lista
        return cajeros
    
    

    

#sesgo
# if sesgo_express:
#             if random.random() < 0.7:
#                 numeroArticulos = random.randint(1, 10)
#             else:
#                 numeroArticulos = random.randint(11, 50)
#         else:
#             numeroArticulos = random.randint(1, 50)




