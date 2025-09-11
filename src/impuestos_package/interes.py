class Interes:
    def __init__(self, TO: float, MV: float, tasa: float, dias: int):
        self.TO = TO
        self.MV = MV
        self.tasa = tasa
        self.dias = dias
        
    def calcular(self) -> float:
        """
        Calcula el Interés (I).
        Fórmula: I = (TO + MV) * (tasa / 360) * dias
        """
        return (self.TO + self.MV) * (self.tasa / 360) * self.dias
