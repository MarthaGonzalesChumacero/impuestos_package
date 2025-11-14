"""
Ejemplo de cálculo legal puro con impuestos_package
Basado en Ley 2492 (art. 47 y 165)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from impuestos_package.calculadora import CalculadoraDeuda

# --- DummyAPI con las UFV reales 2025-06-23 → 2025-11-10 ---
class DummyAPI:
    def _parse_valor(self, item):
        return float(item["valor"]) if float(item["valor"]) > 0 else None

    def consumir_endpoint(self, fi, ff, timeout=10):
        # UFV reales de las fechas solicitadas
        return [{"valor": "2.73596"}, {"valor": "2.96361"}]

import impuestos_package.calculadora as calc_mod
calc_mod.BCBAPIUFV = DummyAPI
# -------------------------------------------------------------

def main():
    # Datos reales del ejemplo
    TO = 500                 # Tributo omitido
    fecha_inicio = "2025-06-23"
    fecha_fin = "2025-11-10"
    tasa = 6                 # Tasa anual de interés (Ley 2492, DS 27310)
    dias = 140               # Días de mora reales
    porcentaje = 12          # Sanción del 12% (pago voluntario)

    # Crear instancia
    calc = CalculadoraDeuda(
        TO=TO,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        tasa=tasa,
        dias=dias,
        porcentaje=porcentaje
    )

    # Ejecutar cálculo
    resultado = calc.calcular()

    # Mostrar resultados
    print("\nCálculo legal según Ley 2492:")
    print("-----------------------------")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
