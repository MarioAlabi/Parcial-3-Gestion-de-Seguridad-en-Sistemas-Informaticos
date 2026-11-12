# Parcial 3: Gestión de Seguridad en Sistemas Informáticos

**Universidad Católica de El Salvador (UNICAES)**  
**Facultad de Ingeniería y Arquitectura — Escuela de Ingeniería en Desarrollo de Software**  
**Asignatura:** Gestión de Seguridad en Sistemas Informáticos  
**Ciclo:** VIII — Ciclo II-2026  

---

### Integrantes del Equipo:
* **Dennis Ademir Guevara Martínez** (2023-GM-607)
* **Mario Edgardo Villeda Alabi** (2023-VA-651)
* **Luis Felipe Balcaceres Silvestre** (2023-BS-602)

---

## 📌 Contenido del Repositorio

Este repositorio contiene la entrega técnica integral correspondiente al Parcial 3, enfocada en la investigación, explotación controlada, análisis pericial y mitigación en profundidad de la vulnerabilidad **Cross-Site Scripting (XSS / CWE-79)**.

```
├── index.html                             # PORTAL CENTRAL (Homepage unificada del ecosistema)
├── ebook_interactivo.html                 # 2. Ebook Interactivo (Expediente web multimedia)
├── revista_tecnica.html                   # 3. Revista Técnica (Edición editorial de 20 páginas)
├── Revista_Tecnica_XSS_Academy.pdf        # PDF oficial de la Revista Técnica (20 páginas)
├── informe_tecnico.html                   # 4. Informe Técnico (Visor web oficial UNICAES)
├── Informe_Tecnico_Vulnerabilidad_XSS_UNICAES.docx  # Informe técnico en formato Word
├── Informe_Tecnico_Vulnerabilidad_XSS_UNICAES.pdf   # Informe técnico en formato PDF oficial
├── Informe_Tecnico_Vulnerabilidad_XSS_UNICAES.md    # Informe técnico en formato Markdown
├── Presentacion_XSS_UNICAES.html          # Diapositivas web interactivas para exposición
├── Presentacion_XSS_UNICAES.pptx          # Presentación en formato PowerPoint
├── Guion_Presentacion_y_Defensa_XSS.md              # Guión y preguntas clave para la defensa
├── Laboratorio_XSS/                       # 1. Security Workbench (Simulador interactivo en Flask)
│   ├── app.py                             # Servidor Flask con los 3 vectores y enrutador del portal
│   ├── iniciar_laboratorio.sh             # Script de arranque automatizado
│   ├── templates/index.html               # Interfaz del Workbench y Pipeline Debugger
│   ├── Dockerfile / docker-compose.yml    # Contenedorización lista para producción
│   └── README.md                          # Manual técnico del laboratorio
└── Laboratorio_XSS_UNICAES.zip            # Paquete comprimido portable de entrega
```

---

## 🚀 Puesta en Marcha del Laboratorio

### Requisitos:
* Python 3.8 o superior
* Flask (`pip install flask`)

### Ejecución rápida:
```bash
cd Laboratorio_XSS
./iniciar_laboratorio.sh
```
O de forma manual:
```bash
pip install -r Laboratorio_XSS/requirements.txt
python3 Laboratorio_XSS/app.py
```
El simulador interactivo iniciará en: `http://localhost:5000`

---

## 🛡️ Aspectos Clave Demostrados

1. **Flujo de Ataque en 3 Fases:**
   - **Fase 1 (Taller del Atacante):** Creación de enlaces manipulados y comentarios de ingeniería social con previsualización en caliente.
   - **Fase 2 (Navegador Víctima):** Simulación del entorno de navegación de la víctima (sesión autenticada de estudiante).
   - **Fase 3 (Terminal C2 Atacante):** Servidor de Comando y Control (`malo.com/c2`) que captura tokens y ejecuta secuestro de sesión (*Session Hijacking*).

2. **Pipeline Debugger en Vivo (Paso a Paso con F10):**
   - 4 Breakpoints que inspeccionan el ciclo de vida de la inyección: `[BP1 Source]` ➔ `[BP2 Backend]` ➔ `[BP3 Parser DOM]` ➔ `[BP4 Impacto C2]`.

3. **Demostración de Blindaje en Vivo (Toggle Seguro / Vulnerable):**
   - **XSS Reflejado:** Sanitización con *Context-Aware Output Encoding* (`html.escape`).
   - **XSS Almacenado:** Sanitización en persistencia y presentación + bandera `HttpOnly`.
   - **XSS Basado en DOM:** Reemplazo de sumideros peligrosos (`innerHTML`) por sumideros seguros (`textContent`).
   - **Cabeceras de Defensa:** Implementación de *Content Security Policy (CSP)*.

