import requests

class BCBAPIUFV:
    

    BASE_URL = "https://www.bcb.gob.bo/librerias/charts/ufv.php"

    def consumir_endpoint(self, fecha_inicio: str, fecha_fin: str = None):
        

        if fecha_fin is None:
            fecha_fin = fecha_inicio

        url = f"{self.BASE_URL}?cFecIni={fecha_inicio}&cFecFin={fecha_fin}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data   
            else:
                print(f" Error en la petición. Código: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(" Error en la conexión a la API UFV:", e)
            return None
