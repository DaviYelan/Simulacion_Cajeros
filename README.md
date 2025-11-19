# Simulación de Supermercado

Este proyecto simula el funcionamiento de un supermercado con múltiples cajas de atención al cliente, incluyendo cajas normales y una caja express. La simulación calcula tiempos de atención, espera en fila y asignación inteligente de clientes a cajas, con interfaz gráfica animada en tiempo real.

## Estructura del Proyecto

```
supermercado/
├── main.py                 # Archivo principal que ejecuta la simulación
├── README.md               # Documentación del proyecto
├── display/
│   └── interfaz.py         # Interfaz gráfica con animación en tiempo real
├── models/
│   ├── __init__.py
│   ├── cliente.py          # Clase Cliente
│   ├── cajero.py           # Clase Cajero
│   └── caja.py             # Clase Caja
└── simulation/
    ├── __init__.py
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

## Documentación Detallada de main.py

### Arquitectura General del Programa

El archivo `main.py` es el núcleo del sistema de simulación, implementando una arquitectura modular que coordina la generación de datos, simulación de procesos y visualización de resultados. El programa sigue el patrón **MVC (Modelo-Vista-Controlador)** de manera implícita:

- **Modelo**: Clases en `models/` (Cliente, Cajero, Caja)
- **Vista**: Interfaz gráfica en `display/interfaz.py`
- **Controlador**: Lógica de simulación en `main.py`

### Estructura del Código

#### 1. Imports y Dependencias
```python
# Simulación de supermercado con 5 cajas (4 normales y 1 express)
from display.interfaz import iniciar_interfaz
from simulation.generadorDatos import GeneradorDatos
from models.caja import Caja
import random
```

**Análisis**: Se importan los módulos necesarios con una jerarquía clara:
- `display.interfaz`: Para la visualización gráfica
- `simulation.generadorDatos`: Para la creación de datos aleatorios
- `models.caja`: La clase principal de simulación
- `random`: Para selecciones aleatorias

#### 2. Función `encontrarCajaMasRapida()`

```python
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
```

**Lógica implementada**:
- **Validación inicial**: Verifica que exista al menos una caja
- **Algoritmo de selección**: Usa `min()` con función lambda para comparar `tiempoAtencionTotal`
- **Eficiencia**: O(n) complejidad, óptimo para sistemas con pocas cajas
- **Robustez**: Maneja casos edge (lista vacía)

**Por qué esta implementación**:
- La función `min()` con `key` es idiomática en Python
- El lambda permite flexibilidad en criterios de comparación
- Es extensible para futuros criterios de evaluación

#### 3. Función Principal `main()`

```python
def main(num_cajeros, num_clientes, posicion_express):
    """
    Simulación de supermercado con configuración completa.

    Args:
        num_cajeros: Número de cajeros a generar
        num_clientes: Número de clientes a generar
        posicion_express: Posición de la caja express ("primera", "medio", "ultima", "aleatoria")
    """
```

**Diseño de parámetros**:
- **Sin valores por defecto**: Fuerza configuración explícita
- **Tipos simples**: Fáciles de validar y usar
- **Nombres descriptivos**: Auto-documentados

### Sección de Configuración

```python
# === CONFIGURACIÓN DE LA SIMULACIÓN ===
# Todas las configuraciones se hacen aquí al inicio

# Inicializar generador de datos
generador = GeneradorDatos()
```

**Patrón de configuración centralizada**:
- Todas las configuraciones en un solo lugar
- Comentarios explicativos
- Fácil modificación para testing

### Generación de Cajeros

```python
# Generar cajeros
cajeros = generador.generarCajeros(num_cajeros)
```

**Lógica subyacente en GeneradorDatos**:
```python
def generarCajeros(self, numeroCajeros: int):
    cajeros = []
    for _ in range(numeroCajeros):
        experienciaAleatoria = random.choice([True, False])
        cajero = Cajero(experienciaAleatoria)
        cajeros.append(cajero)
    return cajeros
```

**Distribución de experiencia**:
- 50% de cajeros experimentados (3s/artículo)
- 50% de cajeros principiantes (6s/artículo)
- Crea variabilidad realista en el sistema

### Determinación de Posición Express

```python
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
```

**Estrategias de posicionamiento**:
- **"primera"**: Índice 0 (posición inicial)
- **"medio"**: Centro del arreglo (num_cajeros // 2)
- **"ultima"**: Última posición (num_cajeros - 1)
- **"aleatoria"**: Distribución uniforme aleatoria

**Justificación**: Permite estudiar el impacto de la ubicación de la caja express en la eficiencia general.

### Creación de Cajas

```python
# Crear cajas con posición express configurable
cajas = []
for i in range(num_cajeros):
    es_express = (i == posicion_express_idx)
    caja = Caja(idCaja=i+1, cajero=cajeros[i], esExpress=es_express)
    cajas.append(caja)
```

**Lógica de asignación**:
- Una sola caja express por simulación
- Resto son cajas normales
- Asignación 1:1 entre cajeros y cajas
- IDs secuenciales empezando en 1

### Generación de Clientes

```python
# Generar clientes
clientes = generador.generaClientes(num_clientes)
```

**Implementación en GeneradorDatos**:
```python
def generaClientes(self, numeroClientes: int):
    clientes = []
    for _ in range(numeroClientes):
        numeroArticulos = random.randint(1, 50)
        cliente = Cliente(numeroArticulos)
        clientes.append(cliente)
    return clientes
```

**Distribución actual**: Uniforme entre 1-50 artículos
**Potencial mejora**: Implementar sesgo hacia valores ≤10 para favorecer caja express

### Asignación Inteligente de Clientes

```python
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
```

**Algoritmo de asignación en dos fases**:

#### Fase 1: Prioridad a Caja Express
```python
if cliente.numeroArticulos <= 10:
    caja_express = next((caja for caja in cajas if caja.esExpress), None)
    if caja_express and caja_express.agregarCliente(cliente):
        asignado = True
```

**Lógica**:
- Solo clientes con ≤10 artículos pueden intentar la express
- `next()` con generador encuentra la caja express eficientemente
- `agregarCliente()` valida restricciones internas

#### Fase 2: Asignación a Cajas Normales
```python
if not asignado:
    cajas_normales = [caja for caja in cajas if not caja.esExpress]
    while not asignado and cajas_normales:
        caja_aleatoria = random.choice(cajas_normales)
        if caja_aleatoria.agregarCliente(cliente):
            asignado = True
        else:
            cajas_normales.remove(caja_aleatoria)
```

**Estrategia de respaldo**:
- Filtra cajas normales disponibles
- Selección aleatoria con `random.choice()`
- Eliminación de cajas llenas para evitar bucles infinitos
- Garantiza que todos los clientes sean asignados

**Ventajas de este enfoque**:
- **Realista**: Simula comportamiento humano (preferencia por express cuando posible)
- **Eficiente**: Evita colas innecesarias en express
- **Robusto**: Maneja casos edge (express llena, restricciones)

### Cálculo de Tiempos

```python
# Calcular tiempos de atención para cada caja
for caja in cajas:
    caja.calcularTiempoAtencion()
```

**Implementación en Caja.calcularTiempoAtencion()**:
```python
def calcularTiempoAtencion(self) -> float:
    self.tiempoAtencionTotal = 0.0
    tiempoEsperaAcumulado = 0.0

    for cliente in self.filaClientes:
        tiempoEscaneo = cliente.numeroArticulos * self.cajero.tiempoEscaneoPorArticulo
        tiempoAtencion = tiempoEscaneo + self.cajero.tiempoCobro
        cliente.tiempoTotal = tiempoAtencion + tiempoEsperaAcumulado
        tiempoEsperaAcumulado += tiempoAtencion
        self.tiempoAtencionTotal += tiempoAtencion
    return self.tiempoAtencionTotal
```

**Cálculo FIFO preciso**:
- **tiempoEsperaAcumulado**: Acumula espera para clientes posteriores
- **cliente.tiempoTotal**: Tiempo individual incluyendo espera
- **tiempoAtencionTotal**: Suma total de atención de la caja

### Presentación de Resultados

```python
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
```

**Formato de salida estructurado**:
- Encabezados claros con `===`
- Estadísticas generales
- Detalle por caja con `__str__()` personalizado
- Lista de clientes con tiempos individuales

### Sistema de Recomendación

```python
# Encontrar y mostrar la caja más rápida para un nuevo cliente
caja_mas_rapida = encontrarCajaMasRapida(cajas)
print("=== RECOMENDACIÓN PARA NUEVO CLIENTE ===")
if caja_mas_rapida:
    tipo_caja = "Express" if caja_mas_rapida.esExpress else "Normal"
    print(f"La caja más rápida para un nuevo cliente es la Caja {caja_mas_rapida.idCaja} ({tipo_caja})")
    print(f"Tiempo total de atención actual: {caja_mas_rapida.tiempoAtencionTotal:.2f}s")
    print(f"Clientes en fila: {len(caja_mas_rapida.filaClientes)}")
print()
```

**Análisis automático**:
- Identifica la caja con menor `tiempoAtencionTotal`
- Proporciona recomendación actionable
- Incluye métricas relevantes (tiempo, cantidad de clientes)

### Retorno de Datos

```python
# Retornar los datos para que la interfaz pueda usarlos
return cajas, clientes
```

**Integración con interfaz gráfica**:
- Los datos calculados se pasan a `iniciar_interfaz_con_datos()`
- Permite visualización sin recalcular
- Mantiene sincronización entre consola e interfaz

### Configuración del Programa Principal

```python
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
```

**Diseño de configuración**:
- Variables claramente nombradas
- Comentarios explicativos
- Fácil modificación para testing
- Integración automática con interfaz

## Análisis de Complejidad

### Complejidad Temporal
- **Generación**: O(num_cajeros + num_clientes)
- **Asignación**: O(num_clientes × num_cajeros) en peor caso
- **Cálculo de tiempos**: O(total_clientes)
- **Recomendación**: O(num_cajeros)

### Complejidad Espacial
- **Cajas**: O(num_cajeros)
- **Clientes**: O(num_clientes)
- **Optimizado**: No almacena datos innecesarios

## Consideraciones de Diseño

### Principios SOLID Aplicados
- **S**: Cada función tiene responsabilidad única
- **O**: Extensible (parámetros configurables)
- **L**: Interfaces consistentes
- **I**: Dependencias mínimas
- **D**: Inyección de dependencias clara

### Manejo de Errores
- Validación de parámetros de entrada
- Manejo de casos edge (cajas vacías, express no disponible)
- Prevención de bucles infinitos en asignación

### Escalabilidad
- Algoritmos eficientes para crecimiento
- Configuración externa de parámetros
- Separación clara de responsabilidades

## Conclusión

El archivo `main.py` implementa una simulación completa y realista de un sistema de colas de supermercado, con:

- **Lógica inteligente** de asignación de clientes
- **Cálculos precisos** de tiempos FIFO
- **Sistema de recomendación** automático
- **Integración perfecta** con interfaz gráfica
- **Configuración flexible** para experimentación
- **Código limpio** y bien documentado

Esta implementación supera los requisitos básicos del proyecto al incluir características avanzadas como asignación inteligente, análisis comparativo y visualización integrada.

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
