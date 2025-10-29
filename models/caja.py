from models.cliente import Cliente
from models.cajero import Cajero
from typing import List

class Caja:
    def __init__(self, idCaja: int, cajero: Cajero, esExpress : bool, filaInicial : List[Cliente] = None):
        self.idCaja = idCaja
        self.cajero = cajero
        self.esExpress = esExpress
        self.filaClientes = filaInicial if filaInicial is not None else [] # si no hay fila inicial, se crea una vacía
        self.tiempoAtencionTotal = 0.0  # tiempo total de atención en la caja
        self.LIMITE_EXPRESS = 10  # límite de artículos para cajas express

    def agregarCliente(self, cliente: Cliente):
        if self.esExpress and cliente.numeroArticulos > self.LIMITE_EXPRESS:
            print(f"El cliente no puede usar la caja express {self.idCaja}.")
            return False
        else:
            self.filaClientes.append(cliente)
            return True
        
    def calcularTiempoAtencion(self) -> float:
        self.tiempoAtencionTotal = 0.0

        #obtenemos la velocidad y tiempo del cajero asignado a la caja
        tiempoEscaneoPorArticulos = self.cajero.tiempoEscaneoPorArticulo
        tiempoCobros = self.cajero.tiempoCobro

        tiempoEsperaAcumulado = 0.0  # tiempo de espera acumulado para clientes posteriores

        #recorremos la fila
        for cliente in self.filaClientes:
            tiempoEscaneoPorCliente = cliente.numeroArticulos * tiempoEscaneoPorArticulos
            tiempoAtencionPorCliente = tiempoEscaneoPorCliente + tiempoCobros
            cliente.tiempoTotal = tiempoAtencionPorCliente + tiempoEsperaAcumulado  # tiempo total incluye espera
            tiempoEsperaAcumulado += tiempoAtencionPorCliente  # acumulamos el tiempo de atención para el siguiente cliente
            self.tiempoAtencionTotal += tiempoAtencionPorCliente # acumulamos el tiempo total de atención
        return self.tiempoAtencionTotal
    
    def __str__(self):
        tipo_caja = "Express" if self.esExpress else "Normal"
        return (f"Caja {self.idCaja} ({tipo_caja}) atendida por {self.cajero} "
                f"con {len(self.filaClientes)} clientes en fila. "
                f"Tiempo total de atención: {self.tiempoAtencionTotal:.2f}s")
