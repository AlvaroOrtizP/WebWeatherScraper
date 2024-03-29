import cv2
import pytesseract
from PIL import Image

def extract_text_from_table(image_path):
    """
    Extrae texto de una tabla en una imagen.

    Parameters:
    - image_path (str): Ruta de la imagen.

    Returns:
    - str: Texto extraído de la tabla.
    """
    # Leer la imagen con opencv
    image = cv2.imread(image_path)

    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral para resaltar los contornos
    _, threshold_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # Encontrar contornos en la imagen
    contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extraer texto de cada contorno
    extracted_text = ""
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y + h, x:x + w]
        text = pytesseract.image_to_string(Image.fromarray(roi))
        extracted_text += text + "\n"

    return extracted_text

if __name__ == "__main__":
    print("------------------------------------------------------------------------------------------------")
    print("EXTRACCIÓN DE TEXTO DE TABLA")
    
    # Ruta de la captura de pantalla
    screenshot_path = "windguru_screenshot.png"

    # Extraer texto de la tabla en la imagen
    extracted_text = extract_text_from_table(screenshot_path)

    # Imprimir el texto extraído
    print("Texto extraído:")
    print(extracted_text)
    
    print("EXTRACCIÓN DE TEXTO COMPLETADA")
    print("------------------------------------------------------------------------------------------------")
