from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from utils.calculator import calculate_cuprum_despiece, parse_dimensions
from database import get_db
import json
import logging

logger = logging.getLogger(__name__)
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
    
    # 1. Detectar si el usuario menciona Series específicas
    series_keywords = ["serie 2", "serie 3", "cuprum", "2 pulgadas", "3 pulgadas", 
                       "3100", "4100", "5100", "1.5", "1 1/2", "económica",
                       "cancel de baño", "bacalar", "1305", "1306", "inoxidable", 
                       "euroalum", "2500", "2800", "3500", "3800", "3900", "4000", "4500",
                       "templado", "batiente", "cristal", "herraje", "bisagra"]
    
    if any(x in msg for x in series_keywords):
        dims = parse_dimensions(msg)
        
        if dims:
            # El calculador usa mm, parse_dimensions nos da cm
            at_mm = dims["width_cm"] * 10
            alt_mm = dims["height_cm"] * 10
            
            # Por defecto usamos XO, pero si detectamos OXXO cambiamos la config
            if "3100" in msg:
                serie = "3100"
                config_id = "VENTANA_BATIENTE_3100"
            elif "4100" in msg:
                serie = "4100"
                config_id = "XO_VENTANA_4100"
            elif "5100" in msg:
                serie = "5100"
                config_id = "XO_VENTANA_5100"
            elif "1.5" in msg or "1 1/2" in msg or "económica" in msg:
                serie = "1.5"
                config_id = "XO_VENTANA_1_5"
            elif "cancel" in msg or "baño" in msg:
                serie = "cancel_bano"
                config_id = "CANCEL_CORREDIZO_SEMILUJO"
                
                # Detección de sistemas Premium dentro de canceles
                if "bacalar" in msg or "1305" in msg:
                    serie = "premium"
                    config_id = "BACALAR_1305"
                elif "tubular" in msg or "1306" in msg:
                    serie = "premium"
                    config_id = "TUBULAR_1306"

            elif "euroalum 2500" in msg or "2500" in msg:
                serie = "euroalum_2500"
                config_id = "VENTANA_BATIENTE_2500"
            elif "euroalum 2800" in msg or "2800" in msg:
                serie = "euroalum_2800"
                config_id = "XO_VENTANA_2800"
            elif "euroalum 3500" in msg or "3500" in msg:
                serie = "euroalum_3500"
                config_id = "PUERTA_BATIENTE_3500"
            elif "euroalum 3800" in msg or "3800" in msg:
                serie = "euroalum_3800"
                config_id = "XO_VENTANA_3800"
            elif "euroalum 3900" in msg or "3900" in msg:
                serie = "euroalum_3900"
                config_id = "XO_PUERTA_3900"
            elif "euroalum 4000" in msg or "4000" in msg:
                serie = "euroalum_4000"
                config_id = "XO_VENTANA_4000"
            elif "euroalum 4500" in msg or "4500" in msg:
                serie = "euroalum_4500"
                config_id = "XO_PUERTA_4500"

            elif "templado" in msg or "batiente" in msg:
                serie = "tempered"
                config_id = "PUERTA_BATIENTE_TEMPLADO"

            elif "2" in msg:
                serie = "2"
                config_id = "XO_VENTANA_2"
            else:
                serie = "3"
                config_id = "XO_PUERTA_CERCO_TRASLAPE_PUERTA"
                if "oxxo" in msg:
                    config_id = "OXXO_PUERTA_MOSQ_CERCO_TRASLAPE_PUERTA"
                elif "ventana" in msg:
                    config_id = "XO_VENTANA_CERCO_TRASLAPE_VENTANA"
            
            res = calculate_cuprum_despiece(at_mm, alt_mm, config_id, serie=serie)
            
            if "error" in res:
                return {"reply": f"Lo siento, hubo un problema con la configuración: {res['error']}"}

            # Persistencia para auditoría y Fase 1
            try:
                async with get_db() as db:
                    # Buscamos la primera organización disponible para el demo
                    org = await db.fetchrow("SELECT id FROM organizations LIMIT 1")
                    
                    if org:
                        await db.execute(
                            """
                            INSERT INTO quotes (organization_id, total_mxn_cents, details, customer_name, status) 
                            VALUES ($1, $2, $3, $4, $5)
                            """,
                            org["id"],
                            0, 
                            res, # asyncpg maneja dicts directamente para JSONB
                            "Cliente Chat",
                            "draft"
                        )
                    else:
                        logger.warning("No hay organizaciones en la DB para guardar la cotización.")
            except Exception as e:
                logger.error(f"Error persistiendo quote: {e}")

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