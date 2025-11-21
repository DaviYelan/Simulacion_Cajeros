import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.generadorDatos import GeneradorDatos
from models.caja import Caja
import random

class SupermercadoGUI:
    def __init__(self, root, cajas_precalculadas=None, clientes_precalculados=None):
        self.root = root
        self.root.title("Simulación de Supermercado")
        # Ventana más grande para mostrar todo
        self.root.geometry("1600x900")
        self.root.configure(bg="#f0f0f0")

        # Variables de simulación
        self.cajas = cajas_precalculadas or []
        self.clientes_precalculados = clientes_precalculados
        self.animacion_activa = False
        self.velocidad_animacion = 1000  # milisegundos
        self.modo_precalculado = cajas_precalculadas is not None

        # Cargar imágenes
        self.cargar_imagenes()

        # Crear interfaz
        self.crear_interfaz()

        # Si hay datos precalculados, mostrarlos inmediatamente
        if self.modo_precalculado:
            # Guardar el estado original de las filas antes de mostrar
            self.clientes_originales = []
            for caja in self.cajas:
                self.clientes_originales.append(caja.filaClientes.copy())

            self.mostrar_simulacion_precalculada()
            # En modo precalculado, permitir nueva simulación con configuración modificable
            # Los controles permanecen habilitados para que el usuario pueda cambiarlos
        
    def cargar_imagenes(self):
        """Carga las imágenes de cajero y cliente"""
        try:
            img_cajero = Image.open("imagenes/Cajero.png")
            img_cliente = Image.open("imagenes/Cliente.png")
            
            # Redimensionar imágenes más pequeñas para ahorrar espacio
            img_cajero = img_cajero.resize((40, 40), Image.Resampling.LANCZOS)
            img_cliente = img_cliente.resize((30, 30), Image.Resampling.LANCZOS)
            
            self.img_cajero = ImageTk.PhotoImage(img_cajero)
            self.img_cliente = ImageTk.PhotoImage(img_cliente)
            self.imagenes_cargadas = True
        except Exception as e:
            #print(f"No se pudieron cargar las imágenes: {e}")
            #print("Se usarán representaciones alternativas")
            self.imagenes_cargadas = False
            self.img_cajero = None
            self.img_cliente = None
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame superior con controles 
        frame_controles = tk.Frame(self.root, bg="#2c3e50", height=80)
        frame_controles.pack(fill=tk.X, padx=5, pady=5)
        frame_controles.pack_propagate(False)
        
        # Título
        titulo = tk.Label(
            frame_controles, 
            text="🛒 SIMULACIÓN DE SUPERMERCADO 🛒",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=5)
        
        # Frame de configuración y botones en una sola línea
        frame_config = tk.Frame(frame_controles, bg="#2c3e50")
        frame_config.pack(pady=5)

        tk.Label(frame_config, text="Cajeros:",
                bg="#2c3e50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=3)

        self.spin_cajeros = tk.Spinbox(frame_config, from_=3, to=8, width=4, font=("Arial", 9))
        self.spin_cajeros.delete(0, tk.END)
        self.spin_cajeros.insert(0, "5")
        self.spin_cajeros.pack(side=tk.LEFT, padx=3)

        tk.Label(frame_config, text="Clientes:",
                bg="#2c3e50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=3)

        self.spin_clientes = tk.Spinbox(frame_config, from_=10, to=50, width=4, font=("Arial", 9))
        self.spin_clientes.delete(0, tk.END)
        self.spin_clientes.insert(0, "25")
        self.spin_clientes.pack(side=tk.LEFT, padx=3)

        tk.Label(frame_config, text="Posición Express:",
                bg="#2c3e50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=3)

        self.combo_posicion = ttk.Combobox(frame_config, values=["primera", "medio", "ultima", "aleatoria"],
                                         width=8, font=("Arial", 9), state="readonly")
        self.combo_posicion.set("ultima")
        self.combo_posicion.pack(side=tk.LEFT, padx=3)

        tk.Label(frame_config, text="Velocidad:",
                bg="#2c3e50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=3)

        self.spin_velocidad = tk.Spinbox(frame_config, from_=500, to=3000, increment=500,
                                        width=4, font=("Arial", 9))
        self.spin_velocidad.delete(0, tk.END)
        self.spin_velocidad.insert(0, "1000")
        self.spin_velocidad.pack(side=tk.LEFT, padx=3)
        tk.Label(frame_config, text="ms",
                bg="#2c3e50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=3)

        # Separador
        tk.Frame(frame_config, bg="white", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Selector de tipo de sensibilidad
        tk.Label(frame_config, text="Escenario:",
                bg="#2c3e50", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)

        self.combo_sensibilidad = ttk.Combobox(frame_config,
                                              values=["Normal", "Baja Demanda", "Alta Demanda",
                                                     "Servicio Lento", "Servicio Rápido"],
                                              width=12, font=("Arial", 7), state="readonly")
        self.combo_sensibilidad.set("Normal")
        self.combo_sensibilidad.bind("<<ComboboxSelected>>", self.cambiar_escenario)
        self.combo_sensibilidad.pack(side=tk.LEFT, padx=2)

        # Controles de sensibilidad (ocultos inicialmente)
        self.frame_avanzado = tk.Frame(frame_config, bg="#2c3e50")

        tk.Label(self.frame_avanzado, text="Demanda:",
                bg="#2c3e50", fg="white", font=("Arial", 7)).pack(side=tk.LEFT, padx=1)

        self.scale_demanda = tk.Scale(self.frame_avanzado, from_=0.5, to=2.0, resolution=0.1,
                                     orient=tk.HORIZONTAL, length=60, bg="#2c3e50",
                                     fg="white", highlightthickness=0, font=("Arial", 6))
        self.scale_demanda.set(1.0)
        self.scale_demanda.pack(side=tk.LEFT, padx=1)

        tk.Label(self.frame_avanzado, text="Servicio:",
                bg="#2c3e50", fg="white", font=("Arial", 7)).pack(side=tk.LEFT, padx=1)

        self.scale_servicio = tk.Scale(self.frame_avanzado, from_=0.5, to=2.0, resolution=0.1,
                                      orient=tk.HORIZONTAL, length=60, bg="#2c3e50",
                                      fg="white", highlightthickness=0, font=("Arial", 6))
        self.scale_servicio.set(1.0)
        self.scale_servicio.pack(side=tk.LEFT, padx=1)
        
        # Separador vertical
        tk.Frame(frame_config, bg="white", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de control
        self.btn_iniciar = tk.Button(
            frame_config,
            text="🚀 INICIAR",
            command=self.iniciar_simulacion,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=3,
            cursor="hand2"
        )
        self.btn_iniciar.pack(side=tk.LEFT, padx=3)

        self.btn_detener = tk.Button(
            frame_config,
            text="⏸️ DETENER",
            command=self.detener_animacion,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=3,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_detener.pack(side=tk.LEFT, padx=3)

        # Separador
        tk.Frame(frame_config, bg="white", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        
        # Frame principal 
        self.frame_principal = tk.Frame(self.root, bg="#ecf0f1")
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame de estadísticas
        self.frame_stats = tk.Frame(self.root, bg="#34495e")

        self.label_stats = tk.Label(
            self.frame_stats,
            text="",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            justify=tk.LEFT
        )
        self.label_stats.pack(pady=8, padx=15)

        # Frame de eventos (footer) - más alto para múltiples líneas
        self.frame_eventos = tk.Frame(self.root, bg="#2c3e50", height=80)
        self.frame_eventos.pack(fill=tk.X, padx=5, pady=5)
        self.frame_eventos.pack_propagate(False)

        # Label de eventos con mejor formato
        self.label_eventos = tk.Label(
            self.frame_eventos,
            text="📋 EVENTOS:\n• Simulación lista para iniciar",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="white",
            anchor="w",
            justify=tk.LEFT
        )
        self.label_eventos.pack(fill=tk.X, padx=10, pady=5)

        # Lista para almacenar eventos
        self.eventos_log = []
    
    def mostrar_simulacion_precalculada(self):
        """Muestra la simulación con datos precalculados del main.py"""
        # Limpiar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Dibujar cajas con datos precalculados
        self.dibujar_cajas_grid()

        # Configurar velocidad de animación
        self.velocidad_animacion = int(self.spin_velocidad.get())

        # Reiniciar las filas de clientes a su estado original para la animación
        self.resetear_clientes()

        # Iniciar animación
        self.animacion_activa = True
        self.btn_iniciar.config(state=tk.NORMAL)  # Permitir reiniciar
        self.btn_detener.config(state=tk.NORMAL)
        self.animar_atencion()

    def resetear_clientes(self):
        """Resetea las filas de clientes a su estado original para reiniciar la animación"""
        # Los datos precalculados incluyen las filas originales, pero la animación las modifica
        # Necesitamos guardar el estado original al inicio
        if not hasattr(self, 'clientes_originales'):
            # Guardar el estado original de las filas
            self.clientes_originales = []
            for caja in self.cajas:
                self.clientes_originales.append(caja.filaClientes.copy())

        # Restaurar las filas originales
        for i, caja in enumerate(self.cajas):
            caja.filaClientes = self.clientes_originales[i].copy()

    def iniciar_simulacion(self):
        """Inicia una nueva simulación con animación automática"""
        # Siempre permitir nuevas simulaciones, incluso en modo precalculado
        # El usuario puede cambiar la configuración y ejecutar nuevas simulaciones

        # Ocultar estadísticas si estaban visibles
        self.frame_stats.pack_forget()

        # Inicializar log de eventos
        self.eventos_log = []
        self._log_evento("Simulación iniciada")

        # Limpiar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Obtener valores de sensibilidad
        demanda_multiplier = float(self.scale_demanda.get())
        servicio_multiplier = float(self.scale_servicio.get())

        # Generar datos con configuración de la interfaz
        generador = GeneradorDatos()
        num_cajeros = int(self.spin_cajeros.get())
        num_clientes_base = int(self.spin_clientes.get())
        posicion_express = self.combo_posicion.get()

        # Aplicar multiplicador de demanda
        num_clientes = int(num_clientes_base * demanda_multiplier)

        cajeros = generador.generarCajeros(num_cajeros, servicio_multiplier)

        # Determinar posición de la caja express
        posicion_express_idx = None
        if posicion_express == "primera":
            posicion_express_idx = 0
        elif posicion_express == "medio":
            posicion_express_idx = num_cajeros // 2  # Posición central
        elif posicion_express == "ultima":
            posicion_express_idx = num_cajeros - 1
        elif posicion_express == "aleatoria":
            posicion_express_idx = random.randint(0, num_cajeros - 1)

        # Crear cajas con configuración
        self.cajas = []
        for i in range(num_cajeros):
            es_express = (i == posicion_express_idx)
            caja = Caja(idCaja=i+1, cajero=cajeros[i], esExpress=es_express)
            self.cajas.append(caja)

        # Generar y asignar clientes aleatoriamente (sin preferencia por express)
        clientes = generador.generaClientes(num_clientes)
        for cliente in clientes:
            asignado = False
            cajas_disponibles = self.cajas.copy()  # Copia de todas las cajas

            # Intentar asignar a cualquier caja disponible aleatoriamente
            while not asignado and cajas_disponibles:
                caja_aleatoria = random.choice(cajas_disponibles)
                if caja_aleatoria.agregarCliente(cliente):
                    asignado = True
                else:
                    # Si no se pudo asignar, remover de la lista para evitar loop infinito
                    cajas_disponibles.remove(caja_aleatoria)

        # Calcular tiempos
        for caja in self.cajas:
            caja.calcularTiempoAtencion()

        self.dibujar_cajas_grid()

        # Configurar velocidad de animación
        self.velocidad_animacion = int(self.spin_velocidad.get())

        # Iniciar animación
        self.animacion_activa = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.animar_atencion()
    
    def dibujar_cajas_grid(self):
        """Dibuja las cajas en formato grid compacto (2x3)"""
        
        for idx, caja in enumerate(self.cajas):
            # Calcular posición en grid
            if idx < 3:
                fila = 0
                columna = idx
            else:
                fila = 1
                columna = idx - 3
            
            color_bg = "#e8f5e9" if caja.esExpress else "#e3f2fd"
            color_border = "#4caf50" if caja.esExpress else "#2196f3"
            
            # Frame de la caja 
            frame_caja = tk.Frame(
                self.frame_principal,
                bg=color_bg,
                relief=tk.RAISED,
                borderwidth=2,
                highlightbackground=color_border,
                highlightthickness=2
            )
            frame_caja.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")
            
            # Configurar peso de columnas y filas para distribución uniforme
            self.frame_principal.grid_columnconfigure(columna, weight=1)
            self.frame_principal.grid_rowconfigure(fila, weight=1)
            
            # Encabezado de la caja 
            frame_header = tk.Frame(frame_caja, bg=color_border)
            frame_header.pack(fill=tk.X)
            
            tipo_caja = "🏃 EXPRESS" if caja.esExpress else f"🛒 CAJA {caja.idCaja}"
            tk.Label(
                frame_header,
                text=tipo_caja,
                font=("Arial", 11, "bold"),
                bg=color_border,
                fg="white"
            ).pack(pady=3)
            
            # Info del cajero y tiempo en una línea
            experiencia = "⭐" if caja.cajero.experiencia else "🔰"
            tiempo_inicial = sum(
                (c.numeroArticulos * caja.cajero.tiempoEscaneoPorArticulo + caja.cajero.tiempoCobro)
                for c in caja.filaClientes
            )
            
            info_text = f"{experiencia} | ⏱️ {tiempo_inicial:.0f}s | 👥 {len(caja.filaClientes)}"
            tk.Label(
                frame_header,
                text=info_text,
                font=("Arial", 8),
                bg=color_border,
                fg="white"
            ).pack(pady=2)
            
            # Frame para cajero y fila 
            frame_contenido = tk.Frame(frame_caja, bg=color_bg)
            frame_contenido.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Cajero 
            frame_cajero = tk.Frame(frame_contenido, bg=color_bg)
            frame_cajero.pack(side=tk.LEFT)
            
            if self.imagenes_cargadas and self.img_cajero:
                tk.Label(frame_cajero, image=self.img_cajero, bg=color_bg).pack()
            else:
                tk.Label(
                    frame_cajero,
                    text="👨‍💼",
                    font=("Arial", 20),
                    bg=color_bg
                ).pack()
            
            tk.Label(
                frame_cajero,
                text=f"{caja.cajero.tiempoEscaneoPorArticulo}s\n{caja.cajero.tiempoCobro}s",
                font=("Arial", 7),
                bg=color_bg
            ).pack()
            
            # Separador
            tk.Frame(frame_contenido, bg=color_border, width=2).pack(side=tk.LEFT, fill=tk.Y, padx=3)
            
            # Fila de clientes con Canvas y Scrollbar horizontal
            frame_fila_container = tk.Frame(frame_contenido, bg=color_bg)
            frame_fila_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Canvas para scroll horizontal de clientes
            canvas_clientes = tk.Canvas(
                frame_fila_container, 
                bg=color_bg, 
                height=80,
                highlightthickness=0
            )
            scrollbar_h = ttk.Scrollbar(
                frame_fila_container, 
                orient=tk.HORIZONTAL, 
                command=canvas_clientes.xview
            )
            
            frame_clientes = tk.Frame(canvas_clientes, bg=color_bg)
            frame_clientes.caja_id = idx
            
            frame_clientes.bind(
                "<Configure>",
                lambda e, canvas=canvas_clientes: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas_clientes.create_window((0, 0), window=frame_clientes, anchor="nw")
            canvas_clientes.configure(xscrollcommand=scrollbar_h.set)
            
            canvas_clientes.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            if len(caja.filaClientes) > 6:  # Mostrar scrollbar solo si hay muchos clientes
                scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
            
            self.dibujar_clientes(frame_clientes, caja.filaClientes)
    
    def dibujar_clientes(self, frame_clientes, clientes):
        """Dibuja los clientes en la fila (versión compacta)"""
        # Limpiar clientes existentes
        for widget in frame_clientes.winfo_children():
            widget.destroy()
        
        # Dibujar nuevos clientes 
        for idx, cliente in enumerate(clientes):
            frame_cliente = tk.Frame(
                frame_clientes, 
                bg="#ffffff", 
                relief=tk.RAISED, 
                borderwidth=1
            )
            frame_cliente.pack(side=tk.LEFT, padx=2, pady=2)
            
            if self.imagenes_cargadas and self.img_cliente:
                tk.Label(frame_cliente, image=self.img_cliente, bg="#ffffff").pack(padx=2, pady=2)
            else:
                tk.Label(
                    frame_cliente,
                    text="👤",
                    font=("Arial", 16),
                    bg="#ffffff"
                ).pack(padx=2, pady=2)
            
            tk.Label(
                frame_cliente,
                text=f"{cliente.numeroArticulos}",
                font=("Arial", 7, "bold"),
                bg="#ffffff"
            ).pack(padx=2)
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas finales de la simulación con tiempos totales y COSTOS incluyendo penalización SLA"""
        if not self.cajas:
            return

        # Calcular tiempos reales basados en la configuración inicial
        tiempos_reales = []
        for caja in self.cajas:
            tiempo_total = caja.tiempoAtencionTotal
            tiempos_reales.append((caja, tiempo_total))

        tiempos_reales.sort(key=lambda x: x[1])
        caja_mas_rapida = tiempos_reales[0][0]
        caja_mas_lenta = tiempos_reales[-1][0]

        # Encontrar caja express
        caja_express = next((c for c in self.cajas if c.esExpress), None)

        # Calcular COSTOS TOTALES incluyendo PENALIZACIÓN SLA
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from simulation.simulation import Costos

            # Crear lista de TODOS los clientes atendidos (simulando finalización)
            todos_los_clientes = []
            for caja in self.cajas:
                # Para estadísticas finales, asumir que todos los clientes fueron atendidos
                # Usar los clientes que estaban en las filas al final
                todos_los_clientes.extend(caja.filaClientes)

            if todos_los_clientes:
                calculador_costos = Costos(
                    c_caja_min=2.0,
                    c_espera_min=0.5,
                    c_sla_penalizacion=10.0,
                    sla_tiempo_limite_seg=480,
                    sla_objetivo_porcentaje=80
                )

                costos_dict = calculador_costos.calcular_costos_simulacion(self.cajas, todos_los_clientes)

                costo_total = costos_dict['costo_total_usd']
                costo_cajas = costos_dict['costo_cajas_usd']
                costo_espera = costos_dict['costo_espera_usd']
                costo_sla = costos_dict['costo_sla_usd']  # <-- PENALIZACIÓN SLA
                sla_actual = costos_dict['sla_actual_porcentaje']

                # Mostrar costos incluyendo penalización
                stats_text = f" RESULTADOS: ✅ Simulación completada | "
                stats_text += f"💰 COSTO TOTAL: ${costo_total:.2f} | "
                stats_text += f"🏪 Cajas: ${costo_cajas:.2f} | "
                stats_text += f"⏱️ Espera: ${costo_espera:.2f} | "
                stats_text += f"⚠️ SLA Penalización: ${costo_sla:.2f} | "  # <-- PENALIZACIÓN MOSTRADA
                stats_text += f"📊 SLA: {sla_actual:.1f}% | "
            else:
                # Sin clientes para calcular costos
                stats_text = f" RESULTADOS: ✅ Simulación completada | "
        except Exception as e:
            # Fallback si hay error en cálculo de costos
            stats_text = f" RESULTADOS: ✅ Simulación completada | "
            print(f"Error calculando costos: {e}")

        # Agregar info de cajas
        stats_text += f" Más rápida: Caja {caja_mas_rapida.idCaja} ({caja_mas_rapida.tiempoAtencionTotal:.0f}s) | "
        stats_text += f" Más lenta: Caja {caja_mas_lenta.idCaja} ({caja_mas_lenta.tiempoAtencionTotal:.0f}s) | "

        # Agregar tiempos de TODAS las cajas
        stats_text += "Tiempos finales: "
        tiempos_cajas = []
        for caja in self.cajas:
            tipo = "E" if caja.esExpress else "N"
            tiempos_cajas.append(f"C{caja.idCaja}{tipo}:{caja.tiempoAtencionTotal:.0f}s")
        stats_text += " | ".join(tiempos_cajas)

        if caja_express:
            # Comparar con promedio de cajas normales
            cajas_normales = [c for c in self.cajas if not c.esExpress]
            if cajas_normales:
                promedio_normales = sum(c.tiempoAtencionTotal for c in cajas_normales) / len(cajas_normales)
                diferencia = caja_express.tiempoAtencionTotal - promedio_normales

        self.label_stats.config(text=stats_text)
        self.frame_stats.pack(fill=tk.X, padx=5, pady=5)
    
    def detener_animacion(self):
        """Detiene la animación"""
        self.animacion_activa = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
    
    def animar_atencion(self):
        """Anima la atención de un cliente en cada caja y monitorea SLA para apertura automática"""
        if not self.animacion_activa:
            return

        # Verificar si quedan clientes
        hay_clientes = any(len(caja.filaClientes) > 0 for caja in self.cajas)

        if not hay_clientes:
            self.detener_animacion()
            self.mostrar_estadisticas()
            return

        # Monitorear SLA y abrir cajas automáticamente si es necesario
        self.evaluar_apertura_automatica_dinamica()

        # Atender un cliente en cada caja que tenga fila
        for caja in self.cajas:
            if len(caja.filaClientes) > 0:
                # Remover el primer cliente
                caja.filaClientes.pop(0)
                # Recalcular tiempo de atención después de remover cliente
                caja.calcularTiempoAtencion()

        # Redibujar todas las cajas
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        self.dibujar_cajas_grid()

        # Programar siguiente animación
        self.root.after(self.velocidad_animacion, self.animar_atencion)

    def cambiar_escenario(self, event=None):
        """Cambia los valores de sensibilidad según el escenario seleccionado"""
        escenario = self.combo_sensibilidad.get()

        if escenario == "Normal":
            self.frame_avanzado.pack_forget()  # Ocultar controles avanzados
            self.scale_demanda.set(1.0)
            self.scale_servicio.set(1.0)
        else:
            # Mostrar controles avanzados para escenarios personalizados
            self.frame_avanzado.pack(side=tk.LEFT, padx=2)
            if escenario == "Baja Demanda":
                self.scale_demanda.set(0.7)
                self.scale_servicio.set(1.0)
            elif escenario == "Alta Demanda":
                self.scale_demanda.set(1.5)
                self.scale_servicio.set(1.0)
            elif escenario == "Servicio Lento":
                self.scale_demanda.set(1.0)
                self.scale_servicio.set(0.7)
            elif escenario == "Servicio Rápido":
                self.scale_demanda.set(1.0)
                self.scale_servicio.set(1.5)

    def evaluar_apertura_automatica(self):
        """Evalúa automáticamente si se debe abrir una nueva caja usando las reglas del backend"""
        if not self.cajas:
            return

        # Usar la misma lógica del backend para calcular costos y SLA
        try:
            # Importar Costos del backend
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from simulation.simulation import Costos

            # Calcular costos usando la clase Costos (misma lógica del backend)
            calculador_costos = Costos(
                c_caja_min=2.0,
                c_espera_min=0.5,
                c_sla_penalizacion=10.0,
                sla_tiempo_limite_seg=480,
                sla_objetivo_porcentaje=80
            )

            # Crear lista de clientes para el cálculo
            todos_los_clientes = []
            for caja in self.cajas:
                todos_los_clientes.extend(caja.filaClientes)

            if not todos_los_clientes:
                return

            costos_dict = calculador_costos.calcular_costos_simulacion(self.cajas, todos_los_clientes)

            # Aplicar reglas de apertura basadas en evidencia experimental
            num_cajas_actual = len(self.cajas)
            sla_actual = costos_dict['sla_actual_porcentaje']

            # Regla 1: Mantener al menos 4 cajas (basado en experimentos)
            if num_cajas_actual < 4:
                self._agregar_caja_automatica("Regla 1: Mínimo 4 cajas requeridas")
                return

            # Regla 2: Abrir si SLA < 85% (umbral óptimo encontrado en experimentos)
            if sla_actual < 85.0:
                # Calcular costo marginal estimado (basado en análisis de sensibilidad)
                # Costo adicional de una caja: c_caja * tiempo_promedio
                tiempo_promedio_operacion = sum(caja.tiempoAtencionTotal for caja in self.cajas) / len(self.cajas)
                costo_marginal = 2.0 * (tiempo_promedio_operacion / 60.0)  # $2/min * tiempo en minutos

                if costo_marginal <= 50.0:  # Límite establecido en reglas
                    self._agregar_caja_automatica(f"Regla 2: SLA {sla_actual:.1f}% < 85% (Costo marginal: ${costo_marginal:.1f})")
                    return

            # Regla 3: Demanda alta con cajas insuficientes
            total_clientes = len(todos_los_clientes)
            demanda_alta = total_clientes > 30  # Umbral basado en experimentos
            if demanda_alta and num_cajas_actual < 6:  # Máximo óptimo encontrado
                self._agregar_caja_automatica(f"Regla 3: Demanda alta ({total_clientes} clientes) con {num_cajas_actual} cajas")
                return

        except Exception as e:
            # Si hay error en el cálculo, usar lógica simplificada
            print(f"Error en evaluación automática: {e}. Usando lógica simplificada.")

            total_clientes = sum(len(caja.filaClientes) for caja in self.cajas)
            if total_clientes > 40 and len(self.cajas) < 6:  # Lógica básica de respaldo
                self._agregar_caja_automatica("Lógica simplificada: Alta demanda detectada")

    def evaluar_apertura_automatica_dinamica(self):
        """Evalúa apertura automática durante la animación con reglas del backend"""
        if not self.cajas:
            return

        # Solo evaluar cada 5 pasos para evitar apertura excesiva
        if not hasattr(self, '_pasos_sin_evaluar'):
            self._pasos_sin_evaluar = 0
        self._pasos_sin_evaluar += 1

        if self._pasos_sin_evaluar < 5:  # Evaluar cada 5 pasos
            return
        self._pasos_sin_evaluar = 0

        try:
            # Importar Costos del backend
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from simulation.simulation import Costos

            # Calcular costos usando la MISMA lógica del backend
            calculador_costos = Costos(
                c_caja_min=2.0,
                c_espera_min=0.5,
                c_sla_penalizacion=10.0,
                sla_tiempo_limite_seg=480,
                sla_objetivo_porcentaje=80
            )

            # Crear lista de clientes para el cálculo
            todos_los_clientes = []
            for caja in self.cajas:
                todos_los_clientes.extend(caja.filaClientes)

            # Solo evaluar si hay suficientes clientes (al menos 5)
            if len(todos_los_clientes) < 5:
                return

            costos_dict = calculador_costos.calcular_costos_simulacion(self.cajas, todos_los_clientes)

            # Aplicar reglas del backend: SLA < 85% Y costo marginal ≤ $50
            sla_actual = costos_dict['sla_actual_porcentaje']
            costo_sla_actual = costos_dict['costo_sla_usd']  # <-- PENALIZACIÓN ACTUAL

            if sla_actual < 85.0:
                # Calcular costo marginal (como en backend)
                tiempo_promedio_operacion = sum(caja.tiempoAtencionTotal for caja in self.cajas) / len(self.cajas)
                costo_marginal = 2.0 * (tiempo_promedio_operacion / 60.0)  # $2/min * minutos

                # Umbral estricto: máximo $50
                if costo_marginal <= 50.0:
                    self._agregar_caja_automatica_dinamica(
                        f"SLA {sla_actual:.1f}% < 85% (Penalización actual: ${costo_sla_actual:.1f}) - Costo marginal: ${costo_marginal:.1f} ≤ $50"
                    )
                    return

        except Exception as e:
            # Silencioso en caso de error
            pass

    def _agregar_caja_automatica_dinamica(self, razon):
        """Agrega una caja automáticamente durante la animación - NUEVAS CAJAS SIEMPRE SON NORMALES"""
        if len(self.cajas) >= 8:
            return

        num_cajeros = len(self.cajas) + 1

        # Crear cajero
        generador = GeneradorDatos()
        servicio_multiplier = float(self.scale_servicio.get())
        cajeros = generador.generarCajeros(1, servicio_multiplier)

        # NUEVAS CAJAS DINÁMICAS SIEMPRE SON NORMALES (no express)
        # Solo la caja originalmente configurada como express lo es
        es_express = False

        nueva_caja = Caja(idCaja=num_cajeros, cajero=cajeros[0], esExpress=es_express)
        self.cajas.append(nueva_caja)

        # Redistribuir algunos clientes a la nueva caja
        self._redistribuir_clientes_nueva_caja()

        # Recalcular tiempos de atención para todas las cajas después de redistribución
        for caja in self.cajas:
            caja.calcularTiempoAtencion()

        # Log del evento
        self._log_evento(f"➕ Caja {num_cajeros} abierta: {razon}")

    def _redistribuir_clientes_nueva_caja(self):
        """Redistribuye clientes a la nueva caja para balancear carga"""
        if len(self.cajas) < 2:
            return

        nueva_caja = self.cajas[-1]  # Última caja agregada
        clientes_redistribuidos = 0

        # Mover algunos clientes de cajas congestionadas
        for caja in self.cajas[:-1]:  # Todas menos la nueva
            if len(caja.filaClientes) > 3:  # Si tiene más de 3 clientes
                # Mover 1-2 clientes
                num_mover = min(2, len(caja.filaClientes) // 2)
                for _ in range(num_mover):
                    if caja.filaClientes:
                        cliente = caja.filaClientes.pop()  # Mover del final
                        nueva_caja.agregarCliente(cliente)
                        clientes_redistribuidos += 1

        if clientes_redistribuidos > 0:
            self._log_evento(f"🔄 {clientes_redistribuidos} clientes redistribuidos a nueva caja")

    def _log_evento(self, mensaje):
        """Registra un evento en el log sin timestamp"""
        self.eventos_log.append(mensaje)

        # Mantener solo los últimos 6 eventos para mejor organización
        if len(self.eventos_log) > 6:
            self.eventos_log = self.eventos_log[-6:]

        # Actualizar display con mejor formato
        if len(self.eventos_log) <= 3:
            # Para pocos eventos, mostrar en una línea
            eventos_texto = " • ".join(self.eventos_log)
        else:
            # Para más eventos, mostrar en dos líneas
            mitad = len(self.eventos_log) // 2
            linea1 = " • ".join(self.eventos_log[:mitad])
            linea2 = " • ".join(self.eventos_log[mitad:])
            eventos_texto = f"{linea1}\n{linea2}"

        self.label_eventos.config(text=f"📋 EVENTOS:\n{eventos_texto}")

    def _agregar_caja_automatica(self, razon):
        """Agrega una nueva caja al sistema automáticamente"""
        if len(self.cajas) >= 8:  # Límite máximo
            return  # Silencioso para apertura automática

        # Crear nueva caja
        num_cajeros = len(self.cajas) + 1
        posicion_express = self.combo_posicion.get()

        # Determinar si la nueva caja es express
        if posicion_express == "ultima":
            es_express = (len(self.cajas) == num_cajeros - 1)  # La última es express
        else:
            es_express = False  # Por simplicidad, nuevas cajas son normales

        # Crear cajero para la nueva caja
        generador = GeneradorDatos()
        servicio_multiplier = float(self.scale_servicio.get())
        cajeros = generador.generarCajeros(1, servicio_multiplier)
        nueva_caja = Caja(idCaja=num_cajeros, cajero=cajeros[0], esExpress=es_express)

        self.cajas.append(nueva_caja)

        # Mostrar notificación de apertura automática
        print(f"🔄 Caja {num_cajeros} abierta automáticamente: {razon}")

    def abrir_nueva_caja(self):
        """Evalúa manualmente si se debe abrir una nueva caja (para uso del botón)"""
        if not self.cajas:
            return

        # Usar la misma lógica automática pero mostrar resultados
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from simulation.simulation import Costos

            calculador_costos = Costos(
                c_caja_min=2.0, c_espera_min=0.5, c_sla_penalizacion=10.0,
                sla_tiempo_limite_seg=480, sla_objetivo_porcentaje=80
            )

            todos_los_clientes = []
            for caja in self.cajas:
                todos_los_clientes.extend(caja.filaClientes)

            if not todos_los_clientes:
                self.mostrar_mensaje("Sin clientes", "No hay clientes para evaluar")
                return

            costos_dict = calculador_costos.calcular_costos_simulacion(self.cajas, todos_los_clientes)

            num_cajas_actual = len(self.cajas)
            sla_actual = costos_dict['sla_actual_porcentaje']
            costo_sla_actual = costos_dict['costo_sla_usd']  # <-- PENALIZACIÓN ACTUAL
            total_clientes = len(todos_los_clientes)

            # Evaluar reglas
            if num_cajas_actual < 4:
                self._agregar_caja_automatica("Regla 1: Mínimo 4 cajas requeridas")
                self.dibujar_cajas_grid()
                self.mostrar_mensaje("Caja abierta", "Regla 1: Mínimo 4 cajas requeridas")
            elif sla_actual < 85.0:
                tiempo_promedio_operacion = sum(caja.tiempoAtencionTotal for caja in self.cajas) / len(self.cajas)
                costo_marginal = 2.0 * (tiempo_promedio_operacion / 60.0)
                if costo_marginal <= 50.0:
                    self._agregar_caja_automatica(f"Regla 2: SLA {sla_actual:.1f}% < 85% (Penalización: ${costo_sla_actual:.1f})")
                    self.dibujar_cajas_grid()
                    self.mostrar_mensaje("Caja abierta", f"SLA {sla_actual:.1f}% < 85%\nPenalización actual: ${costo_sla_actual:.1f}\nCosto marginal: ${costo_marginal:.1f}")
                else:
                    self.mostrar_mensaje("No abrir caja", f"SLA {sla_actual:.1f}% < 85% (Penalización: ${costo_sla_actual:.1f})\npero costo marginal ${costo_marginal:.1f} > $50")
            elif total_clientes > 30 and num_cajas_actual < 6:
                self._agregar_caja_automatica(f"Regla 3: Demanda alta ({total_clientes} clientes)")
                self.dibujar_cajas_grid()
                self.mostrar_mensaje("Caja abierta", f"Demanda alta: {total_clientes} clientes")
            else:
                self.mostrar_mensaje("Condiciones óptimas", f"SLA: {sla_actual:.1f}% (Penalización: ${costo_sla_actual:.1f})\nCajas: {num_cajas_actual}\nClientes: {total_clientes}")

        except Exception as e:
            self.mostrar_mensaje("Error", f"Error en evaluación: {str(e)}")

    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un mensaje informativo"""
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("300x150")
        popup.configure(bg="#34495e")
        popup.transient(self.root)

        label = tk.Label(popup, text=mensaje, font=("Arial", 10),
                        bg="#34495e", fg="white", justify=tk.CENTER)
        label.pack(pady=20, padx=20)

        btn_ok = tk.Button(popup, text="OK", command=popup.destroy,
                          bg="#27ae60", fg="white", font=("Arial", 9, "bold"))
        btn_ok.pack(pady=5)



def iniciar_interfaz_con_datos(cajas, clientes):
    """Función para iniciar la interfaz gráfica con datos precalculados"""
    root = tk.Tk()
    app = SupermercadoGUI(root, cajas_precalculadas=cajas, clientes_precalculados=clientes)
    root.mainloop()

def iniciar_interfaz():
    """Función para iniciar la interfaz gráfica independiente"""
    root = tk.Tk()
    app = SupermercadoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()