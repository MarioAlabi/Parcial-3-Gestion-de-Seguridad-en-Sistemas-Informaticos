# Laboratorio Práctico de Seguridad: Demostración y Mitigación de Cross-Site Scripting (XSS)

**Universidad Católica de El Salvador (UNICAES)**  
**Facultad de Ingeniería y Arquitectura — Escuela de Ingeniería en Desarrollo de Software**  
**Asignatura:** Gestión de Seguridad en Sistemas Informáticos  
**Ciclo:** VIII - Ciclo II-2026  
**Responsables:**
- Dennis Ademir Guevara Martínez (2023-GM-607)
- Mario Edgardo Villeda Alabi (2023-VA-651)
- Luis Felipe Balcaceres Silvestre (2023-BS-602)

---

## 1. Descripción del Laboratorio

Este entorno de pruebas ha sido desarrollado como evidencia práctica para el taller de seguridad evaluado en el Parcial 3. Integra una interfaz profesional basada en el concepto **Security Workbench Cyber-Investigativo** (inspirado en la estética técnica de *XSS Academy*), permitiendo experimentar de forma interactiva y controlada los tres tipos principales de Cross-Site Scripting (CWE-79), analizando su comportamiento tanto en estado **Vulnerable** como en estado **Mitigado (Modo Seguro)**.

### Características Principales:
1. **Flujo de Ataque en 3 Fases:**
   - **Fase 1 (Taller del Atacante):** Creación del payload, generación en tiempo real de la URL trampa manipulada (`?q=` en reflejado y `#hash` en DOM) y chips de payloads rápidos.
   - **Fase 2 (Navegador de la Víctima):** Ventana simulada de navegador con barra de URL interactiva, sesión activa de estudiante y renderizado en caliente.
   - **Fase 3 (Impacto Dual y C2):** Terminal de Comando y Control (C2 `malo.com`) que registra cookies exfiltradas y permite demostrar **Session Hijacking** en vivo.
2. **Pipeline Debugger Paso a Paso (F10 / Auto):**
   - 4 Breakpoints de auditoría: `[BP1 Source / Entrada]` ➔ `[BP2 Backend / Bypass HTTP]` ➔ `[BP3 Parser DOM]` ➔ `[BP4 Impacto C2]`.
   - Inspección en vivo de variables (`payload`, filtro `html.escape`, flags `HttpOnly` y `CSP`).
3. **Módulo Didáctico de Blindaje y Código Comparativo:**
   - Explicación detallada de blindaje para cada vector con bloques de código comparativos (*Inseguro vs Blindado*).

---

## 2. Requisitos e Instalación

### Opción Rápida (Recomendada):
Ejecuta el script automatizado:
```bash
./iniciar_laboratorio.sh
```

### Opción Manual:
```bash
pip install -r requirements.txt
python3 app.py
```
El servidor quedará disponible en: `http://localhost:5000`

---

## 3. Escenarios del Laboratorio y Guía de Demostración

### Escenario 1: XSS Reflejado (Búsqueda Web)
- **Ruta:** `/reflejado`
- **Mecanismo:** La entrada recibida mediante el parámetro GET `q` se concatena directamente en el documento HTML.
- **Vectores de prueba pedagógicos:**
  - Standard Script: `<script>alert('PoC: XSS Reflejado');</script>`
  - Evento onerror en imagen: `<img src=x onerror="alert('Ejecución vía atributo HTML')">`
  - Defacement / Modificación estética: `<u><h2 style="color:cyan">Portal Alterado</h2></u>`
- **Demostración de Mitigación:** Al activar el "Modo Seguro" en la barra superior, la función `html.escape()` neutraliza los caracteres `< > " ' &`, convirtiéndolos en entidades inofensivas.

### Escenario 2: XSS Almacenado / Persistente (Tablón de Comentarios)
- **Ruta:** `/almacenado`
- **Mecanismo:** El texto del comentario se guarda en memoria y se sirve a cada cliente subsiguiente que visite la página.
- **Impacto:** Cualquier usuario que acceda a la sección ejecuta el código inyectado de forma desatendida.
- **Demostración de Mitigación:** Sanitización tanto en la persistencia como en la capa de presentación (Template Auto-escaping).

### Escenario 3: XSS Basado en DOM
- **Ruta:** `/dom`
- **Mecanismo:** La fuente no confiable es `location.hash` (el fragmento `#` de la URL). El script del navegador lee el valor y lo asigna a un sumidero inseguro (`innerHTML`).
- **Demostración de Mitigación:** Reemplazo del sumidero inseguro por `textContent` o `innerText`, lo que fuerza al navegador a interpretar los datos como texto plano.

### Escenario 4: Inspección de Sesión y Bandera `HttpOnly`
- **Ruta:** `/inspeccion`
- **Mecanismo:** Permite comprobar en vivo cómo la directiva `HttpOnly` en las cookies del estándar RFC 6265 bloquea el acceso desde `document.cookie`.
- **Clave para la defensa:** Demostrar por qué `HttpOnly` mitiga el robo de cookies (Session Hijacking) pero no detiene otros impactos de XSS como acciones forzadas o phishing visual.

