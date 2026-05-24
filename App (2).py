from flask import Flask, render_template_string, request, jsonify
import time

app = Flask(__name__)

HTML_CHAT = '''
<!DOCTYPE html>
<html>
<head>
    <title>WorldGlass Demo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #ece5dd; margin:0; }
        .header { background: #075e54; color: white; padding: 15px; font-weight: bold; }
        .chat { padding: 10px; height: 80vh; overflow-y: auto; }
        .msg { margin: 10px 0; padding: 8px 12px; border-radius: 7px; max-width: 70%; }
        .user { background: #dcf8c6; margin-left: auto; }
        .bot { background: white; }
        .input { display: flex; padding: 10px; background: #f0f0f0; }
        input { flex: 1; padding: 10px; border: none; border-radius: 20px; }
        button { background: #075e54; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 50%; }
    </style>
</head>
<body>
    <div class="header">WorldGlass Demo - Cotizador IA</div>
    <div class="chat" id="chat">
        <div class="msg bot">Hola 👋 Soy el bot de WorldGlass. <br><br>¿Qué necesitas cotizar?<br>1. Cancel de baño<br>2. Ventana<br>3. Barandal</div>
    </div>
    <div class="input">
        <input id="texto" placeholder="Escribe aquí..." onkeypress="if(event.key=='Enter') enviar()">
        <button onclick="enviar()">➤</button>
    </div>
    <script>
        function addMsg(text, who) {
            let div = document.createElement('div');
            div.className = 'msg ' + who;
            div.innerHTML = text;
            document.getElementById('chat').appendChild(div);
            document.getElementById('chat').scrollTop = 999999;
        }
        async function enviar() {
            let input = document.getElementById('texto');
            let text = input.value;
            if (!text) return;
            addMsg(text, 'user');
            input.value = '';
            let res = await fetch('/bot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: text})
            });
            let data = await res.json();
            setTimeout(() => addMsg(data.reply, 'bot'), 500);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_CHAT)

@app.route('/bot', methods=['POST'])
def bot():
    msg = request.json['msg'].lower()
    
    if '1' in msg or 'baño' in msg or 'cancel' in msg:
        reply = "Perfecto. Para cancel de baño necesito:<br><br>1. Ancho en cm<br>2. Alto en cm<br>3. Color aluminio: Natural, Blanco, Negro o Champagne<br><br>Ejemplo: 150x190 negro"
    elif '150x190' in msg:
        reply = "Calculando con base de datos WorldGlass...<br><br>✅ Cancel corredizo 150x190 negro mate<br>✅ Cristal templado 9mm<br>✅ Herrajes importados<br><br><b>Total instalado: $8,450 MXN</b><br><br>¿Quieres ver cómo quedaría? Sube foto del espacio"
    elif 'hola' in msg:
        reply = "Hola 👋 ¿Qué necesitas cotizar?<br>1. Cancel de baño<br>2. Ventana<br>3. Barandal"
    else:
        reply = f"Procesando: {msg}. WorldGlass usa IA para cotizar en segundos 🚀<br><br>Escribe 'cancel 150x190 negro' para ver demo"
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=5000, debug=True)