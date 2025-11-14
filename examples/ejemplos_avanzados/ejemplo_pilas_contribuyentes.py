from impuestos_package.calculadora import CalculadoraDeuda
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

# Clase Pila para almacenar los cálculos
class Pila:
    """Implementación de una pila para almacenar el historial de cálculos."""
    def __init__(self):
        self.items = []

    def push(self, item):
        """Agrega un elemento a la pila (historial)."""
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
        """Muestra el historial de cálculos en la pila."""
        print("\nHistorial de cálculos:")
        for item in reversed(self.items):  # Mostrar desde el más reciente
            print(f"{item}")

# Función principal para realizar los cálculos
def main():
    # Crear instancia de la calculadora
    calc = CalculadoraDeuda(
        TO=1500,
        fecha_inicio="2025-01-01",
        fecha_fin="2025-06-01",
        tasa=6,
        dias=180,
        porcentaje=15
    )

    # Instanciar la pila para guardar el historial
    historial = Pila()

    # Calcular para ayer (simulamos la fecha de ayer)
    resultado_ayer = calc.calcular()
    historial.push(f"Cálculo realizado el {datetime.now().strftime('%Y-%m-%d')} (ayer): {resultado_ayer}")

    # Calcular para hoy
    calc.fecha_inicio = "2025-01-01"  # Cambiar fecha si es necesario
    calc.fecha_fin = "2025-06-01"
    resultado_hoy = calc.calcular()
    historial.push(f"Cálculo realizado el {datetime.now().strftime('%Y-%m-%d')} (hoy): {resultado_hoy}")

    # Mostrar el historial de cálculos
    historial.mostrar_historial()

if __name__ == "__main__":
    main()
