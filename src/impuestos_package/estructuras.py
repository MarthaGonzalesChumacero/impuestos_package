"""
Módulo: estructuras.py
Autor: Martha Gonzales Chumacero
Descripción:
Este módulo extiende la funcionalidad de la librería `impuestos_package`
implementando estructuras de datos clásicas (Pila, Cola y Árbol Binario)
para optimizar cálculos, auditorías y gestión de operaciones tributarias.
"""

from collections import deque

# =====================================================
# 🔹 Clase PILA (Stack)
# =====================================================

class Pila:
    """
    Implementación de una pila (estructura LIFO).
    Se utiliza para registrar el historial de operaciones o cálculos.
    """

    def __init__(self):
        self.items = []

    def push(self, item):
        """Agrega un elemento a la pila."""
        self.items.append(item)

    def pop(self):
        """Elimina el elemento superior y lo retorna."""
        return self.items.pop() if not self.esta_vacia() else None

    def cima(self):
        """Devuelve el elemento superior sin eliminarlo."""
        return self.items[-1] if not self.esta_vacia() else None

    def esta_vacia(self):
        """Verifica si la pila está vacía."""
        return len(self.items) == 0

    def tamano(self):
        """Retorna el número de elementos en la pila."""
        return len(self.items)

    def __repr__(self):
        return f"Pila({self.items})"


# =====================================================
# 🔹 Clase COLA (Queue)
# =====================================================

class Cola:
    """
    Implementación de una cola (estructura FIFO).
    Ideal para gestionar cálculos pendientes o tareas tributarias.
    """

    def __init__(self):
        self.items = deque()

    def encolar(self, item):
        """Agrega un elemento al final de la cola."""
        self.items.append(item)

    def desencolar(self):
        """Elimina y devuelve el primer elemento."""
        return self.items.popleft() if not self.esta_vacia() else None

    def frente(self):
        """Devuelve el primer elemento sin eliminarlo."""
        return self.items[0] if not self.esta_vacia() else None

    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return len(self.items) == 0

    def tamano(self):
        """Devuelve la cantidad de elementos en la cola."""
        return len(self.items)

    def __repr__(self):
        return f"Cola({list(self.items)})"


# =====================================================
# 🔹 Árbol Binario (Binary Tree)
# =====================================================

class Nodo:
    """Nodo de un árbol binario simple."""

    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

    def __repr__(self):
        return f"Nodo({self.valor})"


class ArbolDeuda:
    """
    Árbol binario para representar jerarquías de cálculo tributario.
    Ejemplo:
        Raíz → Deuda Total
        Izquierdo → Mantenimiento de Valor
        Derecho → Interés / Sanción
    """

    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        """Inserta un nuevo nodo en el árbol."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_rec(self.raiz, valor)

    def _insertar_rec(self, nodo, valor):
        """Inserción recursiva (por orden alfabético o numérico)."""
        if valor < nodo.valor:
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
        print(nodo.valor)
        if nodo.izq:
            self.preorden(nodo.izq)
        if nodo.der:
            self.preorden(nodo.der)

    def buscar(self, valor):
        """Busca un valor dentro del árbol."""
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izq, valor)
        else:
            return self._buscar_rec(nodo.der, valor)

    def mostrar_arbol(self, nodo=None, prefijo="", es_izquierdo=True):
        """
        Muestra visualmente el árbol en formato jerárquico.
        Ejemplo:
        └── Deuda Total
            ├── Interés
            └── Mantenimiento de Valor
        """
        if nodo is None:
            nodo = self.raiz
        if nodo is not None:
            print(prefijo + ("└── " if es_izquierdo else "├── ") + str(nodo.valor))
            if nodo.izq or nodo.der:
                if nodo.izq:
                    self.mostrar_arbol(nodo.izq, prefijo + ("    " if es_izquierdo else "│   "), True)
                if nodo.der:
                    self.mostrar_arbol(nodo.der, prefijo + ("    " if es_izquierdo else "│   "), False)


# =====================================================
# 🔹 Ejemplos rápidos de uso
# =====================================================
if __name__ == "__main__":

    print("\n=== Ejemplo de Pila ===")
    pila = Pila()
    pila.push("MV calculado")
    pila.push("Interés calculado")
    print(pila)
    print("Pop:", pila.pop())

    print("\n=== Ejemplo de Cola ===")
    cola = Cola()
    cola.encolar("Contribuyente 1")
    cola.encolar("Contribuyente 2")
    print(cola)
    print("Desencolado:", cola.desencolar())

    print("\n=== Ejemplo de ÁrbolDeuda ===")
    arbol = ArbolDeuda()
    arbol.insertar("Deuda Total")
    arbol.insertar("Mantenimiento de Valor")
    arbol.insertar("Interés")
    arbol.insertar("Sanción")

    print("\nRecorrido en preorden:")
    arbol.preorden()

    print("\nRepresentación visual del árbol:")
    arbol.mostrar_arbol()
