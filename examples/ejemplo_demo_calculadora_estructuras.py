"""
Ejemplo de uso de la clase CalculadoraDeuda mejorada
con estructuras de datos (Pila, Cola y Árbol).
Incluye un modo “offline” que simula valores UFV
cuando la API del BCB no está disponible.
"""

# ============================================================
# 🔹 Simular API UFV (modo offline sin conexión)
# ============================================================

from impuestos_package import calculadora as calc_mod

class DummyAPI:
    """Simula los valores UFV del BCB para entornos offline."""
    def _parse_valor(self, item):
        return float(item["valor"])

    def consumir_endpoint(self, fi, ff, timeout=10):
        # UFVs simuladas para 2025-06-23 → 2025-11-10
        return [{"valor": "2.73596"}, {"valor": "2.96361"}]

# Sobrescribe la API real del paquete por la simulada
calc_mod.BCBAPIUFV = DummyAPI

# ============================================================
# 🔹 Importar la clase principal
# ============================================================

from impuestos_package.calculadora import CalculadoraDeuda

# ============================================================
# 🔹 Crear una instancia de la calculadora
# ============================================================

calc = CalculadoraDeuda(
    TO=500,                     # Tributo Omitido
    fecha_inicio="2025-06-23",  # Fecha inicial
    fecha_fin="2025-11-10",     # Fecha final
    tasa=6,                     # Tasa de interés anual
    dias=140,                   # Días de mora
    porcentaje=12               # Sanción en %
)

# ============================================================
# 🔹 Ejecutar el cálculo
# ============================================================

resultado = calc.calcular()

print("\n💰 Resultado final del cálculo:")
for k, v in resultado.items():
    print(f"{k}: {v}")

# ============================================================
# 🔹 Mostrar historial (uso de Pila)
# ============================================================

calc.mostrar_historial()

# ============================================================
# 🔹 Agregar y procesar cálculos en cola (uso de Cola)
# ============================================================

calc.agregar_a_cola("Revisión de cálculo 2025-A")
calc.agregar_a_cola("Cálculo de contribuyente B")
calc.procesar_cola()

# ============================================================
# 🔹 Mostrar estructura del árbol (uso de Árbol)
# ============================================================

calc.mostrar_arbol_deuda()

print("\n✅ Ejemplo ejecutado correctamente.")
