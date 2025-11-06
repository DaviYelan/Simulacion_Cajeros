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

        # Limpiar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Generar datos con configuración de la interfaz
        generador = GeneradorDatos()
        num_cajeros = int(self.spin_cajeros.get())
        num_clientes = int(self.spin_clientes.get())
        posicion_express = self.combo_posicion.get()

        cajeros = generador.generarCajeros(num_cajeros)

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

        # Generar y asignar clientes de manera aleatoria
        clientes = generador.generaClientes(num_clientes)
        for cliente in clientes:
            asignado = False

            # Determinar cajas válidas para el cliente
            if cliente.numeroArticulos <= 10:
                # Cliente puede usar cualquier caja (express o normal)
                cajas_validas = self.cajas
            else:
                # Cliente solo puede usar cajas normales
                cajas_validas = [caja for caja in self.cajas if not caja.esExpress]

            # Intentar asignar a una caja aleatoria de las válidas
            intentos = 0
            while not asignado and cajas_validas and intentos < 100:
                caja_aleatoria = random.choice(cajas_validas)
                if caja_aleatoria.agregarCliente(cliente):
                    asignado = True
                else:
                    # Si no se pudo asignar, remover de la lista para evitar loop infinito
                    cajas_validas.remove(caja_aleatoria)
                intentos += 1

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
        """Muestra las estadísticas finales de la simulación con tiempos totales de todas las cajas"""
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

        # Crear texto con tiempos de TODAS las cajas
        stats_text = f" RESULTADOS: ✅ Simulación completada | "
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
        """Anima la atención de un cliente en cada caja"""
        if not self.animacion_activa:
            return
        
        # Verificar si quedan clientes
        hay_clientes = any(len(caja.filaClientes) > 0 for caja in self.cajas)
        
        if not hay_clientes:
            self.detener_animacion()
            self.mostrar_estadisticas()
            return
        
        # Atender un cliente en cada caja que tenga fila
        for caja in self.cajas:
            if len(caja.filaClientes) > 0:
                # Remover el primer cliente
                caja.filaClientes.pop(0)
        
        # Redibujar todas las cajas
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        self.dibujar_cajas_grid()
        
        # Programar siguiente animación
        self.root.after(self.velocidad_animacion, self.animar_atencion)


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