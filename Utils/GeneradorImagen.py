from PIL import Image, ImageDraw, ImageFont
import datetime


def crear_imagen(data):
    """
    Crea una imagen con datos meteorológicos en forma de tabla.

    Parameters:
    - data (dict): Diccionario de datos meteorológicos.

    Returns:
    - Image: Objeto de imagen creado.
    """
    # Define los colores de la tabla y las fuentes de texto
    bg_color = (49, 68, 99)  # azul oscuro
    text_color = (255, 255, 255)  # blanco
    font = ImageFont.truetype("arial.ttf", size=16)
    header_font = ImageFont.truetype("arialbd.ttf", size=18)
    title_font = ImageFont.truetype("arialbd.ttf", size=24)

    # Define las dimensiones de la imagen y la tabla
    width, height = 800, 750
    table_width, table_height = 500, 250

    # Crea la imagen y el objeto de dibujo
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Agrega el título con la fecha actual centrada en la parte superior
    title = "Datos meteorológicos del " + datetime.date.today().strftime("%d/%m/%Y")
    title_width, title_height = title_font.getsize(title)
    draw.text(((width - title_width) / 2, 20), title, font=title_font, fill=text_color)

    # Dibuja el encabezado de la tabla
    draw.rectangle((25, 75, 700, 125), fill=text_color)
    draw.text((40, 90), "Hora", font=header_font, fill=bg_color)
    draw.text((110, 90), "Viento", font=header_font, fill=bg_color)
    draw.text((180, 90), "Ráfagas", font=header_font, fill=bg_color)
    draw.text((265, 90), "Al olas", font=header_font, fill=bg_color)
    draw.text((340, 90), "Per olas", font=header_font, fill=bg_color)
    draw.text((435, 90), "Tem", font=header_font, fill=bg_color)

    # Dibuja cada fila de la tabla
    x, y = 25, 150
    for key, value in data.items():
        draw.rectangle((x, y, x+table_width, y+30), fill=text_color)
        draw.text((x+10, y+8), key, font=font, fill=bg_color)
        draw.text((x+100, y+8), value["viento"], font=font, fill=bg_color)
        draw.text((x+180, y+8), value["rafagas"], font=font, fill=bg_color)
        draw.text((x+260, y+8), value["olas_altura"], font=font, fill=bg_color)
        draw.text((x+340, y+8), value["periodo_olas"], font=font, fill=bg_color)
        draw.text((x+420, y+8), value["temperatura_tierra"], font=font, fill=bg_color)
    
        y += 30

    # Devuelve la imagen
    return img
