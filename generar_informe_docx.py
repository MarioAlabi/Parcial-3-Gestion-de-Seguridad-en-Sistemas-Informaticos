#!/usr/bin/env python3
"""
Generador de Informe Técnico Profesional en formato DOCX
Universidad Católica de El Salvador (UNICAES)
Materia: Gestión de Seguridad en Sistemas Informáticos
Tema: Análisis Técnico, Diagramas de Flujo y Mitigación de Cross-Site Scripting (XSS - CWE-79)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def crear_informe():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    COLOR_PRIMARIO = RGBColor(15, 23, 42)
    COLOR_AZUL = RGBColor(2, 132, 199)
    COLOR_TEXTO = RGBColor(51, 65, 85)

    # PORTADA
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("UNIVERSIDAD CATÓLICA DE EL SALVADOR\n")
    r_uni.font.name = "Calibri"
    r_uni.font.size = Pt(16)
    r_uni.font.bold = True
    r_uni.font.color.rgb = COLOR_PRIMARIO

    r_fac = p_uni.add_run("FACULTAD DE INGENIERÍA Y ARQUITECTURA\nESCUELA DE INGENIERÍA EN DESARROLLO DE SOFTWARE\n")
    r_fac.font.name = "Calibri"
    r_fac.font.size = Pt(13)
    r_fac.font.bold = True
    r_fac.font.color.rgb = COLOR_AZUL

    r_mat = p_uni.add_run("GESTIÓN DE SEGURIDAD EN SISTEMAS INFORMÁTICOS — SECCIÓN A\n")
    r_mat.font.name = "Calibri"
    r_mat.font.size = Pt(11)
    r_mat.font.italic = True
    r_mat.font.color.rgb = COLOR_TEXTO

    doc.add_paragraph("\n" * 3)

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run("INFORME TÉCNICO DE VULNERABILIDAD:\nANATOMÍA, DIAGRAMAS DE FLUJO Y DEFENSA INTEGRAL DE XSS\n")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(18)
    r_tit.font.bold = True
    r_tit.font.color.rgb = COLOR_AZUL

    r_sub = p_tit.add_run("Análisis de Fallo CWE-79, Mecánica de Parsers y Estrategias de Mitigación en Código Seguro")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_TEXTO

    doc.add_paragraph("\n" * 4)

    p_resp = doc.add_paragraph()
    p_resp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_resp_hdr = p_resp.add_run("INTEGRANTES DE INVESTIGACIÓN:\n")
    r_resp_hdr.font.name = "Calibri"
    r_resp_hdr.font.size = Pt(11)
    r_resp_hdr.font.bold = True
    r_resp_hdr.font.color.rgb = COLOR_PRIMARIO

    integrantes = [
        ("Guevara Martínez, Dennis Ademir", "2023-GM-607"),
        ("Villeda Alabi, Mario Edgardo", "2023-VA-651"),
        ("Balcaceres Silvestre, Luis Felipe", "2023-BS-602")
    ]
    for nombre, carnet in integrantes:
        r = p_resp.add_run(f" • {nombre}  —  Carnet: {carnet}\n")
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = COLOR_TEXTO

    doc.add_paragraph("\n" * 2)

    p_fecha = doc.add_paragraph()
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_fecha = p_fecha.add_run("SANTA ANA, EL SALVADOR — NOVIEMBRE DE 2026\nCICLO II-2026 — PARCIAL 3")
    r_fecha.font.name = "Calibri"
    r_fecha.font.size = Pt(10)
    r_fecha.font.bold = True
    r_fecha.font.color.rgb = COLOR_TEXTO

    doc.add_page_break()

    # FUNCIONES HELPER
    def agregar_titulo_1(texto):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(texto)
        r.font.name = "Calibri"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = COLOR_AZUL
        return p

    def agregar_titulo_2(texto):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(texto)
        r.font.name = "Calibri"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARIO
        return p

    def agregar_parrafo(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(texto)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = COLOR_TEXTO
        return p

    def agregar_codigo(texto):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        r = p.add_run(texto)
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(56, 189, 248)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 1. INTRODUCCIÓN
    agregar_titulo_1("1. INTRODUCCIÓN Y JUSTIFICACIÓN TÉCNICA")
    agregar_parrafo(
        "En el desarrollo web moderno, la seguridad del lado del cliente representa un pilar crítico. Cross-Site Scripting (XSS), "
        "catalogado como CWE-79 ('Neutralización inadecuada de entradas durante la generación de páginas web') y clasificado en A03: Injection "
        "de OWASP Top 10, permite que un atacante inyecte scripts ejecutables en páginas visitadas por usuarios legítimos, burlando la Política "
        "de Mismo Origen (Same-Origin Policy - SOP) y comprometiendo sesiones, confidencialidad e integridad."
    )

    # 2. ANATOMÍA Y MECÁNICA
    agregar_titulo_1("2. ANATOMÍA Y MECÁNICA PROFUNDA DE CWE-79")
    agregar_parrafo(
        "El fallo surge en el Analizador HTML (Parser) del navegador web. Al encontrar el delimitador '<', el analizador léxico pasa "
        "del 'Data State' al 'Tag Open State'. Si la entrada no confiable contiene la etiqueta <script>, el motor suspende la construcción "
        "del DOM y transfiere el flujo de control al motor de ejecución de JavaScript. Los datos del usuario son promovidos a instrucciones ejecutables."
    )

    agregar_titulo_2("2.1 Los Cuatro Contextos Sintácticos de Inyección")
    tabla_ctx = doc.add_table(rows=5, cols=3)
    tabla_ctx.alignment = WD_TABLE_ALIGNMENT.CENTER
    enc_ctx = ["Contexto Sintáctico", "Ejemplo Vulnerable", "Mecanismo de Ruptura"]
    for j, h in enumerate(enc_ctx):
        c = tabla_ctx.cell(0, j)
        c.text = h
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_ctx = [
        ("1. Cuerpo HTML", "<p>Hola USER</p>", "Inyecta una nueva etiqueta <script> en el DOM."),
        ("2. Atributo HTML", '<input value="USER">', 'Cierra comillas e inyecta eventos (onfocus=alert(1)).'),
        ("3. Bloque JavaScript", "var id = 'USER';", "Rompe el literal de cadena ('; alert(1); //)."),
        ("4. Esquema de URL", '<a href="USER">', 'Inyecta pseudoprotocolos ejecutables (javascript:...).')
    ]
    for i, f in enumerate(filas_ctx, start=1):
        for j, val in enumerate(f):
            c = tabla_ctx.cell(i, j)
            c.text = val
            set_cell_background(c, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 80, 80, 100, 100)
            c.paragraphs[0].runs[0].font.size = Pt(9)
            c.paragraphs[0].runs[0].font.color.rgb = COLOR_TEXTO

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 3. TAXONOMÍA Y DIAGRAMAS DE FLUJO
    agregar_titulo_1("3. TAXONOMÍA Y DIAGRAMAS DE FLUJO POR TIPO")

    agregar_titulo_2("3.1 XSS Reflejado (Tipo I - No Persistente)")
    agregar_parrafo(
        "La carga maliciosa viaja dentro de la petición HTTP (parámetros GET de búsqueda o mensajes de error) y el servidor la refleja "
        "de regreso en el HTML sin escapar. Requiere ingeniería social para engañar a la víctima."
    )
    agregar_codigo(
        "DIAGRAMA DE FLUJO: XSS REFLEJADO (TIPO I)\n"
        "[1. ATACANTE]  ──(Enlace malicioso ?q=<script>)──>  [2. VÍCTIMA]\n"
        "[2. VÍCTIMA]   ──(Petición GET HTTP al sitio)────>  [3. SERVIDOR WEB]\n"
        "[3. SERVIDOR]  ──(Devuelve HTML con script)──────>  [2. NAVEGADOR VÍCTIMA]\n"
        "[2. VÍCTIMA]   💥 Ejecuta script en contexto SOP y exfiltra document.cookie al C2"
    )

    agregar_titulo_2("3.2 XSS Almacenado (Tipo II - Persistente / Máxima Severidad)")
    agregar_parrafo(
        "La inyección se guarda permanentemente en la base de datos o almacenamiento del servidor. Cada usuario que entra a la sección "
        "comprometida ejecuta el script de forma pasiva y desatendida, sin requerir enlaces engañosos."
    )
    agregar_codigo(
        "DIAGRAMA DE FLUJO: XSS ALMACENADO (TIPO II)\n"
        "[1. ATACANTE]  ──(POST formulario con script)───>  [2. SERVIDOR WEB]\n"
        "[2. SERVIDOR]  ──(INSERT INTO comentarios)──────>  [3. BASE DE DATOS]\n"
        "[4. VÍCTIMA N] ──(Navega hacia el portal web)────>  [2. SERVIDOR WEB]\n"
        "[2. SERVIDOR]  ──(SELECT de BD y sirve HTML)────>  [4. NAVEGADOR VÍCTIMA]\n"
        "[4. VÍCTIMA N] 💥 Script se ejecuta automáticamente para todos los visitantes"
    )

    agregar_titulo_2("3.3 XSS Basado en DOM (Tipo 0 / Client-Side XSS)")
    agregar_parrafo(
        "El servidor web no participa en la vulnerabilidad ni recibe la carga maliciosa en sus logs. La carga viaja en el fragmento # "
        "de la URL. Un script cliente lee una Fuente (Source) como location.hash y la escribe en un Sumidero Inseguro (Sink) como innerHTML."
    )
    agregar_codigo(
        "DIAGRAMA DE FLUJO: XSS BASADO EN DOM (TIPO 0)\n"
        "[1. ATACANTE]  ──(Enlace con fragmento #payload)─>  [2. NAVEGADOR CLIENTE]\n"
        "[2. NAVEGADOR] ──(Petición GET sin fragmento #)──>  [3. SERVIDOR WEB]\n"
        "[3. SERVIDOR]  ──(Entrega JS legítimo)───────────>  [2. NAVEGADOR CLIENTE]\n"
        "[2. NAVEGADOR] 🔍 JS lee Source: location.hash\n"
        "[2. NAVEGADOR] ⚠️ JS escribe en Sink inseguro: innerHTML = hash\n"
        "[2. NAVEGADOR] 💥 El navegador compila y ejecuta el script localmente"
    )

    # 4. TRIADA CIA
    agregar_titulo_1("4. IMPACTO EN LA TRIADA DE SEGURIDAD (CIA)")
    agregar_parrafo(
        "• Confidencialidad (ALTO): Robo de tokens de autenticación y lectura de datos sensibles en el DOM.\n"
        "• Integridad (CRÍTICO): Defacement, alteración de transacciones en curso y phishing in-situ.\n"
        "• Disponibilidad (MEDIO): Bloqueo del hilo de ejecución de JavaScript y denegación de servicio local."
    )

    # 5. MITIGACIONES
    agregar_titulo_1("5. ESTRATEGIA INTEGRAL DE DEFENSA EN PROFUNDIDAD")
    agregar_parrafo(
        "1. Output Encoding Contextual: Convertir delimitadores (< > & \" ') en entidades seguras con html.escape().\n"
        "2. Bandera HttpOnly (RFC 6265): Ocultar cookies de sesión a la API document.cookie de JavaScript.\n"
        "3. Content Security Policy (CSP Nivel 3): Cabecera HTTP que prohíbe scripts inline ('unsafe-inline') y eval().\n"
        "4. Sumideros Seguros en DOM: Utilizar element.textContent en lugar de innerHTML."
    )

    # 6. CONCLUSIONES
    agregar_titulo_1("6. CONCLUSIONES Y REFERENCIAS")
    agregar_parrafo(
        "El análisis experimental y conceptual demuestra que XSS es una falla estructural de separación entre datos e instrucciones. "
        "La integración simultánea de codificación contextual, directivas CSP y cookies seguras con HttpOnly erradica la superficie de ataque.\n\n"
        "Referencias: OWASP Top 10 (A03:2021 Injection), MITRE CWE-79, NIST SP 800-53 Rev. 5, RFC 6265."
    )

    ruta_salida = "/home/marioalabi/Nextcloud/Unicaes_Ciclo_8/GESTION DE SEGURIDAD EN SISTEMAS INFORMATICOS/Periodo3/Parcial 3/Informe_Tecnico_Vulnerabilidad_XSS_UNICAES.docx"
    doc.save(ruta_salida)
    print(f"[+] DOCX generado exitosamente: {ruta_salida}")

if __name__ == "__main__":
    crear_informe()
