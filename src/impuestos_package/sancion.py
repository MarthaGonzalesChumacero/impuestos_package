class Sancion:
    def __init__(self, TO: float, porcentaje: float):
        self.TO = TO
        self.porcentaje = porcentaje
        
    def calcular(self) -> float:
        """
        Calcula la Sanción (S).
        Fórmula: S = TO * (porcentaje / 100)
        """
        return self.TO * (self.porcentaje / 100)
