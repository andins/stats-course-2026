# Trabaja con un agente de IA

**En pocas palabras:** un agente de IA es un asistente de chat que además puede leer los archivos de tu proyecto, escribir código y cuadernos (*notebooks*) y ejecutar comandos. El **skill statistics-advisor** es una carpeta de instrucciones que hace que un agente se comporte como un asesor estadístico cuidadoso que sigue este curso: pregunta qué tipo de análisis estás haciendo antes de elegir una prueba, comprueba los supuestos, informa de los tamaños del efecto con sus intervalos y cita fuentes. Esta página te enseña a poner en marcha ambas cosas, con la ruta más sencilla para cada proveedor habitual.

No necesitas un agente para seguir este curso. Las [guías prácticas](./README.md#aplica-lo-que-aprendes) funcionan por sí solas. Un agente ayuda sobre todo cuando quieres código adaptado a tus propios datos, una segunda opinión sobre tu plan o una explicación de un resultado.

## Antes de empezar: cuatro precauciones

1. **Los agentes se equivocan, a veces con mucha seguridad.** Trata la respuesta como el borrador de un asistente rápido. Contrasta el razonamiento con las páginas del curso, ejecuta tú el código y mira los gráficos. El skill le indica al agente que no invente números de página, pero aun así comprueba cualquier referencia que te dé.
2. **Privacidad.** Todo lo que lee el agente suele enviarse a los servidores del proveedor. No le des a un agente en la nube datos de pacientes, datos sujetos a un acuerdo de confidencialidad ni resultados sin publicar sin comprobar antes la normativa de tu institución. Opciones más seguras: describir las columnas y mostrar unas pocas filas de ejemplo inventadas, usar un subconjunto anonimizado, o preguntar a tu institución qué herramientas aprobadas ofrece.
3. **Mantén el control.** Un agente que ejecuta comandos puede cambiar o borrar archivos. Trabaja dentro de tu [carpeta de proyecto](./project-structure.md), haz un *commit* en Git antes de una sesión larga, deja la configuración de aprobación en **preguntar primero** para ver cada comando, y no le permitas nunca tocar `data/raw`.
4. **Sigue aprendiendo.** Pregunta *por qué*, no solo *qué*. Un buen hábito es pedirle al agente que te indique la página del curso que explica cada decisión que toma.

## Paso 1: elige una herramienta

Los planes, las cuotas gratuitas y los nombres de los modelos cambian a menudo, así que consulta la página de cada proveedor para conocer las condiciones actuales.

| Si... | Usa | Necesitas |
|---|---|---|
| ya seguiste [Prepara tu ordenador](./setup-environment.md) y quieres el comienzo más sencillo | **El chat de VS Code con GitHub Copilot** | Una cuenta de GitHub. Al iniciar sesión se activa un plan gratuito con una cuota mensual limitada. El alumnado y el profesorado pueden solicitar acceso gratuito a través de [GitHub Education](https://github.com/education). |
| tienes una suscripción a Claude | **Claude Code**, como extensión de VS Code o en una terminal | Un plan de pago de Claude o una cuenta de Claude Console |
| tienes una suscripción a ChatGPT | **Codex**, como extensión de VS Code, en una terminal o en la aplicación de escritorio de ChatGPT | Una cuenta de ChatGPT |
| tienes una cuenta de Google y te manejas con una terminal | **Gemini CLI** | Una cuenta de Google |
| ya usas Cursor | **Cursor** | Una cuenta de Cursor |
| solo puedes usar un navegador web | **Un chat web**: Claude, ChatGPT, Gemini o Copilot | Una cuenta. La aplicación web de Claude acepta el skill como archivo subido; para los demás usa la [alternativa de un único archivo](#chat-web-sin-un-skill-instalado). |

Si no tienes preferencia, empieza con **VS Code y GitHub Copilot**. Todo lo que instalaste para el curso ya está en su sitio.

## Paso 2: instala el skill

Un *skill* es una carpeta con un archivo llamado `SKILL.md` y archivos de apoyo. Al principio los agentes solo leen su breve descripción, y cargan las instrucciones completas cuando tu pregunta encaja. El formato es un estándar abierto, así que la misma carpeta funciona en todas las herramientas siguientes. Solo tiene que estar en el lugar donde mira cada herramienta.

El skill está en la carpeta `statistics-advisor` del repositorio del curso, junto al propio curso. Instala **solo esa carpeta**, no todo el repositorio: un repositorio copiado dentro de una carpeta de skills no tiene `SKILL.md` en su nivel superior, así que no se cargará ningún skill. El instalador de abajo se ocupa de esto.

### 2a. Consigue el repositorio

Si tienes Git (véase [Organiza tu proyecto](./project-structure.md#control-de-versiones-con-git-opcional)), abre una terminal en la carpeta donde guardas tus proyectos y ejecuta (sustituye la dirección por la que te hayan dado):

```text
git clone <REPOSITORY ADDRESS>
cd stats-course-2026
```

¿No tienes Git? En la página web del repositorio elige **Code > Download ZIP**, descomprímelo y abre una terminal en la carpeta descomprimida. Puede que la carpeta se llame `stats-course-2026-main`; el nombre no importa.

### 2b. Ejecuta el instalador

El instalador copia el skill en la carpeta adecuada para tu herramienta. Solo necesita Python, que ya configuraste en [Prepara tu ordenador](./setup-environment.md). Elige la línea de tu herramienta:

| Tu herramienta | Comando |
|---|---|
| Chat de VS Code (GitHub Copilot) | `python3 tools/install_skill.py --tool copilot` |
| Claude Code, Claude en VS Code | `python3 tools/install_skill.py --tool claude` |
| Codex (VS Code, terminal o aplicación) | `python3 tools/install_skill.py --tool agents` |
| Gemini CLI | `python3 tools/install_skill.py --tool gemini` |
| Cursor | `python3 tools/install_skill.py --tool cursor` |

En Windows escribe `py tools\install_skill.py --tool copilot` en su lugar. Si no se encuentra ni `python3` ni `py`, ejecútalo con uv: `uv run --no-project python tools/install_skill.py --tool copilot`. Añade `--dry-run` para ver dónde se instalaría el skill sin copiar nada.

Por defecto el skill se instala para **todos tus proyectos**. Para instalarlo **solo en un proyecto**, añade su carpeta, por ejemplo `--project ~/projects/my-first-analysis`; así se guarda con ese proyecto y puede incluirse en sus *commits*.

**Para actualizar** el skill más adelante, ejecuta `git pull` en el repositorio (o vuelve a descargar el ZIP) y ejecuta el mismo comando del instalador: reemplaza la copia anterior.

### 2c. O cópialo a mano

El instalador solo copia una carpeta. Puedes hacer lo mismo tú. La carpeta del skill es `statistics-advisor` dentro del repositorio, y tiene que acabar en la carpeta de skills de tu herramienta, conservando el nombre `statistics-advisor`:

| Herramienta | Carpeta para todos tus proyectos | O, solo para un proyecto |
|---|---|---|
| Chat de VS Code (Copilot) | `~/.copilot/skills/` | `.github/skills/` |
| Claude Code, Claude en VS Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex, en VS Code, terminal o aplicación | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` o `~/.agents/skills/` | `.gemini/skills/` o `.agents/skills/` |
| Cursor | `~/.cursor/skills/` o `~/.agents/skills/` | `.cursor/skills/` o `.agents/skills/` |

`~` es tu carpeta personal (`C:\Users\<tú>` en Windows). Las rutas que empiezan por `.` en la última columna son relativas a la carpeta de tu proyecto.

**macOS y Linux**, desde la carpeta del repositorio (sustituye `.copilot` por `.claude` o `.agents` según la tabla):

```text
mkdir -p ~/.copilot/skills
cp -r statistics-advisor ~/.copilot/skills/
```

**Windows** (PowerShell, desde la carpeta del repositorio):

```text
New-Item -ItemType Directory -Force "$HOME\.copilot\skills" | Out-Null
Copy-Item -Recurse statistics-advisor "$HOME\.copilot\skills\"
```

Para actualizar a mano, borra primero la copia anterior (`rm -r ~/.copilot/skills/statistics-advisor`, o `Remove-Item -Recurse -Force "$HOME\.copilot\skills\statistics-advisor"` en Windows) y copia la nueva.

Los skills pueden contener scripts que un agente puede ejecutar, así que instala solo skills de fuentes en las que confíes.

## Paso 3: inicia el agente y comprueba que ve el skill

Abre un chat **nuevo** después de instalarlo (los agentes leen la lista de skills al iniciar una sesión), con la carpeta de tu proyecto abierta. Después, o bien pregunta,

> ¿Qué skills tienes disponibles? ¿Está statistics-advisor entre ellos?

o búscalo en la lista de skills de la herramienta:

| Herramienta | Busca el skill con | Invócalo explícitamente con |
|---|---|---|
| Chat de VS Code | escribe `/` en el cuadro del chat | `/statistics-advisor` |
| Claude Code | escribe `/` | `/statistics-advisor` |
| Codex | escribe `$`, o `/skills` | `$statistics-advisor` |
| Gemini CLI | `/skills list` | menciónalo: «usa el skill statistics-advisor» |
| Cursor | escribe `/` en el chat de Agent | `/statistics-advisor` |

El skill también se activa **solo** cuando tu pregunta trata de estadística, así que invocarlo explícitamente solo es necesario cuando no se activa. Gemini CLI te pide confirmación la primera vez que activa un skill.

## Notas por herramienta

### VS Code con GitHub Copilot

1. Pasa el cursor sobre el icono de Copilot en la barra de estado, elige **Use AI Features** e inicia sesión con GitHub.
2. Abre la carpeta de tu proyecto (**File > Open Folder**). Si VS Code te pregunta si confías en ella, elige **Trust**.
3. Abre la vista de Chat con `Ctrl+Alt+I` (`Cmd+Ctrl+I` en macOS). Haz clic en `+` para un chat nuevo.
4. Elige **Copilot** como destino de la sesión y **Agent** como modo, y mantén los permisos en **Manual** para aprobar cada comando o uso de herramienta.
5. Instala el skill en `~/.copilot/skills/` (Paso 2), inicia un chat nuevo y haz tu pregunta.

Si usas en su lugar el destino de sesión **Local**, VS Code también lee `~/.claude/skills/` y `~/.agents/skills/`, y al escribir `/skills` se abre el menú de skills.

### Claude Code

Instala la extensión **Claude Code** desde la vista de Extensiones de VS Code (`Ctrl+Shift+X`, `Cmd+Shift+X` en macOS), ábrela con el icono de la chispa (*Spark*) o con el elemento **✻ Claude Code** de la barra de estado, e inicia sesión. Para usarlo en una terminal, abre una en la carpeta de tu proyecto e instálalo:

```text
# macOS, Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Abre una terminal nueva, ejecuta `claude` en la carpeta de tu proyecto y sigue las indicaciones para iniciar sesión. El skill va en `~/.claude/skills/`. Si algo falla, consulta la [guía de instalación](https://code.claude.com/docs/en/setup) de Anthropic.

### Codex (OpenAI)

Instala la extensión OpenAI Codex desde la vista de Extensiones de VS Code, o sigue la [documentación de Codex](https://developers.openai.com/codex) para usarlo en una terminal o en la aplicación de escritorio de ChatGPT. Inicia sesión con tu cuenta de ChatGPT. El skill va en `~/.agents/skills/`. Si no aparece, reinicia Codex.

### Gemini CLI

Sigue la [documentación de Gemini CLI](https://geminicli.com/docs/) para instalarlo e iniciar sesión con tu cuenta de Google, y después ejecuta `gemini` en la carpeta de tu proyecto. Pon el skill en `~/.gemini/skills/` (o `~/.agents/skills/`), y luego ejecuta `/skills list` para confirmarlo y `/skills reload` tras añadirlo.

### Cursor

Pon el skill en `~/.cursor/skills/` (o `~/.agents/skills/`) y escribe `/` en el chat de Agent para encontrarlo. Cursor también carga skills de las carpetas de Claude y de Codex.

## Chat web sin un skill instalado

Un chat web no puede leer una carpeta de tu ordenador, pero hay dos formas sencillas de darle las mismas instrucciones. Genera ambos archivos con un solo comando desde la carpeta del repositorio (solo necesita Python, que configuraste antes):

```text
python3 tools/package_skill.py
```

En Windows usa `py tools\package_skill.py`. Si no se encuentra el comando `python3` ni `py`, ejecútalo con uv: `uv run --no-project python tools/package_skill.py`. Crea una carpeta `dist/` con dos archivos.

**La aplicación web de Claude (claude.ai):** sube `dist/statistics-advisor.zip` en **Customize > Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills)). Después funciona como las demás herramientas: se activa solo ante preguntas de estadística. En los planes Enterprise, un administrador debe habilitar antes los skills.

**ChatGPT, Gemini, el chat de Copilot o cualquier otro chat:** adjunta `dist/statistics-advisor-single-file.md` a una conversación nueva (o añádelo a un Proyecto, a un Gem o a un asistente personalizado si tu herramienta los tiene) y empieza con:

> Sigue las instrucciones adjuntas de statistics-advisor durante toda esta conversación. Empieza haciéndome las preguntas de triaje que describe.

Este único archivo contiene las instrucciones del skill y sus cuatro documentos de referencia. Hay dos limitaciones. El chat no puede ejecutar tus archivos ni los scripts auxiliares, así que escribirá código para que lo pegues y lo ejecutes tú en un cuaderno. Y solo puede trabajar con lo que le cuentes, así que describe tus columnas, unidades y diseño del estudio en lugar de subir datos confidenciales.

## Cómo sacarle partido al skill

### Cuéntale lo que necesita saber

La primera tarea del skill es preguntar si tus datos ya están recogidos, si la pregunta se decidió antes de ver los datos y si quieres predicción o una respuesta causal. Obtendrás una primera respuesta mejor si lo indicas desde el principio:

- **La pregunta** con palabras sencillas, y qué piensas decidir con la respuesta.
- **El diseño del estudio:** cómo se recogieron los datos, si la exposición se asignó al azar, cuántas unidades hay, si hay mediciones repetidas o grupos.
- **Los datos:** el nombre del archivo, las columnas que importan y sus unidades, cuánto falta.
- **Lo que quieres recibir:** una explicación, una recomendación o un cuaderno en tu carpeta `notebooks/`.

### Ejemplos de mensajes

- *Planificar:* «Estoy planificando un estudio de una variante del gen LDLR y el colesterol LDL, con 15 familias y 20 familiares por familia. ¿Cuántas familias necesito? Usa el skill statistics-advisor.»
- *Explorar:* «Tengo `data/raw/ldl_2024.csv`. Todavía no tengo una hipótesis concreta. Ayúdame a explorarlo. Crea un cuaderno en `notebooks/` y no modifiques el archivo original.»
- *Elegir una prueba:* «Antes de recoger los datos decidí comparar la presión arterial antes y después del tratamiento en 40 pacientes. ¿Qué análisis corresponde y qué supuestos tengo que comprobar?»
- *Causal:* «Quiero saber si portar una variante genética afecta al colesterol LDL, pero nadie asignó los genotipos y los portadores difieren en ascendencia y en quién se hizo la prueba. Explícame paso a paso por qué tengo que ajustar.»
- *Revisar mi trabajo:* «Aquí tienes mi plan de análisis y mis resultados. ¿Qué se me ha pasado? Revisa los supuestos, las comparaciones múltiples y los datos faltantes.»
- *Entender:* «Explica qué significa un intervalo de confianza para la pendiente de una regresión e indícame la página del curso correspondiente.»

### Cómo es una buena respuesta

El skill funciona si el agente:

- **pregunta** de qué tipo de análisis se trata antes de recomendar una prueba, cuando no está claro;
- empieza con una **respuesta breve en lenguaje sencillo** y luego da los detalles;
- **enumera los supuestos** e indica cómo comprobar cada uno;
- informa de una **estimación con su intervalo de confianza**, no solo de «significativo»;
- avisa de los **valores p exploratorios, las comparaciones múltiples y los datos faltantes** cuando corresponde;
- **cita fuentes** y dice cuándo no está seguro;
- ofrece crear un **cuaderno** e indica las **páginas del curso** correspondientes (módulo y título; búscalas en el buscador de la barra lateral del curso), para que puedas seguir el razonamiento.

Si salta directamente a un valor p, dile: «Usa el skill statistics-advisor y empieza por las preguntas de triaje».

### Dale al agente las normas de la casa de tu proyecto

La mayoría de los agentes leen un breve archivo de instrucciones de la carpeta del proyecto (`AGENTS.md` para VS Code, Codex y otros; `CLAUDE.md` para Claude Code; `GEMINI.md` para Gemini CLI). Unas pocas líneas evitan los problemas más comunes. Guarda esto como `AGENTS.md` (y una copia llamada `CLAUDE.md` si usas Claude Code) y adáptalo a tu proyecto:

```text
# Project instructions

- Run all Python with `uv run`. Add libraries with `uv add <name>`; never install packages globally.
- data/raw/ is read-only: never edit, move or delete files there. Write cleaned data to data/processed/.
- Notebooks go in notebooks/ (numbered 01_, 02_, ...), figures in results/figures/, tables in results/tables/.
- Use relative paths and set random seeds.
- Report effect sizes with confidence intervals, state assumptions and how they were checked,
  and say how many rows were dropped for missing data.
- Ask me before assuming anything about the study design.
- Ask before running any command that deletes files or changes Git history.
```

Si tu herramienta no lee un archivo así, pega las mismas líneas al principio del chat.

### Revisa lo que produce el agente

- **Lee el código** antes de fiarte de él y ejecuta los cuadernos desde el principio (**Restart**, luego **Run All**).
- **Asegúrate de que usa el entorno de tu proyecto:** `uv run`, o el kernel `.venv` en VS Code. Si ves `ModuleNotFoundError`, esa suele ser la causa.
- **Compáralo con el curso:** la guía práctica correspondiente muestra la receta estándar. Si el agente hace algo distinto, pregúntale por qué.
- **Mira tú mismo los datos.** Los gráficos detectan problemas que ningún resumen detecta (véase [Cómo: explorar un conjunto de datos](./02-exploring-data/how-to/explore-a-dataset.md)).
- **Guarda el registro:** haz un *commit* en Git después de cada paso que funcione, y anota en `docs/` las decisiones que tomáis tú y el agente.

## Solución de problemas

| Problema | Qué probar |
|---|---|
| El skill no aparece en la lista | Comprueba que la carpeta se llama exactamente `statistics-advisor` y que `SKILL.md` está directamente dentro. El error habitual es copiar todo el repositorio (o una segunda carpeta `statistics-advisor` dentro de la primera) en lugar de la carpeta `statistics-advisor` que hay dentro; el instalador (`tools/install_skill.py`) lo evita. Después abre un chat nuevo; en Gemini CLI ejecuta `/skills reload`; en Codex, reinícialo. |
| El skill aparece en la lista pero el agente lo ignora | Invócalo explícitamente (`/statistics-advisor`, o `$statistics-advisor` en Codex), o empieza tu mensaje con «Usa el skill statistics-advisor». |
| Dice que no puede leer ni ejecutar archivos | Probablemente estés en un chat web, o los permisos de archivos y comandos de la herramienta están desactivados. Usa la vía del archivo único y ejecuta tú el código, o abre la carpeta de tu proyecto en VS Code. |
| El instalador dice que no encuentra `SKILL.md` | Ejecútalo desde dentro del repositorio descargado: la carpeta `tools` y la carpeta `statistics-advisor` deben estar una junto a otra. Si moviste `install_skill.py` a otro sitio, devuélvelo a su lugar. |
| `ModuleNotFoundError` cuando el agente ejecuta código | Pídele que use `uv run`, o selecciona el kernel `.venv` del proyecto. No le dejes instalar paquetes de forma global. |
| El agente pide ejecutar un comando que no entiendes | Di que no y pídele que lo explique. Siempre puedes aprobar los comandos de uno en uno. |
| Una referencia o un número de página parece inventado | Contrástalo con `references/core-references.md` en la carpeta del skill, o con la fuente original. Pídele al agente que diga de qué no está seguro. |
| Llegas al límite de uso del proveedor | Espera a que se renueve la cuota, cambia de herramienta (la misma carpeta del skill funciona en varias) o usa las guías prácticas, que no necesitan agente. |
| Errores de descarga o de inicio de sesión en una red universitaria o de empresa | Suelen deberse a la configuración de certificados o del proxy. Consulta la documentación de red del proveedor o pregunta a tu equipo de TI. |

---
**Anterior:** [Organiza tu proyecto](./project-structure.md) · [Inicio](./README.md) · [Glosario](./glossary.md)
