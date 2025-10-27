# Simulación de supermercado con 5 cajas (4 normales y 1 express)
from display.interfaz import iniciar_interfaz
from simulation.generadorDatos import GeneradorDatos
from models.caja import Caja
import random

def encontrarCajaMasRapida(cajas):
    """
    Encuentra la caja que atendería más rápido a un nuevo cliente.
    Considera el tiempo total de atención acumulado en cada caja.
    """
    if not cajas:
        return None

    # Encontrar la caja con el menor tiempo de atención total
    caja_mas_rapida = min(cajas, key=lambda caja: caja.tiempoAtencionTotal)
    return caja_mas_rapida

def main(num_cajeros, num_clientes, posicion_express):
    """
    Simulación de supermercado con configuración completa.

    Args:
        num_cajeros: Número de cajeros a generar
        num_clientes: Número de clientes a generar
        posicion_express: Posición de la caja express ("primera", "medio", "ultima", "aleatoria")
    """
    # === CONFIGURACIÓN DE LA SIMULACIÓN ===
    # Todas las configuraciones se hacen aquí al inicio

    # Inicializar generador de datos
    generador = GeneradorDatos()

    # Generar cajeros
    cajeros = generador.generarCajeros(num_cajeros)

    # Determinar posición de la caja express
    posicion_express_idx = None
    if posicion_express == "primera":
        posicion_express_idx = 0
    elif posicion_express == "medio":
        posicion_express_idx = num_cajeros // 2
    elif posicion_express == "ultima":
        posicion_express_idx = num_cajeros - 1
    elif posicion_express == "aleatoria":
        posicion_express_idx = random.randint(0, num_cajeros - 1)

    # Crear cajas con posición express configurable
    cajas = []
    for i in range(num_cajeros):
        es_express = (i == posicion_express_idx)
        caja = Caja(idCaja=i+1, cajero=cajeros[i], esExpress=es_express)
        cajas.append(caja)

    # Generar clientes
    clientes = generador.generaClientes(num_clientes)

    # Asignar clientes a cajas con lógica inteligente
    for cliente in clientes:
        asignado = False

        # Si el cliente puede usar express (≤10 artículos), intentar primero la caja express
        if cliente.numeroArticulos <= 10:
            caja_express = next((caja for caja in cajas if caja.esExpress), None)
            if caja_express and caja_express.agregarCliente(cliente):
                asignado = True

        # Si no se asignó a express (o no puede usarla), asignar a caja normal aleatoria
        if not asignado:
            cajas_normales = [caja for caja in cajas if not caja.esExpress]
            while not asignado and cajas_normales:
                caja_aleatoria = random.choice(cajas_normales)
                if caja_aleatoria.agregarCliente(cliente):
                    asignado = True
                else:
                    # Si no se pudo asignar, remover de la lista para evitar loop infinito
                    cajas_normales.remove(caja_aleatoria)

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

    # Encontrar y mostrar la caja más rápida para un nuevo cliente
    caja_mas_rapida = encontrarCajaMasRapida(cajas)
    print("=== RECOMENDACIÓN PARA NUEVO CLIENTE ===")
    if caja_mas_rapida:
        tipo_caja = "Express" if caja_mas_rapida.esExpress else "Normal"
        print(f"La caja más rápida para un nuevo cliente es la Caja {caja_mas_rapida.idCaja} ({tipo_caja})")
        print(f"Tiempo total de atención actual: {caja_mas_rapida.tiempoAtencionTotal:.2f}s")
        print(f"Clientes en fila: {len(caja_mas_rapida.filaClientes)}")
    print()

    # Retornar los datos para que la interfaz pueda usarlos
    return cajas, clientes

if __name__ == "__main__":
    # === CONFIGURACIÓN FÁCIL DE LA SIMULACIÓN ===
    # Cambia estos valores para probar diferentes escenarios

    # Número de cajeros/cajas
    num_cajeros = 5

    # Número de clientes
    num_clientes = 25

    # Posición de la caja express: "primera", "medio", "ultima", "aleatoria"
    posicion_express = "primera"

    # Ejecutar simulación con la configuración
    cajas, clientes = main(num_cajeros, num_clientes, posicion_express)

    # Iniciar interfaz gráfica con los datos de la simulación
    from display.interfaz import iniciar_interfaz_con_datos
    iniciar_interfaz_con_datos(cajas, clientes)