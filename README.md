# Simulación de Supermercado

Este proyecto simula el funcionamiento de un supermercado con múltiples cajas de atención al cliente, incluyendo cajas normales y una caja express. La simulación calcula tiempos de atención, espera en fila y asignación de clientes a cajas.

## Estructura del Proyecto

```
supermercado/
├── main.py                 # Archivo principal que ejecuta la simulación
└── display/                # Parte grafica de la simulacion
├── models/
│   ├── cliente.py          # Clase Cliente
│   ├── cajero.py           # Clase Cajero
│   └── caja.py             # Clase Caja
└── simulation/
    └── generadorDatos.py   # Generador de datos aleatorios
```

## Modelos

### Cliente
Representa a un cliente del supermercado.

**Atributos:**
- `numeroArticulos`: Número de artículos que lleva el cliente (1-50)
- `tiempoTotal`: Tiempo total que el cliente pasa en el sistema (incluyendo espera en fila)

**Métodos:**
- `__str__()`: Devuelve una representación en cadena del cliente

### Cajero
Representa a un empleado que atiende en una caja.

**Atributos:**
- `experiencia`: Booleano que indica si el cajero tiene experiencia
- `tiempoEscaneoPorArticulo`: Tiempo en segundos para escanear cada artículo (3s si experimentado, 6s si no)
- `tiempoCobro`: Tiempo de cobro aleatorio entre 15-30 segundos

**Métodos:**
- `tiempoEscaneoPorArticulos()`: Retorna el tiempo de escaneo por artículo
- `tiempoCobro()`: Retorna el tiempo de cobro
- `__str__()`: Representación en cadena del cajero

### Caja
Representa una caja de atención al cliente.

**Atributos:**
- `idCaja`: Identificador único de la caja
- `cajero`: Instancia del cajero asignado
- `esExpress`: Booleano que indica si es caja express
- `filaClientes`: Lista de clientes en fila
- `tiempoAtencionTotal`: Tiempo total de atención en la caja
- `LIMITE_EXPRESS`: Límite de artículos para cajas express (10)

**Métodos:**
- `agregarCliente(cliente)`: Agrega un cliente a la fila, verificando restricciones express
- `calcularTiempoAtencion()`: Calcula tiempos de atención y espera para todos los clientes
- `__str__()`: Representación en cadena de la caja

## Componentes de Simulación

### GeneradorDatos
Clase responsable de generar datos aleatorios para la simulación.

**Métodos:**
- `generaClientes(numClientes)`: Genera una lista de clientes con número aleatorio de artículos
- `generarCajeros(numCajeros)`: Genera una lista de cajeros con experiencia aleatoria

## Flujo de la Simulación

1. **Inicialización:**
   - Se crea un generador de datos
   - Se generan 5 cajeros con experiencia aleatoria
   - Se crean 5 cajas: 4 normales y 1 express

2. **Generación de Clientes:**
   - Se generan N clientes con número aleatorio de artículos (1-50)

3. **Asignación de Clientes:**
   - Para cada cliente, se intenta asignar a una caja aleatoria
   - Si la caja es express y el cliente tiene más de 10 artículos, se rechaza la asignación
   - Se repite hasta encontrar una caja disponible

4. **Cálculo de Tiempos:**
   - Para cada caja, se calcula el tiempo de atención de cada cliente
   - Se acumula el tiempo de espera: cada cliente posterior espera el tiempo de atención de los anteriores
   - El tiempo total de un cliente = tiempo de escaneo + tiempo de cobro + tiempo de espera acumulado

5. **Resultados:**
   - Se muestran estadísticas de cada caja
   - Se listan los tiempos individuales de cada cliente

## Lógica de Tiempo

### Tiempo de Atención por Cliente
```
tiempoEscaneo = numeroArticulos × tiempoEscaneoPorArticulo
tiempoAtencion = tiempoEscaneo + tiempoCobro
```

### Tiempo Total por Cliente (incluyendo espera)
```
tiempoTotalCliente = tiempoAtencionCliente + tiempoEsperaAcumulado
tiempoEsperaAcumulado += tiempoAtencionCliente  # Para el siguiente cliente
```

## Restricciones Express

- Las cajas express solo aceptan clientes con ≤ 10 artículos
- Si un cliente con > 10 artículos intenta usar express, es rechazado
- El sistema busca automáticamente otra caja disponible

## Ejecución

```bash
python main.py
```

## Salida de Ejemplo

```
=== RESULTADOS DE LA SIMULACIÓN ===
Total de clientes generados: 20
Total de cajas: 5 (4 normales, 1 express)

Caja 1 (Normal) atendida por Cajero con experiencia...
Clientes en fila:
  Cliente con 27 artículos., Tiempo total en ser atendido: 106.00s
  Cliente con 4 artículos., Tiempo total en ser atendido: 106.00s + 46.00s = 152.00s
  ...
```

## Notas Técnicas

- Los tiempos están en segundos
- La experiencia del cajero afecta la velocidad de escaneo
- El tiempo de cobro es aleatorio para cada cajero
- La simulación usa asignación aleatoria de clientes a cajas
- Los tiempos se acumulan correctamente considerando la fila FIFO (First In, First Out)
