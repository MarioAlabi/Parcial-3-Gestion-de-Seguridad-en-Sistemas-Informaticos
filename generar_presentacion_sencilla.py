#!/usr/bin/env python3
"""
Generador de Presentación Simple y Visual de XSS (7 Diapositivas)
Universidad Católica de El Salvador (UNICAES)
Estructura:
1. Portada
2. Integrantes
3. ¿Qué es XSS? (+ Imagen)
4. XSS Reflejado (+ Imagen)
5. XSS Almacenado (+ Imagen)
6. XSS Basado en DOM (+ Imagen)
7. ¿Cómo prevenirlo? (+ Imagen)
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Colores del tema
COLOR_BG_DARK       = RGBColor(11, 19, 43)    # #0B132B Fondo oscuro elegante
COLOR_BG_CARD       = RGBColor(26, 38, 57)    # #1A2639 Tarjeta
COLOR_BORDER_CARD   = RGBColor(51, 65, 85)    # Borde
COLOR_CYAN          = RGBColor(0, 232, 198)   # #00E8C6 Cyan
COLOR_BLUE          = RGBColor(56, 189, 248)  # #38BDF8 Azul
COLOR_RED           = RGBColor(239, 68, 68)   # #EF4444 Rojo
COLOR_AMBER         = RGBColor(245, 158, 11)  # #F59E0B Ámbar
COLOR_GREEN         = RGBColor(16, 185, 129)  # #10B981 Verde
COLOR_TEXT_PRIMARY  = RGBColor(248, 250, 252) # Blanco
COLOR_TEXT_MUTED    = RGBColor(148, 163, 184) # Gris

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category="GESTIÓN DE SEGURIDAD EN SISTEMAS INFORMÁTICOS • UNICAES", slide_num=None):
    # Badge categoría
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = FONT_TITLE
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN

    # Título principal
    tit_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
    tf_tit = tit_box.text_frame
    tf_tit.word_wrap = True
    tf_tit.margin_left = tf_tit.margin_top = tf_tit.margin_right = tf_tit.margin_bottom = 0
    p_tit = tf_tit.paragraphs[0]
    p_tit.text = title_text
    p_tit.font.name = FONT_TITLE
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_TEXT_PRIMARY

    # Línea decorativa
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BORDER_CARD
    line.line.fill.background()

    # Número de slide
    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.4), Inches(0.8), Inches(0.35))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 08"
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.name = FONT_TITLE
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_TEXT_MUTED

def add_speaker_notes(slide, notes_text):
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    tf.text = notes_text

def crear_presentacion():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    base_dir = "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3"
    img_dir  = os.path.join(base_dir, "imagenes")

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Barra lateral decorativa
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.15), Inches(5.0))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_CYAN
    bar.line.fill.background()

    tb1 = slide1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(11.0), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "UNIVERSIDAD CATÓLICA DE EL SALVADOR • FIA"
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.space_after = Pt(16)

    p1 = tf1.add_paragraph()
    p1.text = "CROSS-SITE SCRIPTING\n(XSS)"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_PRIMARY
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Análisis Conceptual, Clasificación de Tipos y Prevención (CWE-79)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_BLUE
    p2.space_after = Pt(30)

    p3 = tf1.add_paragraph()
    p3.text = "GESTIÓN DE SEGURIDAD EN SISTEMAS INFORMÁTICOS — SECCIÓN “A”"
    p3.font.name = FONT_TITLE
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER
    p3.space_after = Pt(8)

    p4 = tf1.add_paragraph()
    p4.text = "Evaluación del Parcial 3 • Santa Ana, El Salvador • Noviembre de 2026"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(11)
    p4.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(slide1, "Buenos días ingeniero y compañeros. Hoy presentaremos de forma clara y directa qué es Cross-Site Scripting (XSS), sus principales tipos y cómo se previenen.")

    # =========================================================================
    # DIAPOSITIVA 2: INTEGRANTES
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "EQUIPO DE INVESTIGACIÓN", category="INTEGRANTES DEL GRUPO", slide_num=2)

    integrantes = [
        ("Dennis Ademir Guevara Martínez", "2023-GM-607", "Investigador / Expositor", COLOR_CYAN),
        ("Mario Edgardo Villeda Alabi", "2023-VA-651", "Investigador / Expositor", COLOR_BLUE),
        ("Luis Felipe Balcaceres Silvestre", "2023-BS-602", "Investigador / Expositor", COLOR_AMBER)
    ]

    for i, (nombre, carnet, rol, color) in enumerate(integrantes):
        left = Inches(0.8 + i * 4.0)
        top = Inches(2.0)
        width = Inches(3.7)
        height = Inches(4.5)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_BG_CARD
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = slide2.shapes.add_textbox(left + Inches(0.3), top + Inches(0.4), width - Inches(0.6), height - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_icon = tf.paragraphs[0]
        p_icon.text = f"👤 INTEGRANTE 0{i+1}"
        p_icon.font.name = FONT_TITLE
        p_icon.font.size = Pt(12)
        p_icon.font.bold = True
        p_icon.font.color.rgb = color
        p_icon.space_after = Pt(20)

        p_nom = tf.add_paragraph()
        p_nom.text = nombre
        p_nom.font.name = FONT_TITLE
        p_nom.font.size = Pt(18)
        p_nom.font.bold = True
        p_nom.font.color.rgb = COLOR_TEXT_PRIMARY
        p_nom.space_after = Pt(14)

        p_car = tf.add_paragraph()
        p_car.text = f"Carnet: {carnet}"
        p_car.font.name = FONT_BODY
        p_car.font.size = Pt(14)
        p_car.font.color.rgb = COLOR_CYAN
        p_car.space_after = Pt(10)

        p_rol = tf.add_paragraph()
        p_rol.text = rol
        p_rol.font.name = FONT_BODY
        p_rol.font.size = Pt(12)
        p_rol.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(slide2, "Nuestro equipo está conformado por Dennis Guevara, Mario Villeda y Luis Balcaceres, estudiantes de Ingeniería en Desarrollo de Software.")

    # =========================================================================
    # DIAPOSITIVA 3: ¿QUÉ ES XSS?
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "¿QUÉ ES CROSS-SITE SCRIPTING (XSS)?", category="CONCEPTO FUNDAMENTAL", slide_num=3)

    # Tarjeta de Texto (Izquierda)
    card3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card3.fill.solid()
    card3.fill.fore_color.rgb = COLOR_BG_CARD
    card3.line.color.rgb = COLOR_CYAN
    card3.line.width = Pt(1.5)

    tb3 = slide3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "DESCRIPCIÓN SENCILLA:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(12)

    bullets3 = [
        ("¿Qué es?", "Es una vulnerabilidad web que permite a un atacante inyectar scripts maliciosos (generalmente JavaScript) dentro de páginas web que otros usuarios visitan."),
        ("¿Por qué ocurre?", "Porque la aplicación web recibe datos del usuario y los muestra en pantalla sin validarlos ni codificarlos adecuadamente."),
        ("¿Cuál es el peligro?", "El navegador de la víctima no puede saber si el script es legítimo o malicioso y lo ejecuta con todos los privilegios del sitio web."),
        ("Consecuencias:", "Robo de cuentas y contraseñas (Session Hijacking), alteración visual de la página y redirección a portales falsos.")
    ]

    for label, desc in bullets3:
        p_item = tf3.add_paragraph()
        p_item.space_after = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # Imagen (Derecha)
    img_xss = os.path.join(img_dir, "img_que_es_xss.png")
    if os.path.exists(img_xss):
        slide3.shapes.add_picture(img_xss, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide3, "Cross-Site Scripting (XSS) ocurre cuando un atacante logra inyectar código JavaScript malicioso en una página web. El navegador de la víctima lo ejecuta pensando que proviene del sitio oficial, lo que permite robar cookies de sesión o falsificar la página.")

    # =========================================================================
    # DIAPOSITIVA 4: XSS REFLEJADO
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "TIPO 1: XSS REFLEJADO (NO PERSISTENTE)", category="CLASIFICACIÓN DE XSS", slide_num=4)

    card4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card4.fill.solid()
    card4.fill.fore_color.rgb = COLOR_BG_CARD
    card4.line.color.rgb = COLOR_CYAN
    card4.line.width = Pt(1.5)

    tb4 = slide4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    p.text = "CARACTERÍSTICAS PRINCIPALES:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(12)

    bullets4 = [
        ("¿Cómo funciona?", "El script malicioso viaja directamente dentro de la petición (por ejemplo, en un parámetro de búsqueda en la URL como ?q=script)."),
        ("No persistente:", "El servidor toma ese parámetro y lo refleja de inmediato en la respuesta HTML, pero NO lo guarda en la base de datos."),
        ("Requiere engaño:", "El atacante necesita que la víctima haga clic en un enlace manipulado enviado por correo, mensaje o redes sociales."),
        ("Mitigación básica:", "Codificar la salida en el servidor (con html.escape) para que los caracteres < y > se muestren como texto plano.")
    ]

    for label, desc in bullets4:
        p_item = tf4.add_paragraph()
        p_item.space_after = Pt(10)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    img_ref = os.path.join(img_dir, "img_xss_reflejado.png")
    if os.path.exists(img_ref):
        slide4.shapes.add_picture(img_ref, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide4, "El XSS Reflejado no se almacena en el servidor. El código viaja en el enlace, el servidor lo devuelve tal cual en la respuesta, y el navegador lo ejecuta. Requiere que la víctima haga clic en el enlace malicioso.")

    # =========================================================================
    # DIAPOSITIVA 5: XSS ALMACENADO
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "TIPO 2: XSS ALMACENADO (PERSISTENTE)", category="CLASIFICACIÓN DE XSS", slide_num=5)

    card5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card5.fill.solid()
    card5.fill.fore_color.rgb = COLOR_BG_CARD
    card5.line.color.rgb = COLOR_RED
    card5.line.width = Pt(1.5)

    tb5 = slide5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "EL TIPO MÁS PELIGROSO:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_after = Pt(12)

    bullets5 = [
        ("Guardado en Servidor:", "El atacante envía el script en un formulario (comentarios de un blog, foros, perfil) y queda grabado en la Base de Datos."),
        ("Infección Pasiva y Masiva:", "Cada vez que cualquier usuario entra a ver esa sección, el servidor le envía el código malicioso automáticamente."),
        ("Cero Interacción Extra:", "La víctima no necesita hacer clic en ningún enlace raro: solo con entrar a la página web legítima ya resulta infectada."),
        ("Impacto Máximo:", "Permite robar las sesiones de cientos o miles de usuarios, incluidos los administradores del sistema.")
    ]

    for label, desc in bullets5:
        p_item = tf5.add_paragraph()
        p_item.space_after = Pt(10)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    img_alm = os.path.join(img_dir, "img_xss_almacenado.png")
    if os.path.exists(img_alm):
        slide5.shapes.add_picture(img_alm, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide5, "El XSS Almacenado es el más destructor porque queda guardado en la base de datos. Cualquier persona que visite la página web legítima se infecta de manera pasiva y automática, sin necesidad de ingeniería social.")

    # =========================================================================
    # DIAPOSITIVA 6: XSS BASADO EN DOM
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "TIPO 3: XSS BASADO EN DOM (CLIENT-SIDE)", category="CLASIFICACIÓN DE XSS", slide_num=6)

    card6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card6.fill.solid()
    card6.fill.fore_color.rgb = COLOR_BG_CARD
    card6.line.color.rgb = COLOR_AMBER
    card6.line.width = Pt(1.5)

    tb6 = slide6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "100% EN EL NAVEGADOR:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(12)

    bullets6 = [
        ("El Servidor No Interviene:", "A diferencia de los otros, el servidor web nunca recibe ni procesa el código malicioso. Ocurre enteramente en el cliente."),
        ("Fuente Peligrosa (Source):", "Un script JavaScript de la página lee datos locales manipulables, como el fragmento # de la URL (location.hash)."),
        ("Sumidero Inseguro (Sink):", "Escribe ese valor directamente en la pantalla usando funciones peligrosas como innerHTML o eval()."),
        ("Invisible para WAFs:", "Como el fragmento # nunca viaja en la petición HTTP hacia el servidor, los firewalls tradicionales no lo pueden detectar."),
        ("Solución en Frontend:", "Cambiar innerHTML por textContent para que el navegador solo escriba texto literal.")
    ]

    for label, desc in bullets6:
        p_item = tf6.add_paragraph()
        p_item.space_after = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    img_dom = os.path.join(img_dir, "img_xss_dom.png")
    if os.path.exists(img_dom):
        slide6.shapes.add_picture(img_dom, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide6, "En el XSS basado en DOM el servidor ni se entera. El fallo está en los scripts JavaScript locales que toman valores de la URL con location.hash y los inyectan con innerHTML. La solución es usar textContent.")

    # =========================================================================
    # DIAPOSITIVA 7: CASOS FAMOSOS DE ATAQUES XSS
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "CASOS FAMOSOS DE ATAQUES XSS EN LA HISTORIA", category="IMPACTO REAL EN EL MUNDO", slide_num=7)

    card7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card7.fill.solid()
    card7.fill.fore_color.rgb = COLOR_BG_CARD
    card7.line.color.rgb = COLOR_RED
    card7.line.width = Pt(1.5)

    tb7 = slide7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "TRES CASOS HISTÓRICOS REALES:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_after = Pt(12)

    bullets7 = [
        ("1. Gusano Samy (MySpace 2005):", "El ataque XSS más rápido de la historia. Infectó a 1 millón de usuarios en menos de 20 horas. Forzaba a agregarlo como amigo con la frase 'Samy is my hero' y saturó los servidores de MySpace."),
        ("2. Gusano de TweetDeck / Twitter (2014):", "Un tweet con código malicioso que se auto-retuiteaba automáticamente cuando los usuarios pasaban el cursor sobre él. Infectó a más de 80,000 cuentas en minutos."),
        ("3. Espionaje en Yahoo! Mail (2015):", "XSS Almacenado dentro de correos HTML. Con solo abrir un correo sospechoso, el atacante podía leer toda la bandeja de entrada y enviar correos en nombre de la víctima."),
        ("Lección:", "El XSS no es teórico: ha afectado a las plataformas más gigantescas de internet.")
    ]

    for label, desc in bullets7:
        p_item = tf7.add_paragraph()
        p_item.space_after = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    img_casos = os.path.join(img_dir, "img_casos_famosos.png")
    if os.path.exists(img_casos):
        slide7.shapes.add_picture(img_casos, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide7, "Para ver que el XSS no es solo teoría, existen casos históricos impactantes: el Gusano Samy en MySpace infectó a un millón de personas en menos de un día; el gusano de Twitter provocó retweets automáticos masivos en 2014; y en Yahoo Mail permitía espiar la bandeja de entrada con solo abrir un correo.")

    # =========================================================================
    # DIAPOSITIVA 8: ¿CÓMO PREVENIRLO?
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "¿CÓMO PREVENIR Y DEFENDERNOS DE XSS?", category="RESUMEN DE MITIGACIÓN", slide_num=8)

    card8 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
    card8.fill.solid()
    card8.fill.fore_color.rgb = COLOR_BG_CARD
    card8.line.color.rgb = COLOR_GREEN
    card8.line.width = Pt(1.5)

    tb8 = slide8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.6), Inches(4.5))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "TRES REGLAS DE ORO:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(12)

    bullets8 = [
        ("1. Codificación de Salida (Encoding):", "Nunca insertar datos del usuario sin codificar. Convertir < a &lt; y > a &gt; para que el navegador los pinte como texto y nunca los ejecute."),
        ("2. Cookies con Bandera HttpOnly:", "Emitir las cookies de sesión con HttpOnly=True. Esto oculta físicamente la cookie al JavaScript e impide el robo de cuentas."),
        ("3. Cabecera CSP (Content Security Policy):", "Configurar en el servidor la cabecera CSP para prohibir la ejecución de scripts en línea ('unsafe-inline') y bloquear conexiones a servidores atacantes."),
        ("Conclusión:", "La combinación de estas tres medidas elimina el riesgo de XSS de forma definitiva.")
    ]

    for label, desc in bullets8:
        p_item = tf8.add_paragraph()
        p_item.space_after = Pt(10)
        r1 = p_item.add_run()
        r1.text = f"• {label} "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_PRIMARY

        r2 = p_item.add_run()
        r2.text = desc
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    img_prev = os.path.join(img_dir, "img_prevencion.png")
    if os.path.exists(img_prev):
        slide8.shapes.add_picture(img_prev, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))

    add_speaker_notes(slide8, "Para defendernos aplicamos tres cosas: codificar las salidas para evitar la inyección, activar HttpOnly para que no puedan robarnos la sesión, y configurar Content Security Policy en el servidor. Con esto blindamos la aplicación. Muchas gracias por su atención.")

    # Guardar en ambas ubicaciones
    path_parent = os.path.join(base_dir, "Presentacion_XSS_UNICAES.pptx")
    path_lab    = os.path.join(base_dir, "Laboratorio_XSS", "Presentacion_XSS_UNICAES.pptx")

    prs.save(path_parent)
    prs.save(path_lab)
    print("[OK] Presentación sencilla y visual generada con éxito:")
    print(f"  -> {path_parent}")
    print(f"  -> {path_lab}")

if __name__ == "__main__":
    crear_presentacion()
