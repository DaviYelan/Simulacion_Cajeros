# Explicación de Cambios en Clases y Uso del Sistema

## 🔧 Cambios Específicos por Clase

### 1. `models/cajero.py` - Modificaciones para Análisis de Sensibilidad

**Cambios realizados:**
```python
class Cajero:
    def __init__(self, tieneExperiencia: bool, service_multiplier: float = 1.0):
        self.experiencia = tieneExperiencia
        self.service_multiplier = service_multiplier

        if self.experiencia:
            self.tiempoEscaneoPorArticulo = 3 * service_multiplier
        else:
            self.tiempoEscaneoPorArticulo = 6 * service_multiplier
        self.tiempoCobro = random.randint(15, 30) * service_multiplier
```

**Cómo funciona:**
- **Parámetro nuevo:** `service_multiplier` permite escalar tiempos de servicio para análisis de sensibilidad
- **Aplicación:** Multiplica tiempos base de escaneo y cobro por el factor especificado
- **Ejemplos:**
  - `service_multiplier = 0.8`: Reduce tiempos 20% (servicio más rápido)
  - `service_multiplier = 1.2`: Aumenta tiempos 20% (servicio más lento)
  - `service_multiplier = 1.0`: Comportamiento original (default)

**Soporte al documento:**
- ✅ Implementa análisis de sensibilidad para "tiempos de servicio" (±10-20%)
- ✅ Permite variar eficiencia del personal como factor de robustez
- ✅ Mantiene reproducibilidad cuando se usan semillas

### 2. `simulation/generadorDatos.py` - Generación con Parámetros Variables

**Cambios realizados:**
```python
def generarCajeros(self, numeroCajeros: int, service_multiplier: float = 1.0):
    cajeros = [] #lista vacia para almacenar cajeros
    for _ in range(numeroCajeros):
        experienciaAleatoria = random.choice([True, False]) #generamos experiencia aleatoria
        cajero = Cajero(experienciaAleatoria, service_multiplier) #creamos instancia de cajero con experiencia aleatoria
        cajeros.append(cajero) #agregamos cajero a la lista
    return cajeros
```

**Cómo funciona:**
- **Transmisión de parámetros:** Pasa `service_multiplier` a cada instancia de Cajero creada
- **Consistencia:** Todos los cajeros en una simulación usan el mismo multiplicador de servicio
- **Backward compatibility:** Default `1.0` mantiene funcionamiento original

**Soporte al documento:**
- ✅ Habilita variaciones sistemáticas en eficiencia de servicio
- ✅ Soporta análisis de sensibilidad requerido por domento.txt
- ✅ Mantiene aleatoriedad en experiencia pero control en tiempos

### 3. `simulation/simulation.py` - Clase Costos (Base del Sistema)

**Estructura completa:**
```python
class Costos:
    def __init__(self,
                 c_caja_min: float,
                 c_espera_min: float,
                 c_sla_penalizacion: float,
                 sla_tiempo_limite_seg: float,
                 sla_objetivo_porcentaje: float):
        self.c_caja_min = c_caja_min
        self.c_espera_min = c_espera_min
        self.c_sla_penalizacion = c_sla_penalizacion
        self.sla_tiempo_limite_seg = sla_tiempo_limite_seg
        self.sla_objetivo_porcentaje = sla_objetivo_porcentaje

    def calcular_costos_simulacion(self, cajas: List[Caja], clientes: List[Cliente]) -> Dict[str, Any]:
        # Cálculos de métricas y costos
        return {
            "s_cajas": s_cajas,
            "total_clientes": total_clientes,
            "t_operacion_min": t_operacion_min,
            "suma_t_sistema_min": suma_t_sistema_min,
            "sla_actual_porcentaje": sla_actual_porcentaje,
            "costo_cajas_usd": costo_cajas_usd,
            "costo_espera_usd": costo_espera_usd,
            "costo_sla_usd": costo_sla_usd,
            "costo_total_usd": costo_total_usd
        }
```

**Fórmulas implementadas:**
- **CT (Costo Total):** `c_caja·(s·tiempo) + c_espera·(Σ tiempo en sistema) + c_SLA·(incumplimiento)`
- **E[T] (Tiempo en Sistema):** `Σ(tiempo en sistema) / total_clientes`
- **%SLA:** `(clientes_cumplen / total_clientes) × 100`
- **Incumplimiento:** `max(0, SLA_objetivo - SLA_actual)`

**Cómo funciona:**
- **Cálculo automático:** Procesa listas de cajas y clientes para generar métricas
- **Retorno estructurado:** Diccionario con todas las métricas para matriz de corridas
- **Validación incluida:** Manejo de casos edge (0 cajas, 0 clientes)

**Soporte al documento:**
- ✅ Implementa fórmula CT exacta del domento.txt
- ✅ Calcula indicadores por réplica (E[T], %SLA)
- ✅ Genera datos estructurados para análisis y gráficos
- ✅ Soporta evaluación de trade-off costo vs servicio

### 4. `main.py` - Núcleo del Experimento

**Cambios principales:**
- **Parámetros main():** `client_multiplier=1.0`, `service_multiplier=1.0`, `seed=None`
- **Semillas:** `random.seed(seed)` para reproducibilidad cuando seed != None
- **Ajuste dinámico:** `num_clientes_ajustado = int(num_clientes * client_multiplier)`
- **6 funciones nuevas:** Experimento, gráficos, sensibilidad, regla, documentación, reflexión

**Flujo de ejecución completo:**
1. `run_experiment()`: 150 simulaciones con semillas específicas
2. `generar_graficos()`: Visualización de 4 gráficos comparativos
3. `analisis_sensibilidad()`: Pruebas ±20% en λ y tiempos de servicio
4. `proponer_regla_apertura()`: Análisis de evidencia y regla propuesta
5. `documentar_supuestos()`: V&V conceptual completo
6. `reflexion_abpr()`: Reflexión del proceso de aprendizaje

## 🧪 Guía de Uso y Modificación de main.py

### Ejecutar Sistema Completo
```bash
python main.py
```
**Salida:** Experimento + sensibilidad + regla + documentación completa

### Modificar Parámetros del Experimento

**Ubicación:** Función `run_experiment()` en main.py

```python
# Modificar niveles de cajas estudiadas
s_levels = [2, 3, 4, 5, 6, 7, 8]  # Agregar más opciones

# Cambiar horizontes de demanda
horizons = [25, 50, 75, 100, 125, 150, 200]  # Más granular

# Aumentar precisión estadística
R = 20  # Más réplicas por configuración

# Ajustar parámetros de costo
cost_params = {
    'c_caja_min': 3.0,  # $3/min por caja
    'c_espera_min': 0.8,  # $0.80/min por cliente
    'c_sla_penalizacion': 15.0,  # $15 por punto porcentual
    'sla_tiempo_limite_seg': 600,  # 10 minutos límite
    'sla_objetivo_porcentaje': 90  # 90% objetivo SLA
}
```

### Crear Pruebas Específicas

**Agregar función de prueba individual:**
```python
def probar_configuracion_especifica():
    """Probar configuración específica sin experimento completo"""
    s = 5
    num_clientes = 100
    seed = 12345  # Reproducibilidad

    cajas, clientes, costos = main(s, num_clientes, "primera",
                                   client_multiplier=1.0,
                                   service_multiplier=1.0,
                                   seed=seed)

    print(f"=== RESULTADOS CONFIGURACIÓN ESPECÍFICA ===")
    print(f"Cajas: {s}, Clientes: {num_clientes}")
    print(f"Costo Total: ${costos['costo_total_usd']:.2f}")
    print(f"SLA Actual: {costos['sla_actual_porcentaje']:.1f}%")
    print(f"Tiempo Promedio: {costos['suma_t_sistema_min']/costos['total_clientes']:.2f} min")

# Agregar al final del archivo
if __name__ == "__main__":
    probar_configuracion_especifica()  # Para pruebas rápidas
```

### Personalizar Análisis de Sensibilidad

**Ubicación:** Función `analisis_sensibilidad()`

```python
# Extender rangos de variación
lambda_multipliers = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]  # ±30%
service_multipliers = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]  # ±30%

# Más réplicas para mejor precisión
R = 15  # En lugar de 5
```

### Modificar Regla de Decisión

**Ubicación:** Función `proponer_regla_apertura()`

```python
# Ajustar umbrales de decisión
sla_threshold = 90.0  # Cambiar de 85% a 90%
costo_sla_por_punto = 15.0  # Penalización por punto

# Lógica más sofisticada
if ct_marginal > (costo_sla_por_punto * sla_marginal):
    decision = "No abrir - costo > beneficio"
else:
    decision = "Abrir caja adicional"
```

### Ejecutar Componentes Selectivamente

**Modificar bloque principal:**
```python
if __name__ == "__main__":
    # Descomentar solo lo que se quiera ejecutar

    # 1. Solo experimento base
    # matriz_corridas, _ = run_experiment()

    # 2. Solo análisis de sensibilidad
    # resultados_sens = analisis_sensibilidad()

    # 3. Solo propuesta de regla
    # configs = proponer_regla_apertura(matriz_corridas)

    # 4. Solo documentación
    # documentar_supuestos()
    # reflexion_abpr()

    # 5. Sistema completo (recomendado)
    matriz_corridas, _ = run_experiment()
    resultados_sens = analisis_sensibilidad()
    configs = proponer_regla_apertura(matriz_corridas)
    documentar_supuestos()
    reflexion_abpr()
```

## 🔍 Verificación y Depuración

### Verificar Funcionamiento
```bash
# Sintaxis
python -m py_compile main.py

# Ejecución completa
python main.py

# Verificar archivos generados
ls -la *.png  # resultados_experimento.png
```

### Depurar Problemas
```python
# Agregar prints de debug en main()
print(f"Debug: s={s}, clientes={num_clientes_ajustado}, seed={seed}")
print(f"Debug: costos calculados: {costos}")

# Verificar semillas
print(f"Semilla usada: {seed}")
```

## 📊 Archivos Generados

- `resultados_experimento.png`: 4 gráficos comparativos
- Salida consola: Métricas detalladas y análisis
- Estructuras de datos: `matriz_corridas`, `resultados_sensibilidad`

## 🎯 Recomendaciones de Uso

1. **Para desarrollo:** Usar pruebas selectivas con `probar_configuracion_especifica()`
2. **Para experimentos:** Ejecutar sistema completo con parámetros modificados
3. **Para validación:** Verificar reproducibilidad cambiando semillas
4. **Para análisis:** Modificar umbrales en `proponer_regla_apertura()`

El sistema está diseñado para ser **modular**, **configurable** y **extensible**, permitiendo fácil modificación sin comprometer la funcionalidad core.