#!/usr/bin/env python3
"""
Generador de Diagramas y Gráficos Visuales para la Presentación de XSS
Universidad Católica de El Salvador (UNICAES)
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_REG = "/usr/share/fonts/google-noto/NotoSans-Regular.ttf"
FONT_PATH_BOLD = "/usr/share/fonts/google-noto/NotoSans-Bold.ttf"

def get_font(size, bold=False):
    path = FONT_PATH_BOLD if bold else FONT_PATH_REG
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

# Paleta de Colores
BG_COLOR       = (15, 23, 42)      # #0F172A Fondo oscuro
PANEL_COLOR    = (30, 41, 59)      # #1E293B Card interior
PANEL_ALT      = (26, 38, 57)      # Card secundario
BORDER_COLOR   = (51, 65, 85)      # Borde gris azulado
CYAN           = (0, 232, 198)     # #00E8C6 Cyan
BLUE           = (56, 189, 248)    # #38BDF8 Azul
RED            = (239, 68, 68)     # #EF4444 Rojo
AMBER          = (245, 158, 11)    # #F59E0B Ámbar
GREEN          = (16, 185, 129)    # #10B981 Verde
TEXT_WHITE     = (248, 250, 252)   # Blanco
TEXT_MUTED     = (148, 163, 184)   # Gris

def draw_arrow(draw, start, end, color=CYAN, width=3):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    # Flecha simple
    if x2 > x1: # Horizontal hacia derecha
        draw.polygon([(x2, y2), (x2-12, y2-7), (x2-12, y2+7)], fill=color)
    elif y2 > y1: # Vertical hacia abajo
        draw.polygon([(x2, y2), (x2-7, y2-12), (x2+7, y2-12)], fill=color)

# -------------------------------------------------------------
# 1. IMAGEN: ¿QUÉ ES XSS?
# -------------------------------------------------------------
def crear_img_que_es_xss(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Marco
    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    # Título superior del diagrama
    f_tit = get_font(22, bold=True)
    draw.text((40, 35), "DIAGRAMA CONCEPTUAL: INYECCIÓN DE SCRIPT", fill=CYAN, font=f_tit)

    f_sub = get_font(14)
    draw.text((40, 68), "El atacante burla la confianza del navegador para ejecutar código en la víctima.", fill=TEXT_MUTED, font=f_sub)

    # Paso 1: Atacante
    draw.rounded_rectangle([40, 115, 300, 280], radius=12, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((60, 130), "1. ATACANTE", fill=RED, font=get_font(18, bold=True))
    draw.text((60, 165), "• Diseña un payload malicioso:", fill=TEXT_WHITE, font=get_font(14))
    draw.rounded_rectangle([55, 195, 285, 255], radius=6, fill=(11, 19, 43))
    draw.text((65, 205), "<script>", fill=AMBER, font=get_font(13, bold=True))
    draw.text((65, 225), "  robarCookies();", fill=CYAN, font=get_font(13))
    draw.text((65, 240), "</script>", fill=AMBER, font=get_font(13, bold=True))

    # Flecha 1 -> 2
    draw_arrow(draw, (305, 195), (355, 195), color=RED, width=4)
    draw.text((310, 170), "Inyección", fill=RED, font=get_font(12, bold=True))

    # Paso 2: Servidor Web Vulnerable
    draw.rounded_rectangle([360, 115, 620, 280], radius=12, fill=PANEL_COLOR, outline=AMBER, width=2)
    draw.text((380, 130), "2. WEB VULNERABLE", fill=AMBER, font=get_font(18, bold=True))
    draw.text((380, 165), "• Recibe la entrada del usuario.", fill=TEXT_WHITE, font=get_font(14))
    draw.text((380, 195), "• NO valida ni codifica datos.", fill=RED, font=get_font(14, bold=True))
    draw.text((380, 225), "• Concatena el script directo", fill=TEXT_WHITE, font=get_font(14))
    draw.text((380, 245), "  en la página HTML devuelta.", fill=TEXT_WHITE, font=get_font(14))

    # Flecha 2 -> 3
    draw_arrow(draw, (625, 195), (675, 195), color=BLUE, width=4)
    draw.text((630, 170), "HTML", fill=BLUE, font=get_font(12, bold=True))

    # Paso 3: Navegador de la Víctima
    draw.rounded_rectangle([680, 115, 910, 280], radius=12, fill=PANEL_COLOR, outline=BLUE, width=2)
    draw.text((700, 130), "3. NAVEGADOR VÍCTIMA", fill=BLUE, font=get_font(18, bold=True))
    draw.text((700, 165), "• Recibe el HTML con el script.", fill=TEXT_WHITE, font=get_font(14))
    draw.text((700, 195), "• Confía en el sitio web.", fill=CYAN, font=get_font(14))
    draw.text((700, 225), "• ¡Ejecuta el JavaScript", fill=RED, font=get_font(14, bold=True))
    draw.text((700, 245), "  con privilegios plenos!", fill=RED, font=get_font(14, bold=True))

    # Flecha hacia abajo (Consecuencia)
    draw_arrow(draw, (795, 285), (795, 335), color=RED, width=4)

    # Paso 4: Impacto y Consecuencia
    draw.rounded_rectangle([40, 345, 910, 580], radius=12, fill=PANEL_COLOR, outline=CYAN, width=2)
    draw.text((60, 365), "4. CONSECUENCIAS DIRECTAS DEL ATAQUE (IMPACTO)", fill=CYAN, font=get_font(18, bold=True))

    # 3 Tarjetas de Consecuencia
    draw.rounded_rectangle([60, 405, 320, 555], radius=8, fill=(11, 19, 43), outline=BORDER_COLOR)
    draw.text((75, 420), "🔑 Secuestro de Sesión", fill=RED, font=get_font(15, bold=True))
    draw.text((75, 450), "El script extrae las cookies", fill=TEXT_WHITE, font=get_font(13))
    draw.text((75, 470), "de autenticación y las envía", fill=TEXT_WHITE, font=get_font(13))
    draw.text((75, 490), "al atacante (Session Hijack).", fill=TEXT_WHITE, font=get_font(13))

    draw.rounded_rectangle([345, 405, 625, 555], radius=8, fill=(11, 19, 43), outline=BORDER_COLOR)
    draw.text((360, 420), "🎭 Phishing In-Site", fill=AMBER, font=get_font(15, bold=True))
    draw.text((360, 450), "Inyecta formularios falsos", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 470), "dentro del sitio legítimo con", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 490), "candado HTTPS verde activo.", fill=TEXT_WHITE, font=get_font(13))

    draw.rounded_rectangle([650, 405, 890, 555], radius=8, fill=(11, 19, 43), outline=BORDER_COLOR)
    draw.text((665, 420), "💥 Desfiguración Web", fill=BLUE, font=get_font(15, bold=True))
    draw.text((665, 450), "Modifica el DOM, texto,", fill=TEXT_WHITE, font=get_font(13))
    draw.text((665, 470), "imágenes y realiza acciones", fill=TEXT_WHITE, font=get_font(13))
    draw.text((665, 490), "en nombre del usuario.", fill=TEXT_WHITE, font=get_font(13))

    img.save(output_path)
    print(f"Generado: {output_path}")

# -------------------------------------------------------------
# 2. IMAGEN: XSS REFLEJADO
# -------------------------------------------------------------
def crear_img_xss_reflejado(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    draw.text((40, 35), "TIPO 1: XSS REFLEJADO (NO PERSISTENTE)", fill=CYAN, font=get_font(22, bold=True))
    draw.text((40, 68), "El script malicioso viaja en la petición (URL) y se refleja en la respuesta sin guardarse.", fill=TEXT_MUTED, font=get_font(14))

    # Flujo en 4 pasos
    # Caja 1: Enlace Atacante
    draw.rounded_rectangle([40, 115, 440, 240], radius=10, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((55, 125), "PASO 1: ENLACE MALICIOSO", fill=RED, font=get_font(16, bold=True))
    draw.text((55, 150), "El atacante crea un enlace manipulado:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([50, 175, 430, 225], radius=6, fill=(11, 19, 43))
    draw.text((60, 185), "portal.com/buscar?q=", fill=TEXT_MUTED, font=get_font(12))
    draw.text((195, 185), "<script>alert(1)</script>", fill=CYAN, font=get_font(12, bold=True))
    draw.text((60, 205), "Enviado por correo, chat o phishing.", fill=AMBER, font=get_font(11))

    # Caja 2: Víctima Clic
    draw.rounded_rectangle([510, 115, 910, 240], radius=10, fill=PANEL_COLOR, outline=AMBER, width=2)
    draw.text((525, 125), "PASO 2: VÍCTIMA HACE CLIC", fill=AMBER, font=get_font(16, bold=True))
    draw.text((525, 150), "• La víctima desprevenida pulsa el link.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((525, 175), "• El navegador envía la petición HTTP GET", fill=TEXT_WHITE, font=get_font(13))
    draw.text((525, 195), "  al servidor de la aplicación legítima.", fill=TEXT_WHITE, font=get_font(13))

    # Flecha 1 -> 2
    draw_arrow(draw, (445, 175), (505, 175), color=AMBER, width=3)

    # Flecha hacia abajo a paso 3
    draw_arrow(draw, (710, 245), (710, 285), color=BLUE, width=3)

    # Caja 3: Servidor Refleja
    draw.rounded_rectangle([510, 290, 910, 420], radius=10, fill=PANEL_COLOR, outline=BLUE, width=2)
    draw.text((525, 300), "PASO 3: RESPUESTA DEL SERVIDOR", fill=BLUE, font=get_font(16, bold=True))
    draw.text((525, 325), "• El servidor lee 'q' y lo incrusta:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([520, 350, 900, 400], radius=6, fill=(11, 19, 43))
    draw.text((530, 360), "<p>Resultados para: <script>alert(1)</script></p>", fill=RED, font=get_font(11))
    draw.text((530, 380), "¡No se guarda en BD! Solo se refleja.", fill=TEXT_MUTED, font=get_font(11))

    # Flecha 3 -> 4
    draw_arrow(draw, (505, 355), (445, 355), color=RED, width=3)

    # Caja 4: Ejecución en Víctima
    draw.rounded_rectangle([40, 290, 440, 420], radius=10, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((55, 300), "PASO 4: EJECUCIÓN DEL SCRIPT", fill=RED, font=get_font(16, bold=True))
    draw.text((55, 325), "• El navegador procesa la respuesta.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 350), "• Se ejecuta el código JavaScript.", fill=CYAN, font=get_font(13, bold=True))
    draw.text((55, 375), "• Se exfiltran cookies o datos privados.", fill=RED, font=get_font(13))

    # Caja de Resumen inferior
    draw.rounded_rectangle([40, 445, 910, 580], radius=10, fill=(11, 19, 43), outline=CYAN, width=2)
    draw.text((60, 460), "CARACTERÍSTICAS CLAVE DEL XSS REFLEJADO:", fill=CYAN, font=get_font(16, bold=True))
    draw.text((60, 490), "✔ NO PERSISTENTE: El script solo dura lo que tarda la petición y no queda en el servidor.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 515), "✔ REQUIERE INGENIERÍA SOCIAL: La víctima debe hacer clic voluntariamente en el enlace.", fill=AMBER, font=get_font(13, bold=True))
    draw.text((60, 540), "✔ MITIGACIÓN DIRECTA: Codificar entidades HTML (html.escape) en todos los parámetros GET.", fill=GREEN, font=get_font(13, bold=True))

    img.save(output_path)
    print(f"Generado: {output_path}")

# -------------------------------------------------------------
# 3. IMAGEN: XSS ALMACENADO
# -------------------------------------------------------------
def crear_img_xss_almacenado(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    draw.text((40, 35), "TIPO 2: XSS ALMACENADO (PERSISTENTE) - MÁXIMA GRAVEDAD", fill=RED, font=get_font(22, bold=True))
    draw.text((40, 68), "El código malicioso se guarda permanentemente en la base de datos del servidor.", fill=TEXT_MUTED, font=get_font(14))

    # Flujo
    # Caja 1: Atacante publica
    draw.rounded_rectangle([40, 115, 290, 260], radius=10, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((55, 125), "1. ATACANTE", fill=RED, font=get_font(16, bold=True))
    draw.text((55, 155), "Publica un comentario", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 175), "o mensaje en el foro con", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 195), "script inyectado oculto.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 225), "📝 Formulario POST", fill=AMBER, font=get_font(12, bold=True))

    draw_arrow(draw, (295, 185), (345, 185), color=RED, width=3)

    # Caja 2: Base de Datos Servidor
    draw.rounded_rectangle([350, 115, 600, 260], radius=10, fill=PANEL_COLOR, outline=AMBER, width=2)
    draw.text((365, 125), "2. BASE DE DATOS", fill=AMBER, font=get_font(16, bold=True))
    draw.text((365, 155), "El servidor guarda el", fill=TEXT_WHITE, font=get_font(13))
    draw.text((365, 175), "payload en crudo sin filtrar.", fill=RED, font=get_font(13, bold=True))
    draw.text((365, 205), "💾 Queda grabado", fill=TEXT_WHITE, font=get_font(13))
    draw.text((365, 225), "de forma permanente.", fill=TEXT_WHITE, font=get_font(13))

    draw_arrow(draw, (605, 185), (655, 185), color=BLUE, width=3)

    # Caja 3: Entrega a Múltiples Víctimas
    draw.rounded_rectangle([660, 115, 910, 260], radius=10, fill=PANEL_COLOR, outline=CYAN, width=2)
    draw.text((675, 125), "3. SERVIDO A TODOS", fill=CYAN, font=get_font(16, bold=True))
    draw.text((675, 155), "Cualquier estudiante o", fill=TEXT_WHITE, font=get_font(13))
    draw.text((675, 175), "docente que entre al foro", fill=TEXT_WHITE, font=get_font(13))
    draw.text((675, 195), "recibe el comentario", fill=TEXT_WHITE, font=get_font(13))
    draw.text((675, 225), "infectado como legítimo.", fill=RED, font=get_font(13, bold=True))

    # Flecha hacia abajo
    draw_arrow(draw, (785, 265), (785, 305), color=RED, width=3)

    # Caja 4: Infección Masiva
    draw.rounded_rectangle([40, 310, 910, 440], radius=10, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((60, 325), "4. INFECCIÓN PASIVA Y MASIVA (CERO INTERACCIÓN EXTRA)", fill=RED, font=get_font(16, bold=True))
    draw.text((60, 355), "• La víctima NO necesita pulsar ningún enlace externo ni sospechoso.", fill=TEXT_WHITE, font=get_font(14))
    draw.text((60, 380), "• Basta con navegar al foro de la universidad para que el script se ejecute.", fill=AMBER, font=get_font(14, bold=True))
    draw.text((60, 405), "• El atacante puede robar las sesiones de cientos de usuarios en segundos.", fill=CYAN, font=get_font(14))

    # Resumen
    draw.rounded_rectangle([40, 460, 910, 580], radius=10, fill=(11, 19, 43), outline=BORDER_COLOR)
    draw.text((60, 475), "¿POR QUÉ ES EL MÁS PELIGROSO?", fill=AMBER, font=get_font(15, bold=True))
    draw.text((60, 505), "1. No depende del error de un usuario individual (no requiere phishing).", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 528), "2. Afecta potencialmente a administradores del sistema con privilegios elevados.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 551), "3. Permanece latente hasta que un administrador limpie manualmente la base de datos.", fill=TEXT_WHITE, font=get_font(13))

    img.save(output_path)
    print(f"Generado: {output_path}")

# -------------------------------------------------------------
# 4. IMAGEN: XSS BASADO EN DOM
# -------------------------------------------------------------
def crear_img_xss_dom(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    draw.text((40, 35), "TIPO 3: XSS BASADO EN DOM (CLIENT-SIDE)", fill=AMBER, font=get_font(22, bold=True))
    draw.text((40, 68), "Ocurre 100% en el navegador cliente. El servidor backend nunca ve el ataque.", fill=TEXT_MUTED, font=get_font(14))

    # Diagrama Fuente -> Script -> Sumidero
    # Fuente (Source)
    draw.rounded_rectangle([40, 115, 300, 270], radius=10, fill=PANEL_COLOR, outline=CYAN, width=2)
    draw.text((55, 125), "1. FUENTE (SOURCE)", fill=CYAN, font=get_font(16, bold=True))
    draw.text((55, 155), "Datos controlados por el", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 175), "usuario en el navegador:", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 205), "• location.hash (#...)", fill=AMBER, font=get_font(13, bold=True))
    draw.text((55, 225), "• document.referrer", fill=TEXT_WHITE, font=get_font(13))
    draw.text((55, 245), "• window.name", fill=TEXT_WHITE, font=get_font(13))

    draw_arrow(draw, (305, 190), (355, 190), color=CYAN, width=3)

    # Script Intermedio
    draw.rounded_rectangle([360, 115, 610, 270], radius=10, fill=PANEL_COLOR, outline=BLUE, width=2)
    draw.text((375, 125), "2. SCRIPT LOCAL", fill=BLUE, font=get_font(16, bold=True))
    draw.text((375, 155), "JavaScript lee la fuente:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([370, 180, 600, 245], radius=6, fill=(11, 19, 43))
    draw.text((380, 190), "var h = location.hash;", fill=TEXT_WHITE, font=get_font(11))
    draw.text((380, 215), "// Pasa el dato directo", fill=TEXT_MUTED, font=get_font(11))
    draw.text((380, 230), "div.innerHTML = h;", fill=RED, font=get_font(11, bold=True))

    draw_arrow(draw, (615, 190), (665, 190), color=RED, width=3)

    # Sumidero (Sink)
    draw.rounded_rectangle([670, 115, 910, 270], radius=10, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((685, 125), "3. SUMIDERO (SINK)", fill=RED, font=get_font(16, bold=True))
    draw.text((685, 155), "Función peligrosa de DOM:", fill=TEXT_WHITE, font=get_font(13))
    draw.text((685, 185), "• element.innerHTML", fill=RED, font=get_font(13, bold=True))
    draw.text((685, 205), "• document.write()", fill=RED, font=get_font(13))
    draw.text((685, 225), "• eval()", fill=RED, font=get_font(13))
    draw.text((685, 245), "¡Fuerza parseo de código!", fill=AMBER, font=get_font(12, bold=True))

    # Caja: Por qué el servidor no interviene
    draw.rounded_rectangle([40, 295, 910, 435], radius=10, fill=PANEL_COLOR, outline=AMBER, width=2)
    draw.text((60, 310), "🚫 EL ROL DEL SERVIDOR: COMPLETAMENTE OMITIDO", fill=AMBER, font=get_font(16, bold=True))
    draw.text((60, 340), "• En el protocolo HTTP, el fragmento de la URL después del numeral (#) NUNCA se envía al servidor.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 365), "• Los Web Application Firewalls (WAF) son 100% CIEGOS ante este tipo de ataque.", fill=RED, font=get_font(13, bold=True))
    draw.text((60, 390), "• La solución debe aplicarse en el frontend: usar 'element.textContent' en lugar de 'innerHTML'.", fill=GREEN, font=get_font(13, bold=True))

    # Comparativa de código abajo
    draw.rounded_rectangle([40, 455, 460, 580], radius=8, fill=(11, 19, 43), outline=RED)
    draw.text((55, 465), "❌ INSEGURO (innerHTML)", fill=RED, font=get_font(14, bold=True))
    draw.text((55, 495), "caja.innerHTML = userParam;", fill=RED, font=get_font(12))
    draw.text((55, 525), "Interpreta etiquetas <img onerror>", fill=TEXT_MUTED, font=get_font(11))
    draw.text((55, 545), "y ejecuta el script del atacante.", fill=TEXT_MUTED, font=get_font(11))

    draw.rounded_rectangle([490, 455, 910, 580], radius=8, fill=(11, 19, 43), outline=GREEN)
    draw.text((505, 465), "✔ SEGURO (textContent)", fill=GREEN, font=get_font(14, bold=True))
    draw.text((505, 495), "caja.textContent = userParam;", fill=GREEN, font=get_font(12))
    draw.text((505, 525), "Trata todo como caracteres literales.", fill=TEXT_MUTED, font=get_font(11))
    draw.text((505, 545), "Cero riesgo de ejecución.", fill=TEXT_MUTED, font=get_font(11))

    img.save(output_path)
    print(f"Generado: {output_path}")

# -------------------------------------------------------------
# 5. IMAGEN: PREVENCIÓN / RESUMEN
# -------------------------------------------------------------
def crear_img_prevencion(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    draw.text((40, 35), "RESUMEN: ¿CÓMO PREVENIR Y ERRADICAR XSS?", fill=GREEN, font=get_font(22, bold=True))
    draw.text((40, 68), "Las tres defensas fundamentales que neutralizan el riesgo en cualquier aplicación.", fill=TEXT_MUTED, font=get_font(14))

    # 3 Columnas
    # Pilar 1: Codificación
    draw.rounded_rectangle([40, 115, 310, 560], radius=12, fill=PANEL_COLOR, outline=CYAN, width=2)
    draw.text((60, 135), "1. CODIFICACIÓN", fill=CYAN, font=get_font(18, bold=True))
    draw.text((60, 160), "(OUTPUT ENCODING)", fill=CYAN, font=get_font(13))
    draw.text((60, 195), "Convertir caracteres de", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 215), "control sintáctico a", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 235), "entidades visuales:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([55, 270, 295, 370], radius=6, fill=(11, 19, 43))
    draw.text((70, 285), "<  -->  &lt;", fill=AMBER, font=get_font(14, bold=True))
    draw.text((70, 315), ">  -->  &gt;", fill=AMBER, font=get_font(14, bold=True))
    draw.text((70, 345), "\"  -->  &quot;", fill=AMBER, font=get_font(14, bold=True))
    draw.text((60, 395), "El navegador lo dibuja", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 415), "como texto plano y", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 435), "NUNCA lo ejecuta.", fill=GREEN, font=get_font(13, bold=True))

    # Pilar 2: Cookies HttpOnly
    draw.rounded_rectangle([340, 115, 610, 560], radius=12, fill=PANEL_COLOR, outline=BLUE, width=2)
    draw.text((360, 135), "2. COOKIES SEGURAS", fill=BLUE, font=get_font(18, bold=True))
    draw.text((360, 160), "(BANDERA HTTPONLY)", fill=BLUE, font=get_font(13))
    draw.text((360, 195), "Proteger el secreto de", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 215), "sesión en Set-Cookie:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([355, 270, 595, 370], radius=6, fill=(11, 19, 43))
    draw.text((365, 290), "Set-Cookie: token=...;", fill=TEXT_MUTED, font=get_font(11))
    draw.text((365, 315), "  HttpOnly;", fill=GREEN, font=get_font(13, bold=True))
    draw.text((365, 335), "  Secure; SameSite=Lax", fill=BLUE, font=get_font(12))
    draw.text((360, 395), "Oculta la cookie a", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 415), "document.cookie.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 435), "¡Impide el robo de sesión!", fill=GREEN, font=get_font(13, bold=True))

    # Pilar 3: CSP
    draw.rounded_rectangle([640, 115, 910, 560], radius=12, fill=PANEL_COLOR, outline=GREEN, width=2)
    draw.text((660, 135), "3. CABECERA CSP", fill=GREEN, font=get_font(18, bold=True))
    draw.text((660, 160), "(CONTENT SECURITY POLICY)", fill=GREEN, font=get_font(13))
    draw.text((660, 195), "Lista blanca de ejecución", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 215), "para el navegador:", fill=TEXT_WHITE, font=get_font(13))
    draw.rounded_rectangle([655, 270, 895, 370], radius=6, fill=(11, 19, 43))
    draw.text((665, 285), "Content-Security-Policy:", fill=TEXT_MUTED, font=get_font(10))
    draw.text((665, 305), "  default-src 'self';", fill=CYAN, font=get_font(11))
    draw.text((665, 325), "  script-src 'self' 'nonce-..'", fill=GREEN, font=get_font(11))
    draw.text((665, 345), "  connect-src 'self'", fill=BLUE, font=get_font(11))
    draw.text((660, 395), "Prohíbe scripts inline", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 415), "y bloquea conexiones al", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 435), "servidor del atacante.", fill=GREEN, font=get_font(13, bold=True))

    img.save(output_path)
    print(f"Generado: {output_path}")

# -------------------------------------------------------------
# 6. IMAGEN: CASOS FAMOSOS DE XSS
# -------------------------------------------------------------
def crear_img_casos_famosos(output_path):
    img = Image.new('RGB', (950, 620), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([15, 15, 935, 605], radius=16, outline=BORDER_COLOR, width=2)
    
    draw.text((40, 35), "CASOS HISTÓRICOS Y REALES DE ATAQUES XSS", fill=RED, font=get_font(22, bold=True))
    draw.text((40, 68), "Incidentes reales donde fallos de XSS impactaron a millones de usuarios globales.", fill=TEXT_MUTED, font=get_font(14))

    # Caso 1: Samy Worm (MySpace 2005)
    draw.rounded_rectangle([40, 115, 310, 560], radius=12, fill=PANEL_COLOR, outline=RED, width=2)
    draw.text((60, 135), "1. GUSANO SAMY", fill=RED, font=get_font(18, bold=True))
    draw.text((60, 160), "MySpace (2005) - XSS Almacenado", fill=AMBER, font=get_font(12, bold=True))
    
    draw.rounded_rectangle([55, 190, 295, 275], radius=6, fill=(11, 19, 43))
    draw.text((65, 205), "⚡ 1 Millón de Víctimas", fill=CYAN, font=get_font(14, bold=True))
    draw.text((65, 230), "En menos de 20 horas", fill=TEXT_WHITE, font=get_font(13))
    draw.text((65, 250), "¡El virus más rápido!", fill=RED, font=get_font(12, bold=True))

    draw.text((60, 295), "• Samy Kamkar inyectó un", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 318), "  script en su perfil social.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 345), "• Cada visitante agregaba a", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 368), "  Samy como amigo y copiaba", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 391), "  el código a su propio perfil.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((60, 420), "• Agregaba la frase viral:", fill=TEXT_MUTED, font=get_font(12))
    draw.text((60, 440), "  'Samy is my hero'.", fill=AMBER, font=get_font(12, bold=True))
    draw.text((60, 475), "• Consecuencia:", fill=TEXT_WHITE, font=get_font(13, bold=True))
    draw.text((60, 498), "  MySpace tuvo que apagar", fill=RED, font=get_font(13))
    draw.text((60, 521), "  sus servidores mundiales.", fill=RED, font=get_font(13))

    # Caso 2: Gusano de Twitter / TweetDeck (2014)
    draw.rounded_rectangle([340, 115, 610, 560], radius=12, fill=PANEL_COLOR, outline=BLUE, width=2)
    draw.text((360, 135), "2. GUSANO TWITTER", fill=BLUE, font=get_font(18, bold=True))
    draw.text((360, 160), "TweetDeck (2014) - XSS Almacenado", fill=CYAN, font=get_font(12, bold=True))

    draw.rounded_rectangle([355, 190, 595, 275], radius=6, fill=(11, 19, 43))
    draw.text((365, 205), "🐦 Auto-Retweet Viral", fill=BLUE, font=get_font(14, bold=True))
    draw.text((365, 230), "+80,000 cuentas tomadas", fill=TEXT_WHITE, font=get_font(13))
    draw.text((365, 250), "Propagación en segundos", fill=AMBER, font=get_font(12, bold=True))

    draw.text((360, 295), "• Un tweet incluía código JS", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 318), "  sin escapar en TweetDeck.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 345), "• Al pasar el cursor sobre", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 368), "  el tweet, el script forzaba", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 391), "  un retweet automático.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 420), "• Las cuentas de miles de", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 440), "  usuarios e instituciones", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 460), "  publicaron el virus.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((360, 490), "• Consecuencia:", fill=TEXT_WHITE, font=get_font(13, bold=True))
    draw.text((360, 513), "  TweetDeck fue desactivado", fill=RED, font=get_font(13))
    draw.text((360, 533), "  de emergencia.", fill=RED, font=get_font(13))

    # Caso 3: Yahoo! Mail (2015)
    draw.rounded_rectangle([640, 115, 910, 560], radius=12, fill=PANEL_COLOR, outline=AMBER, width=2)
    draw.text((660, 135), "3. YAHOO! MAIL", fill=AMBER, font=get_font(18, bold=True))
    draw.text((660, 160), "Yahoo! (2015) - Stored Webmail", fill=GREEN, font=get_font(12, bold=True))

    draw.rounded_rectangle([655, 190, 895, 275], radius=6, fill=(11, 19, 43))
    draw.text((665, 205), "✉️ Lectura de Correos", fill=AMBER, font=get_font(14, bold=True))
    draw.text((665, 230), "Espionaje masivo de inbox", fill=TEXT_WHITE, font=get_font(13))
    draw.text((665, 250), "Basta con abrir el correo", fill=RED, font=get_font(12, bold=True))

    draw.text((660, 295), "• El atacante enviaba un", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 318), "  correo con HTML malicioso.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 345), "• El filtro de Yahoo no", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 368), "  escapaba ciertos atributos.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 395), "• Solo con ver el email,", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 418), "  el script leía todos los", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 440), "  correos privados y enviaba", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 460), "  copias al atacante.", fill=TEXT_WHITE, font=get_font(13))
    draw.text((660, 490), "• Consecuencia:", fill=TEXT_WHITE, font=get_font(13, bold=True))
    draw.text((660, 513), "  Reconocimiento y bug", fill=GREEN, font=get_font(13))
    draw.text((660, 533), "  bounty de alto impacto.", fill=GREEN, font=get_font(13))

    img.save(output_path)
    print(f"Generado: {output_path}")

def main():
    dirs = [
        "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3/imagenes",
        "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3/Laboratorio_XSS/imagenes"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        crear_img_que_es_xss(os.path.join(d, "img_que_es_xss.png"))
        crear_img_xss_reflejado(os.path.join(d, "img_xss_reflejado.png"))
        crear_img_xss_almacenado(os.path.join(d, "img_xss_almacenado.png"))
        crear_img_xss_dom(os.path.join(d, "img_xss_dom.png"))
        crear_img_prevencion(os.path.join(d, "img_prevencion.png"))
        crear_img_casos_famosos(os.path.join(d, "img_casos_famosos.png"))

if __name__ == "__main__":
    main()
