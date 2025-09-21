"""
Ejemplo básico de uso de la librería impuestos_package
"""

from impuestos_package.calculadora import CalculadoraDeuda

# --- OPCIONAL: usar DummyAPI en lugar de la API real ---
class DummyAPI:
    def _parse_valor(self, item):
        # Simula el comportamiento del método _parse_valor de BCBAPIUFV
        return float(item["valor"]) if float(item["valor"]) > 0 else None

    def consumir_endpoint(self, fi, ff, timeout=10):
        # Simula la respuesta de la API: UFV inicial 2.27267 y final 2.8689
        return [{"valor": "2.27267"}, {"valor": "2.8689"}]

import impuestos_package.calculadora as calc_mod
calc_mod.BCBAPIUFV = DummyAPI
# -------------------------------------------------------

def main():
    # Datos de ejemplo
    TO = 383  # Total Original
    fecha_inicio = "2018-07-20"
    fecha_fin = "2025-09-15"
    tasa = 18       # 12% anual
    dias = 1461       # días de retraso
    porcentaje = 12 # sanción en %

    # Crear instancia de la calculadora
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
    print(" Resultado de la deuda tributaria:")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
