"""
Tests unitarios para el módulo estructuras.py
Autor: Martha Gonzales Chumacero
Basado en los contenidos de la materia Estructura de Datos (2025)
"""

import pytest
from impuestos_package.estructuras import Pila, Cola, ArbolDeuda


# =====================================================
# 🔹 Pruebas para la clase PILA
# =====================================================
def test_pila_operaciones_basicas():
    pila = Pila()
    assert pila.esta_vacia() is True

    pila.push("Cálculo 1")
    pila.push("Cálculo 2")

    assert pila.tamano() == 2
    assert pila.cima() == "Cálculo 2"

    elemento = pila.pop()
    assert elemento == "Cálculo 2"
    assert pila.tamano() == 1

def test_pila_pop_en_vacia():
    pila = Pila()
    assert pila.pop() is None


# =====================================================
# 🔹 Pruebas para la clase COLA
# =====================================================
def test_cola_operaciones_basicas():
    cola = Cola()
    assert cola.esta_vacia() is True

    cola.encolar("Contribuyente 1")
    cola.encolar("Contribuyente 2")
    cola.encolar("Contribuyente 3")

    assert cola.tamano() == 3
    assert cola.frente() == "Contribuyente 1"

    primero = cola.desencolar()
    assert primero == "Contribuyente 1"
    assert cola.tamano() == 2

def test_cola_desencolar_en_vacia():
    cola = Cola()
    assert cola.desencolar() is None


# =====================================================
# 🔹 Pruebas para la clase ÁRBOL DEUDA
# =====================================================
def test_arbol_insercion_y_busqueda():
    arbol = ArbolDeuda()
    arbol.insertar("Deuda Total")
    arbol.insertar("Mantenimiento de Valor")
    arbol.insertar("Interés")
    arbol.insertar("Sanción")

    assert arbol.buscar("Deuda Total") is True
    assert arbol.buscar("Mantenimiento de Valor") is True
    assert arbol.buscar("Interés") is True
    assert arbol.buscar("No Existe") is False

def test_arbol_preorden(capsys):
    arbol = ArbolDeuda()
    valores = ["Deuda Total", "Interés", "Mantenimiento de Valor", "Sanción"]
    for v in valores:
        arbol.insertar(v)
    arbol.preorden()

    captured = capsys.readouterr()
    for v in valores:
        assert v in captured.out
