def calculate_shower_door(width_cm: int, height_cm: int, color: str = "natural", glass_type: str = "9mm") -> dict:
    """
    Calcula precio de cancel de baño basado en dimensiones y materiales.

    Fórmula:
    - Precio por m2 de aluminio (según color)
    - Precio por m2 de cristal (según grosor)
    - Herrajes (fijo)
    - Instalación (fijo)
    - Margen de ganancia (30%)

    Args:
        width_cm: Ancho en centímetros
        height_cm: Alto en centímetros
        color: Color del aluminio (natural, blanco, negro, champagne)
        glass_type: Tipo de cristal (6mm, 8mm, 9mm)

    Returns:
        dict con breakdown del precio
    """
    # Precios base (configurables)
    aluminum_price_per_m2 = {
        "natural": 450,
        "blanco": 520,
        "negro": 580,
        "champagne": 550
    }

    glass_price_per_m2 = {
        "6mm": 350,
        "8mm": 420,
        "9mm": 480
    }

    # Normalizar color y tipo de cristal
    color = color.lower()
    glass_type = glass_type.lower()

    # Usar valores por defecto si no existen
    aluminum_price = aluminum_price_per_m2.get(color, 450)
    glass_price = glass_price_per_m2.get(glass_type, 480)

    # Cálculos
    area_m2 = (width_cm * height_cm) / 10000
    aluminum_cost = area_m2 * aluminum_price
    glass_cost = area_m2 * glass_price
    hardware_cost = 850  # Promedio herrajes
    installation_cost = 1200  # Instalación fija

    subtotal = aluminum_cost + glass_cost + hardware_cost + installation_cost

    # Margen de ganancia (30%)
    final_price = subtotal * 1.3

    return {
        "product": "cancel_bano",
        "dimensions": {"width_cm": width_cm, "height_cm": height_cm},
        "materials": {
            "color": color,
            "glass_type": glass_type
        },
        "breakdown": {
            "aluminum_cost": round(aluminum_cost, 2),
            "glass_cost": round(glass_cost, 2),
            "hardware_cost": hardware_cost,
            "installation_cost": installation_cost,
            "subtotal": round(subtotal, 2),
            "margin_percentage": 30,
            "margin_amount": round(subtotal * 0.3, 2)
        },
        "total_mxn": round(final_price, 2),
        "area_m2": round(area_m2, 2)
    }


def parse_dimensions(text: str) -> dict:
    """
    Extrae dimensiones del texto usando regex (gratuito, sin OpenAI).

    Busca patrones como "150x190", "150 x 190", "150X190"

    Args:
        text: Texto del usuario

    Returns:
        dict con {width, height} o None si no encuentra
    """
    import re

    # Buscar patrón de dimensiones
    match = re.search(r'(\d+)\s*[xX]\s*(\d+)', text)

    if match:
        width = int(match.group(1))
        height = int(match.group(2))

        # Validar rangos razonables
        if 50 <= width <= 300 and 50 <= height <= 300:
            return {"width_cm": width, "height_cm": height}

    return None


def extract_product_type(text: str) -> str:
    """
    Identifica tipo de producto del texto.

    Returns:
        "cancel", "ventana", "barandal" o "unknown"
    """
    text_lower = text.lower()

    if "cancel" in text_lower or "baño" in text_lower:
        return "cancel"
    elif "ventana" in text_lower or "window" in text_lower:
        return "ventana"
    elif "barandal" in text_lower or "railing" in text_lower:
        return "barandal"
    else:
        return "unknown"


def extract_color(text: str) -> str:
    """
    Extrae color del texto.

    Returns:
        Color encontrado o "natural" por defecto
    """
    text_lower = text.lower()

    colors = {
        "negro": "negro",
        "black": "negro",
        "blanco": "blanco",
        "white": "blanco",
        "natural": "natural",
        "champagne": "champagne"
    }

    for color_key, color_value in colors.items():
        if color_key in text_lower:
            return color_value

    return "natural"  # Por defecto
