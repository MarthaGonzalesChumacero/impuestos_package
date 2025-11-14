import logging
from datetime import datetime  # Importamos datetime para trabajar con fechas
from .mv import MantenimientoValor
from .interes import Interes
from .sancion import Sancion
from .ufv import BCBAPIUFV, UFVFetchError
from .estructuras import Pila, Cola, ArbolDeuda, Nodo

logger = logging.getLogger(__name__)

class CalculadoraDeuda:
    def __init__(self, TO: float, fecha_inicio: str, fecha_fin: str, tasa: float, dias: int, porcentaje: float):
        self.TO = TO
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tasa = tasa
        self.dias = dias
        self.porcentaje = porcentaje

        # Validaciones básicas
        if TO < 0 or dias < 0 or porcentaje < 0:
            raise ValueError("Los parámetros no pueden ser negativos.")
        
        # Estructuras de datos
        self.historial = Pila()
        self.cola_calculos = Cola()
        self.arbol_deuda = ArbolDeuda()

        # Fecha actual para registrar el cálculo
        self.fecha_calculo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
        self.historial.push(f"[Inicio] Cálculo inicializado con TO={TO} en {self.fecha_calculo}")

    def _obtener_ufvs(self):
        """Obtiene los valores UFV para el rango de fechas."""
        api = BCBAPIUFV()
        try:
            datos = api.consumir_endpoint(self.fecha_inicio, self.fecha_fin)
            ufv_venc = api._parse_valor(datos[0])
            ufv_pago = api._parse_valor(datos[-1])
            if not ufv_venc or not ufv_pago:
                raise UFVFetchError("Valores UFV inválidos para las fechas especificadas.")
            return ufv_venc, ufv_pago
        except UFVFetchError as e:
            logger.error(f"Error al obtener UFVs: {str(e)}")
            return None, None

    def calcular(self):
        """Ejecuta el cálculo completo e integra las estructuras de datos."""
        try:
            ufv_venc, ufv_pago = self._obtener_ufvs()
            if ufv_venc is None or ufv_pago is None:
                return {"error": "No se pudieron obtener los valores de UFV correctamente."}
            
            # Cálculos
            mv = MantenimientoValor(self.TO, ufv_pago, ufv_venc).calcular()
            i = Interes(self.TO, mv, self.tasa, self.dias).calcular()
            s = Sancion(self.TO, self.porcentaje).calcular()
            dt = self.TO + mv + i + s

            # Registrar en el historial con la fecha del cálculo
            self.historial.push(f"[Resultado] MV = {mv} en {self.fecha_calculo}")
            self.historial.push(f"[Resultado] I = {i} en {self.fecha_calculo}")
            self.historial.push(f"[Resultado] S = {s} en {self.fecha_calculo}")
            self.historial.push(f"[Final] Deuda Total (DT) = {dt} en {self.fecha_calculo}")

            # Construcción jerárquica con árbol de deuda
            self._construir_arbol_deuda()

            return {"TO": round(self.TO, 2), "MV": mv, "I": i, "S": s, "DT": round(dt, 2), "Fecha de Cálculo": self.fecha_calculo}
        
        except Exception as e:
            logger.error(f"Error en el cálculo: {str(e)}")
            return {"error": str(e)}

    def _construir_arbol_deuda(self):
        """Construye el árbol de jerarquía tributaria (TO → MV → Interés → Sanción)."""
        raiz = Nodo("Tributo Omitido")
        raiz.izq = Nodo("Mantenimiento de Valor")
        raiz.izq.izq = Nodo("Interés")
        raiz.izq.izq.izq = Nodo("Sanción")
        self.arbol_deuda.raiz = raiz

    def mostrar_arbol_deuda(self):
        """Muestra visualmente la jerarquía del cálculo tributario."""
        print("\n🌳 Estructura jerárquica de la deuda tributaria:")
        self.arbol_deuda.mostrar_arbol()

    def mostrar_historial(self):
        """Muestra los pasos guardados en la pila (historial de cálculo)."""
        print("\nHistorial de cálculo:")
        for paso in self.historial.items:
            print(" -", paso)

    def agregar_a_cola(self, descripcion):
        """Agrega una tarea de cálculo pendiente a la cola."""
        self.cola_calculos.encolar(descripcion)
        print(f"Cálculo agregado a la cola: {descripcion}")

    def procesar_cola(self):
        """Procesa todos los cálculos pendientes en la cola."""
        print("\nProcesando cálculos pendientes...")
        while not self.cola_calculos.esta_vacia():
            tarea = self.cola_calculos.desencolar()
            print(f"Procesado: {tarea}")
            resultado = self.calcular()  # Llamamos al método de cálculo
            print("Resultado del cálculo:")
            for k, v in resultado.items():
                print(f"{k}: {v}")
