# UNIVERSIDAD CATÓLICA DE EL SALVADOR
## FACULTAD DE INGENIERÍA Y ARQUITECTURA
### INGENIERÍA EN DESARROLLO DE SOFTWARE
**Gestión de Seguridad en Sistemas Informáticos — Sección “A”**

---

# INFORME TÉCNICO DE VULNERABILIDAD
## Anatomía, Impacto y Defensa Integral de Cross-Site Scripting (XSS - CWE-79)

**Integrantes de Investigación:**
* Guevara Martínez, Dennis Ademir — Carnet: `2023-GM-607`
* Villeda Alabi, Mario Edgardo — Carnet: `2023-VA-651`
* Balcaceres Silvestre, Luis Felipe — Carnet: `2023-BS-602`

**Lugar y Fecha:** Santa Ana, El Salvador — Noviembre de 2026 (Ciclo II-2026)

---

## 1. INTRODUCCIÓN Y JUSTIFICACIÓN TÉCNICA

En el ecosistema del desarrollo web contemporáneo, la seguridad de las aplicaciones del lado del cliente representa uno de los mayores desafíos operacionales para las organizaciones. Entre las vulnerabilidades que aquejan a la capa de presentación, el **Cross-Site Scripting (XSS)**, catalogado por el consorcio MITRE bajo el identificador **CWE-79** (*"Neutralización inadecuada de entradas durante la generación de páginas web"*), ha mantenido una presencia ininterrumpida dentro de las principales categorías de riesgo de OWASP a lo largo de más de dos décadas.

El principio fundamental detrás de una debilidad XSS consiste en la incapacidad del navegador web para distinguir si un fragmento de código JavaScript ejecutable proviene del desarrollador legítimo del sitio o si fue incrustado por un tercero a través de una entrada de datos no confiable. Una vez que el navegador interpreta el script en el contexto de seguridad del origen (*Same-Origin Policy*), el código malicioso adquiere acceso irrestricto a los recursos locales del usuario, permitiendo el secuestro de credenciales de sesión (*Session Hijacking*), la alteración visual del sitio (*Defacement*), el redireccionamiento a portales fraudulentos y la ejecución de operaciones no autorizadas en nombre de la víctima.

El presente informe documenta la investigación, desarrollo experimental y verificación de mecanismos de defensa implementados para la evaluación del Parcial 3 de Gestión de Seguridad en Sistemas Informáticos en la Universidad Católica de El Salvador. A través de un laboratorio interactivo construido ad-hoc, se analizan los vectores de ataque más críticos y se formulan las estrategias de mitigación definitivas aplicadas en la industria del software.

---

## 2. OBJETIVOS DEL TRABAJO

### 2.1 Objetivo General
Analizar técnica y experimentalmente la vulnerabilidad Cross-Site Scripting (CWE-79) mediante la implementación de un laboratorio interactivo y reproducible, formulando las contramedidas de mitigación en profundidad requeridas para el desarrollo seguro de software institucional y empresarial.

### 2.2 Objetivos Específicos
1. Identificar y clasificar las variantes de XSS (Reflejado, Almacenado y Basado en DOM), describiendo su flujo de ejecución y superficies de ataque asociadas.
2. Desarrollar una prueba de concepto (PoC) en un entorno controlado que evidencie el impacto del secuestro de sesiones cuando las cookies de autenticación carecen de atributos de protección.
3. Implementar y validar contramedidas técnicas basadas en estándares internacionales, tales como la codificación de contexto (*Context-Aware Output Encoding*), la directiva de cabeceras HTTP *Content Security Policy (CSP Nivel 3)* y el atributo `HttpOnly`.

---

## 3. FICHA TÉCNICA DE LA VULNERABILIDAD

| Parámetro | Detalle Técnico |
| :--- | :--- |
| **Identificador Estándar** | CWE-79: *Improper Neutralization of Input During Web Page Generation* |
| **Clasificación OWASP** | A03:2021 - Injection (*Top 10 Web Application Security Risks*) |
| **Métrica CVSS v3.1** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N` (Base Score: 6.1 - 7.5 Medio/Alto) |
| **Vector de Explotación** | Red / HTTP (Parámetros GET/POST, Cabeceras HTTP, Base de Datos, Fragmento URL DOM) |
| **Requisito de Interacción** | Requiere interacción del usuario (`UI:R` - Clic en hipervínculo o navegación a página infectada) |
| **Alcance de Seguridad** | Cambiado (`Scope: Changed` - Salta de la aplicación web al contexto del navegador cliente) |
| **Impacto Principal** | Compromiso de Confidencialidad (Robo de tokens) e Integridad (Manipulación del DOM) |

---

## 4. TAXONOMÍA Y CLASIFICACIÓN DE CROSS-SITE SCRIPTING

### 4.1 XSS Reflejado (Tipo I - No Persistente)
El XSS reflejado ocurre cuando una aplicación web recibe datos procedentes de una petición HTTP (usualmente en parámetros de búsqueda o mensajes de error) y los incluye de forma inmediata en la respuesta HTML sin haber aplicado sanitización o codificación de entidades. Dado que la carga maliciosa no se conserva en los servidores, el atacante depende de la ingeniería social: debe inducir a la víctima a pulsar un enlace manipulado enviado por correo electrónico o mensajería instantánea.

```http
GET /buscar?q=<script>alert('XSS_Reflejado')</script> HTTP/1.1
Host: portal-academico.edu.sv

<!-- Respuesta vulnerable del servidor: -->
<p>Resultados para: <script>alert('XSS_Reflejado')</script></p>
```

### 4.2 XSS Almacenado (Tipo II - Persistente)
Representa la variante de mayor severidad operativa. En el XSS almacenado, la entrada proporcionada por el atacante es guardada permanentemente en la infraestructura de persistencia de la aplicación (bases de datos relacionales, documentos NoSQL, sistemas de foros, comentarios o perfiles de usuario). Cuando cualquier usuario navega hacia la sección comprometida, el servidor extrae el script infectado y lo sirve como parte legítima de la página, ejecutándose sin requerir que la víctima pulse ningún enlace externo.

### 4.3 XSS Basado en DOM (Tipo 0 / Client-Side XSS)
A diferencia de las variantes tradicionales, en el XSS basado en DOM la vulnerabilidad no reside en la generación de HTML en el backend, sino completamente en los scripts JavaScript ejecutados en el navegador del cliente. La vulnerabilidad se manifiesta cuando un script local lee datos de una "Fuente" (*Source*) manipulable por el usuario —como `window.location.hash`, `document.referrer` o `document.URL`— y los pasa directamente hacia un "Sumidero" de ejecución (*Sink*) peligroso, tales como `element.innerHTML`, `document.write` o `eval()`.

---

## 5. PRUEBA DE CONCEPTO (PoC) Y EVIDENCIA DEL LABORATORIO

Para sustentar la investigación con evidencia práctica verificable, el equipo diseñó y programó un laboratorio interactivo en Python (Flask) con una interfaz gráfica basada en Bootstrap. Dicho entorno permite alternar en tiempo real entre un modo vulnerable y un modo mitigado mediante un interruptor en el panel de control.

### 5.1 Escenario 1: Demostración de Inyección Reflejada
En el módulo de búsqueda `/reflejado`, se comprobó que la entrada directa del usuario en el parámetro GET `q` era renderizada sin escapar. Se introdujo una carga de prueba estructurada mediante un vector de imagen HTML con controlador de eventos:
```html
<img src=x onerror="alert('PoC_UNICAES: Ejecución de script vía evento onerror')">
```
*Resultado:* El navegador intentó cargar una imagen inexistente desde `x`, disparando de inmediato la excepción y ejecutando la función `alert()` en el contexto de origen del sitio web. Al activar el "Modo Seguro", el servidor procesó el parámetro con `html.escape(consulta)`, reemplazando `<` por `&lt;` y `>` por `&gt;`, provocando que el navegador mostrara la carga como simple texto plano.

### 5.2 Escenario 2: Demostración de Persistencia en Tablón de Comentarios
En la ruta `/almacenado`, se simuló un sistema colaborativo donde los mensajes de los usuarios son conservados en memoria. Al enviar un mensaje con código inyectado, este quedó disponible para cualquier sesión subsecuente, demostrando la capacidad de un atacante para infectar pasivamente a múltiples visitantes sin interacción directa.

### 5.3 Escenario 3: Manipulación de Flujo en el DOM
En la vista `/dom`, se inspeccionó un script cliente encargado de personalizar la bienvenida a partir del fragmento `#` de la URL. Se contrastó la ejecución vulnerable provocada por `contenedor.innerHTML = hash` frente a la implementación segura con `contenedor.textContent = hash`, confirmando que esta última propiedad trata cualquier delimitador de etiquetas como caracteres literales de cadena, eliminando el riesgo de ejecución sin sobrecosto de rendimiento.

### 5.4 Escenario 4: Auditoría de Cookies y Mitigación con HttpOnly
Para ilustrar el riesgo de *Session Hijacking*, se configuró una cookie de prueba `session_auth_token`. En el modo vulnerable, al invocar `document.cookie` desde la consola de JavaScript, el valor del token fue expuesto de forma íntegra. Posteriormente, al marcar la bandera `httponly=True` en la cabecera `Set-Cookie`, la API `document.cookie` retornó una cadena vacía, evidenciando que el motor de JavaScript queda físicamente inhabilitado para leer el secreto de sesión conforme al estándar RFC 6265.

---

## 6. ANÁLISIS DE IMPACTO EN LA TRIADA DE SEGURIDAD (CIA)

| Pilar de Seguridad | Nivel de Compromiso | Manifestación del Ataque XSS |
| :--- | :---: | :--- |
| **Confidencialidad** | **ALTO** | Exfiltración de credenciales de sesión, tokens JWT, información personal ingresada en formularios y lectura de datos privados en el DOM. |
| **Integridad** | **CRÍTICO** | Desfiguración del portal (*Defacement*), alteración de transacciones financieras en curso, inserción de falsos campos de autenticación (*Phishing in-site*). |
| **Disponibilidad** | **MEDIO / BAJO** | Generación de bucles infinitos en el hilo principal de JavaScript, bloqueo del navegador del usuario final y denegación de servicio local. |

---

## 7. ESTRATEGIA INTEGRAL DE DEFENSA EN PROFUNDIDAD

La mitigación eficaz del Cross-Site Scripting no puede depender de una sola capa defensiva. Siguiendo el principio de Defensa en Profundidad (*Defense in Depth*), se deben articular controles a nivel de aplicación, arquitectura y transporte:

### 7.1 Codificación de Salida Sensible al Contexto (Context-Aware Output Encoding)
Es la regla de oro para erradicar XSS: nunca insertar datos no confiables en una página sin antes codificarlos en función del contexto sintáctico exacto donde se renderizarán (HTML Body, Atributos HTML, Bloques Script, URLs o Reglas CSS). En entornos modernos, los motores de plantillas como Jinja2, Blade o React aplican auto-escaping por defecto, el cual nunca debe desactivarse mediante funciones peligrosas como `safe` o `dangerouslySetInnerHTML`.

### 7.2 Política de Seguridad de Contenido (Content Security Policy - CSP Nivel 3)
CSP es una cabecera de respuesta HTTP (`Content-Security-Policy`) que restringe los orígenes autorizados desde los cuales el navegador puede cargar y ejecutar recursos ejecutables. Al definir una política estricta, se inhabilita la ejecución de scripts en línea (`'unsafe-inline'`) y la función `eval()`, neutralizando la gran mayoría de cargas XSS incluso si lograron insertarse en el HTML:
```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; object-src 'none'; base-uri 'self';
```

### 7.3 Endurecimiento de Cookies de Sesión (Atributos RFC 6265)
Todas las cookies asociadas al estado de autenticación deben emitirse acompañadas de tres banderas obligatorias:
* `HttpOnly`: Oculta la cookie a las APIs de JavaScript del navegador, impidiendo el robo directo de la sesión.
* `Secure`: Exige que la cookie únicamente sea transmitida mediante canales cifrados con TLS/HTTPS.
* `SameSite=Strict` o `Lax`: Limita la inclusión de la cookie en peticiones entre orígenes cruzados, mitigando ataques de CSRF.

### 7.4 Sanitización Rigurosa de HTML Rico
En aplicaciones donde se requiere que los usuarios ingresen formato HTML (editores WYSIWYG, foros formateados), se debe emplear una biblioteca de sanitización probada como DOMPurify en el cliente o Bleach/sanitize-html en el servidor. Estas herramientas analizan el árbol DOM y filtran minuciosamente cualquier etiqueta peligrosa (`<script>`, `<iframe>`, `<object>`) o atributo con manejadores de eventos (`onload`, `onerror`, `onclick`).

---

## 8. CONCLUSIONES

1. El Cross-Site Scripting (CWE-79) continúa siendo una amenaza de primer nivel debido a la continua expansión de aplicaciones web de página única (SPA) y la creciente delegación de lógica de negocio hacia el lado del cliente (navegador).
2. La demostración experimental en el laboratorio desarrollado evidenció que un fallo en la validación o codificación de entradas permite a un atacante ejecutar código con los mismos privilegios del usuario autenticado, transformando el navegador en un vector de ataque activo contra la infraestructura institucional.
3. La defensa ante XSS debe ser estructural: la codificación contextual de salida, el aprovisionamiento de cabeceras CSP robustas y el confinamiento de credenciales mediante `HttpOnly` conforman una tríada de salvaguardas que reduce drásticamente la superficie de ataque en los sistemas de información contemporáneos.

---

## 9. REFERENCIAS BIBLIOGRÁFICAS

* **OWASP Foundation.** (2021). *OWASP Top 10:2021 - A03:2021-Injection*. Recuperado de https://owasp.org/Top10/A03_2021-Injection/
* **MITRE Corporation.** (2024). *CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')*. Common Weakness Enumeration.
* **National Institute of Standards and Technology (NIST).** (2020). *Security and Privacy Controls for Information Systems and Organizations* (Special Publication 800-53, Rev. 5). U.S. Department of Commerce.
* **World Wide Web Consortium (W3C).** (2023). *Content Security Policy Level 3*. W3C Working Draft.
* **Barth, A.** (2011). *HTTP State Management Mechanism* (RFC 6265). Internet Engineering Task Force (IETF).

