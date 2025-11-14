from impuestos_package.calculadora import CalculadoraDeuda

# Cálculo de deuda de un contribuyente con diferentes tributos
calc_tributo1 = CalculadoraDeuda(
    TO=1000,
    fecha_inicio="2025-01-01",
    fecha_fin="2025-06-01",
    tasa=5,
    dias=120,
    porcentaje=12
)

calc_tributo2 = CalculadoraDeuda(
    TO=2000,
    fecha_inicio="2025-01-01",
    fecha_fin="2025-06-01",
    tasa=6,
    dias=150,
    porcentaje=24
)

# Ejecutar cálculos
resultado_tributo1 = calc_tributo1.calcular()
resultado_tributo2 = calc_tributo2.calcular()

# Mostrar resultados
print("\n Resultado para Tributo 1:")
for k, v in resultado_tributo1.items():
    print(f"{k}: {v}")

print("\n Resultado para Tributo 2:")
for k, v in resultado_tributo2.items():
    print(f"{k}: {v}")
