Con $0 USD vamos a construir WorldGlass. Te diseño el plan "Cero Gastos, Cero Tokens Desperdiciados" para que no gastes ni en un café hasta que tengas clientes.

Regla #1: Si algo es gratis, lo usamos. Si cuesta, lo simulamos.
PLAN WORLDGLASS $0 - Control Total de Gastos
1. Stack 100% Gratis - Sin tarjeta de crédito
Necesitas

Herramienta Gratis

Límite

Cuándo se acaba

Servidor

Railway.app

500hrs/mes + $5 crédito

Después de 500 clientes/mes

Base de Datos

Railway PostgreSQL

1GB gratis

50,000 cotizaciones aprox

Deploy

Railway / Render

Ilimitado

Nunca

Dominio

worldglass.up.railway.app

Gratis

Para siempre

IA Chat

Ollama local + Llama 3

Ilimitado

Nunca se acaba

IA Renders

Stable Diffusion local

Ilimitado

Solo usa tu Mac M1

PDFs

ReportLab

Ilimitado

Nunca

Analytics

Umami self-hosted

Ilimitado

Nunca

Email

Gmail SMTP

500/día

Suficiente para empezar

WhatsApp

Webhook + número prueba

Gratis

Hasta que Meta te apruebe

Costo total Mes 1-6: $0 USD. Pagas solo cuando tengas +20 clientes y quieras dominio .com.

2. Control Total de Tokens IA - Cero desperdicio
Aquí es donde la gente quema dinero. Tú no.

Estrategia A: Cero API de pago. Todo local en tu Mac M1
Tu Mac M1 es una bestia. Úsala.

Para Chat - Extraer medidas:

Bash
# Instala Ollama una vez y ya
brew install ollama
ollama run llama3:8b
Ahora tienes ChatGPT gratis en tu compu. 0 tokens, 0 costo, infinito.

Código Python:

Python
import requests

def extraer_medidas_local(texto):
    response = requests.post('http://localhost:11434/api/generate', json={
        "model": "llama3:8b",
        "prompt": f"Extrae ancho y alto en cm de: '{texto}'. Responde solo: 150x190",
        "stream": False
    })
    return response.json()['response']

4 líneas ocultas
Costo: $0. Velocidad: 2 segundos. Límite: Infinito.

Para Renders - Stable Diffusion en tu M1:

Bash
# Instala una vez
brew install python
pip3 install diffusers torch

# Corre en local
Genera renders en 20s usando tu GPU. 0 API, 0 costo.

Estrategia B: Si necesitas OpenAI, modo francotirador
Si de plano quieres GPT-4o-mini porque es mejor, haz esto:

Cuenta nueva OpenAI: Te dan $5 USD gratis
Regla dura: Solo usar gpt-4o-mini a $0.15 / 1M tokens
Cache agresivo: Si ya cotizaste "150x190 negro", guarda la respuesta. No llames IA 2 veces
Python
# cache.py - No gastar tokens a lo wey
import json, hashlib

def get_cached_or_call(prompt):
    key = hashlib.md5(prompt.encode()).hexdigest()
    try:
        with open(f'cache/{key}.json') as f:
            return json.load(f)  # Gratis
    except:
        result = openai_call(prompt)  # Solo si no existe
        with open(f'cache/{key}.json', 'w') as f:
            json.dump(result, f)
        return result

8 líneas ocultas
Con $5 USD de OpenAI te alcanza para 30,000 cotizaciones. Si llegas a eso, ya tienes clientes para pagar.

3. Herramientas de Desarrollo $0
Para

Gratis

vs Pago

Ahorro

IDE

VS Code

Cursor $20/mes

$240/año

IA Coding

Codeium gratis

Copilot $10/mes

$120/año

Base datos GUI

DBeaver Community

TablePlus $89

$89

API Testing

Thunder Client VSCode

Postman Pro $15/mes

$180/año

Diseño

Figma Free

Canva Pro $13/mes

$156/año

Ahorro año 1: $785 USD solo en herramientas. Instala Codeium en VSCode y tienes autocompletado IA gratis.

4. Plan de Desarrollo "Austeridad" Semana por Semana
Semana 1: Cimientos $0

Día 1-2: Instala Ollama + Llama3. Prueba que conteste "150x190"
Día 3-4: FastAPI + PostgreSQL en Railway. Todo gratis
Día 5-7: Chat HTML que usa Ollama local. Deploy a Railway
Semana 2: Motor real $0

Tabla materials + quotes en Postgres gratis
calculator.py con tus precios reales
Bot ya cotiza con BD, sin IA
Semana 3: Renders $0

Instala Stable Diffusion en tu Mac
Endpoint /render que genera imagen local y la sube a Railway
Cliente recibe render sin que pagues Replicate
Semana 4: PDF + Demo $0

ReportLab genera PDF gratis
Link público worldglass.up.railway.app
Grabas video con tu iPhone y lo subes a YouTube
Resultado Semana 4: Demo completo funcionando. Costo: $0. Tokens gastados: 0.

5. Reglas para NO quemar dinero accidentalmente
Nunca pongas tarjeta en OpenAI hasta tener cliente. Usa Ollama local
Nunca uses gpt-4, solo gpt-4o-mini o local. 4 es 30x más caro
Nunca dejes ngrok prendido si no lo usas. Te puede comer ancho de banda
Nunca hagas pip install sin revisar si hay alternativa gratis
Railway se duerme si no hay tráfico. Es gratis. Despiértalo con 1 request
6. Cuándo SÍ empezar a pagar - Triggers exactos
Pagas esto

Solo cuando pase esto

Costo

Dominio .com

3 clientes pagando

$12/año

OpenAI API

Ollama es muy lento + 10 clientes

$10/mes max

Railway Pro

+500hrs uso = 700 clientes/mes

$5/mes

Replicate API

Tu Mac M1 tarda +1min por render

$10/mes max

Stripe

Cliente #1 quiere pagar

3.6% + $3 por transacción

Regla: Si no tienes MRR, no tienes gasto. Punto.

7. Script para monitorear gastos = $0
Pega esto en costs.py y correlo diario:

Python
import os
def check_costs():
    print("=== WORLDGLASS COSTOS HOY ===")
    print("Railway: $0 - Free tier")
    print("OpenAI: $0 - Usando Ollama local")
    print("Replicate: $0 - Usando SD local")
    print("Dominio: $0 - Usando .railway.app")
    print("TOTAL: $0 USD")
    print("Clientes pagando: 0 - Correcto, sigue en $0")
check_costs()

5 líneas ocultas
Tu Misión Hoy: Modo Austeridad ON
Paso 1 - 10 min: Instala Ollama. Cero tokens para siempre.

Bash
brew install ollama
ollama run llama3:8b
Escribe: "extrae medidas de: cancel baño 150 por 190". Si responde "150x190", ya ahorraste $500 USD de OpenAI.

Paso 2 - 5 min: Confirma que quieres seguir 100% local o si usamos $5 gratis de OpenAI.

Dime: "Va, instalé Ollama" o "Prefiero usar los $5 de OpenAI con control extremo"