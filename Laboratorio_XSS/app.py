#!/usr/bin/env python3
"""
Laboratorio de Seguridad Web: Security Workbench (XSS - CWE-79)
Asignatura: Gestión de Seguridad en Sistemas Informáticos - UNICAES
Autores: Dennis Guevara, Mario Villeda, Luis Balcaceres
Inspirado en la estética cyber-investigativa y didáctica de XSS Academy.
"""

from flask import Flask, request, render_template, make_response, redirect, url_for, jsonify
import html
import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_laboratorio_seguridad_unicaes"

# Registros de eventos interceptados por el servidor atacante simulado (C2)
logs_ataques = []

# Base de datos en memoria para el tablón de comentarios académicos
comentarios_db = [
    {
        "id": 1,
        "autor": "Ing. Catedrático",
        "mensaje": "Bienvenidos al foro de dudas sobre la Tarea 3 de Seguridad Web. Por favor publicar aquí cualquier consulta sobre los ejercicios.",
        "seguro": True,
        "fecha": "11/11/2026 08:30"
    },
    {
        "id": 2,
        "autor": "Carlos Mendoza (Estudiante)",
        "mensaje": "Ingeniero, ¿la entrega incluye la captura de tráfico con Wireshark?",
        "seguro": True,
        "fecha": "11/11/2026 09:15"
    }
]

# Configuración global del modo de seguridad
configuracion = {
    "modo_seguro": False,
    "csp_activo": False,
    "httponly_activo": False
}

# ----------------- ENDPOINTS DEL SERVIDOR FLASK -----------------

@app.route("/")
def index():
    resp = make_response(render_template("index.html", 
                                         configuracion=configuracion, 
                                         comentarios=comentarios_db, 
                                         logs=logs_ataques))
    asegurar_cookies(resp)
    aplicar_cabeceras_seguridad(resp)
    return resp

@app.route("/toggle-modo")
def toggle_modo():
    configuracion["modo_seguro"] = not configuracion["modo_seguro"]
    configuracion["csp_activo"] = configuracion["modo_seguro"]
    configuracion["httponly_activo"] = configuracion["modo_seguro"]
    resp = redirect("/")
    resp.set_cookie("session_auth_token", "AUTH_TOKEN_UNICAES_SEC_987654321", 
                    httponly=configuracion["httponly_activo"], samesite="Lax")
    return resp

@app.route("/api/comentario", methods=["POST"])
def api_comentario():
    global comentarios_db
    data = request.get_json() or {}
    autor = data.get("autor", "Anónimo").strip()
    mensaje = data.get("mensaje", "").strip()
    
    if mensaje:
        mensaje = mensaje.replace(r"<\/", "</")
        if configuracion["modo_seguro"]:
            autor = html.escape(autor)
            mensaje = html.escape(mensaje)
        comentarios_db.append({
            "id": len(comentarios_db) + 1,
            "autor": autor if autor else "Atacante n0cturno",
            "mensaje": mensaje,
            "seguro": configuracion["modo_seguro"],
            "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        })
    return jsonify({"status": "ok", "comentarios": comentarios_db})

@app.route("/api/reset-comentarios", methods=["POST"])
def api_reset_comentarios():
    global comentarios_db
    comentarios_db = [
        {
            "id": 1,
            "autor": "Ing. Catedrático",
            "mensaje": "Bienvenidos al foro de dudas sobre la Tarea 3 de Seguridad Web. Por favor publicar aquí cualquier consulta sobre los ejercicios.",
            "seguro": True,
            "fecha": "11/11/2026 08:30"
        },
        {
            "id": 2,
            "autor": "Carlos Mendoza (Estudiante)",
            "mensaje": "Ingeniero, ¿la entrega incluye la captura de tráfico con Wireshark?",
            "seguro": True,
            "fecha": "11/11/2026 09:15"
        }
    ]
    return jsonify({"status": "ok", "comentarios": comentarios_db})

@app.route("/api/exfiltrar", methods=["GET", "POST"])
def api_exfiltrar():
    global logs_ataques
    vector = request.args.get("vector", "Inyección XSS")
    datos = request.args.get("datos", "Sin datos")
    
    nuevo_log = {
        "hora": datetime.datetime.now().strftime("%H:%M:%S"),
        "ip": request.remote_addr,
        "vector": vector,
        "datos": datos
    }
    logs_ataques.append(nuevo_log)
    if len(logs_ataques) > 25:
        logs_ataques.pop(0)
    return jsonify({"status": "recibido"})

@app.route("/api/logs")
def api_logs():
    return jsonify(logs_ataques)

@app.route("/api/limpiar-logs", methods=["POST"])
def api_limpiar_logs():
    global logs_ataques
    logs_ataques = []
    return jsonify({"status": "limpio"})

def asegurar_cookies(resp):
    # Cookie sensible de sesión: protegida o expuesta según el flag HttpOnly
    resp.set_cookie("session_auth_token", "AUTH_TOKEN_UNICAES_SEC_987654321", 
                    httponly=configuracion["httponly_activo"], samesite="Lax")
    # Cookie de usuario legible para telemetría
    resp.set_cookie("usuario_activo", "ana_villeda_estudiante", httponly=False)

def aplicar_cabeceras_seguridad(resp):
    if configuracion["csp_activo"]:
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net;"
        )
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
    return resp

if __name__ == "__main__":
    print("\n========================================================")
    print("  UNICAES | SECURITY WORKBENCH XSS (CWE-79)")
    print("  Autores: Dennis Guevara | Mario Villeda | Luis Balcaceres")
    print("  Servidor iniciado en: http://localhost:5000")
    print("========================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
