# Documentación de Implementaciones Nuevas - Experimento de Simulación de Supermercado

## Fecha de Implementación
2025-11-14

## Resumen
Se implementó el diseño experimental completo para la simulación de supermercado, integrando el cálculo de costos y métricas de rendimiento según los requisitos del Taller 4.

## 1. Clase Costos (simulation/simulation.py)

### Descripción
Nueva clase que calcula los costos operativos y métricas clave de una simulación.

### Parámetros del Constructor
- `c_caja_min` (float): Costo por caja activa (USD/min) - default: 2.0
- `c_espera_min` (float): Costo del tiempo en sistema (USD/min por cliente) - default: 0.5
- `c_sla_penalizacion` (float): Penalización por punto porcentual de SLA incumplido - default: 10.0
- `sla_tiempo_limite_seg` (float): Límite de tiempo (seg) para SLA - default: 480 (8 min)
- `sla_objetivo_porcentaje` (float): Porcentaje objetivo del SLA - default: 80

### Método Principal: calcular_costos_simulacion()
**Parámetros:**
- `cajas` (List[Caja]): Lista de objetos Caja
- `clientes` (List[Cliente]): Lista de objetos Cliente

**Retorna:** Diccionario con métricas calculadas:
- `s_cajas`: Número de cajas activas
- `total_clientes`: Total de clientes
- `t_operacion_min`: Tiempo total de operación en minutos
- `suma_t_sistema_min`: Suma de tiempos en sistema en minutos
- `sla_actual_porcentaje`: Porcentaje de cumplimiento SLA
- `costo_cajas_usd`: Costo de cajas
- `costo_espera_usd`: Costo de espera
- `costo_sla_usd`: Costo de penalización SLA
- `costo_total_usd`: Costo total (CT)

### Fórmulas Implementadas
- **Costo_cajas** = c_caja × s × T_operacion
- **Costo_espera** = c_espera × Σ(T_sistema)
- **Costo_SLA** = c_SLA × max(0, SLA_objetivo - SLA_actual)
- **CT** = Costo_cajas + Costo_espera + Costo_SLA

## 2. Modificaciones a main.py

### Nuevos Imports
```python
from simulation.simulation import Costos
import statistics
```

### Modificación de la Función main()
- **Cambio en retorno:** Ahora retorna `cajas, clientes, costos_dict`
- **Integración de Costos:** Se instancia Costos con parámetros fijos y se calcula costos_dict al final

### Nueva Función: run_experiment()

#### Propósito
Ejecuta el experimento completo con múltiples configuraciones y réplicas.

#### Parámetros del Experimento
- **Niveles de s:** [3, 4, 5, 6, 7] (número de cajas)
- **Horizontes:** [50, 100, 150] (número de clientes)
- **Réplicas (R):** 10 por configuración
- **Parámetros de costo:** Fijos como arriba

#### Estructura de Ejecución
```python
for s in s_levels:
    for num_clients in horizons:
        for replica in range(R):
            # Ejecutar simulación
            # Calcular costos
            # Almacenar en matriz
```

#### Matriz de Corridas
- **Estructura:** Lista de diccionarios
- **Campos por corrida:** s, num_clients, replica, + todos los campos de costos_dict
- **Total de corridas:** 150 (15 configuraciones × 10 réplicas)

#### Cálculos Agregados por Configuración
Para cada combinación (s, num_clients):
- **CT promedio** ± desviación estándar
- **E[T] promedio** ± desviación estándar (tiempo en sistema promedio)
- **%SLA promedio** ± desviación estándar

#### Salida por Consola
- Resumen del experimento
- Progreso por configuración
- Resultados agregados con estadísticas
- Muestra de la matriz (primeras 10 corridas)

#### Datos para Graficación
- `matriz_corridas`: Lista completa de todas las corridas
- `datos_para_graficar`: Copia de matriz_corridas para análisis futuro

### Modificación del Bloque if __name__
- **Antes:** Configuración manual y ejecución única
- **Ahora:** Llamada a `run_experiment()` para ejecución completa del experimento

## 3. Resultados del Experimento

### Configuraciones Ejecutadas
- **Total:** 15 configuraciones (5 niveles s × 3 horizontes)
- **Réplicas:** 10 por configuración
- **Total corridas:** 150

### Métricas Calculadas
- Costos totales (CT) en USD
- Tiempos promedio en sistema (E[T]) en minutos
- Porcentajes de cumplimiento SLA (%SLA)

### Observaciones Iniciales
- Rendimientos decrecientes: Aumento de s incrementa costos con mejoras marginales en SLA
- Variabilidad: Desviaciones estándar muestran estabilidad del sistema
- Escalabilidad: Sistema maneja diferentes cargas de clientes

## 4. Estructura para Extensiones Futuras

### Análisis de Sensibilidad
- Preparado para variar ±10-20% λ (tasa de llegada) o tiempos de servicio
- Estructura de datos permite comparación fácil

### Graficación
- Datos estructurados para gráficos de:
  - CT vs s (por horizonte)
  - %SLA vs s
  - E[T] vs carga

### Documentación V&V
- Código comentado con justificaciones
- Supuestos documentados en parámetros
- Resultados reproducibles con semillas aleatorias

## 5. Archivos Modificados
- `simulation/simulation.py`: Agregada clase Costos
- `main.py`: Modificaciones completas para experimento

## 6. Archivos Nuevos
- `nuevo_implementado.md`: Esta documentación

---
*Implementación completada para la primera parte del experimento. Lista para análisis de sensibilidad, graficación y documentación completa.*