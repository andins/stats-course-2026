# Prepara tu ordenador

**En pocas palabras:** para ejecutar los cuadernos (*notebooks*) y el código de las guías prácticas necesitas tres cosas: un lugar donde escribir y ejecutar código, Python con un puñado de bibliotecas de estadística y una forma de mantener esas bibliotecas separadas para cada proyecto. Esta página te lleva hasta ahí partiendo de un ordenador limpio, en Windows, macOS o Linux, en unos 30 minutos. Solo tienes que hacerlo una vez.

Usamos dos herramientas:

- **VS Code**, un editor gratuito que también puede ejecutar cuadernos.
- **uv**, una herramienta gratuita que instala Python por ti y guarda las bibliotecas de cada proyecto en su propio entorno aislado. No hace falta instalar Python por separado, y nada de lo que hagas aquí puede estropear otro proyecto ni tu sistema.

Si prefieres no instalar nada, consulta [Sin instalación: Google Colab](#sin-instalación-google-colab) al final. Para saber cómo organizar las carpetas de un análisis cuando ya lo tengas todo listo, consulta [Organiza tu proyecto](./project-structure.md). Para que un asistente de IA te ayude con el análisis, consulta [Trabaja con un agente de IA](./use-an-agent.md).

## Qué tendrás al terminar

- VS Code con las extensiones de Python y Jupyter.
- Una carpeta de proyecto con un entorno de Python 3.12 que incluye `numpy`, `pandas`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn` y `jupyterlab`: todo lo que usan los cuadernos y las guías prácticas del curso.
- Un archivo (`uv.lock`) que registra las versiones exactas instaladas, de modo que el mismo entorno pueda reconstruirse en cualquier ordenador.

## Paso 1: Instala VS Code

Descarga el instalador para tu sistema desde [code.visualstudio.com](https://code.visualstudio.com/) y ejecútalo. Si prefieres la línea de comandos:

**Windows** (en PowerShell):

```text
winget install --id Microsoft.VisualStudioCode -e
```

**macOS:** abre el archivo descargado y arrastra *Visual Studio Code* a la carpeta *Applications*. Si usas Homebrew: `brew install --cask visual-studio-code`.

**Linux:** en Debian o Ubuntu, descarga el archivo `.deb` desde la web e instálalo con `sudo apt install ./<file>.deb`. Muchas distribuciones también ofrecen `sudo snap install --classic code`. Para Fedora y otros sistemas, sigue las [instrucciones oficiales para Linux](https://code.visualstudio.com/docs/setup/linux).

Después abre VS Code, haz clic en el icono de **Extensions** de la barra izquierda (o pulsa `Ctrl+Shift+X`, `Cmd+Shift+X` en macOS) e instala dos extensiones, ambas publicadas por Microsoft: **Python** y **Jupyter**.

## Paso 2: Abre una terminal e instala uv

Una terminal es una ventana donde escribes comandos. Abre una:

- **Windows:** abre el menú Inicio, escribe *PowerShell* y ábrelo.
- **macOS:** pulsa `Cmd+Space`, escribe *Terminal* y pulsa Enter.
- **Linux:** pulsa `Ctrl+Alt+T` en la mayoría de los escritorios, o busca *Terminal*.

Después instala uv.

**Windows** (PowerShell):

```text
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Como alternativa: `winget install --id=astral-sh.uv -e`.

**macOS y Linux:**

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En una instalación de Linux muy mínima puede faltar `curl`; instálalo antes (`sudo apt install curl` en Debian o Ubuntu) o usa `wget -qO- https://astral.sh/uv/install.sh | sh`. En macOS con Homebrew, también sirve `brew install uv`.

**Cierra la terminal y abre una nueva**, y comprueba que ha funcionado:

```text
uv --version
```

Debería mostrar un número de versión. Si dice que no encuentra el comando, consulta [Solución de problemas](#solución-de-problemas).

## Paso 3: Crea un proyecto y su entorno

Estos comandos son los mismos en todos los sistemas. Crean una carpeta para tu primer análisis, le dicen a uv que use Python 3.12 e instalan las bibliotecas en un entorno que pertenece solo a esa carpeta.

```text
cd ~
mkdir projects
cd projects
mkdir my-first-analysis
cd my-first-analysis

uv init --bare
uv python pin 3.12
uv add numpy pandas scipy statsmodels scikit-learn matplotlib seaborn jupyterlab
```

La primera ejecución descarga Python y las bibliotecas, lo que tarda unos minutos. Después, la carpeta contiene:

| Archivo o carpeta | Qué es |
|---|---|
| `pyproject.toml` | La lista de bibliotecas que necesita tu proyecto. |
| `uv.lock` | Las versiones exactas instaladas. Consérvalo: hace que el entorno sea reproducible. |
| `.python-version` | La versión de Python que usa el proyecto. |
| `.venv/` | El propio entorno. No lo edites nunca a mano ni lo copies entre ordenadores; reconstrúyelo con `uv sync`. |

La misma lista de paquetes está también en [requirements.txt](./notebooks/requirements.txt). Si tienes ese archivo en la carpeta del proyecto, `uv add -r requirements.txt` hace lo mismo que el largo comando `uv add` de arriba.

Guarda tus proyectos en un lugar sencillo, como `projects` dentro de tu carpeta personal. Las carpetas sincronizadas con OneDrive, Dropbox o iCloud pueden ralentizarse o dar conflictos con los miles de archivos pequeños de un entorno. Para hacer copias de seguridad y compartir tu trabajo, usa [Git](./project-structure.md#control-de-versiones-con-git-opcional).

## Paso 4: Abre el proyecto en VS Code y ejecuta un cuaderno

1. En VS Code elige **File > Open Folder** y selecciona `my-first-analysis`.
2. Crea dentro una carpeta llamada `notebooks` (clic derecho en la lista de archivos, *New Folder*).
3. Descarga un cuaderno del curso, por ejemplo el [cuaderno sobre error de medición](./notebooks/measurement-error-attenuation.ipynb), y guárdalo en esa carpeta `notebooks`.
4. Abre el cuaderno en VS Code. Haz clic en **Select Kernel** arriba a la derecha, elige **Python Environments** y, después, la entrada que mencione `.venv` y Python 3.12.
5. Haz clic en **Run All**. Los gráficos y las tablas aparecen debajo de las celdas.

¿Prefieres el navegador? En la carpeta del proyecto ejecuta `uv run jupyter lab`; se abre JupyterLab con el mismo entorno.

## Paso 5: Comprueba que todo está instalado

En una celda nueva de un cuaderno (o en cualquier cuaderno), ejecuta:

```python
import sys
import numpy, pandas, scipy, statsmodels, sklearn, matplotlib, seaborn

print("Python", sys.version.split()[0])
for module in (numpy, pandas, scipy, statsmodels, sklearn, matplotlib, seaborn):
    print(f"{module.__name__:12s} {module.__version__}")
```

Deberías ver una versión de Python 3.12 y un número de versión para cada biblioteca, sin ningún error. El código del curso se probó con Python 3.12 y versiones recientes de las bibliotecas (por ejemplo pandas 3.1, scipy 1.18, statsmodels 0.15, scikit-learn 1.9).

Para ejecutar un script desde la terminal en lugar de un cuaderno, usa `uv run python my_script.py` dentro de la carpeta del proyecto; uv siempre usa el entorno propio del proyecto.

## Más adelante: añadir una biblioteca o reconstruir el entorno en otro ordenador

- **Añadir una biblioteca:** `uv add <package-name>`. Para los ejemplos bayesianos opcionales: `uv add pymc bambi arviz` (son grandes; instálalas solo si las necesitas).
- **Reconstruir el mismo entorno** en un ordenador nuevo o tras una instalación limpia: instala VS Code y uv (pasos 1 y 2), copia la carpeta del proyecto *sin* `.venv` y ejecuta `uv sync` dentro de ella.
- **Actualizar las bibliotecas:** `uv lock --upgrade` y después `uv sync`. Hazlo entre proyectos, no a mitad de un análisis, porque las versiones nuevas pueden cambiar ligeramente los resultados.

## Solución de problemas

| Problema | Qué hacer |
|---|---|
| `uv: command not found` (o «no se reconoce») justo después de instalar | Cierra la terminal y abre una nueva; el instalador modifica la ruta de búsqueda solo para las terminales nuevas. Si sigue fallando, reinicia el ordenador. |
| `invalid peer certificate: UnknownIssuer` u otro error de certificado durante la descarga | Es típico de las redes de empresas o universidades que inspeccionan el tráfico seguro. Indica a uv que use los certificados del sistema: `export UV_SYSTEM_CERTS=1` (macOS, Linux) o `$env:UV_SYSTEM_CERTS = "1"` (Windows PowerShell) y repite el comando. Las versiones antiguas de uv lo llaman `UV_NATIVE_TLS`. |
| Las descargas se agotan o fallan en una red que exige un proxy | Pide a tu equipo informático la dirección del proxy y asígnala a `HTTPS_PROXY`. |
| `ModuleNotFoundError: No module named 'pandas'` en un cuaderno | El cuaderno está usando el kernel equivocado. Haz clic en **Select Kernel** y elige el `.venv` de tu proyecto. |
| El kernel de `.venv` no aparece en VS Code | Pulsa `Ctrl+Shift+P` (`Cmd+Shift+P` en macOS), ejecuta **Python: Select Interpreter** y elige la entrada `.venv`. Si no aparece, comprueba que has abierto en VS Code la *carpeta del proyecto* (la que contiene `pyproject.toml`). |
| No puedes instalar software en tu ordenador | Pide a tu equipo informático que instale VS Code y uv, o usa Google Colab (más abajo). |
| Los gráficos no aparecen en un script ejecutado desde la terminal | Los cuadernos muestran los gráficos automáticamente; los scripts necesitan `plt.show()` al final, o `plt.savefig("figure.png")`. |

## Si no puedes o no quieres usar uv

La vía clásica también funciona: instala Python 3.12 o posterior, crea un entorno con el módulo `venv` incluido en Python e instala las bibliotecas con `pip`, usando el [requirements.txt](./notebooks/requirements.txt) del curso.

**Windows:** descarga Python desde [python.org](https://www.python.org/downloads/) y marca *Add python.exe to PATH* en el instalador. Después, en PowerShell dentro de la carpeta de tu proyecto:

```text
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell se niega a ejecutar el script de activación, ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e inténtalo de nuevo.

**macOS y Linux:** necesitas `python3` versión 3.12 o posterior. El que viene con macOS suele ser demasiado antiguo, así que instala uno actual desde [python.org](https://www.python.org/downloads/) o con Homebrew; en Debian o Ubuntu quizá necesites también `sudo apt install python3-venv`:

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En VS Code, selecciona el intérprete de `.venv` como se describe en el paso 4. Pierdes el archivo de bloqueo (*lockfile*), así que anota lo que has instalado con `pip freeze > requirements-frozen.txt` cuando tu análisis ya funcione.

## Sin instalación: Google Colab

[Google Colab](https://colab.research.google.com/) ejecuta cuadernos en tu navegador con `numpy`, `pandas`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib` y `seaborn` ya disponibles. Abre Colab, elige **File > Upload notebook** y selecciona un cuaderno del curso. Es una buena forma de probar cosas, pero tus archivos desaparecen al terminar la sesión a menos que los guardes en Google Drive, y **no debes subir datos confidenciales ni de pacientes** sin comprobar antes la normativa de tu institución.

---
**Siguiente:** [Organiza tu proyecto](./project-structure.md) · [Inicio](./README.md) · [Glosario](./glossary.md)
