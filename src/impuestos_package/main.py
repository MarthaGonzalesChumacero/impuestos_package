from impuestos_package.calculadora import CalculadoraDeuda
from impuestos_package.ufv import BCBAPIUFV


def main():

    # Datos base
    TO = 1000
    fecha_inicio = "2023-01-01"
    fecha_fin = "2023-01-31"
    tasa = 0.05
    dias = 30
    porcentaje = 0.2

    
    api = BCBAPIUFV()
    datos = api.consumir_endpoint(fecha_inicio, fecha_fin)

    if not datos:
        print("❌ No se pudieron obtener las UFVs desde la API.")
        return

    
    ufv_venc = float(datos[0]["val_ufv"])   # primera fecha
    ufv_pago = float(datos[-1]["val_ufv"])  # última fecha

   
    calc = CalculadoraDeuda(TO, ufv_pago, ufv_venc, tasa, dias, porcentaje)

    
    resultado = calc.calcular()

    
    print("Resultado de la deuda total")
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")


if __name__ == "__main__":
    main()
