class MantenimientoValor:
    def __init__(self, TO: float, ufv_pago: float, ufv_venc: float):
        self.TO = TO
        self.ufv_pago = ufv_pago
        self.ufv_venc = ufv_venc
        
    def calcular(self) -> float:
        """
        Calcula el Mantenimiento de Valor (MV).
        Fórmula: MV = TO * ( (UFV_pago / UFV_venc) - 1 )
        """
        return self.TO * ((self.ufv_pago / self.ufv_venc) - 1)
