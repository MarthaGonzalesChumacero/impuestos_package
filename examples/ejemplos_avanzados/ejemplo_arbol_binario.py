from impuestos_package.calculadora import CalculadoraDeuda

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

# Nodo para el árbol binario
class Nodo:
    """Nodo de un árbol binario simple."""
    def __init__(self, valor):
        self.valor = valor
        self.izq = None  # Hijo izquierdo
        self.der = None  # Hijo derecho

    def __repr__(self):
        return f"Nodo({self.valor})"


# Árbol Binario para representar las tareas
class ArbolDeuda:
    """Árbol Binario para almacenar tareas de contribuyentes y cálculos"""
    
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        """Inserta un nuevo nodo en el árbol binario."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_rec(self.raiz, valor)

    def _insertar_rec(self, nodo, valor):
        """Inserción recursiva en el árbol binario (por valor alfabético o numérico)."""
        if valor['nombre'] < nodo.valor['nombre']:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar_rec(nodo.izq, valor)
        else:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar_rec(nodo.der, valor)

    def preorden(self, nodo=None):
        """Recorrido en preorden (raíz → izquierda → derecha)."""
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return  # Árbol vacío, salir
        print(f"Procesando {nodo.valor['nombre']}")
        # Configurar datos del contribuyente
        calc = CalculadoraDeuda(
            TO=nodo.valor['TO'],
            fecha_inicio=nodo.valor['fecha_inicio'],
            fecha_fin=nodo.valor['fecha_fin'],
            tasa=nodo.valor['tasa'],
            dias=nodo.valor['dias'],
            porcentaje=nodo.valor['porcentaje']
        )
        # Ejecutar cálculo
        resultado = calc.calcular()
        print("Resultado del cálculo:")
        for k, v in resultado.items():
            print(f"{k}: {v}")
        
        # Llamar recursivamente a los hijos izquierdo y derecho
        if nodo.izq:
            self.preorden(nodo.izq)
        if nodo.der:
            self.preorden(nodo.der)

    def mostrar_arbol(self, nodo=None, prefijo="", es_izquierdo=True):
        """Mostrar el árbol binario en formato jerárquico."""
        if nodo is None:
            nodo = self.raiz
        if nodo is not None:
            print(prefijo + ("└── " if es_izquierdo else "├── ") + str(nodo.valor['nombre']))
            if nodo.izq or nodo.der:
                if nodo.izq:
                    self.mostrar_arbol(nodo.izq, prefijo + ("    " if es_izquierdo else "│   "), True)
                if nodo.der:
                    self.mostrar_arbol(nodo.der, prefijo + ("    " if es_izquierdo else "│   "), False)


def main():
    # Lista de contribuyentes con sus datos personalizados
    contribuyentes = [
        {"nombre": "Contribuyente A", "TO": 1500, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 6, "dias": 180, "porcentaje": 15},
        {"nombre": "Contribuyente B", "TO": 2000, "fecha_inicio": "2025-06-01", "fecha_fin": "2025-11-10", "tasa": 6, "dias": 150, "porcentaje": 10},
        {"nombre": "Contribuyente C", "TO": 1200, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 5, "dias": 200, "porcentaje": 20}
    ]

    # Crear instancia del árbol de deuda
    arbol_deuda = ArbolDeuda()

    # Insertar contribuyentes en el árbol
    for contribuyente in contribuyentes:
        arbol_deuda.insertar(contribuyente)

    # Mostrar la estructura jerárquica del árbol
    print("\nEstructura jerárquica del árbol de deuda:")
    arbol_deuda.mostrar_arbol()

    # Procesar los cálculos en preorden
    print("\nProcesando cálculos pendientes en preorden...")
    arbol_deuda.preorden()  # Recorrido en preorden para procesar cada contribuyente

if __name__ == "__main__":
    main()
