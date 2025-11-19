# Archivo: simulation/costos.py

from models.caja import Caja
from models.cliente import Cliente
from typing import List, Dict, Any

class Costos:
    """
    Calcula los costos operativos y de servicio de una simulación
    basado en los requisitos del Taller 4.
    """
    def __init__(self, 
                 c_caja_min: float, 
                 c_espera_min: float, 
                 c_sla_penalizacion: float,
                 sla_tiempo_limite_seg: float,
                 sla_objetivo_porcentaje: float):
        """
        Inicializa la calculadora de costos con los parámetros del negocio.

        Args:
            c_caja_min (float): Costo por caja activa (USD/min).
            c_espera_min (float): Costo del tiempo en sistema (USD/min por cliente).
            c_sla_penalizacion (float): Penalización por punto porcentual de SLA incumplido.
            sla_tiempo_limite_seg (float): Límite de tiempo (en seg) para el SLA (ej. 480s para 8 min).
            sla_objetivo_porcentaje (float): Porcentaje objetivo del SLA (ej. 80 para 80%).
        """
        self.c_caja_min = c_caja_min
        self.c_espera_min = c_espera_min
        self.c_sla_penalizacion = c_sla_penalizacion
        self.sla_tiempo_limite_seg = sla_tiempo_limite_seg
        self.sla_objetivo_porcentaje = sla_objetivo_porcentaje

    def calcular_costos_simulacion(self, cajas: List[Caja], clientes: List[Cliente]) -> Dict[str, Any]:
        """
        Calcula todos los costos y métricas clave de una sola corrida de simulación.
        """
        
        # --- 1. Calcular Métricas de Simulación ---

        # s (Número de cajas activas)
        s_cajas = len(cajas)
        if s_cajas == 0:
            return {"error": "No hay cajas para calcular."} # Control de error

        # T_operacion (Tiempo total de operación en minutos)
        # Es el tiempo de la caja que más tardó en terminar.
        t_operacion_seg = max(caja.tiempoAtencionTotal for caja in cajas)
        t_operacion_min = t_operacion_seg / 60.0

        # Suma(T_sistema) (Suma de tiempo total de todos los clientes en minutos)
        total_clientes = len(clientes)
        if total_clientes == 0:
            return {"error": "No hay clientes para calcular."} # Control de error
            
        suma_t_sistema_seg = sum(cliente.tiempoTotal for cliente in clientes)
        suma_t_sistema_min = suma_t_sistema_seg / 60.0

        # %SLA (Porcentaje de cumplimiento de SLA)
        clientes_cumplen_sla = sum(1 for cliente in clientes if cliente.tiempoTotal <= self.sla_tiempo_limite_seg)
        sla_actual_porcentaje = (clientes_cumplen_sla / total_clientes) * 100.0

        # --- 2. Calcular Costos (Taller 4) ---

        # Costo_cajas = c_caja * s * T_operacion
        costo_cajas_usd = self.c_caja_min * s_cajas * t_operacion_min

        # Costo_espera = c_espera * Suma(T_sistema)
        costo_espera_usd = self.c_espera_min * suma_t_sistema_min

        # Costo_SLA = c_SLA * (incumplimiento)
        incumplimiento_pct = max(0, self.sla_objetivo_porcentaje - sla_actual_porcentaje)
        costo_sla_usd = self.c_sla_penalizacion * incumplimiento_pct

        # Costo Total (CT)
        costo_total_usd = costo_cajas_usd + costo_espera_usd + costo_sla_usd

        # --- 3. Retornar todo en un diccionario ---
        # Esto es perfecto para tu "Matriz de Corridas"
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