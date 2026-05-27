import re
import math

CUPRUM_SERIE_3_DATA = {
    "configuraciones": {
        "XO_PUERTA_CERCO_TRASLAPE_PUERTA": {
            "perfiles": [
                {"comp": "Riel 3\"", "clave": "69957", "cant": 1, "formula": "AT"},
                {"comp": "Jamba (cabezal)", "clave": "67826", "cant": 1, "formula": "AT"},
                {"comp": "Adaptador paloma", "clave": "adapt_paloma", "cant": 1, "formula": "AT - 65"},
                {"comp": "Jambas", "clave": "67826", "cant": 2, "formula": "ALT - 26"},
                {"comp": "Zoclos", "clave": "67842", "cant": 3, "formula": "(AT - 167) / 3"},
                {"comp": "Cabezales", "clave": "67836", "cant": 3, "formula": "(AT - 167) / 3"},
                {"comp": "Cerco chapa fijo", "clave": "67847", "cant": 1, "formula": "ALT"},
                {"comp": "Cerco chapa corredizo", "clave": "67847", "cant": 1, "formula": "ALT - 40"},
                {"comp": "Traslape fijo", "clave": "67848", "cant": 1, "formula": "ALT"},
                {"comp": "Traslapes corredizos", "clave": "67848", "cant": 3, "formula": "ALT - 40"}
            ],
            "vidrios": [
                {"tipo": "fijo", "cant": 1, "w": "(AT - 117) / 3", "h": "ALT - 95"},
                {"tipo": "corredizo", "cant": 2, "w": "(AT - 117) / 3", "h": "ALT - 135"}
            ]
        },
        "OXXO_PUERTA_MOSQ_CERCO_TRASLAPE_PUERTA": {
            "perfiles": [
                {"comp": "Riel 3\"", "clave": "69957", "cant": 1, "formula": "AT"},
                {"comp": "Jamba c/mosquitero", "clave": "67826", "cant": 1, "formula": "AT"},
                {"comp": "Adaptador mosquitero", "clave": "9966", "cant": 1, "formula": "AT"},
                {"comp": "Jambas", "clave": "67826", "cant": 2, "formula": "ALT - 26"},
                {"comp": "Zoclos", "clave": "67842", "cant": 4, "formula": "(AT - 330) / 4"},
                {"comp": "Cabezales", "clave": "67836", "cant": 4, "formula": "(AT - 330) / 4"},
                {"comp": "Cerco chapa fijos", "clave": "67847", "cant": 2, "formula": "ALT - 30"},
                {"comp": "Cerco chapa corredizos", "clave": "67847", "cant": 2, "formula": "ALT - 40"},
                {"comp": "Traslapes fijos", "clave": "67848", "cant": 2, "formula": "ALT - 30"},
                {"comp": "Traslapes corredizos", "clave": "67848", "cant": 2, "formula": "ALT - 40"},
                {"comp": "Vertical mosquitero", "clave": "66534", "cant": 4, "formula": "ALT - 20"},
                {"comp": "Horizontal mosquitero", "clave": "66533", "cant": 4, "formula": "(AT - 10) / 4"},
                {"comp": "Adaptador OXXO", "clave": "adapt_oxxo", "cant": 2, "formula": "ALT - 50"}
            ],
            "vidrios": [
                {"tipo": "fijo", "cant": 2, "w": "(AT - 265) / 4", "h": "ALT - 125"},
                {"tipo": "corredizo", "cant": 2, "w": "(AT - 265) / 4", "h": "ALT - 135"}
            ]
        }
    }
}

def evaluate_formula(formula: str, at: float, alt: float) -> float:
    """Convierte texto como '(AT - 167) / 3' en un número real"""
    # Sanitización básica: solo permitir números, operadores y AT/ALT
    clean_formula = formula.replace("AT", str(at)).replace("ALT", str(alt))
    try:
        # Usamos un diccionario vacío para __builtins__ por seguridad
        return round(float(eval(clean_formula, {"__builtins__": None}, {})), 2)
    except Exception as e:
        print(f"Error evaluando formula {formula}: {e}")
        return 0.0

def calculate_cuprum_3_despiece(at_mm: float, alt_mm: float, config_id: str, merma_pct: float = 0.05):
    """
    Calcula el despiece completo para la Serie 3 Cuprum.
    """
    config = CUPRUM_SERIE_3_DATA["configuraciones"].get(config_id)
    if not config:
        return {"error": "Configuración no encontrada"}

    resultado = {
        "vista_cliente": {
            "configuracion": config_id.replace("_", " "),
            "dimensiones_totales": {"ancho": at_mm, "alto": alt_mm},
            "vidrios": []
        },
        "vista_tecnica": {
            "cortes_perfiles": [],
            "optimizacion_barras": []
        }
    }

    # 1. Calcular cortes individuales
    claves_totales = {} # Para sumar longitud total por clave de perfil

    for p in config["perfiles"]:
        longitud_corte = evaluate_formula(p["formula"], at_mm, alt_mm)
        resultado["vista_tecnica"]["cortes_perfiles"].append({
            "componente": p["comp"],
            "clave": p["clave"],
            "cantidad": p["cant"],
            "medida_mm": longitud_corte
        })

        # Sumar para el cálculo de barras
        claves_totales[p["clave"]] = claves_totales.get(p["clave"], 0) + (longitud_corte * p["cant"])

    # 2. Calcular vidrios
    for v in config["vidrios"]:
        resultado["vista_cliente"]["vidrios"].append({
            "tipo": v["tipo"],
            "cantidad": v["cant"],
            "ancho_mm": evaluate_formula(v["w"], at_mm, alt_mm),
            "alto_mm": evaluate_formula(v["h"], at_mm, alt_mm)
        })

    # 3. Calcular barras de 6.10m necesarias
    BARRA_STD_MM = 6100
    for clave, longitud_total in claves_totales.items():
        longitud_con_merma = longitud_total * (1 + merma_pct)
        barras_necesarias = math.ceil(longitud_con_merma / BARRA_STD_MM)

        resultado["vista_tecnica"]["optimizacion_barras"].append({
            "clave": clave,
            "longitud_total_mm": round(longitud_total, 2),
            "longitud_con_merma_mm": round(longitud_con_merma, 2),
            "barras_6_10m": barras_necesarias
        })

    return resultado

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
