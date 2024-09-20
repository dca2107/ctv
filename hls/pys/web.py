import requests
import re
import sys

def get_html_content(url: str):
    """
    Hace una solicitud GET a la URL y obtiene el contenido HTML.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error al obtener el contenido HTML de {url}: {e}")
        return ""

def extract_links_from_html(html_content: str):
    """
    Extrae todos los enlaces <a> de un contenido HTML utilizando expresiones regulares.
    """
    pattern = r'href=["\'](https?://[^\s"\'<>]+)["\']'
    links = re.findall(pattern, html_content)
    return links

def save_links_to_m3u8(links, output_file: str):
    """
    Guarda los enlaces extraídos en un archivo .m3u8.
    """
    with open(output_file, "w") as f:
        f.write("#EXTM3U\n")
        for link in links:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080\n{link}\n")

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <url> <output_file>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    html_content = get_html_content(url)

    if html_content:
        links = extract_links_from_html(html_content)

        if links:
            save_links_to_m3u8(links, output_file)
            print(f"Enlaces guardados en {output_file}.")
        else:
            print("No se encontraron enlaces en la página.")
    else:
        print(f"No se pudo obtener el contenido HTML de {url}.")

if __name__ == "__main__":
    main()
