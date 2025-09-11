
# Librería para Cálculo de Deuda Tributaria

Esta librería está diseñada para calcular la **deuda tributaria** de un contribuyente a partir de diferentes factores como el **total original de la deuda (TO)**, el **mantenimiento de valor (MV)**, los **intereses (I)**, y las **sanciones (S)**. A continuación, se explica cómo utilizarla.

## Estructura del Proyecto

La estructura de carpetas de este proyecto es la siguiente:

```
impuestos_package/
├── src/
│   └── impuestos_package/
│       ├── __init__.py
│       ├── calculadora.py
│       ├── mv.py
│       ├── interes.py
│       ├── sancion.py
│       ├── ufv.py
│       └── main.py
├── LICENSE
├── pyproject.toml
├── setup.py
├── README.md  <-- Este archivo
└── .gitignore
```

### Descripción de Archivos

- **`src/impuestos_package/`**: Esta es la carpeta principal donde se encuentran las clases que calculan la deuda tributaria.
- **`main.py`**: Este es el archivo principal para ejecutar el cálculo de la deuda total.
- **`calculadora.py`**: Contiene la clase `CalculadoraDeuda` que gestiona el cálculo de la deuda total combinando `MantenimientoValor`, `Interes`, y `Sancion`.
- **`mv.py`**: Contiene la clase `MantenimientoValor` que calcula el valor actualizado de la deuda según las UFVs.
- **`interes.py`**: Contiene la clase `Interes` que calcula el interés generado por la deuda.
- **`sancion.py`**: Contiene la clase `Sancion` que calcula la sanción aplicada a la deuda.

---

## Instalación

1. **Clona el repositorio** (si no lo tienes localmente):

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```

2. **Accede al directorio del proyecto**:

   ```bash
   cd impuestos_package
   ```

3. **Crea un entorno virtual e instálalo**:

   Si aún no tienes un entorno virtual creado:

   ```bash
   python -m venv venv
   ```

4. **Activa el entorno virtual**:

   En Windows, usa:

   ```bash
   .env\Scripts\Activate.ps1
   ```

---

## Uso

### 1. **Estructura y Cálculos**

La librería permite calcular la deuda tributaria total a partir de tres componentes clave:

- **Mantenimiento de Valor (MV)**: Se calcula tomando el **Total Original (TO)** y multiplicándolo por la diferencia entre la **UFV de pago** y la **UFV de vencimiento**.

- **Interés (I)**: Se calcula sobre la deuda (TO + MV), multiplicado por la **tasa de interés** anual y los **días de retraso**.

- **Sanción (S)**: Se calcula sobre el **TO** multiplicado por el **porcentaje de sanción**.

### 2. **Ejemplo de Uso**

Dentro de `main.py`, puedes ver el siguiente ejemplo de uso para calcular la deuda tributaria:

```python
from impuestos_package.calculadora import CalculadoraDeuda

# Datos de ejemplo
TO = 1000
ufv_pago = 2.9
ufv_venc = 2.8
tasa = 0.05  # 5% anual
dias = 30
porcentaje = 0.2  # 20% de sanción

# Crear instancia de la calculadora
calc = CalculadoraDeuda(TO, ufv_pago, ufv_venc, tasa, dias, porcentaje)

# Ejecutar cálculo
resultado = calc.calcular()

# Mostrar resultados
print("🔹 Resultado de la deuda total")
for k, v in resultado.items():
    print(f"{k}: {v}")
```

### 3. **Cálculo Detallado**

Ejecutar este script imprimirá lo siguiente:

```
🔹 Resultado de la deuda total
TO: 1000.0
MV: 0.9
I: 0.15
S: 200.0
DeudaTotal: 1200.05
```

- **TO**: Total original de la deuda.
- **MV**: Mantenimiento de valor calculado con las UFVs.
- **I**: Intereses calculados según la tasa y días de retraso.
- **S**: Sanción aplicada.
- **DeudaTotal**: Suma de TO, MV, I y S.

---

## Estructura del Código

### 1. **`calculadora.py`**

Contiene la clase `CalculadoraDeuda`, que es la encargada de coordinar los cálculos de la deuda, llamando a las clases `MantenimientoValor`, `Interes`, y `Sancion`.

```python
class CalculadoraDeuda:
    def __init__(self, TO, ufv_pago, ufv_venc, tasa, dias, porcentaje):
        self.TO = TO
        self.ufv_pago = ufv_pago
        self.ufv_venc = ufv_venc
        self.tasa = tasa
        self.dias = dias
        self.porcentaje = porcentaje

    def calcular(self):
        mv = MantenimientoValor(self.TO, self.ufv_pago, self.ufv_venc)
        interes = Interes(self.TO, mv.calcular(), self.tasa, self.dias)
        sancion = Sancion(self.TO, self.porcentaje)

        MV = mv.calcular()
        I = interes.calcular()
        S = sancion.calcular()
        DT = self.TO + MV + I + S

        return {
            "TO": round(self.TO, 2),
            "MV": round(MV, 2),
            "I": round(I, 2),
            "S": round(S, 2),
            "DeudaTotal": round(DT, 2)
        }
```

### 2. **`mv.py`**

Clase que calcula el Mantenimiento de Valor (MV).

```python
class MantenimientoValor:
    def __init__(self, TO, ufv_pago, ufv_venc):
        self.TO = TO
        self.ufv_pago = ufv_pago
        self.ufv_venc = ufv_venc

    def calcular(self):
        return self.TO * (self.ufv_pago - self.ufv_venc)
```

### 3. **`interes.py`**

Clase que calcula el interés sobre el monto de la deuda.

```python
class Interes:
    def __init__(self, TO, MV, tasa, dias):
        self.TO = TO
        self.MV = MV
        self.tasa = tasa
        self.dias = dias

    def calcular(self):
        base = self.TO + self.MV
        return base * self.tasa * self.dias / 360
```

### 4. **`sancion.py`**

Clase que calcula la sanción sobre la deuda original (TO).

```python
class Sancion:
    def __init__(self, TO, porcentaje):
        self.TO = TO
        self.porcentaje = porcentaje

    def calcular(self):
        return self.TO * self.porcentaje
```

---

## Contribuir

Si deseas mejorar o contribuir a este proyecto, por favor realiza un **fork** del repositorio y envía tus cambios mediante un **pull request**.

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo LICENSE para más detalles.
