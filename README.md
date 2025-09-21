#  impuestos_package

`impuestos_package` es una librería desarrollada en Python para facilitar cálculos tributarios en Bolivia, como el **mantenimiento de valor (MV)**, **intereses**, **sanciones** e indicadores basados en la **UFV (Unidad de Fomento a la Vivienda)**.

Este paquete fue desarrollado, probado y publicado oficialmente en el Índice de Paquetes de Python (**PyPI**).

Puedes verlo y descargarlo directamente desde:  
[https://pypi.org/project/impuestos-package/](https://pypi.org/project/impuestos-package/)

---

##  Instalación

Para instalar la librería desde PyPI, ejecuta:

```bash
pip install impuestos-package
```

Esto instalará automáticamente la versión más reciente del paquete.

---

##  ¿Qué incluye este paquete?

El paquete cuenta con una arquitectura modular que permite importar solamente lo necesario. Incluye:

- `calculadora.py` → Clase principal para calcular deuda total.
- `mv.py` → Cálculo del mantenimiento de valor con base en UFV.
- `interes.py` → Cálculo del interés simple.
- `sancion.py` → Cálculo de sanciones tributarias.
- `ufv.py` → Consulta de UFVs desde la API del Banco Central de Bolivia (BCB).

La librería permite calcular la **deuda tributaria** de un contribuyente considerando:

- **Tributo Omitido (TO)**
- **Mantenimiento de Valor (MV)**
- **Interés (I)**
- **Sanción (S)**

Se conecta automáticamente con la **API del BCB** para obtener los valores UFV y realizar los cálculos.

Cada módulo ha sido probado con test unitarios y de integración para asegurar precisión y confiabilidad.

---

##  Testing

Este proyecto incluye pruebas automatizadas con `pytest`.

### Ejecutar todos los tests:
```bash
pytest -q
```

### Ver cobertura de código:
```bash
pytest --cov=impuestos_package --cov-report=term-missing
```

Ejemplo de salida:

```
collected 19 items
19 passed in 0.55s
TOTAL coverage: 95%
```

---

##  Ejemplo de Uso

```python
from impuestos_package.calculadora import CalculadoraDeuda

# Crear instancia
calc = CalculadoraDeuda(
    TO=383  # Total Original
    fecha_inicio = "2018-07-20"
    fecha_fin = "2025-09-15"
    tasa = 18       # 12% anual
    dias = 1461       # días de retraso
    porcentaje = 12 # sanción en %
)

# Calcular deuda
resultado = calc.calcular()

print(" Resultado de la deuda tributaria:")
for k, v in resultado.items():
    print(f"{k}: {v}")
```

### Salida esperada (ejemplo)

```
 Resultado de la deuda tributaria:
TO: 1000.48
MV: 353.18
I: 45.96
S: 45.96
DT: 882.62
```

---

##  Estructura del proyecto

```
impuestos_package/
├── src/
│   └── impuestos_package/
│       ├── __init__.py
│       ├── calculadora.py
│       ├── interes.py
│       ├── mv.py
│       ├── sancion.py
│       └── ufv.py
├── tests/
│   ├── test_calculadora.py
│   ├── test_interes.py
│   ├── test_mv.py
│   ├── test_sancion.py
│   └── test_ufv.py
├── examples/
│   └── ejemplo_basico.py
├── README.md
├── pyproject.toml
└── LICENSE
```

---

##  Licencia

Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [`LICENSE`](./LICENSE) para más información.

---

##  Contribuciones

1. Haz un **fork** del repositorio.  
2. Crea una nueva rama:  
   ```bash
   git checkout -b mi-mejora
   ```
3. Realiza tus cambios y corre los tests.  
4. Envía un **pull request**.

---

Se aceptan sugerencias, mejoras y reportes de errores.  
Si deseas colaborar, ¡eres bienvenido/a!

---




