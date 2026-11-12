#!/usr/bin/env python3
"""
Generador de Presentación PPTX de Alta Calidad para el Parcial 3
Universidad Católica de El Salvador (UNICAES)
Asignatura: Gestión de Seguridad en Sistemas Informáticos
Tema: Anatomía, Impacto y Defensa Integral de Cross-Site Scripting (XSS - CWE-79)
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Colores del Sistema de Diseño (Cyber / Slate / Navy DevSecOps)
COLOR_BG_DARK       = RGBColor(11, 19, 43)    # #0B132B Azul Noche Profundo
COLOR_BG_CARD       = RGBColor(26, 38, 57)    # #1A2639 Card / Panel
COLOR_BG_CODE       = RGBColor(15, 23, 42)    # #0F172A Terminal / Monospace
COLOR_BORDER_CARD   = RGBColor(45, 60, 80)    # Borde sutil de tarjeta
COLOR_CYAN          = RGBColor(0, 232, 198)   # #00E8C6 Acento Cyan Eléctrico
COLOR_BLUE_SKY      = RGBColor(56, 189, 248)  # #38BDF8 Azul Celeste
COLOR_AMBER         = RGBColor(245, 158, 11)  # #F59E0B Ámbar / Alerta
COLOR_RED_ALERT     = RGBColor(239, 68, 68)   # #EF4444 Rojo Peligro
COLOR_GREEN_SAFE    = RGBColor(16, 185, 129)  # #10B981 Verde Seguro
COLOR_TEXT_PRIMARY  = RGBColor(248, 250, 252) # #F8FAFC Blanco Brillante
COLOR_TEXT_MUTED    = RGBColor(148, 163, 184) # #94A3B8 Gris Texto Secundario

FONT_HEADING = "Calibri"
FONT_BODY    = "Calibri"
FONT_CODE    = "Consolas"

def crear_presentacion():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="GESTIÓN DE SEGURIDAD EN SISTEMAS INFORMÁTICOS • UNICAES", slide_num=None):
        # Badge de Categoría
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_CYAN

        # Título Principal
        tit_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf_tit = tit_box.text_frame
        tf_tit.word_wrap = True
        tf_tit.margin_left = tf_tit.margin_top = tf_tit.margin_right = tf_tit.margin_bottom = 0
        p_tit = tf_tit.paragraphs[0]
        p_tit.text = title_text
        p_tit.font.name = FONT_HEADING
        p_tit.font.size = Pt(22)
        p_tit.font.bold = True
        p_tit.font.color.rgb = COLOR_TEXT_PRIMARY

        # Línea de Acento Decorativa
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER_CARD
        line.line.fill.background()

        # Número de slide
        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.4), Inches(0.6), Inches(0.35))
            tf_num = num_box.text_frame
            p_num = tf_num.paragraphs[0]
            p_num.text = f"{slide_num:02d}"
            p_num.alignment = PP_ALIGN.RIGHT
            p_num.font.name = FONT_HEADING
            p_num.font.size = Pt(11)
            p_num.font.bold = True
            p_num.font.color.rgb = COLOR_TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, badge_color=COLOR_CYAN, border_color=COLOR_BORDER_CARD, bg_color=COLOR_BG_CARD):
        # Card Background Shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        # Text Box within Card
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = badge_color
        p_title.space_after = Pt(10)

        # Items
        for item in items:
            p = tf.add_paragraph()
            p.space_after = Pt(6)
            if isinstance(item, tuple):
                label, val = item
                r_lbl = p.add_run()
                r_lbl.text = f"• {label}: "
                r_lbl.font.name = FONT_BODY
                r_lbl.font.size = Pt(11)
                r_lbl.font.bold = True
                r_lbl.font.color.rgb = COLOR_TEXT_PRIMARY
                
                r_val = p.add_run()
                r_val.text = val
                r_val.font.name = FONT_BODY
                r_val.font.size = Pt(11)
                r_val.font.color.rgb = COLOR_TEXT_MUTED
            else:
                r = p.add_run()
                r.text = f"• {item}"
                r.font.name = FONT_BODY
                r.font.size = Pt(11)
                r.font.color.rgb = COLOR_TEXT_PRIMARY

    def add_code_card(slide, left, top, width, height, title, code_lines, badge_color=COLOR_BLUE_SKY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_BG_CODE
        card.line.color.rgb = COLOR_BORDER_CARD
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = f"⚙ {title.upper()}"
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(11)
        p_title.font.bold = True
        p_title.font.color.rgb = badge_color
        p_title.space_after = Pt(8)

        for line in code_lines:
            p = tf.add_paragraph()
            p.space_after = Pt(3)
            r = p.add_run()
            r.text = line
            r.font.name = FONT_CODE
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_CYAN if line.strip().startswith(("#", "//", "<!--", "/*")) else COLOR_TEXT_PRIMARY

    def add_speaker_notes(slide, notes_text):
        notes = slide.notes_slide
        tf = notes.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Decoración geométrica sutil
    banner = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(0.15), Inches(5.2))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_CYAN
    banner.line.fill.background()

    tb_cover = slide1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11.3), Inches(5.2))
    tf1 = tb_cover.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "UNIVERSIDAD CATÓLICA DE EL SALVADOR • FIA • INGENIERÍA EN DESARROLLO DE SOFTWARE"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "ANATOMÍA, IMPACTO Y DEFENSA INTEGRAL\nDE CROSS-SITE SCRIPTING (XSS)"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_PRIMARY
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Análisis de Vulnerabilidad CWE-79, Demostración Experimental de Laboratorio y Contramedidas DevSecOps"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.italic = True
    p2.font.color.rgb = COLOR_BLUE_SKY
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "EVALUACIÓN DEL PARCIAL 3 — GESTIÓN DE SEGURIDAD EN SISTEMAS INFORMÁTICOS (SECCIÓN A)"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER
    p3.space_after = Pt(10)

    p4 = tf1.add_paragraph()
    p4.text = "INTEGRANTES DE INVESTIGACIÓN:\n" \
              "• Guevara Martínez, Dennis Ademir — Carnet: 2023-GM-607\n" \
              "• Villeda Alabi, Mario Edgardo — Carnet: 2023-VA-651\n" \
              "• Balcaceres Silvestre, Luis Felipe — Carnet: 2023-BS-602\n\n" \
              "Santa Ana, El Salvador — Ciclo II-2026"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(11)
    p4.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(slide1, 
        "ORADOR: Dennis Guevara (Apertura).\n\n"
        "Buenos días/tardes ingeniero y compañeros. Hoy nuestro equipo presentará la investigación técnica "
        "y el taller práctico de laboratorio sobre Cross-Site Scripting (XSS - CWE-79), correspondiente a la "
        "evaluación del Parcial 3 de Gestión de Seguridad en Sistemas Informáticos. Analizaremos desde la raíz "
        "del fallo en el navegador hasta las contramedidas en profundidad que neutralizan este vector de forma definitiva.")

    # =========================================================================
    # SLIDE 2: AGENDA Y REPARTO ESTRATÉGICO
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "AGENDA TÉCNICA Y REPARTO DE EXPOSICIÓN", slide_num=2)

    add_card(slide2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "BLOQUE 1: FUNDAMENTOS", [
                 ("Responsable", "Dennis Guevara"),
                 ("Tiempo", "3 - 4 Minutos"),
                 ("Ficha CWE-79", "Taxonomía oficial MITRE y métricas CVSS v3.1"),
                 ("Causa Raíz", "Modelo de confianza del navegador y Same-Origin Policy"),
                 ("Variantes", "Reflejado (Tipo I), Almacenado (Tipo II) y DOM (Tipo 0)"),
                 ("Superficie", "Análisis de puntos de entrada no confiables")
             ], badge_color=COLOR_CYAN)

    add_card(slide2, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8), 
             "BLOQUE 2: LABORATORIO POc", [
                 ("Responsable", "Mario Villeda"),
                 ("Tiempo", "5 - 6 Minutos"),
                 ("Workbench", "Presentación de la arquitectura de auditoría DevSecOps"),
                 ("Pipeline Debugger", "Traza paso a paso en 4 Breakpoints"),
                 ("Explotación", "Inyección Reflejada, Persistencia en BD y flujo DOM"),
                 ("Terminal C2", "Interceptación de tráfico de ataque en tiempo real")
             ], badge_color=COLOR_BLUE_SKY)

    add_card(slide2, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8), 
             "BLOQUE 3: IMPACTO Y DEFENSA", [
                 ("Responsable", "Luis Balcaceres"),
                 ("Tiempo", "3 - 4 Minutos"),
                 ("Session Hijacking", "Demostración de extracción de cookies de autenticación"),
                 ("Tríada CIA", "Impacto real en Confidencialidad, Integridad y Disponibilidad"),
                 ("Defensa en 3 Capas", "Output Encoding, CSP Nivel 3 y Cookies RFC 6265"),
                 ("Defensa / Q&A", "Banco de preguntas técnicas del jurado (Todo el equipo)")
             ], badge_color=COLOR_AMBER)

    add_speaker_notes(slide2, 
        "ORADOR: Dennis Guevara.\n\n"
        "Hemos estructurado nuestra exposición en 3 bloques complementarios de 12 a 15 minutos en total: "
        "Dennis abrirá con el marco teórico y taxonomía formal; Mario tomará el control en vivo del Security Workbench "
        "para demostrar la depuración de los 3 tipos de XSS; y Luis cerrará evidenciando el secuestro de credenciales "
        "y cómo aplicar la defensa en profundidad en código y cabeceras.")

    # =========================================================================
    # SLIDE 3: OBJETIVOS DEL TRABAJO
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "OBJETIVOS DE LA INVESTIGACIÓN Y DEL LABORATORIO", slide_num=3)

    add_card(slide3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.6), 
             "OBJETIVO GENERAL", [
                 "Analizar técnica y experimentalmente la debilidad Cross-Site Scripting (CWE-79) mediante la implementación "
                 "de un laboratorio interactivo y reproducible, formulando y validando las contramedidas de mitigación en "
                 "profundidad requeridas para el desarrollo seguro de software institucional y empresarial."
             ], badge_color=COLOR_CYAN)

    add_card(slide3, Inches(0.8), Inches(3.7), Inches(3.7), Inches(2.9), 
             "OBJETIVO ESPECÍFICO 1", [
                 ("Taxonomía y Vectores", "Identificar y clasificar las variantes de XSS (Reflejado, Almacenado y Basado en DOM), describiendo su flujo de ejecución y superficies de ataque asociadas.")
             ], badge_color=COLOR_BLUE_SKY)

    add_card(slide3, Inches(4.8), Inches(3.7), Inches(3.7), Inches(2.9), 
             "OBJETIVO ESPECÍFICO 2", [
                 ("Prueba de Concepto (PoC)", "Desarrollar un entorno controlado que evidencie el impacto real del secuestro de sesiones (Session Hijacking) cuando las cookies carecen de atributos de protección.")
             ], badge_color=COLOR_AMBER)

    add_card(slide3, Inches(8.8), Inches(3.7), Inches(3.733), Inches(2.9), 
             "OBJETIVO ESPECÍFICO 3", [
                 ("Mitigación Integral", "Implementar y validar contramedidas basadas en estándares internacionales: Context-Aware Output Encoding, cabecera CSP Nivel 3 y atributos RFC 6265 HttpOnly/SameSite.")
             ], badge_color=COLOR_GREEN_SAFE)

    add_speaker_notes(slide3, 
        "ORADOR: Dennis Guevara.\n\n"
        "Nuestro objetivo primordial no fue solo repetir la teoría, sino construir una plataforma práctica donde "
        "cada vector pueda ser visualizado a través de los lentes de un analizador DevSecOps. Buscamos entender "
        "la mecánica exacta por la cual un atacante burla las defensas y cómo mitigarlo de manera permanente.")

    # =========================================================================
    # SLIDE 4: FICHA TÉCNICA DE LA VULNERABILIDAD (CWE-79)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "FICHA TÉCNICA: CROSS-SITE SCRIPTING (CWE-79)", slide_num=4)

    add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "DATOS DE CLASIFICACIÓN ESTÁNDAR", [
                 ("Identificador MITRE", "CWE-79: Improper Neutralization of Input During Web Page Generation"),
                 ("OWASP Top 10:2021", "A03:2021 - Injection (Posición histórica ininterrumpida)"),
                 ("Métrica CVSS v3.1", "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"),
                 ("Base Score CVSS", "6.1 (Medio) a 7.5 (Alto en persistente)"),
                 ("Vector de Ataque", "Red / HTTP (AV:N - Ataque remoto sin proximidad física)"),
                 ("Complejidad de Ataque", "Baja (AC:L - No requiere condiciones especializadas)"),
                 ("Privilegios Previos", "Ninguno (PR:N - Explotable por usuarios no autenticados)")
             ], badge_color=COLOR_CYAN)

    add_card(slide4, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
             "CRITERIOS DE IMPACTO Y ALCANCE", [
                 ("Requisito de Interacción (UI:R)", "Requiere que la víctima realice una acción (hacer clic en un enlace o navegar a la sección infectada)."),
                 ("Salto de Alcance (Scope: Changed - S:C)", "El aspecto más crítico: la debilidad se origina en el servidor web pero impacta directamente en el contexto de seguridad del navegador del cliente."),
                 ("Compromiso de Confidencialidad (C:L / C:H)", "Lectura de cookies de sesión, tokens JWT, datos personales y secretos del DOM."),
                 ("Compromiso de Integridad (I:L / I:H)", "Modificación arbitraria del contenido de la página, alteración de transferencias o formularios de autenticación."),
                 ("Compromiso de Disponibilidad (A:N / A:L)", "Potencial congelamiento del hilo principal del navegador mediante bucles infinitos en JS.")
             ], badge_color=COLOR_AMBER)

    add_speaker_notes(slide4, 
        "ORADOR: Dennis Guevara.\n\n"
        "Destaco un parámetro vital de la ficha CVSS: 'Scope: Changed'. ¿Qué significa? Que aunque la vulnerabilidad "
        "se introduce por un descuido en el backend del servidor web, el daño y la ejecución del código no ocurren en el servidor, "
        "sino que saltan hacia la máquina y navegador del usuario final. Esto convierte a la aplicación vulnerable en un puente "
        "involuntario para atacar a sus propios clientes.")

    # =========================================================================
    # SLIDE 5: LA CAUSA RAÍZ Y EL MODELO DE CONFIANZA DEL NAVEGADOR
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "¿POR QUÉ OCURRE XSS? LA RAÍZ DEL FALLO", slide_num=5)

    add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "EL MODELO DE EJECUCIÓN WEB", [
                 ("La Causa Raíz", "La incapacidad inherente del navegador web para distinguir entre scripts legítimos concebidos por el desarrollador y código inyectado por un tercero."),
                 ("Confusión de Contexto", "Ocurre cuando datos proporcionados por el usuario se concatenan directamente en la respuesta sin delimitar claramente datos vs. instrucciones ejecutables."),
                 ("Same-Origin Policy (SOP)", "La política de mismo origen asume que todo script que se ejecuta en `portal.edu.sv` fue autorizado por el dueño del portal."),
                 ("Privilegios Concedidos", "Al script inyectado se le otorgan automáticamente las cookies del origen, acceso a LocalStorage, llamadas a endpoints protegidos y control del DOM.")
             ], badge_color=COLOR_RED_ALERT)

    add_code_card(slide5, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "EJEMPLO DE CONFUSIÓN DE CONTEXTO SINTÁCTICO", [
                      "// El servidor backend concatena la variable 'busqueda' sin codificar:",
                      "response = '<p>Resultados para: ' + request.args.get('q') + '</p>'",
                      "",
                      "// Caso Normal (Dato puro):",
                      "// Input: 'ciberseguridad'",
                      "// Render: <p>Resultados para: ciberseguridad</p>",
                      "",
                      "// Caso Malicioso (Ruptura sintáctica):",
                      "// Input: <script>alert(document.cookie)</script>",
                      "// Render vulnerable:",
                      "// <p>Resultados para: <script>alert(document.cookie)</script></p>",
                      "",
                      "// ¡El parser HTML conmuta al analizador léxico de JavaScript!",
                      "// Para el navegador, ambas etiquetas tienen idéntica legitimidad."
                  ], badge_color=COLOR_BLUE_SKY)

    add_speaker_notes(slide5, 
        "ORADOR: Dennis Guevara.\n\n"
        "La esencia del problema es la confusión léxica: los navegadores combinan estructura HTML, presentación CSS "
        "y lógica JavaScript en un único flujo de texto. Si el servidor no codifica los delimitadores como '<' y '>', "
        "el parser HTML se confunde y conmuta inmediatamente al motor de JavaScript, ejecutando el código con la plena "
        "confianza de la Same-Origin Policy.")

    # =========================================================================
    # SLIDE 6: TAXONOMÍA DE XSS: 3 VARIANTES FUNDAMENTALES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "TAXONOMÍA: LAS TRES VARIANTES CLÁSICAS DE XSS", slide_num=6)

    add_card(slide6, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "XSS REFLEJADO (TIPO I)", [
                 ("Persistencia", "No persistente (Volátil)"),
                 ("Flujo", "Petición HTTP -> Servidor -> Respuesta inmediata"),
                 ("Vector Común", "Parámetros GET en URLs de búsqueda o mensajes de error"),
                 ("Requisito", "Ingeniería social: la víctima debe pulsar un enlace manipulado"),
                 ("Alcance", "Individual por cada usuario que abra el enlace"),
                 ("Severidad CVSS", "Media (Requiere interacción activa de la víctima)")
             ], badge_color=COLOR_CYAN)

    add_card(slide6, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8), 
             "XSS ALMACENADO (TIPO II)", [
                 ("Persistencia", "Persistente (Grabado en servidor)"),
                 ("Flujo", "Inyección -> Base de Datos -> Servido a todos los clientes"),
                 ("Vector Común", "Tablones de comentarios, perfiles de usuario, foros"),
                 ("Requisito", "Ninguno externo: la víctima solo visita la página legítima"),
                 ("Alcance", "Masivo: afecta silenciosamente a todos los visitantes"),
                 ("Severidad CVSS", "Máxima / Crítica (Infección pasiva latente)")
             ], badge_color=COLOR_RED_ALERT)

    add_card(slide6, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8), 
             "XSS EN DOM (TIPO 0)", [
                 ("Persistencia", "Client-Side (Memoria del navegador)"),
                 ("Flujo", "Fuente (Source) -> Script local -> Sumidero (Sink)"),
                 ("Vector Común", "Fragmentos '#' en URL, `document.referrer`, `window.name`"),
                 ("Rol del Servidor", "Completamente omitido; el backend nunca ve la carga"),
                 ("Evasión", "Invisible para los Web Application Firewalls (WAF)"),
                 ("Severidad CVSS", "Alta (Muy común en SPAs como React o Angular)")
             ], badge_color=COLOR_AMBER)

    add_speaker_notes(slide6, 
        "ORADOR: Dennis Guevara (Cierre del Bloque 1).\n\n"
        "Comprender la taxonomía es vital: el XSS Reflejado requiere engañar a la víctima con un enlace específico; "
        "el XSS Almacenado es el más destructor porque permanece latente en la base de datos de la empresa afectando "
        "a cualquiera que navegue por el sitio; y el XSS en DOM es invisible para el servidor y los firewalls perimetrales "
        "porque se genera enteramente en la memoria del navegador. "
        "A continuación, Mario Villeda demostrará cada uno de estos escenarios en nuestro Security Workbench.")

    # =========================================================================
    # SLIDE 7: ARQUITECTURA DEL LABORATORIO: SECURITY WORKBENCH
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "DEMOSTRACIÓN: ARQUITECTURA DEL SECURITY WORKBENCH", slide_num=7)

    add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "PANEL IZQUIERDO: PORTAL ACADÉMICO", [
                 ("Diseño Dividido 50/50", "Simula el entorno del usuario final de UNICAES y la consola de auditoría simultáneamente."),
                 ("Pestaña 1: Búsqueda Reflejada", "Formulario GET con inyección directa en el parámetro `q`."),
                 ("Pestaña 2: Tablón de Dudas", "Foro colaborativo con persistencia en base de datos para simular XSS Almacenado."),
                 ("Pestaña 3: Saludo Dinámico", "Manipulación de `location.hash` en el DOM (`innerHTML` vs `textContent`)."),
                 ("Interruptor Global", "Switch interactivo para alternar en tiempo real entre Modo Vulnerable y Modo Seguro.")
             ], badge_color=COLOR_CYAN)

    add_card(slide7, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
             "PANEL DERECHO: CONSOLA DEVSECOPS", [
                 ("Pipeline Debugger (Superior)", "Depurador en 4 pasos con pausas controladas por botones AJAX y teclas de acceso rápido:"),
                 ("  • Breakpoint 1: Source", "Captura la entrada no confiable enviada por el usuario."),
                 ("  • Breakpoint 2: Backend", "Muestra si el servidor concatena en crudo o aplica `html.escape()`."),
                 ("  • Breakpoint 3: DOM Parser", "Inspecciona el comportamiento del analizador del navegador."),
                 ("  • Breakpoint 4: Impacto", "Monitorea la ejecución del script y la exfiltración."),
                 ("Terminal C2 Atacante (Inferior)", "Simulador de Command & Control que escucha en tiempo real credenciales exfiltradas.")
             ], badge_color=COLOR_BLUE_SKY)

    add_speaker_notes(slide7, 
        "ORADOR: Mario Villeda (Inicio del Bloque 2 - Demo en Vivo).\n\n"
        "Gracias Dennis. Para esta evaluación no queríamos limitarnos a ver alertas aisladas de JavaScript. "
        "Diseñamos el 'Security Workbench', una arquitectura dividida en dos paneles al 50%: "
        "A la izquierda tenemos el portal institucional que vería un estudiante o víctima; "
        "a la derecha, una consola de auditoría DevSecOps con un Pipeline Debugger que congela la ejecución en 4 puntos críticos, "
        "y abajo una terminal C2 atacante que simula al servidor del cibercriminal recibiendo los datos robados.")

    # =========================================================================
    # SLIDE 8: DEMOSTRACIÓN 1: XSS REFLEJADO PASO A PASO
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "ESCENARIO 1: DEPURACIÓN DE XSS REFLEJADO", slide_num=8)

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "ANATOMÍA DE LA EJECUCIÓN REFLEJADA", [
                 ("Vector de Prueba", "Uso de etiqueta HTML con evento onerror para evadir bloqueos simples:"),
                 ("Carga Inyectada", "`<img src=x onerror=\"alert('XSS_UNICAES')\">`"),
                 ("Paso 1: Source", "El usuario introduce el parámetro GET en el buscador."),
                 ("Paso 2: Backend Vulnerable", "Flask recibe `request.args.get('q')` y lo inserta directamente en la plantilla Jinja2 sin codificar."),
                 ("Paso 3: DOM Parser", "El navegador intenta cargar la imagen `x`, falla de inmediato y ejecuta el controlador `onerror`."),
                 ("Paso 4: Mitigación Activa", "En Modo Seguro, el backend aplica `html.escape(q)`, convirtiendo `<` en `&lt;`. El navegador lo imprime como texto puro.")
             ], badge_color=COLOR_CYAN)

    add_code_card(slide8, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "CONTRASTE DE CÓDIGO EN EL SERVIDOR (FLASK)", [
                      "# --- MODO VULNERABLE (Concatenación directa) ---",
                      "@app.route('/reflejado')",
                      "def reflejado_vuln():",
                      "    consulta = request.args.get('q', '')",
                      "    # PELIGRO: Se marca como 'safe' o se concatena en crudo",
                      "    return f'<h2>Resultados para: {consulta}</h2>'",
                      "",
                      "# --- MODO SEGURO (Codificación de entidades) ---",
                      "@app.route('/reflejado')",
                      "def reflejado_seguro():",
                      "    consulta = request.args.get('q', '')",
                      "    # SEGURO: Neutralización contextual inmediata",
                      "    consulta_limpia = html.escape(consulta)",
                      "    return f'<h2>Resultados para: {consulta_limpia}</h2>'"
                  ], badge_color=COLOR_GREEN_SAFE)

    add_speaker_notes(slide8, 
        "ORADOR: Mario Villeda.\n\n"
        "En este primer escenario pulsamos el botón 'Depurar'. Vean cómo en el Breakpoint 1 se captura la entrada. "
        "Avanzamos con F10 al Breakpoint 2: en modo vulnerable, el backend concatena el payload en bruto. "
        "Al llegar al Breakpoint 3, el navegador parsea la etiqueta img, falla al buscar el origen 'x' y ejecuta el alert. "
        "Pero al encender el Modo Seguro, observen el depurador: el Breakpoint 2 se torna verde porque html.escape "
        "reemplazó los delimitadores por entidades &lt; y &gt;, neutralizando por completo la inyección.")

    # =========================================================================
    # SLIDE 9: DEMOSTRACIÓN 2: XSS ALMACENADO Y PERSISTENCIA
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "ESCENARIO 2: PERSISTENCIA EN EL TABLÓN DE COMENTARIOS", slide_num=9)

    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "MECÁNICA DEL ATAQUE ALMACENADO", [
                 ("Persistencia en Memoria / BD", "El atacante redacta un comentario legítimo pero incrusta un script de exfiltración."),
                 ("Inyección Silenciosa", "El backend vulnerable almacena el registro íntegro en la base de datos sin sanitizar."),
                 ("Infección Pasiva", "Cada estudiante o docente que ingrese a ver el foro solicita la lista de comentarios."),
                 ("Ejecución en Cada Cliente", "El HTML generado incluye el script malicioso como si fuera contenido institucional."),
                 ("Impacto C2 Inmediato", "El script extrae las cookies de cada visitante y las despacha silenciosamente a la terminal atacante."),
                 ("Defensa", "Sanitizar antes de guardar y codificar entidades antes de renderizar.")
             ], badge_color=COLOR_RED_ALERT)

    add_code_card(slide9, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "PAYLOAD DE EXFILTRACIÓN AUTOMÁTICA", [
                      "<!-- Carga inyectada en el cuerpo del mensaje: -->",
                      "<script>",
                      "  (function() {",
                      "    // Extraer cookies y token de sesión de la víctima",
                      "    var datos = encodeURIComponent(document.cookie);",
                      "    ",
                      "    // Despachar silently al Servidor C2 atacante",
                      "    fetch('/api/exfiltrar?origen=foro&datos=' + datos, {",
                      "      method: 'GET',",
                      "      mode: 'no-cors'",
                      "    });",
                      "  })();",
                      "</script>",
                      "<!-- La víctima no percibe ninguna anomalía visual -->"
                  ], badge_color=COLOR_AMBER)

    add_speaker_notes(slide9, 
        "ORADOR: Mario Villeda.\n\n"
        "Ahora pasamos a la pestaña 2: Tablón de Comentarios. Este es el caso más crítico. "
        "Publicamos el mensaje malicioso. El servidor lo graba en la base de datos. "
        "A partir de este instante, cualquier usuario que entre a revisar sus tareas en el portal cargará pasivamente "
        "el script. No hace falta que hagan clic en un enlace manipulado ni que abran correos sospechosos: el propio "
        "portal institucional se convierte en el vector de infección pasiva.")

    # =========================================================================
    # SLIDE 10: DEMOSTRACIÓN 3: XSS EN DOM Y MANIPULACIÓN CLIENT-SIDE
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "ESCENARIO 3: FUENTES Y SUMIDEROS EN EL DOM", slide_num=10)

    add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "ANATOMÍA DEL CLIENT-SIDE XSS", [
                 ("El Rol del Servidor", "Completamente inexistente. El servidor responde con un HTML estático genérico."),
                 ("La Fuente (Source)", "Datos leídos directamente por JavaScript: `window.location.hash` (todo lo posterior al `#`)."),
                 ("El Sumidero (Sink) Vulnerable", "`element.innerHTML`: fuerza al navegador a parsear la cadena como nuevas etiquetas DOM."),
                 ("La Corrección (Sink Seguro)", "`element.textContent`: trata la cadena estrictamente como caracteres de texto plano."),
                 ("Evasión de Firewalls", "Como el fragmento `#` nunca se envía en los encabezados HTTP al servidor, ningún WAF puede detectarlo.")
             ], badge_color=COLOR_AMBER)

    add_code_card(slide10, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "COMPARACIÓN CRÍTICA EN JAVASCRIPT", [
                      "// Captura de la Fuente (Source):",
                      "let hash = decodeURIComponent(window.location.hash.substring(1));",
                      "",
                      "// --- IMPLEMENTACIÓN VULNERABLE (Sink Peligroso) ---",
                      "// Interpreta <img onerror=...> y ejecuta el script:",
                      "document.getElementById('saludo').innerHTML = 'Hola, ' + hash;",
                      "",
                      "// --- IMPLEMENTACIÓN ROBUSTA (Sink Seguro) ---",
                      "// Trata cualquier etiqueta como texto literal sin ejecutar:",
                      "document.getElementById('saludo').textContent = 'Hola, ' + hash;",
                      "",
                      "// Opcional con sanitización rigurosa de DOM:",
                      "// contenedor.innerHTML = DOMPurify.sanitize(hash);"
                  ], badge_color=COLOR_CYAN)

    add_speaker_notes(slide10, 
        "ORADOR: Mario Villeda (Cierre del Bloque 2).\n\n"
        "En la pestaña 3 demostramos el XSS en DOM. Vean cómo en el depurador, el Breakpoint 2 marca explícitamente "
        "'Servidor Omitido'. ¿Por qué? Porque el payload viaja en el fragmento de la URL después del numeral, el cual "
        "jamás se envía al servidor por protocolo HTTP. "
        "Si usamos innerHTML, el navegador ejecuta el script; si cambiamos a textContent, el contenido se neutraliza en 0 milisegundos "
        "sin sobrecosto computacional. Ahora Luis Felipe explicará el impacto en la Tríada CIA y las mitigaciones definitivas.")

    # =========================================================================
    # SLIDE 11: IMPACTO EN LA TRÍADA DE SEGURIDAD (CIA)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "EVALUACIÓN DE IMPACTO EN LA TRÍADA DE SEGURIDAD (CIA)", slide_num=11)

    add_card(slide11, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "CONFIDENCIALIDAD (ALTO)", [
                 ("Compromiso", "PÉRDIDA SEVERA DE SECRETOS"),
                 ("Session Hijacking", "Exfiltración de cookies de autenticación (`session_auth_token`) y tokens JWT."),
                 ("Lectura de Datos Privados", "El atacante puede leer calificaciones, expedientes y chats cargados en el DOM."),
                 ("Keylogging In-Browser", "Captura en tiempo real de contraseñas y números de tarjeta mientras el usuario escribe."),
                 ("Exfiltración Silenciosa", "Transmisión hacia servidores C2 remotos sin dejar rastro visible.")
             ], badge_color=COLOR_RED_ALERT)

    add_card(slide11, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8), 
             "INTEGRIDAD (CRÍTICO)", [
                 ("Compromiso", "MANIPULACIÓN TOTAL DEL ESTADO"),
                 ("Defacement del Portal", "Alteración visual completa de la interfaz institucional para dañar reputación."),
                 ("Phishing In-Site", "Inyección de campos falsos de login sobre la URL legítima y con candado HTTPS activo."),
                 ("Operaciones No Autorizadas", "Envío de peticiones `fetch()` con la sesión de la víctima (cambio de correo, transferencias)."),
                 ("Falsificación de Identidad", "Publicación de mensajes en nombre de docentes o administradores.")
             ], badge_color=COLOR_AMBER)

    add_card(slide11, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8), 
             "DISPONIBILIDAD (MEDIO / BAJO)", [
                 ("Compromiso", "DENEGACIÓN DE SERVICIO LOCAL"),
                 ("Bloqueo del Hilo Principal", "Ejecución de bucles infinitos en JavaScript (`while(true)`) que congelan la pestaña."),
                 ("Agotamiento de CPU/RAM", "Consumo masivo de memoria del navegador en la máquina del cliente."),
                 ("Impacto en Servidor", "Bombardeo asíncrono de peticiones recursivas emitidas por miles de navegadores infectados (DoS distribuido).")
             ], badge_color=COLOR_BLUE_SKY)

    add_speaker_notes(slide11, 
        "ORADOR: Luis Balcaceres (Inicio del Bloque 3).\n\n"
        "Gracias Mario. Cuando analizamos XSS desde la Tríada CIA descubrimos que el mito de 'XSS es solo un alert' "
        "es completamente falso. La Confidencialidad e Integridad quedan destrozadas: un atacante no solo roba tokens, "
        "sino que puede inyectar un formulario falso de inicio de sesión dentro de la URL oficial de la universidad, "
        "con certificado SSL válido, haciendo que el phishing sea prácticamente indetectable para cualquier usuario.")

    # =========================================================================
    # SLIDE 12: EL ATAQUE CRÍTICO: SECUESTRO DE SESIÓN (SESSION HIJACKING)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "ANATOMÍA DEL ATAQUE: SESSION HIJACKING", slide_num=12)

    add_card(slide12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "EL PROCEDIMIENTO DEL ATACANTE", [
                 ("El Objetivo", "Apropiarse del secreto de autenticación `session_auth_token` almacenado en las cookies."),
                 ("Acceso No Restringido", "Si la cookie no tiene la bandera `HttpOnly`, el motor de JavaScript puede leerla libremente con `document.cookie`."),
                 ("Canal de Fuga (C2)", "El script malicioso envía la cookie mediante un parámetro en una petición asíncrona hacia el servidor atacante."),
                 ("Suplantación Instantánea", "El atacante inyecta la cookie en su propio navegador y asume la identidad de la víctima."),
                 ("Bypass de Autenticación", "No necesita conocer contraseñas ni superar el segundo factor (2FA) ya completado.")
             ], badge_color=COLOR_RED_ALERT)

    add_code_card(slide12, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "EVIDENCIA EN LA TERMINAL C2 DE NUESTRO LABORATORIO", [
                      "[C2 ATACANTE ESCUCHANDO EN PUERTO 5000 / API EXFILTRAR]",
                      "-------------------------------------------------------",
                      "[!] 17:05:12 - Conexión entrante desde 192.168.1.45",
                      "[!] User-Agent: Mozilla/5.0 (X11; Linux x86_64)...",
                      "[!] Vector detectado: XSS Almacenado en Foro Académico",
                      "",
                      "[CRÍTICO - COOKIE ROBADA EXITOSAMENTE]:",
                      "session_auth_token=AUTH_TOKEN_UNICAES_SEC_987654321;",
                      "usuario=docente_titular; rol=administrador",
                      "",
                      "[+] Estado: Sesión secuestrada con éxito.",
                      "[+] El atacante ahora tiene privilegios administrativos."
                  ], badge_color=COLOR_RED_ALERT)

    add_speaker_notes(slide12, 
        "ORADOR: Luis Balcaceres.\n\n"
        "Observen la pantalla derecha inferior de nuestro Security Workbench: esta es la captura real del log de nuestro servidor C2. "
        "En cuanto la víctima entró al foro, el script leyó document.cookie y despachó el token de sesión. "
        "A partir de este momento, el atacante no necesita descifrar ninguna contraseña: copia el token en su propio navegador "
        "y tiene acceso inmediato a las calificaciones y registros institucionales.")

    # =========================================================================
    # SLIDE 13: ESTRATEGIA DE DEFENSA EN PROFUNDIDAD (3 CAPAS)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "ESTRATEGIA INTEGRAL: DEFENSA EN PROFUNDIDAD", slide_num=13)

    add_card(slide13, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "CAPA 1: CÓDIGO Y SALIDA", [
                 ("Enfoque", "Erradicación en la Fuente"),
                 ("Principio", "Toda entrada es hostil hasta demostrar lo contrario"),
                 ("Técnica Clave", "Codificación Contextual de Salida (Context-Aware Output Encoding)"),
                 ("Mecanismo", "Conversión de caracteres `< > \" ' &` a entidades seguras"),
                 ("Sanitización", "Uso de DOMPurify para cuando se requiere HTML enriquecido")
             ], badge_color=COLOR_CYAN)

    add_card(slide13, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8), 
             "CAPA 2: ARQUITECTURA HTTP", [
                 ("Enfoque", "Confinamiento en el Navegador"),
                 ("Principio", "Restricción de orígenes y recursos ejecutables"),
                 ("Técnica Clave", "Content Security Policy (CSP Nivel 3)"),
                 ("Mecanismo", "Cabecera `Content-Security-Policy` restrictiva"),
                 ("Efecto", "Inhabilita scripts en línea (`unsafe-inline`) y bloquea conexiones al C2 (`connect-src`)")
             ], badge_color=COLOR_BLUE_SKY)

    add_card(slide13, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8), 
             "CAPA 3: TRANSPORTE Y SESIÓN", [
                 ("Enfoque", "Mitigación del Peor Escenario"),
                 ("Principio", "Aislar las credenciales del motor de JavaScript"),
                 ("Técnica Clave", "Endurecimiento de Cookies (RFC 6265)"),
                 ("Mecanismo", "Banderas `HttpOnly`, `Secure` y `SameSite=Strict/Lax`"),
                 ("Efecto", "Si un XSS logra ejecutarse, queda físicamente imposibilitado de robar el token")
             ], badge_color=COLOR_GREEN_SAFE)

    add_speaker_notes(slide13, 
        "ORADOR: Luis Balcaceres.\n\n"
        "La regla número uno de la ciberseguridad moderna es: ninguna defensa aislada es infalible. "
        "Si confiamos únicamente en un firewall, este puede ser evadido con ofuscación. "
        "Por eso aplicamos Defensa en Profundidad estructurada en 3 capas complementarias: "
        "Capa 1 en el código de la aplicación, Capa 2 en las directivas de seguridad del navegador con CSP, "
        "y Capa 3 en el confinamiento físico de las credenciales de sesión mediante banderas RFC 6265.")

    # =========================================================================
    # SLIDE 14: CAPA 1: CODIFICACIÓN CONTEXTUAL VS. SANITIZACIÓN
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "CAPA 1: CODIFICACIÓN CONTEXTUAL Y SANITIZACIÓN", slide_num=14)

    add_card(slide14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "DIFERENCIA TÉCNICA FUNDAMENTAL", [
                 ("Codificación (Output Encoding)", "Transforma los caracteres de delimitación sintáctica en sus entidades equivalentes (`<` a `&lt;`, `>` a `&gt;`)."),
                 ("Efecto del Encoding", "No altera el contenido: el usuario ve la cadena exactamente igual, pero el navegador la interpreta como datos visuales y nunca como código."),
                 ("Sanitización (Sanitization)", "Analiza el árbol sintáctico (AST) y elimina selectivamente etiquetas y atributos prohibidos (`<script>`, `<iframe>`, `onerror`)."),
                 ("Cuándo Usar Cada Una", "Codificación por defecto en el 99% de los casos. Sanitización únicamente cuando la funcionalidad exija admitir formato HTML enriquecido (editores WYSIWYG).")
             ], badge_color=COLOR_CYAN)

    add_code_card(slide14, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "REGLAS DE CODIFICACIÓN SEGÚN EL CONTEXTO", [
                      "<!-- Contexto 1: Cuerpo HTML (Body) -->",
                      "<!-- Convertir: < (&lt;), > (&gt;), & (&amp;) -->",
                      "<p>Bienvenido: {{ usuario | e }}</p>",
                      "",
                      "<!-- Contexto 2: Atributos HTML (Comillas obligatorias) -->",
                      "<!-- Convertir comillas dobles y simples a entidades numéricas -->",
                      "<input type=\"text\" name=\"user\" value=\"{{ nombre | e }}\">",
                      "",
                      "<!-- Contexto 3: Variable en Script JavaScript -->",
                      "<!-- Usar serialización segura JSON / Unicode escape -->",
                      "<script>",
                      "  let token = {{ usuario_token | tojson }};",
                      "</script>",
                      "",
                      "// ¡ADVERTENCIA!: Jamás usar '| safe' o 'dangerouslySetInnerHTML'"
                  ], badge_color=COLOR_BLUE_SKY)

    add_speaker_notes(slide14, 
        "ORADOR: Luis Balcaceres.\n\n"
        "Esta es una distinción fundamental que a menudo se pregunta en auditorías: "
        "La Codificación no borra nada, simplemente traduce los símbolos de control para que el motor del navegador "
        "los dibuje en la pantalla sin interpretarlos. En cambio, la Sanitización con librerías como DOMPurify inspecciona "
        "el árbol DOM y poda quirúrgicamente las ramas y atributos peligrosos. En nuestro laboratorio implementamos "
        "html.escape() como primera barrera infranqueable.")

    # =========================================================================
    # SLIDE 15: CAPA 2: CONTENT SECURITY POLICY (CSP NIVEL 3)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15)
    add_header(slide15, "CAPA 2: CONTENT SECURITY POLICY (CSP NIVEL 3)", slide_num=15)

    add_card(slide15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "EL ROL DE CSP EN EL NAVEGADOR", [
                 ("Definición", "Cabecera HTTP de respuesta que actúa como lista blanca estricta de orígenes y directivas de ejecución."),
                 ("Inhabilitación de Inline Scripts", "Por defecto prohíbe scripts incrustados directamente en el HTML (`<script>...</script>`) y manejadores `onerror/onclick`."),
                 ("Restricción de eval()", "Inhabilita completamente constructores dinámicos peligrosos como `eval()` o `setTimeout(String)`."),
                 ("Confinamiento de Conexiones", "Mediante `connect-src 'self'`, prohíbe que cualquier script (incluso inyectado) contacte servidores C2 externos."),
                 ("Nonces Criptográficos", "Permite scripts legítimos mediante un token aleatorio de un solo uso por cada petición HTTP (`nonce-r4nd0m`).")
             ], badge_color=COLOR_BLUE_SKY)

    add_code_card(slide15, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "CONFIGURACIÓN DE CABECERA CSP ESTRICTA", [
                      "# Cabecera HTTP emitida por el servidor Flask / Nginx:",
                      "Content-Security-Policy: \\",
                      "  default-src 'self'; \\",
                      "  script-src 'self' 'nonce-EDN42...8A' https://cdn.jsdelivr.net; \\",
                      "  style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; \\",
                      "  img-src 'self' data:; \\",
                      "  connect-src 'self'; \\",
                      "  object-src 'none'; \\",
                      "  base-uri 'self';",
                      "",
                      "// Resultado en la Consola del Navegador ante un ataque:",
                      "// [Refused to execute inline script because it violates",
                      "//  the following Content Security Policy directive...]"
                  ], badge_color=COLOR_GREEN_SAFE)

    add_speaker_notes(slide15, 
        "ORADOR: Luis Balcaceres.\n\n"
        "La segunda capa es la Content Security Policy. CSP le entrega al navegador un contrato estricto: "
        "'Solo ejecuta scripts que vengan de mi propio dominio o que lleven un Nonce criptográfico emitido en esta petición'. "
        "Si un atacante logra inyectar una etiqueta <script> en un comentario, el navegador verifica que no tiene el Nonce "
        "y se niega tajantemente a ejecutarla. Además, con la directiva connect-src 'self', bloquea cualquier intento "
        "de contactar al C2 atacante.")

    # =========================================================================
    # SLIDE 16: CAPA 3: ENDURECIMIENTO DE COOKIES (RFC 6265)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16)
    add_header(slide16, "CAPA 3: PROTECCIÓN DE COOKIES DE SESIÓN (RFC 6265)", slide_num=16)

    add_card(slide16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "LAS TRES BANDERAS OBLIGATORIAS", [
                 ("Bandera `HttpOnly`", "Oculta físicamente la cookie al entorno de ejecución de JavaScript. La API `document.cookie` devuelve una cadena vacía."),
                 ("Bandera `Secure`", "Ordena al navegador transmitir la cookie exclusivamente a través de canales protegidos con cifrado TLS/HTTPS."),
                 ("Bandera `SameSite`", "Controla la inclusión de la cookie en peticiones entre sitios distintos:"),
                 ("  • SameSite=Strict", "Nunca envía la cookie en solicitudes originadas desde sitios externos (Máxima protección contra CSRF)."),
                 ("  • SameSite=Lax", "Envío permitido únicamente en navegaciones de nivel superior (GET) iniciadas por el usuario.")
             ], badge_color=COLOR_GREEN_SAFE)

    add_code_card(slide16, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8), 
                  "EMISIÓN ROBUSTA DE COOKIES EN EL SERVIDOR", [
                      "# Emisión vulnerable (por defecto en malas prácticas):",
                      "resp.set_cookie('session_token', token)",
                      "# ¡Expuesto a lectura directa desde JavaScript!",
                      "",
                      "# Emisión Segura y Endurecida (Estándar RFC 6265):",
                      "resp.set_cookie(",
                      "    key='session_auth_token',",
                      "    value=token,",
                      "    httponly=True,     # Bloquea lectura en document.cookie",
                      "    secure=True,       # Solo sobre túnel cifrado HTTPS",
                      "    samesite='Lax',    # Mitiga Cross-Site Request Forgery",
                      "    max_age=3600       # Expiración temporal finita",
                      ")",
                      "",
                      "# Resultado en consola JS al invocar document.cookie:",
                      "# => '' (Cadena vacía: secreto totalmente protegido)"
                  ], badge_color=COLOR_CYAN)

    add_speaker_notes(slide16, 
        "ORADOR: Luis Balcaceres.\n\n"
        "La tercera capa es nuestra red de contención de desastre: si por alguna razón falla el encoding y la política CSP, "
        "la bandera HttpOnly garantiza que el atacante no pueda robar el token de sesión. "
        "En nuestro laboratorio demostramos que al invocar document.cookie con HttpOnly activo, JavaScript solo ve una "
        "cadena vacía. El navegador continúa autenticando al usuario en sus peticiones legítimas al servidor, pero aísla "
        "el secreto del alcance de cualquier script.")

    # =========================================================================
    # SLIDE 17: TABLA COMPARATIVA: MODO VULNERABLE VS. MODO SEGURO
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17)
    add_header(slide17, "COMPARATIVA EXPERIMENTAL: LABORATORIO EN VIVO", slide_num=17)

    # Tabla Comparativa de 4 filas y 3 columnas
    table_shape = slide17.shapes.add_table(5, 3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.266)
    table.columns[2].width = Inches(4.266)

    headers = ["ESCENARIO EVALUADO", "MODO VULNERABLE (INSEGURO)", "MODO MITIGADO (SEGURO)"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BG_CODE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN if col_idx == 0 else (COLOR_RED_ALERT if col_idx == 1 else COLOR_GREEN_SAFE)

    filas = [
        ("1. Búsqueda Reflejada\n(Parámetro GET ?q=)", 
         "• Payload concatenado sin escapar.\n• El evento onerror ejecuta alert().\n• Se expone la sesión al C2.",
         "• Backend aplica html.escape(q).\n• Las etiquetas se transforman en &lt; y &gt;.\n• El navegador lo muestra como texto plano."),
        ("2. Tablón de Comentarios\n(Persistencia en BD)", 
         "• Mensaje guardado en crudo en memoria.\n• Infección pasiva para todos los visitantes.\n• Exfiltración masiva continua.",
         "• Sanitización de entrada previa al guardado.\n• Jinja2 escapa entidades al renderizar.\n• Cero ejecución en clientes."),
        ("3. Saludo Dinámico\n(Fragmento DOM #)", 
         "• Uso de element.innerHTML.\n• El navegador parsea código en cliente.\n• El servidor no puede detectarlo.",
         "• Uso de element.textContent.\n• Asignación literal directa sin parseo.\n• Cero riesgo de ejecución client-side."),
        ("4. Token de Autenticación\n(Cookie de Sesión)", 
         "• Cookie emitida sin banderas.\n• document.cookie expone el token.\n• Secuestro de sesión consumado.",
         "• Cookie con HttpOnly=True y SameSite=Lax.\n• document.cookie retorna cadena vacía.\n• Token aislado del motor JS.")
    ]

    for row_idx, (col0, col1, col2) in enumerate(filas, start=1):
        for c_idx, val in enumerate([col0, col1, col2]):
            cell = table.cell(row_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BG_CARD if row_idx % 2 == 1 else COLOR_BG_DARK
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_PRIMARY

    add_speaker_notes(slide17, 
        "ORADOR: Mario Villeda & Luis Balcaceres.\n\n"
        "Esta tabla resume con total claridad la verificación empírica de nuestra investigación: "
        "en cada uno de los cuatro escenarios pusimos a prueba el antes y el después con el interruptor en caliente. "
        "La evidencia demuestra que la neutralización del XSS es 100% alcanzable cuando se siguen las buenas prácticas "
        "de desarrollo seguro y estándares de la industria.")

    # =========================================================================
    # SLIDE 18: CONCLUSIONES Y LECCIONES DEVSECOPS
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18)
    add_header(slide18, "CONCLUSIONES Y RECOMENDACIONES DEVSECOPS", slide_num=18)

    add_card(slide18, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "1. EL CLIENTE ES HOSTIL", [
                 ("Lección Principal", "El navegador del usuario debe ser considerado un entorno hostil."),
                 ("Lógica en Cliente", "El auge de arquitecturas SPA traslada demasiada lógica al navegador."),
                 ("Consecuencia", "Cualquier entrada del DOM (`location.hash`, `referrer`, `postMessage`) debe tratarse con la misma desconfianza que una petición SQL.")
             ], badge_color=COLOR_CYAN)

    add_card(slide18, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8), 
             "2. LA TRÍADA DE DEFENSA", [
                 ("Enfoque Estructural", "Ningún parche aislado resuelve XSS de forma permanente."),
                 ("La Fórmula Definitiva", "• Codificación contextual en el motor de plantillas.\n• CSP Nivel 3 sin directiva 'unsafe-inline'.\n• Cookies de sesión con HttpOnly y SameSite."),
                 ("Resiliencia", "Si una capa se ve comprometida, las restantes neutralizan el ataque.")
             ], badge_color=COLOR_GREEN_SAFE)

    add_card(slide18, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8), 
             "3. SHIFT-LEFT SECURITY", [
                 ("Integración CI/CD", "La detección de XSS no debe esperar al despliegue en producción."),
                 ("Herramientas SAST", "Linters con reglas de seguridad (ESLint React plugin, Bandit)."),
                 ("Pruebas DAST", "Escaneo automatizado de sumideros de ejecución en el pipeline."),
                 ("Cultura de Equipo", "La seguridad es un requerimiento funcional no negociable.")
             ], badge_color=COLOR_AMBER)

    add_speaker_notes(slide18, 
        "ORADOR: Dennis Guevara (Conclusiones Finales).\n\n"
        "Para concluir nuestra ponencia: XSS sigue vigente en el OWASP Top 10 no por falta de soluciones técnicas, "
        "sino por descuidos en la implementación y confianza ciega en datos de entrada. "
        "La defensa estructural que hemos demostrado prueba que con codificación contextual, CSP y banderas HttpOnly, "
        "podemos erradicar el riesgo de raíz. Muchas gracias por su atención. Quedamos a su entera disposición para "
        "la sesión de preguntas del catedrático y del auditorio.")

    # =========================================================================
    # SLIDE 19: BANCO DE DEFENSA TÉCNICA (PREGUNTAS DEL DOCENTE)
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide19)
    add_header(slide19, "BANCO DE DEFENSA: PREGUNTAS TÉCNICAS DEL CATEDRÁTICO", slide_num=19)

    add_card(slide19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), 
             "Q1: ¿HTTPONLY RESUELVE TODO EL PROBLEMA DE XSS?", [
                 ("Respuesta Técnica", "No. HttpOnly mitiga exclusivamente el robo de la cookie de sesión a través de `document.cookie`. El atacante aún puede realizar peticiones forzadas en nombre de la víctima (vía `fetch` enviando cookies por detrás), desfigurar la interfaz (defacement) o capturar pulsaciones (keylogging).")
             ], badge_color=COLOR_RED_ALERT)

    add_card(slide19, Inches(6.8), Inches(1.8), Inches(5.733), Inches(2.3), 
             "Q2: ¿DIFERENCIA ENTRE SANITIZACIÓN Y CODIFICACIÓN?", [
                 ("Respuesta Técnica", "La Sanitización remueve o poda etiquetas y atributos peligrosos permitiendo pasar código HTML inocuo (DOMPurify). La Codificación (Encoding) convierte los caracteres especiales en entidades seguras (`&lt;`), conservando el dato intacto pero anulando su ejecución léxica.")
             ], badge_color=COLOR_CYAN)

    add_card(slide19, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.3), 
             "Q3: ¿POR QUÉ UN WAF PERIMETRAL NO ES SUFICIENTE?", [
                 ("Respuesta Técnica", "Porque los WAFs se basan en firmas de red. Existen infinitas técnicas de mutación y ofuscación (MutaXSS, codificación alternativa). Además, un WAF nunca ve el tráfico de XSS basado en DOM, ya que se procesa 100% en la memoria del navegador del cliente.")
             ], badge_color=COLOR_AMBER)

    add_card(slide19, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.3), 
             "Q4: ¿POR QUÉ XSS ALMACENADO TIENE MAYOR IMPACTO QUE REFLEJADO?", [
                 ("Respuesta Técnica", "Porque no depende de engañar a la víctima mediante ingeniería social (clic en un enlace). La carga reside en la base de datos y afecta masiva y pasivamente a cualquier usuario legítimo autenticado, incluyendo administradores del sistema.")
             ], badge_color=COLOR_GREEN_SAFE)

    add_speaker_notes(slide19, 
        "ORADOR: Todo el equipo preparado para responder según el tema asignado.\n\n"
        "Este banco de preguntas resume los puntos de presión más habituales de un jurado evaluador: "
        "aclarar que HttpOnly no es una panacea universal sino una barrera de contención de credenciales, "
        "diferenciar con precisión quirúrgica entre encoding y sanitización, "
        "y argumentar por qué la seguridad debe residir en la aplicación y no delegarse a un WAF perimetral.")

    # Guardar presentación en ambas rutas clave
    output_dir_parent = "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3"
    output_dir_lab    = "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3/Laboratorio_XSS"

    path_parent = os.path.join(output_dir_parent, "Presentacion_XSS_UNICAES.pptx")
    path_lab    = os.path.join(output_dir_lab, "Presentacion_XSS_UNICAES.pptx")

    prs.save(path_parent)
    prs.save(path_lab)
    print(f"[OK] Presentación PPTX generada con éxito:")
    print(f"  -> {path_parent}")
    print(f"  -> {path_lab}")

if __name__ == "__main__":
    crear_presentacion()
