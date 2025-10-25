import random
from models.cliente import Cliente
from models.cajero import Cajero

class GeneradorDatos:
    def __init__(self):
        pass
    
    def generaClientes(self, numeroClientes : int):
        clientes = [] #lista vacia para almacenar clientes
        for _ in range(numeroClientes):
            numeroArticulos = random.randint(1, 50) #generamos numero aleatorio de articulos
            cliente = Cliente(numeroArticulos) #instancia de cliente
            clientes.append(cliente) #agregamos cliente  a la lista
        return clientes
    
    def generarCajeros(self, numeroCajeros : int):
        cajeros = [] #lista vacia para almacenar cajeros
        for _ in range(numeroCajeros):
            experienciaAleatoria = random.choice([True, False]) #generamos experiencia aleatoria
            cajero = Cajero(experienciaAleatoria) #creamos instancia de cajero con experiencia aleatoria
            cajeros.append(cajero) #agregamos cajero a la lista
        return cajeros