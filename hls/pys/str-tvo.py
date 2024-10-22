import requests
import re
import base64
import json

# URL del sitio web que quieres visitar
url = "https://conceptoweb-studio.com/radio/video/tvo/"

# Datos del repositorio y archivo de GitHub
github_repo = "dca2107/ctv"  # Reemplaza con tu nombre de usuario/repositorio
github_file_path = "/hls/SV-23-TVO.m3u8"  # Ruta del archivo en tu repo
github_token = "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"  # Reemplaza con tu token de acceso personal

# Función para extraer los enlaces M3U8
def extraer_m3u8():
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Buscar todos los enlaces .m3u8 en el código fuente
        m3u8_links = re.findall(r'(https?://[^\s]+\.m3u8)', response.text)
        return m3u8_links
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return []

# Función para obtener el SHA del archivo existente en GitHub
def obtener_sha():
    api_url = f"https://api.github.com/repos/{github_repo}/contents/{github_file_path}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        file_info = response.json()
        return file_info['sha']
    else:
        print("No se pudo obtener el SHA del archivo.")
        return None

# Función para actualizar el archivo en GitHub
def actualizar_archivo_github(contenido):
    sha = obtener_sha()
    if not sha:
        return
    
    api_url = f"https://api.github.com/repos/{github_repo}/contents/{github_file_path}"
    headers = {"Authorization": f"token {github_token}", "Content-Type": "application/json"}
    
    # Codificar el contenido en base64
    contenido_base64 = base64.b64encode(contenido.encode("utf-8")).decode("utf-8")
    
    # Datos para la actualización del archivo en GitHub
    data = {
        "message": "Actualizar SV-23-TVO.m3u8 con enlaces M3U8",
        "content": contenido_base64,
        "sha": sha
    }
    
    # Hacer la solicitud PUT a la API de GitHub
    response = requests.put(api_url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Archivo actualizado con éxito en GitHub.")
    else:
        print(f"Error al actualizar el archivo: {response.status_code}, {response.text}")

# Función principal
def main():
    # Extraer los enlaces M3U8
    m3u8_links = extraer_m3u8()
    
    if m3u8_links:
        # Crear el contenido del archivo con los enlaces M3U8
        contenido = "\n".join(m3u8_links)
        
        # Actualizar el archivo en GitHub
        actualizar_archivo_github(contenido)
    else:
        print("No se encontraron enlaces M3U8.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
