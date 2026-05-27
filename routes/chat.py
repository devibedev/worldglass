from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.calculator import calculate_cuprum_3_despiece, parse_dimensions

router = APIRouter()

class ChatRequest(BaseModel):
    msg: str

@router.post("/chat")
async def chat_message(request: ChatRequest):
    """
    Endpoint que procesa los mensajes del chat. 
    Detecta si el usuario pide Serie 3 y devuelve los arrays de despiece.
    """
    msg = request.msg.lower()
    
    # 1. Detectar si el usuario menciona Serie 3 o Cuprum
    if "serie 3" in msg or "cuprum" in msg:
        dims = parse_dimensions(msg)
        
        if dims:
            # El calculador usa mm, parse_dimensions nos da cm
            at_mm = dims["width_cm"] * 10
            alt_mm = dims["height_cm"] * 10
            
            # Por defecto usamos XO, pero si detectamos OXXO cambiamos la config
            config_id = "XO_PUERTA_CERCO_TRASLAPE_PUERTA"
            if "oxxo" in msg:
                config_id = "OXXO_PUERTA_MOSQ_CERCO_TRASLAPE_PUERTA"
            
            res = calculate_cuprum_3_despiece(at_mm, alt_mm, config_id)
            
            if "error" in res:
                return {"reply": f"Lo siento, hubo un problema con la configuración: {res['error']}"}

            # Devolvemos la respuesta amigable y los datos estructurados
            return {
                "reply": f"¡Entendido! Aquí tienes el despiece para Serie 3 ({config_id}) de {dims['width_cm']}x{dims['height_cm']}cm.",
                "vista_cliente": res["vista_cliente"],
                "vista_tecnica": res["vista_tecnica"]
            }
        else:
            return {"reply": "Detecto que quieres cotizar Serie 3, pero necesito las medidas. ¿Podrías decirme el Ancho x Alto? (Ejemplo: 200x150)"}

    # Respuesta genérica para otros casos en Fase 1
    return {"reply": "¡Hola! Por ahora puedo ayudarte con el despiece técnico de la Serie 3 de Cuprum. Solo dime las medidas."}

@router.get("/chat/status")
async def chat_status():
    return {"status": "Chat engine online - Serie 3 integration active"}