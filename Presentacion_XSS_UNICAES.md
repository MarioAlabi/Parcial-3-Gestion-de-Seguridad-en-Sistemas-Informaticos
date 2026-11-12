# PRESENTACIÓN: CROSS-SITE SCRIPTING (XSS)
## Conceptos Fundamentales, Clasificación, Casos Reales y Prevención (CWE-79)

**Universidad Católica de El Salvador (UNICAES)**  
**Facultad de Ingeniería y Arquitectura — Escuela de Ingeniería en Desarrollo de Software**  
**Asignatura:** Gestión de Seguridad en Sistemas Informáticos — Sección “A”  
**Evaluación:** Parcial 3  
**Lugar y Fecha:** Santa Ana, El Salvador — Noviembre de 2026  

---

## ESTRUCTURA DE LA PRESENTACIÓN (8 DIAPOSITIVAS)

* **Diapositiva 1:** Portada Institucional
* **Diapositiva 2:** Integrantes del Equipo
* **Diapositiva 3:** ¿Qué es Cross-Site Scripting (XSS)? (+ Diagrama Explicativo)
* **Diapositiva 4:** Tipo 1: XSS Reflejado (No Persistente) (+ Diagrama de Flujo)
* **Diapositiva 5:** Tipo 2: XSS Almacenado (Persistente) (+ Diagrama de Flujo)
* **Diapositiva 6:** Tipo 3: XSS Basado en DOM (Client-Side) (+ Diagrama de Flujo)
* **Diapositiva 7:** Casos Famosos de Ataques XSS en la Historia (+ Gráfico Histórico)
* **Diapositiva 8:** ¿Cómo Prevenir y Defendernos de XSS? (+ Resumen Visual)

---

<!-- SLIDE 1 -->
# DIAPOSITIVA 1: PORTADA

### Contenido en Pantalla:
* **UNIVERSIDAD CATÓLICA DE EL SALVADOR • FIA**
* # CROSS-SITE SCRIPTING (XSS)
* ### Conceptos Fundamentales, Clasificación de Tipos, Casos Reales y Prevención
* **Gestión de Seguridad en Sistemas Informáticos — Sección “A”**
* *Evaluación del Parcial 3 • Santa Ana, El Salvador • Noviembre de 2026*

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"Buenos días/tardes ingeniero y compañeros. Hoy presentaremos de forma clara y directa qué es Cross-Site Scripting (XSS), sus principales tipos, ejemplos reales famosos y cómo se previenen en el desarrollo de software seguro."*

---

<!-- SLIDE 2 -->
# DIAPOSITIVA 2: INTEGRANTES DE INVESTIGACIÓN

### Contenido en Pantalla:
```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│          INTEGRANTE 01          │          INTEGRANTE 02          │          INTEGRANTE 03          │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│  Dennis Ademir Guevara Martínez │   Mario Edgardo Villeda Alabi   │ Luis Felipe Balcaceres Silvestre│
│       Carnet: 2023-GM-607       │       Carnet: 2023-VA-651       │       Carnet: 2023-BS-602       │
│  Ing. en Desarrollo de Software │  Ing. en Desarrollo de Software │  Ing. en Desarrollo de Software │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"Nuestro equipo de investigación está conformado por Dennis Guevara, Mario Villeda y Luis Balcaceres, estudiantes de Ingeniería en Desarrollo de Software de la Universidad Católica de El Salvador."*

---

<!-- SLIDE 3 -->
# DIAPOSITIVA 3: ¿QUÉ ES CROSS-SITE SCRIPTING (XSS)?

### Contenido en Pantalla:
* **Columna Izquierda (Descripción Breve y Sencilla):**
  * **¿Qué es?** Es una vulnerabilidad web que permite a un atacante inyectar scripts maliciosos (generalmente JavaScript) dentro de páginas web que otros usuarios visitan.
  * **¿Por qué ocurre?** Porque el sitio web recibe datos del usuario y los muestra en pantalla sin validarlos ni codificarlos antes.
  * **¿Cuál es el peligro?** El navegador web no puede saber si el código es legítimo o malicioso y lo ejecuta con todos los privilegios del sitio web.
  * **Consecuencias directas:** Robo de cuentas y contraseñas (Session Hijacking), alteración visual de la página y redirección a portales falsos.
* **Columna Derecha (Gráfico Conceptual):**
  * *Diagrama visual que ilustra:* `Atacante -> Inyecta Payload -> Sitio Web Vulnerable -> Navegador de la Víctima -> Robo de Cookies y Sesión`.

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"Cross-Site Scripting (XSS) ocurre cuando un atacante logra inyectar código JavaScript malicioso en una página web. Como el navegador de la víctima no tiene cómo distinguir si ese código fue escrito por el desarrollador legítimo o por un tercero, lo ejecuta ciegamente, permitiendo robar cookies de sesión o alterar la interfaz."*

---

<!-- SLIDE 4 -->
# DIAPOSITIVA 4: TIPO 1 — XSS REFLEJADO (NO PERSISTENTE)

### Contenido en Pantalla:
* **Columna Izquierda (Características Principales):**
  * **¿Cómo viaja?** El script malicioso viaja directamente dentro de la petición HTTP (por ejemplo, en un parámetro de búsqueda en la URL como `?q=<script>...`).
  * **No es persistente:** El servidor toma ese parámetro y lo refleja de inmediato en la respuesta HTML, pero **no lo guarda** en la base de datos.
  * **Requiere engaño:** El atacante debe convencer a la víctima de hacer clic en un enlace manipulado (enviado por correo, chat o redes sociales).
  * **Mitigación básica:** Codificar la salida en el servidor (con `html.escape()`) para que los caracteres `<` y `>` se muestren como texto plano.
* **Columna Derecha (Gráfico de Flujo):**
  * *Diagrama visual que ilustra:* `1. Enlace malicioso enviado -> 2. Víctima hace clic -> 3. Servidor refleja sin guardar -> 4. Script se ejecuta en el navegador`.

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"El XSS Reflejado no se almacena en el servidor. El código malicioso viaja en el propio enlace. Cuando la víctima hace clic, el servidor devuelve el parámetro sin escapar en la página y el navegador lo ejecuta. Depende de la ingeniería social para engañar a la víctima."*

---

<!-- SLIDE 5 -->
# DIAPOSITIVA 5: TIPO 2 — XSS ALMACENADO (PERSISTENTE)

### Contenido en Pantalla:
* **Columna Izquierda (El Tipo Más Peligroso):**
  * **Guardado en el servidor:** El atacante envía el script en un formulario (como comentarios de un blog, foros o campos de perfil) y **queda grabado en la Base de Datos**.
  * **Infección pasiva y masiva:** Cada vez que cualquier usuario entra a ver esa sección, el servidor le envía el código malicioso automáticamente.
  * **Sin enlaces engañosos:** La víctima no necesita hacer clic en ningún enlace raro: solo con entrar a la página web legítima ya resulta infectada.
  * **Impacto crítico:** Permite robar las sesiones de cientos o miles de usuarios en segundos, incluidos los administradores del sistema.
* **Columna Derecha (Gráfico de Flujo):**
  * *Diagrama visual que ilustra:* `1. Atacante envía comentario -> 2. Servidor guarda en BD -> 3. Múltiples víctimas visitan la web -> 4. Infección pasiva y masiva para todos`.

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"El XSS Almacenado es el más peligroso de todos. El código malicioso queda guardado permanentemente en la base de datos de la empresa. No hace falta engañar a nadie con enlaces falsos: cualquier usuario que entre a revisar el foro o la página institucional se infecta de manera pasiva y automática."*

---

<!-- SLIDE 6 -->
# DIAPOSITIVA 6: TIPO 3 — XSS BASADO EN DOM (CLIENT-SIDE)

### Contenido en Pantalla:
* **Columna Izquierda (100% en el Navegador Cliente):**
  * **El servidor no interviene:** A diferencia de los otros tipos, el servidor web nunca recibe ni procesa el código malicioso. Ocurre enteramente en el cliente.
  * **Fuente Peligrosa (Source):** Un script JavaScript local lee datos manipulables de la URL, como el fragmento `#` (`location.hash`).
  * **Sumidero Inseguro (Sink):** Escribe ese valor directamente en la pantalla usando funciones peligrosas como `element.innerHTML` o `eval()`.
  * **Ciego para los WAFs:** Como el fragmento `#` nunca se envía en la petición HTTP hacia el servidor, los firewalls tradicionales no lo pueden detectar.
  * **Solución en Frontend:** Reemplazar `innerHTML` por `textContent` para que el navegador solo escriba texto literal sin interpretar etiquetas.
* **Columna Derecha (Gráfico de Flujo):**
  * *Diagrama visual que ilustra:* `1. URL con #hash -> 2. Servidor backend omitido -> 3. JS local lee Source -> 4. Escribe en innerHTML (Sink) -> 5. Se ejecuta en el DOM`.

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"En el XSS basado en DOM el servidor ni se entera de lo que está pasando. El fallo está en los scripts JavaScript del frontend que leen datos de la URL después del numeral con `location.hash` y los insertan con `innerHTML`. La solución es cambiar a `textContent`, que trata todo como texto literal."*

---

<!-- SLIDE 7 -->
# DIAPOSITIVA 7: CASOS FAMOSOS DE ATAQUES XSS EN LA HISTORIA

### Contenido en Pantalla:
* **Columna Izquierda (Tres Casos Reales de Alto Impacto):**
  * **1. Gusano Samy en MySpace (2005):** El ataque XSS más rápido de la historia. Samy Kamkar infectó a más de **1 millón de usuarios en menos de 20 horas** usando XSS Almacenado en su perfil. Forzaba a los visitantes a agregarlo como amigo con la frase *"Samy is my hero"* y saturó los servidores de MySpace hasta obligar a apagarlos.
  * **2. Gusano de Twitter / TweetDeck (2014):** Un tweet con script malicioso forzaba un **auto-retweet masivo** simplemente al pasar el cursor por encima del mensaje. Se propagó en cascada a más de 80,000 cuentas en cuestión de minutos y obligó al cierre temporal del servicio.
  * **3. Espionaje en Yahoo! Mail (2015):** XSS Almacenado dentro de correos electrónicos en formato HTML. Con solo abrir un correo sospechoso, el atacante podía **leer todos los emails privados de la víctima** y enviar correos haciéndose pasar por ella.
* **Columna Derecha (Gráfico Histórico de Casos):**
  * *Diagrama visual con tarjetas de los 3 ataques, número de víctimas y consecuencias reales.*

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"Para que veamos que el XSS no es solo un concepto teórico de laboratorio, ha dejado huella en la historia: el Gusano Samy en MySpace infectó a un millón de perfiles en menos de un día; el gusano de TweetDeck provocó retweets automáticos descontrolados en 2014; y en Yahoo Mail bastaba con abrir un correo para que un atacante leyera todos tus mensajes privados."*

---

<!-- SLIDE 8 -->
# DIAPOSITIVA 8: ¿CÓMO PREVENIR Y DEFENDERNOS DE XSS?

### Contenido en Pantalla:
* **Columna Izquierda (Tres Reglas de Oro):**
  * **1. Codificación de Salida (Output Encoding):** Nunca insertar datos del usuario sin codificar. Convertir `<` en `&lt;` y `>` en `&gt;` para que el navegador los pinte como texto plano y jamás los ejecute.
  * **2. Cookies con Bandera `HttpOnly`:** Configurar `HttpOnly=True` en las cookies de sesión. Esto oculta físicamente el secreto a `document.cookie` e impide el robo de cuentas.
  * **3. Content Security Policy (CSP):** Cabecera HTTP que prohíbe la ejecución de scripts en línea (`'unsafe-inline'`) y bloquea conexiones a servidores externos del atacante.
  * **Conclusión:** La aplicación combinada de estas tres capas erradica el riesgo de XSS de forma definitiva.
* **Columna Derecha (Gráfico de los 3 Pilares):**
  * *Diagrama visual que ilustra:* `Pilar 1: Codificación (< -> &lt;) | Pilar 2: Cookies HttpOnly | Pilar 3: Cabecera CSP`.

> ### 🎙️ NOTAS PARA EL ORADOR:
> *"Para protegernos aplicamos tres reglas: codificar siempre las salidas para neutralizar las etiquetas, blindar las cookies de sesión con HttpOnly para evitar el Session Hijacking, y activar Content Security Policy en el servidor. Con esto blindamos la aplicación. Muchas gracias por su atención."*
