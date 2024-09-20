import requests
import re
import sys

def get_html_content(url: str):
    """
    Hace una solicitud GET a la URL y obtiene el contenido HTML.

    Args:
        url (str): La URL de la página web.

    Returns:
        str: El contenido HTML de la página.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa
        return response.text
    except requests.RequestException as e:
        print(f"Error al obtener el contenido HTML de {url}: {e}")
        return ""

def extract_links_from_html(html_content: str):
    """
    Extrae todos los enlaces <a> de un contenido HTML utilizando expresiones regulares.

    Args:
        html_content (str): El contenido HTML de la página.

    Returns:
        list: Una lista de enlaces (URLs) encontrados.
    """
    # Expresión regular para encontrar enlaces en etiquetas <a href="">
    pattern = r'href=["\'](https?://[^\s"\'<>]+)["\']'
    links = re.findall(pattern, html_content)
    return links

def main():
    """
    Función principal que extrae enlaces de una página HTML.
    """
    if len(sys.argv) < 2:
        print("Uso: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    # Obtener el contenido HTML de la página
    html_content = get_html_content(url)

    if html_content:
        # Extraer los enlaces usando expresiones regulares
        links = extract_links_from_html(html_content)

        if links:
            print("Enlaces encontrados:")
            for link in links:
                print(link)
        else:
            print("No se encontraron enlaces en la página.")
    else:
        print(f"No se pudo obtener el contenido HTML de {url}.")

if __name__ == "__main__":
    main()
