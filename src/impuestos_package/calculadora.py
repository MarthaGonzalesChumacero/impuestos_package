from .mv import MantenimientoValor
from .interes import Interes
from .sancion import Sancion
from .ufv import BCBAPIUFV   


class CalculadoraDeuda:

    def __init__(self, TO: float, fecha_inicio: str, fecha_fin: str, tasa: float, dias: int, porcentaje: float):
      
        self.TO = TO
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tasa = tasa
        self.dias = dias
        self.porcentaje = porcentaje

    def _obtener_ufvs(self):
        
        api = BCBAPIUFV()
        datos = api.consumir_endpoint(self.fecha_inicio, self.fecha_fin)

        if not datos:
            return None

       
       
        try:
            ufv_venc = float(datos[0]["valor"])   # valor en fecha_inicio
            ufv_pago = float(datos[-1]["valor"])  # valor en fecha_fin
            return ufv_venc, ufv_pago
        except (KeyError, IndexError, ValueError):
            return None

    def calcular(self):
        
        ufvs = self._obtener_ufvs()
        if ufvs is None:
            return {"error": "No se pudieron obtener los valores de UFV desde la API."}

        ufv_venc, ufv_pago = ufvs

        
        mv = MantenimientoValor(self.TO, ufv_pago, ufv_venc)
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
            "DT": round(DT, 2),
        }

