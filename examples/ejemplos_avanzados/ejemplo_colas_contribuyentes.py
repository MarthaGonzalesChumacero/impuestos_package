from datetime import datetime

# --- DummyAPI con las UFV reales 2025-01-01 → 2025-06-01 y 2025-06-01 → 2025-11-10 ---
class DummyAPI:
    def _parse_valor(self, item):
        return float(item["valor"]) if float(item["valor"]) > 0 else None

    def consumir_endpoint(self, fi, ff, timeout=10):
        # UFV simulados para las fechas solicitadas
        if fi == "2025-01-01" and ff == "2025-06-01":
            return [{"valor": "2.73596"}, {"valor": "2.96361"}]
        elif fi == "2025-06-01" and ff == "2025-11-10":
            return [{"valor": "2.96361"}, {"valor": "3.04512"}]
        return [{"valor": "2.73596"}, {"valor": "2.96361"}]  # Default if not specified

import impuestos_package.calculadora as calc_mod
calc_mod.BCBAPIUFV = DummyAPI
# -------------------------------------------------------------

# --- Estructuras de Datos ---

# Pila para almacenar los cálculos realizados
class Pila:
    """Implementación de una pila para almacenar el historial de cálculos."""
    def __init__(self):
        self.items = []

    def push(self, item):
        """Agrega un elemento a la pila."""
        self.items.append(item)

    def pop(self):
        """Elimina y retorna el elemento superior de la pila."""
        if not self.esta_vacia():
            return self.items.pop()
        return None

    def esta_vacia(self):
        """Verifica si la pila está vacía."""
        return len(self.items) == 0

    def mostrar_historial(self):
        """Muestra el historial de cálculos procesados."""
        print("\nHistorial de cálculos procesados (Pila):")
        for item in reversed(self.items):  # Mostrar desde el más reciente
            print(f"{item['nombre']} procesado el {item['fecha']} - Resultado: {item['resultado']}")

# Cola para almacenar los cálculos pendientes
class Cola:
    """Implementación de una cola para gestionar las tareas pendientes (FIFO)."""
    def __init__(self):
        self.items = []

    def encolar(self, item):
        """Agrega un elemento al final de la cola."""
        self.items.append(item)

    def desencolar(self):
        """Elimina y retorna el primer elemento de la cola."""
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return len(self.items) == 0

    def mostrar_historial(self):
        """Muestra el historial de cálculos procesados."""
        print("\nHistorial de cálculos procesados (Cola):")
        for item in self.items:
            print(f"{item['nombre']} procesado el {item['fecha']} - Resultado: {item['resultado']}")

# Nodo para el árbol binario
class Nodo:
    """Nodo de un árbol binario simple."""
    def __init__(self, contribuyente):
        self.contribuyente = contribuyente  # Almacenamos el diccionario del contribuyente completo
        self.izq = None  # Hijo izquierdo
        self.der = None  # Hijo derecho

    def __repr__(self):
        return f"Nodo({self.contribuyente['nombre']})"

# Árbol Binario para representar las tareas
class ArbolDeuda:
    """Árbol Binario para almacenar contribuyentes y sus cálculos"""
    
    def __init__(self):
        self.raiz = None

    def insertar(self, contribuyente):
        """Inserta un nuevo nodo en el árbol binario basado en los apellidos y nombre"""
        if self.raiz is None:
            self.raiz = Nodo(contribuyente)
        else:
            self._insertar_rec(self.raiz, contribuyente)

    def _insertar_rec(self, nodo, contribuyente):
        """Inserción recursiva en el árbol binario (por apellido paterno, materno y nombre)"""
        clave = (contribuyente['apellido_paterno'], contribuyente['apellido_materno'], contribuyente['nombre'])
        clave_nodo = (nodo.contribuyente['apellido_paterno'], nodo.contribuyente['apellido_materno'], nodo.contribuyente['nombre'])

        if clave < clave_nodo:
            if nodo.izq is None:
                nodo.izq = Nodo(contribuyente)
            else:
                self._insertar_rec(nodo.izq, contribuyente)
        else:
            if nodo.der is None:
                nodo.der = Nodo(contribuyente)
            else:
                self._insertar_rec(nodo.der, contribuyente)

    def preorden(self, nodo=None):
        """Recorrido en preorden (raíz → izquierda → derecha)"""
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return
        print(f"Procesando: {nodo.contribuyente['nombre']} {nodo.contribuyente['apellido_paterno']} {nodo.contribuyente['apellido_materno']}")
        
        # Configurar los datos específicos de cada contribuyente en la calculadora
        calc = CalculadoraDeuda(
            TO=nodo.contribuyente['TO'],
            fecha_inicio=nodo.contribuyente['fecha_inicio'],
            fecha_fin=nodo.contribuyente['fecha_fin'],
            tasa=nodo.contribuyente['tasa'],
            dias=nodo.contribuyente['dias'],
            porcentaje=nodo.contribuyente['porcentaje']
        )
        
        # Realizar el cálculo
        try:
            resultado = calc.calcular()
            print(f"Resultado del cálculo para {nodo.contribuyente['nombre']}:")
            for k, v in resultado.items():
                print(f"{k}: {v}")
        except Exception as e:
            print(f"Error al calcular para {nodo.contribuyente['nombre']}: {e}")
        
        # Recorrer recursivamente los hijos izquierdo y derecho
        if nodo.izq:
            self.preorden(nodo.izq)
        if nodo.der:
            self.preorden(nodo.der)

    def mostrar_arbol(self, nodo=None, prefijo="", es_izquierdo=True):
        """Muestra el árbol binario en formato jerárquico"""
        if nodo is None:
            nodo = self.raiz
        if nodo is not None:
            print(prefijo + ("└── " if es_izquierdo else "├── ") + f"{nodo.contribuyente['nombre']} {nodo.contribuyente['apellido_paterno']} {nodo.contribuyente['apellido_materno']}")
            if nodo.izq or nodo.der:
                if nodo.izq:
                    self.mostrar_arbol(nodo.izq, prefijo + ("    " if es_izquierdo else "│   "), True)
                if nodo.der:
                    self.mostrar_arbol(nodo.der, prefijo + ("    " if es_izquierdo else "│   "), False)

# --- CalculadoraDeuda --- (Ejemplo básico)
class CalculadoraDeuda:
    def __init__(self, TO, fecha_inicio, fecha_fin, tasa, dias, porcentaje):
        self.TO = TO
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tasa = tasa
        self.dias = dias
        self.porcentaje = porcentaje

    def calcular(self):
        # Cálculos básicos de deuda tributaria
        mv = self.TO * 0.05  # Mantenimiento de Valor (simulado)
        i = self.TO * 0.03  # Interés (simulado)
        s = self.TO * 0.1   # Sanción (simulado)
        dt = self.TO + mv + i + s  # Deuda Total
        return {"TO": self.TO, "MV": mv, "I": i, "S": s, "DT": dt}

# --- Función principal para realizar los cálculos ---
def main():
    # Lista de contribuyentes con sus datos personalizados
    contribuyentes = [
        {"nombre": "Juan", "apellido_paterno": "Perez", "apellido_materno": "Gomez", "TO": 1500, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 6, "dias": 180, "porcentaje": 15},
        {"nombre": "Maria", "apellido_paterno": "Lopez", "apellido_materno": "Martinez", "TO": 2000, "fecha_inicio": "2025-06-01", "fecha_fin": "2025-11-10", "tasa": 6, "dias": 150, "porcentaje": 10},
        {"nombre": "Carlos", "apellido_paterno": "Garcia", "apellido_materno": "Fernandez", "TO": 1200, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 5, "dias": 200, "porcentaje": 20}
    ]

    # Crear instancia de la calculadora
    calc = CalculadoraDeuda(
        TO=1500,
        fecha_inicio="2025-01-01",
        fecha_fin="2025-06-01",
        tasa=6,
        dias=180,
        porcentaje=15
    )

    # Crear una cola para almacenar las tareas
    cola_calculos = Cola()
    # Crear una pila para el historial
    historial_pila = Pila()
    # Crear una instancia del árbol binario
    arbol_deuda = ArbolDeuda()

    # Agregar tareas a la cola, pila y árbol binario
    for contribuyente in contribuyentes:
        contribuyente['fecha'] = datetime.now().strftime('%Y-%m-%d')  # Fecha actual para el historial
        cola_calculos.encolar(contribuyente)
        historial_pila.push(contribuyente)
        arbol_deuda.insertar(contribuyente)

    # Procesar los cálculos en la cola (FIFO)
    print("\nProcesando cálculos pendientes en cola (FIFO)...")
    while not cola_calculos.esta_vacia():
        contribuyente = cola_calculos.desencolar()
        calc.TO = contribuyente["TO"]
        calc.fecha_inicio = contribuyente["fecha_inicio"]
        calc.fecha_fin = contribuyente["fecha_fin"]
        calc.tasa = contribuyente["tasa"]
        calc.dias = contribuyente["dias"]
        calc.porcentaje = contribuyente["porcentaje"]
        resultado = calc.calcular()
        contribuyente['resultado'] = resultado
        print(f"Resultado de la cola para {contribuyente['nombre']}: {resultado}")

    # Mostrar el historial de cálculos procesados (pila)
    historial_pila.mostrar_historial()

    # Mostrar la estructura jerárquica del árbol
    print("\nEstructura jerárquica del árbol de deuda:")
    arbol_deuda.mostrar_arbol()

    # Procesar los cálculos en preorden (árbol)
    print("\nProcesando cálculos pendientes en árbol binario (Preorden)...")
    arbol_deuda.preorden()

if __name__ == "__main__":
    main()
