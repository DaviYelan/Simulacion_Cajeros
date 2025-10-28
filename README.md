# Simulación de Supermercado

Este proyecto simula el funcionamiento de un supermercado con múltiples cajas de atención al cliente, incluyendo cajas normales y una caja express. La simulación calcula tiempos de atención, espera en fila y asignación de clientes a cajas.

## Estructura del Proyecto

```
supermercado/
├── main.py                 # Archivo principal que ejecuta la simulación
├── README.md               # Documentación del proyecto
├── display/
│   └── interfaz.py         # Interfaz gráfica con animación en tiempo real
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

## Modos de Ejecución

### 1. Modo Consola (main.py)
Ejecuta la simulación en terminal y muestra resultados detallados.

```bash
python main.py
```

**Configuración disponible:**
- `num_cajeros`: Número de cajeros/cajas (3-8)
- `num_clientes`: Número de clientes (10-50)
- `posicion_express`: Posición de caja express ("primera", "medio", "ultima", "aleatoria")

### 2. Modo Interfaz Gráfica (interfaz.py)
Ejecuta la interfaz gráfica independiente con controles interactivos.

```bash
cd display
python interfaz.py
```

### 3. Modo Integrado
Ejecuta simulación inicial + interfaz gráfica automáticamente.

```bash
python main.py  # Automáticamente abre la interfaz después de calcular
```

## Flujo de la Simulación

1. **Configuración Inicial:**
   - Número configurable de cajeros (3-8)
   - Posición configurable de caja express ("primera", "medio", "ultima", "aleatoria")
   - Número configurable de clientes (10-50)

2. **Inicialización:**
   - Se crea un generador de datos
   - Se generan N cajeros con experiencia aleatoria
   - Se crean N cajas: N-1 normales y 1 express en posición configurable

3. **Generación de Clientes:**
   - Se generan M clientes con número aleatorio de artículos (1-50)

4. **Asignación Inteligente de Clientes:**
   - **Clientes con ≤10 artículos**: Intentan primero la caja express
   - **Clientes con >10 artículos**: Van directamente a cajas normales
   - Lógica realista que simula comportamiento de clientes en supermercado

5. **Cálculo de Tiempos:**
   - Para cada caja, se calcula el tiempo de atención de cada cliente
   - Se acumula el tiempo de espera: cada cliente posterior espera el tiempo de atención de los anteriores
   - El tiempo total de un cliente = tiempo de escaneo + tiempo de cobro + tiempo de espera acumulado

6. **Visualización:**
   - **Consola**: Resultados detallados con tiempos individuales
   - **Interfaz gráfica**: Animación en tiempo real de la atención de clientes
   - **Estadísticas**: Comparación de eficiencia entre cajas

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

### Modo Integrado (Recomendado)
Ejecuta simulación completa con interfaz gráfica:

```bash
python main.py
```

### Modo Interfaz Gráfica Independiente
Solo interfaz gráfica con controles interactivos:

```bash
cd display
python interfaz.py
```

### Personalización
Edita las variables en `main.py` para cambiar la configuración inicial:
 
```python
num_cajeros = 5        # Número de cajeros (3-8)
num_clientes = 25      # Número de clientes (10-50)
posicion_express = "primera"  # "primera", "medio", "ultima", "aleatoria"
```

## Características Destacadas

### 🎯 Asignación Inteligente de Clientes
- Los clientes con pocos artículos prefieren automáticamente la caja express
- Simula comportamiento realista de clientes en supermercado
- Evita colas innecesarias en cajas express

### 🎨 Interfaz Gráfica Animada
- Visualización en tiempo real de la atención de clientes
- Animación automática con velocidad configurable
- Diseño intuitivo con colores diferenciados para cajas normales/express

### 📊 Análisis Comparativo
- Recomendación automática de la caja más rápida para nuevos clientes
- Estadísticas detalladas de eficiencia por caja
- Comparación de rendimiento entre cajas normales y express

### 🔧 Configuración Flexible
- Número variable de cajeros y cajas (3-8)
- Posición configurable de caja express
- Cantidad ajustable de clientes
- Velocidad de animación personalizable

## Salida de Ejemplo

```
=== RESULTADOS DE LA SIMULACIÓN ===
Total de clientes generados: 25
Total de cajas: 5 (4 normales, 1 express)

Caja 1 (Express) atendida por Cajero con experiencia...
Clientes en fila:
  Cliente con 6 artículos., Tiempo total en ser atendido: 42.00s
  Cliente con 8 artículos., Tiempo total en ser atendido: 90.00s
  ...

=== RECOMENDACIÓN PARA NUEVO CLIENTE ===
La caja más rápida para un nuevo cliente es la Caja 1 (Express)
```

## Requisitos del Sistema

- Python 3.6+
- Tkinter (incluido en la instalación estándar de Python)
- Pillow (PIL) para imágenes: `pip install pillow`

## Notas Técnicas

- **Tiempos**: Todas las mediciones están en segundos
- **Experiencia del cajero**: Afecta la velocidad de escaneo (3s vs 6s por artículo)
- **Tiempo de cobro**: Aleatorio entre 15-30 segundos por cajero
- **Asignación inteligente**: Los clientes eligen cajas basándose en restricciones express
- **Acumulación de tiempos**: FIFO correcto con espera acumulada en filas
- **Interfaz gráfica**: Diseño responsivo que se adapta al número de cajas

## Arquitectura del Sistema

- **Modular**: Separación clara entre modelos, simulación e interfaz
- **Configurable**: Todos los parámetros principales son ajustables
- **Extensible**: Fácil agregar nuevas funcionalidades
- **Documentado**: Código bien comentado y README completo

## Autores
- **César López
- **Luis Armijos
- **Dilan Chamba 
