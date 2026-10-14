import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# Código INE de Valencia capital: 46250 (Torrent: 46244)
API_URL = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/46250"
API_KEY = os.getenv("AEMET_API_KEY")

def obtener_datos_aemet() -> list[dict]:
    """Obtiene la predicción de AEMET realizando el proceso de 2 pasos."""
    # AEMET espera la API key como parámetro en la URL o en un header api_key
    querystring = {"api_key": API_KEY}
    
    # Paso 1: Solicitar la URL de descarga
    resp_inicial = requests.get(API_URL, params=querystring, timeout=30)
    resp_inicial.raise_for_status()
    datos_metadatos = resp_inicial.json()
    
    # Comprobar que la petición fue exitosa (estado 200 en el JSON de AEMET)
    if datos_metadatos.get("estado") == 200:
        url_datos_reales = datos_metadatos.get("datos")
        
        # Paso 2: Descargar el JSON real con la predicción
        resp_final = requests.get(url_datos_reales, timeout=30)
        resp_final.raise_for_status()
        return resp_final.json()
    else:
        raise Exception(f"Error API AEMET: {datos_metadatos.get('descripcion')}")

if __name__ == "__main__":
    registros = obtener_datos_aemet()
    fecha = date.today().isoformat()
    ruta_salida = f"data/raw/aemet_valencia_{fecha}.json"
    
    # Crear la carpeta si no existe
    os.makedirs("data/raw", exist_ok=True)
    
    # Guardar en la zona raw
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
        
    print(f"Ingesta completada: Datos guardados en {ruta_salida}")