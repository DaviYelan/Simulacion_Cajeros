# Simulación de supermercado con 5 cajas (4 normales y 1 express)

from simulation.generadorDatos import GeneradorDatos
from models.caja import Caja
import random

def main():
    # Inicializar generador de datos
    generador = GeneradorDatos()

    # Generar 5 cajeros
    cajeros = generador.generarCajeros(5)

    # Crear 5 cajas: 4 normales y 1 express
    cajas = []
    for i in range(5):
        es_express = (i == 4)  # La quinta caja es express
        caja = Caja(idCaja=i+1, cajero=cajeros[i], esExpress=es_express)
        cajas.append(caja)

    # Generar clientes (por ejemplo, 25 clientes)
    clientes = generador.generaClientes(25)

    # Asignar clientes a cajas respetando las reglas de express
    for cliente in clientes:
        asignado = False
        while not asignado:
            # Intentar asignar a una caja aleatoria
            caja_aleatoria = random.choice(cajas)
            if caja_aleatoria.agregarCliente(cliente):
                asignado = True

    # Calcular tiempos de atención para cada caja
    for caja in cajas:
        caja.calcularTiempoAtencion()

    # Imprimir resultados de la simulación
    print("=== RESULTADOS DE LA SIMULACIÓN ===")
    print(f"Total de clientes generados: {len(clientes)}")
    print(f"Total de cajas: {len(cajas)} (4 normales, 1 express)")
    print()

    for caja in cajas:
        print(caja)
        print("Clientes en fila:")
        for cliente in caja.filaClientes:
            print(f"  {cliente}")
        print()

if __name__ == "__main__":
    main()