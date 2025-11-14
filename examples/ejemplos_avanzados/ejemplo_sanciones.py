from impuestos_package.calculadora import CalculadoraDeuda

# Cálculo con diferentes sanciones
calc_sancion_12 = CalculadoraDeuda(
    TO=1000,
    fecha_inicio="2025-01-01",
    fecha_fin="2025-06-01",
    tasa=5,
    dias=120,
    porcentaje=12
)

calc_sancion_24 = CalculadoraDeuda(
    TO=1000,
    fecha_inicio="2025-01-01",
    fecha_fin="2025-06-01",
    tasa=5,
    dias=120,
    porcentaje=24
)

# Ejecutar cálculos
resultado_sancion_12 = calc_sancion_12.calcular()
resultado_sancion_24 = calc_sancion_24.calcular()

# Mostrar resultados
print("\n Resultado con Sanción 12%:")
for k, v in resultado_sancion_5.items():
    print(f"{k}: {v}")

print("\n Resultado con Sanción 24%:")
for k, v in resultado_sancion_10.items():
    print(f"{k}: {v}")
