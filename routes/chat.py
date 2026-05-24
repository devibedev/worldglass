from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.calculator import parse_dimensions, extract_product_type, extract_color, calculate_shower_door

router = APIRouter()

class ChatMessage(BaseModel):
    msg: str


@router.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Endpoint del chatbot que procesa mensajes y genera cotizaciones.

    Procesa lenguaje natural para:
    - Extraer dimensiones (150x190)
    - Identificar tipo de producto (cancel, ventana, barandal)
    - Extraer color (negro, blanco, natural, champagne)
    - Generar cotización con cálculo real
    """
    msg = message.msg.lower()

    # PRIORIDAD 1: Procesar cotización real si hay dimensiones
    dimensions = parse_dimensions(msg)
    if dimensions:
        product_type = extract_product_type(msg)
        color = extract_color(msg)

        if product_type == "cancel":
            quote = calculate_shower_door(
                dimensions["width_cm"],
                dimensions["height_cm"],
                color
            )

            breakdown = quote["breakdown"]
            reply = f"""Calculando con base de datos WorldGlass...<br><br>
✅ Cancel corredizo {dimensions['width_cm']}x{dimensions['height_cm']} {color}<br>
✅ Cristal templado {quote['materials']['glass_type']}<br>
✅ Herrajes importados<br>
✅ Área: {quote['area_m2']} m²<br><br>
<b>Total instalado: ${quote['total_mxn']:,.2f} MXN</b><br><br>
Detalle:<br>
- Aluminio: ${breakdown['aluminum_cost']:,.2f}<br>
- Cristal: ${breakdown['glass_cost']:,.2f}<br>
- Herrajes: ${breakdown['hardware_cost']:,.2f}<br>
- Instalación: ${breakdown['installation_cost']:,.2f}<br>
- Margen (30%): ${breakdown['margin_amount']:,.2f}<br><br>
¿Quieres ver cómo quedaría? Sube foto del espacio"""

            return {"reply": reply}

    # PRIORIDAD 2: Solicitar producto si no hay dimensiones
    # Opción 1: Solicitar producto
    if "1" in msg or "baño" in msg or ("cancel" in msg and not dimensions):
        return {
            "reply": "Perfecto. Para cancel de baño necesito:<br><br>1. Ancho en cm<br>2. Alto en cm<br>3. Color aluminio: Natural, Blanco, Negro o Champagne<br><br>Ejemplo: 150x190 negro"
        }

    # Opción 2: Ventana
    elif "2" in msg or "ventana" in msg or "window" in msg:
        return {
            "reply": "Para ventanas necesito:<br><br>1. Ancho en cm<br>2. Alto en cm<br>3. Tipo: Corrediza, Fija o Batiente<br>4. Color<br><br>Ejemplo: ventana corrediza 120x150 blanco"
        }

    # Opción 3: Barandal
    elif "3" in msg or "barandal" in msg or "railing" in msg:
        return {
            "reply": "Para barandales necesito:<br><br>1. Largo en cm<br>2. Altura en cm<br>3. Estilo: Moderno, Clásico o Minimalista<br>4. Color<br><br>Ejemplo: barandal moderno 300x90 negro"
        }

    # Opción 4: Saludo
    elif "hola" in msg or "hi" in msg:
        return {
            "reply": "Hola 👋 ¿Qué necesitas cotizar?<br>1. Cancel de baño<br>2. Ventana<br>3. Barandal"
        }

    # Opción 5: Default
    else:
        return {
            "reply": f"Procesando: {message.msg}. WorldGlass usa IA para cotizar en segundos 🚀<br><br>Escribe 'cancel 150x190 negro' para ver demo"
        }
