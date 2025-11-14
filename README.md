
# `impuestos_package`

`impuestos_package` es una librería desarrollada en Python para facilitar cálculos tributarios en Bolivia, como el **mantenimiento de valor (MV)**, **intereses**, **sanciones** e indicadores basados en la **UFV (Unidad de Fomento a la Vivienda)**. Además, el paquete implementa estructuras de datos como **pilas**, **colas** y **árboles binarios** para organizar, almacenar y procesar de manera eficiente los cálculos tributarios.

Este paquete fue desarrollado, probado y publicado oficialmente en el Índice de Paquetes de Python (**PyPI**).

Puedes verlo y descargarlo directamente desde:  
[https://pypi.org/project/impuestos-package/](https://pypi.org/project/impuestos-package/)

---

## Instalación

Para instalar la librería desde PyPI, ejecuta:

```bash
pip install impuestos-package
```

Esto instalará automáticamente la versión más reciente del paquete.

---

## ¿Qué incluye este paquete?

El paquete cuenta con una arquitectura modular que permite importar solamente lo necesario. Incluye:

- `calculadora.py` → Clase principal para calcular deuda total.
- `mv.py` → Cálculo del mantenimiento de valor con base en UFV.
- `interes.py` → Cálculo del interés simple.
- `sancion.py` → Cálculo de sanciones tributarias.
- `ufv.py` → Consulta de UFVs desde la API del Banco Central de Bolivia (BCB).
- `estructuras.py` → Implementación de estructuras de datos como **Pila**, **Cola** y **Árbol Binario**.

La librería permite calcular la **deuda tributaria** de un contribuyente considerando:

- **Tributo Omitido (TO)**
- **Mantenimiento de Valor (MV)**
- **Interés (I)**
- **Sanción (S)**

Se conecta automáticamente con la **API del BCB** para obtener los valores UFV y realizar los cálculos.

Cada módulo ha sido probado con test unitarios y de integración para asegurar precisión y confiabilidad.

---

## Testing

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

## Ejemplo de Uso

```python
from impuestos_package.calculadora import CalculadoraDeuda

# Crear instancia
calc = CalculadoraDeuda(
    TO=500,  # Total Original
    fecha_inicio="2025-06-23",
    fecha_fin="2025-11-10",
    tasa=6,        # 6% anual
    dias=140,      # días de retraso
    porcentaje=12   # sanción en %
)

# Calcular deuda
resultado = calc.calcular()

print("Resultado de la deuda tributaria (2025):")
for k, v in resultado.items():
    print(f"{k}: {v}")
```

### Salida esperada (ejemplo)

```
Resultado de la deuda tributaria (2025):
------------------------------------------
TO: 500
MV: 41.6
I: 12.64
S: 60.0
DT: 614.24
```

### Ejemplo con Pilas, Colas y Árbol Binario

```python
from datetime import datetime
from impuestos_package.calculadora import CalculadoraDeuda
from impuestos_package.estructuras import Pila, Cola, ArbolDeuda

# Lista de contribuyentes con sus datos personalizados
contribuyentes = [
    {"nombre": "Juan", "apellido_paterno": "Perez", "apellido_materno": "Gomez", "TO": 1500, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 6, "dias": 180, "porcentaje": 15},
    {"nombre": "Maria", "apellido_paterno": "Lopez", "apellido_materno": "Martinez", "TO": 2000, "fecha_inicio": "2025-06-01", "fecha_fin": "2025-11-10", "tasa": 6, "dias": 150, "porcentaje": 10},
    {"nombre": "Carlos", "apellido_paterno": "Garcia", "apellido_materno": "Fernandez", "TO": 1200, "fecha_inicio": "2025-01-01", "fecha_fin": "2025-06-01", "tasa": 5, "dias": 200, "porcentaje": 20}
]

# Crear instancia de la calculadora
calc = CalculadoraDeuda(
    TO=1500,
    fecha_inicio="2025-01-01",
    fecha_fin="2025-06-01",
    tasa=6,
    dias=180,
    porcentaje=15
)

# Crear una cola para almacenar las tareas
cola_calculos = Cola()
# Crear una pila para el historial
historial_pila = Pila()
# Crear una instancia del árbol binario
arbol_deuda = ArbolDeuda()

# Agregar tareas a la cola, pila y árbol binario
for contribuyente in contribuyentes:
    contribuyente['fecha'] = datetime.now().strftime('%Y-%m-%d')  # Fecha actual para el historial
    cola_calculos.encolar(contribuyente)
    historial_pila.push(contribuyente)
    arbol_deuda.insertar(contribuyente)

# Procesar los cálculos en la cola (FIFO)
print("
Procesando cálculos pendientes en cola (FIFO)...")
while not cola_calculos.esta_vacia():
    contribuyente = cola_calculos.desencolar()
    calc.TO = contribuyente["TO"]
    calc.fecha_inicio = contribuyente["fecha_inicio"]
    calc.fecha_fin = contribuyente["fecha_fin"]
    calc.tasa = contribuyente["tasa"]
    calc.dias = contribuyente["dias"]
    calc.porcentaje = contribuyente["porcentaje"]
    resultado = calc.calcular()
    contribuyente['resultado'] = resultado
    print(f"Resultado de la cola para {contribuyente['nombre']}: {resultado}")

# Mostrar el historial de cálculos procesados (pila)
historial_pila.mostrar_historial()

# Mostrar la estructura jerárquica del árbol
print("
Estructura jerárquica del árbol de deuda:")
arbol_deuda.mostrar_arbol()

# Procesar los cálculos en preorden (árbol)
print("
Procesando cálculos pendientes en árbol binario (Preorden)...")
arbol_deuda.preorden()
```

### Salida esperada (con pilas, colas y árboles binarios)

```
Procesando cálculos pendientes en cola (FIFO)...
Resultado de la cola para Juan: {'TO': 1500, 'MV': 75.0, 'I': 45.0, 'S': 150.0, 'DT': 1770.0}
Resultado de la cola para Maria: {'TO': 2000, 'MV': 100.0, 'I': 60.0, 'S': 200.0, 'DT': 2360.0}
Resultado de la cola para Carlos: {'TO': 1200, 'MV': 60.0, 'I': 36.0, 'S': 120.0, 'DT': 1416.0}

Historial de cálculos procesados (Pila):
Carlos procesado el 2025-11-14 - Resultado: {'TO': 1200, 'MV': 60.0, 'I': 36.0, 'S': 120.0, 'DT': 1416.0}
Maria procesado el 2025-11-14 - Resultado: {'TO': 2000, 'MV': 100.0, 'I': 60.0, 'S': 200.0, 'DT': 2360.0}
Juan procesado el 2025-11-14 - Resultado: {'TO': 1500, 'MV': 75.0, 'I': 45.0, 'S': 150.0, 'DT': 1770.0}

Estructura jerárquica del árbol de deuda:
    Juan Perez Gomez
    Maria Lopez Martinez
    Carlos Garcia Fernandez

Procesando cálculos pendientes en árbol binario (Preorden)...
Procesando: Juan Perez Gomez
Resultado del cálculo para Juan:
TO: 1500
MV: 75.0
I: 45.0
S: 150.0
DT: 1770.0
Procesando: Maria Lopez Martinez
Resultado del cálculo para Maria:
TO: 2000
MV: 100.0
I: 60.0
S: 200.0
DT: 2360.0
Procesando: Carlos Garcia Fernandez
Resultado del cálculo para Carlos:
TO: 1200
MV: 60.0
I: 36.0
S: 120.0
DT: 1416.0
```

---

## Estructura del Proyecto

```
impuestos_package/
├── src/
│   └── impuestos_package/
│       ├── __init__.py
│       ├── calculadora.py
│       ├── interes.py
│       ├── mv.py
│       ├── sancion.py
│       ├── ufv.py
│       └── estructuras.py
├── tests/
│   ├── test_calculadora.py
│   ├── test_interes.py
│   ├── test_mv.py
│   ├── test_sancion.py
│   ├── test_ufv.py
│   └── test_estrcuturas.py
├── examples/
│   ├── ejemplo_basico.py
│   ├── ejemplo_demo_calculadora_estructuras.py
│   ├── ejemplos_avanzados/
│   │   ├── ejemplo_arbol_binario.py
│   │   ├── ejemplo_colas_contribuyentes.py
│   │   ├── ejemplo_completo.py
│   │   ├── ejemplo_multiple_tributos.py
│   │   ├── ejemplo_pilas_contribuyentes.py
│   │   ├── ejemplo_sanciones.py
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```
---

## Licencia

Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [`LICENSE`](./LICENSE) para más información.

---

## Contribuciones

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
