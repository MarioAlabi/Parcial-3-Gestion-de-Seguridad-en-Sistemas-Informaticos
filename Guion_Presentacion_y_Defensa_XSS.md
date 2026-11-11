# GUION DE PRESENTACIÓN Y BANCO DE DEFENSA PARA EL PARCIAL
## Taller Técnico: Cross-Site Scripting (XSS - CWE-79)
**Universidad Católica de El Salvador (UNICAES)**  
**Gestión de Seguridad en Sistemas Informáticos — Sección “A”**  
**Integrantes:** Dennis Ademir Guevara • Mario Edgardo Villeda • Luis Felipe Balcaceres  
**Duración Estimada:** 12 - 15 Minutos

---

## 1. REPARTO ESTRATÉGICO DE ROLES Y TIEMPOS

| Bloque | Responsable | Tema / Actividad | Tiempo |
| :--- | :--- | :--- | :---: |
| **Bloque 1** | **Dennis Guevara** | Introducción, Definición formal de XSS (CWE-79, OWASP A03), Clasificación y Vectores. | 3 - 4 min |
| **Bloque 2** | **Mario Villeda** | Demostración técnica en vivo con el Laboratorio: XSS Reflejado, Almacenado y DOM. | 5 - 6 min |
| **Bloque 3** | **Luis Balcaceres** | Riesgo de Session Hijacking, Mitigaciones en caliente (HttpOnly, Output Encoding, CSP) y Conclusiones. | 3 - 4 min |
| **Bloque 4** | **Todo el Equipo** | Sesión de Preguntas y Respuestas del Docente / Audiencia. | 3 - 5 min |

---

## 2. GUION DE EXPOSICIÓN PASO A PASO

### BLOQUE 1: INTRODUCCIÓN TEÓRICA (Dennis Guevara)
*(Diapositivas 1 a 4)*

* **Inicio (Saludo Formal):**
  > *"Buenos días/tardes ingeniero y compañeros. Hoy nuestro equipo presentará el taller práctico sobre una de las vulnerabilidades más críticas y persistentes en el desarrollo web moderno: **Cross-Site Scripting**, catalogado como **CWE-79** y ubicado en el puesto **A03: Injection** del OWASP Top 10."*

* **Concepto Clave (La raíz del fallo):**
  > *"¿Por qué ocurre XSS? La raíz del problema es la **falta de neutralización y codificación de las entradas** proporcionadas por el usuario. Cuando una aplicación web toma datos de una fuente no confiable y los inserta directamente en la respuesta HTML, el navegador web del cliente no tiene forma de distinguir si ese código fue escrito por el desarrollador o por un tercero malicioso. En consecuencia, ejecuta el script dentro del contexto de seguridad del origen legítimo."*

* **Taxonomía / Clasificación:**
  > *"Existen tres grandes categorías que demostraremos hoy:*
  > 1. ***XSS Reflejado (Tipo I):** La carga viaja en la petición (por ejemplo un parámetro GET) y el servidor la refleja de inmediato. Requiere que la víctima haga clic en un enlace manipulado.*
  > 2. ***XSS Almacenado (Tipo II):** El más peligroso; el script se guarda permanentemente en la base de datos o almacenamiento del servidor. Cualquier usuario que visite la página se infecta de forma pasiva.*
  > 3. ***XSS Basado en DOM (Tipo 0):** Ocurre puramente en el cliente cuando un script local lee una fuente como `location.hash` y la escribe en un sumidero peligroso como `innerHTML`.*
  >
  > *A continuación, mi compañero Mario ejecutará la demostración práctica en vivo con nuestro laboratorio desarrollado."*

---

### BLOQUE 2: DEMOSTRACIÓN TÉCNICA EN VIVO (Mario Villeda)
*(Pantalla compartida en `http://localhost:5000` - Security Workbench)*

* **Paso 1: Presentación del Security Workbench (Panel Dividido)**
  > *"Gracias Dennis. Para este taller diseñamos una arquitectura profesional de auditoría llamada **Security Workbench** dividida en dos paneles sincronizados por AJAX:*
  > * A la **izquierda (50%)**: tenemos el portal web académico tal como lo vería un usuario o víctima.
  > * A la **derecha (50%)**: tenemos nuestra consola de auditoría DevSecOps, compuesta por un **Pipeline Debugger** paso a paso arriba y una terminal de **Servidor C2 Atacante** abajo.*
  > * En la barra superior contamos con el switch global para alternar entre **Modo Vulnerable** y **Modo Seguro (Mitigado)**."*

* **Paso 2: Demostración de XSS Reflejado con el Pipeline Debugger (Pestaña 1)**
  > *"Comenzamos con la búsqueda reflejada. Hacemos clic en el chip rápido `<script>alert(1)</script>` y en lugar de ejecutar a ciegas, pulsamos el botón **`[ 🐞 Depurar ]`**.*
  > 
  > *Observen cómo la ejecución se congela en el **Breakpoint 1 (Source)** en el depurador de la derecha. El input del usuario fue capturado.
  > Presiono **F10** para avanzar al **Breakpoint 2 (Backend)**: al estar en modo vulnerable, el servidor no aplicó ningún filtro y concatenó la carga en bruto en la respuesta HTML.
  > Presiono **F10** nuevamente: llegamos al **Breakpoint 3 (DOM Parser)**, donde el motor del navegador interpreta la etiqueta y ejecuta el script.
  > Finalmente avanzamos al **Breakpoint 4 (Impacto)**: la carga extrae las credenciales y las transmite en tiempo real hacia nuestra terminal C2 inferior.*
  > 
  > *Ahora activo el **Modo Seguro** en la barra superior y repito la depuración: observen cómo en el **Breakpoint 2**, la caja se ilumina en verde: `html.escape()` neutralizó los caracteres `<` y `>`, convirtiéndolos en texto plano inocuo y deteniendo el ataque de raíz."*

* **Paso 3: Demostración de XSS Almacenado (Pestaña 2)**
  > *"Pasamos a la pestaña 2: Tablón de Comentarios. Aquí el riesgo es persistente. Publicamos el payload de robo de credenciales: `<script>fetch('/api/exfiltrar?datos=' + document.cookie)...</script>`.*
  > 
  > *El comentario se guarda directamente en la base de datos del servidor. A partir de este momento, cualquier estudiante o docente que ingrese al portal cargará pasivamente el mensaje y su sesión será exfiltrada al C2 sin necesidad de haber hecho clic en un enlace manipulado."*

* **Paso 4: Demostración de XSS en DOM (Pestaña 3)**
  > *"En la pestaña 3 demostramos el XSS en DOM. Aquí el servidor backend no interviene en absoluto.
  > Al pulsar **`[ 🐞 Ejecutar innerHTML ]`**, observen el depurador: el Breakpoint 2 marca explícitamente **'Servidor Omitido'**, porque el vector reside 100% en el código JavaScript del cliente.
  > Al pulsar **`[ Ejecutar textContent ]`**, vemos cómo el uso de una API de asignación segura previene la interpretación de etiquetas HTML.
  > 
  > Ahora mi compañero Luis Felipe explicará la anatomía del secuestro de sesión y las tres capas de defensa en profundidad."*

---

### BLOQUE 3: IMPACTO, MITIGACIONES Y CONCLUSIÓN (Luis Balcaceres)
*(Atención centrada en la Terminal C2 inferior derecha y Diapositivas 8 a 11)*

* **Paso 1: El Secuestro de Sesión (Session Hijacking)**
  > *"Gracias Mario. Como observaron en la terminal C2 inferior derecha, el verdadero objetivo de un cibercriminal no es mostrar una ventana de alerta, sino el **Session Hijacking**. Mediante `document.cookie`, el atacante captura el token `session_auth_token` de la víctima y toma control total de su cuenta sin conocer su contraseña.*
  > 
  > *Observen la terminal en Modo Vulnerable: recibimos la conexión con la cookie íntegra en color rojo."*

* **Paso 2: Las Tres Capas de Defensa en Profundidad (OWASP)**
  > *"Para erradicar y contener este riesgo, aplicamos tres capas de seguridad indispensables:*
  > 1. ***Bandera HttpOnly (RFC 6265):** Al activar el Modo Seguro, el servidor emite la cookie con el atributo `HttpOnly=True`. Observen nuestra terminal C2: el atacante ya no puede ver el token de autenticación; JavaScript solo tiene acceso a variables cosméticas no sensibles.*
  > 2. ***Codificación Contextual (Output Encoding):** Aplicar funciones como `html.escape()` en Python o su equivalente según el contexto sintáctico (HTML body, atributos, JS literal).*
  > 3. ***Content Security Policy (CSP Nivel 3):** Cabecera HTTP que prohíbe scripts incrustados sin nonce (`unsafe-inline`) y bloquea conexiones a servidores C2 no autorizados mediante la directiva `connect-src`.*"

* **Cierre Formal:**
  > *"En conclusión, la seguridad web moderna exige asumir que cualquier entrada del usuario es hostil y que ninguna defensa aislada es infalible. Con la combinación de codificación contextual, CSP y banderas de sesión seguras, blindamos el ecosistema institucional. Muchas gracias por su atención; quedamos listos para responder las preguntas del catedrático."*

---

## 3. BANCO DE PREGUNTAS DIFÍCILES DEL DOCENTE (CON RESPUESTAS EXACTAS)

### Pregunta 1: *"¿Si tengo la bandera HttpOnly activa en mis cookies, ya no tengo que preocuparme por XSS?"*
* **Respuesta para sacar 10:**  
  *"No, ingeniero. La bandera `HttpOnly` mitiga específicamente el **robo directo del token de sesión** a través de `document.cookie`. Sin embargo, el atacante aún tiene la capacidad de ejecutar código en el navegador de la víctima. Podría realizar peticiones asíncronas no autorizadas en su nombre (utilizando `fetch` o `XMLHttpRequest`, las cuales envían la cookie automáticamente por detrás), desfigurar la página (*defacement*), redirigir a un portal de phishing o capturar pulsaciones de teclado (*keylogging*). Por eso HttpOnly es una medida de mitigación de impacto, pero no resuelve la causa raíz de la inyección."*

### Pregunta 2: *"¿Cuál es la diferencia exacta entre Sanitización y Codificación (Encoding)?"*
* **Respuesta para sacar 10:**  
  *"La **Sanitización** consiste en limpiar o remover activamente etiquetas y atributos peligrosos de una entrada (por ejemplo, eliminando `<script>` o `onerror` con librerías como DOMPurify cuando necesitamos permitir HTML enriquecido). La **Codificación (Encoding)**, en cambio, no elimina nada: convierte los caracteres de control sintáctico en sus entidades equivalentes (por ejemplo, `<` pasa a ser `&lt;`). De este modo, el navegador interpreta la entrada como datos visuales y nunca como instrucciones ejecutables."*

### Pregunta 3: *"¿Por qué un Web Application Firewall (WAF) perimetral no es suficiente para erradicar XSS?"*
* **Respuesta para sacar 10:**  
  *"Porque los WAFs se basan en firmas y patrones de expresiones regulares en el tráfico de red. Existen infinitas formas de ofuscar y mutar un payload XSS (MutaXSS, codificación en base64, manipulación de espacios y eventos HTML5) que pueden evadir la inspección del WAF. Además, un WAF perimetral no puede inspeccionar ni proteger contra **DOM-based XSS**, ya que esa inyección se procesa exclusivamente dentro de la memoria del navegador del cliente y nunca viaja en el cuerpo de la petición HTTP hacia el servidor."*

### Pregunta 4: *"¿Cómo previene Content Security Policy (CSP) la ejecución de XSS?"*
* **Respuesta para sacar 10:**  
  *"CSP actúa como una lista blanca (whitelist) a nivel de navegador mediante la cabecera `Content-Security-Policy`. Por defecto, una política estricta prohíbe la ejecución de scripts incrustados en línea (`'unsafe-inline'`) y la función `eval()`. Solo permite ejecutar scripts cargados desde orígenes explícitamente autorizados o que contengan un token criptográfico único de un solo uso (*nonce*) emitido por el servidor en cada petición. Si un atacante inyecta una etiqueta `<script>` en el HTML, el navegador detecta que no tiene el nonce válido y bloquea su ejecución de inmediato."*

### Pregunta 5: *"¿Por qué XSS Almacenado tiene mayor puntuación CVSS que XSS Reflejado?"*
* **Respuesta para sacar 10:**  
  *"En la métrica CVSS v3.1, aunque ambos comparten métricas similares de Confidencialidad e Integridad, el XSS Almacenado tiene un vector de ataque mucho más severo porque no depende de engañar activamente a la víctima mediante un enlace específico (ingeniería social). La carga permanece latente en la base de datos de la empresa, lo que permite afectar de manera masiva, silenciosa y permanente a cualquier usuario autenticado, incluidos administradores del sistema."*

