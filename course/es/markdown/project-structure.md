# Organiza tu proyecto

**En pocas palabras:** un análisis estadístico es un pequeño proyecto de software. Dale una carpeta propia, mantén intactos los datos originales, guarda el código, los resultados y las notas en lugares distintos y deja escrito cómo volver a ejecutarlo. Dentro de seis meses (o cuando una persona revisora te pida un cambio), tú o un colega deberíais poder reproducir cada número y cada figura ejecutando el código desde el principio.

Esta página da por hecho que ya has [preparado tu ordenador](./setup-environment.md).

## La estructura de carpetas

Una carpeta por proyecto, con una estructura como esta:

```text
my-first-analysis/
├── README.md             what the project is and how to rerun it
├── AGENTS.md             optional house rules for an AI agent (see "Work with an AI agent")
├── pyproject.toml        the libraries the project needs (made by uv)
├── uv.lock               the exact versions installed (made by uv; keep it)
├── .gitignore            files Git should not track
├── data/
│   ├── raw/              original data exactly as received: never edited
│   └── processed/        cleaned data produced by your code
├── notebooks/            01_explore.ipynb, 02_model.ipynb, ...
├── src/                  reusable code (functions) and scripts
├── results/
│   ├── figures/          plots produced by your code
│   └── tables/           tables produced by your code
└── docs/
    ├── analysis-plan.md  what you planned to do, written before looking at the data
    └── data-dictionary.md  what each column means, its units, and its allowed values
```

Para crear las carpetas, guarda esto como `make_folders.py` en la carpeta de tu proyecto y ejecuta `uv run python make_folders.py` (o pégalo en una celda de un cuaderno abierto en esa carpeta):

```python
from pathlib import Path

for folder in ["data/raw", "data/processed", "notebooks", "src", "results/figures", "results/tables", "docs"]:
    Path(folder).mkdir(parents=True, exist_ok=True)
```

No necesitas todas ellas para un análisis pequeño. Un proyecto con solo `data/raw`, `notebooks` y `results` ya es mucho mejor que una carpeta llena de `final_v3_REALLY_final.xlsx`.

## Las reglas que más importan

1. **No edites nunca los datos originales.** Guarda el archivo exactamente como llegó del instrumento, de la persona colaboradora o de la base de datos, en `data/raw`. Haz toda la limpieza con código que lea el archivo original y escriba un archivo nuevo en `data/processed`. Así cada cambio que hiciste es visible y repetible, y puedes corregir un error cambiando una línea en lugar de rehacerlo a mano en una hoja de cálculo.
2. **Todo se produce con código.** Cada figura y cada tabla de un informe debe salir de un cuaderno o de un script, no de copiar y pegar. Si cambias los datos o una decisión, vuelve a ejecutar y todo se actualiza.
3. **Una pregunta, un cuaderno, en orden.** Numera los cuadernos (`01_explore.ipynb`, `02_clean.ipynb`, `03_model.ipynb`) para que el orden del análisis sea evidente. Cada cuaderno debe hacer una sola tarea y leer su entrada del resultado del paso anterior.
4. **Los cuadernos exploran; los scripts repiten.** Un cuaderno es el lugar adecuado para mirar gráficos y probar ideas. Cuando varios cuadernos usan un mismo código, o este tarda mucho, pásalo a una función en `src/` e impórtala.
5. **Anota las decisiones.** Registra qué filas excluiste y por qué, cómo trataste los valores faltantes y qué análisis ejecutaste. El número de filas descartadas es algo que te pedirá quien lea tu trabajo. Consulta [Datos faltantes](./02-exploring-data/missing-data.md).
6. **Escribe el plan de análisis antes de mirar.** Para un análisis confirmatorio, anota en `docs/analysis-plan.md` la comparación que vas a contrastar, la variable de respuesta, el modelo y las reglas de exclusión *antes* de explorar los datos. Después, todo lo que añadas tras mirar es exploratorio y debe etiquetarse como tal. Consulta [Exploratorio vs. confirmatorio](./02-exploring-data/exploratory-vs-confirmatory.md).

## Buenos hábitos con los cuadernos

- **Pon los ajustes al principio**: rutas de archivos, la semilla aleatoria, umbrales, nombres de columnas. Así cualquiera puede verlos y cambiarlos en un solo lugar.
- **Fija una semilla aleatoria** siempre que haya aleatoriedad (`rng = np.random.default_rng(0)`, `random_state=0`), para que al volver a ejecutar salgan los mismos números.
- **Ejecútalo desde el principio antes de fiarte.** Usa **Restart** y después **Run All**. Un cuaderno que solo funciona si sus celdas se ejecutan en un orden concreto es un error esperando a ocurrir.
- **Mantén las rutas de archivos relativas al proyecto**, no a tu ordenador (`C:\Users\you\...` deja de funcionar para cualquier otra persona). Este fragmento encuentra la carpeta del proyecto tanto si el cuaderno está en `notebooks/` como en la raíz del proyecto:

```python
from pathlib import Path

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "results" / "figures"

print("Project folder:", ROOT)
# df = pd.read_csv(RAW / "ldl_2024.csv")
# fig.savefig(FIGURES / "ldl_by_genotype.png", dpi=200, bbox_inches="tight")
```

- **Guarda los resultados desde el código**, con nombres descriptivos (`ldl_by_genotype.png`, no `Figure 3.png`).
- **Usa nombres de archivo sencillos:** en minúsculas, sin espacios, con las fechas como `2024-06-15` para que se ordenen correctamente.

## Un README que merece la pena escribir

Un `README.md` breve en la raíz del proyecto responde a las primeras preguntas de quien lo abra:

```text
# LDLR variant study 2024

Is a variant in the LDLR gene linked to LDL cholesterol? Lipid-clinic cohort, 15 families x 20 relatives.

## How to rerun
1. Install uv (see the course page "Set up your computer").
2. In this folder run:  uv sync
3. Open the notebooks in notebooks/ in order (01, 02, ...) and run each one.

## Data
data/raw/ldl_2024.csv  from the clinic team, received 2024-09-12, not modified.
Columns are described in docs/data-dictionary.md.

## Contact
Your name, your email.
```

## Control de versiones con Git (opcional)

Esta sección es opcional: hazla solo si quieres dedicar un poco más de tiempo a aprender Git.

Git registra cada versión de tus archivos, de modo que puedes ver qué ha cambiado, deshacer un error y trabajar con otras personas. También es una buena copia de seguridad para archivos de texto y cuadernos. Instálalo una sola vez:

- **Windows:** `winget install --id Git.Git -e` (o descárgalo desde [git-scm.com](https://git-scm.com/)).
- **macOS:** ejecuta `git --version` en una terminal; si falta Git, macOS te ofrece instalarlo.
- **Linux:** `sudo apt install git` (Debian, Ubuntu) o `sudo dnf install git` (Fedora).

Dile a Git quién eres (una vez por ordenador) y empieza a seguir el proyecto:

```text
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git init
git add .
git commit -m "Start the project"
```

A partir de ahí, `git add .` y `git commit -m "short description of what changed"` guardan una nueva instantánea. Haz un *commit* cuando algo funcione, con un mensaje que diga qué y por qué.

Crea un archivo `.gitignore` en la carpeta del proyecto para que Git omita lo que no debe seguirse:

```text
# the environment is rebuilt with `uv sync`; never commit it
.venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store

# raw data: keep out of Git if it is large or confidential, and back it up elsewhere
# (remove this line if the data is small, public, and you want it versioned too)
data/raw/

# generated by the code, can be recreated
data/processed/
results/
```

Algunas precauciones:

- **No pongas nunca datos confidenciales en Git**, en particular datos de pacientes o cualquier cosa sujeta a un acuerdo de intercambio de datos, y tampoco contraseñas ni claves. Un archivo eliminado en un *commit* posterior sigue estando en el historial. Guarda los datos originales sensibles en un lugar seguro aprobado por tu institución y describe en el README dónde están.
- **Sí debes subir** `pyproject.toml` y `uv.lock`, para que el entorno pueda reconstruirse.
- **Los resultados de los cuadernos pueden contener datos** (tablas impresas, gráficos de registros individuales). Antes de compartir un cuaderno, borra sus resultados (VS Code: **Clear All Outputs** en la barra de herramientas del cuaderno), salvo que quieras compartirlos.
- Para guardar una copia en la nube y compartirla con colegas, crea un repositorio vacío en un servicio como GitHub o GitLab (tu institución puede tener el suyo propio) y sigue las instrucciones que te muestre para conectarlo.

## Reconstruye el proyecto en otro ordenador

Como el proyecto registra su entorno, ponerlo en marcha en otro sitio lleva unos pocos pasos: instala [VS Code y uv](./setup-environment.md), consigue la carpeta del proyecto (`git clone <address>`, o cópiala sin `.venv`), coloca los datos originales en `data/raw` y ejecuta `uv sync` en la carpeta. Después abre los cuadernos y ejecuta Run All.

## Algunas cosas que conviene evitar

- **Analizar en una hoja de cálculo y en código a la vez.** Elige un único lugar donde viva el análisis; usa la hoja de cálculo solo para mirar o introducir datos.
- **Varias copias de los datos con nombres distintos.** Si un archivo cambia, debe ir en `data/processed` junto con el código que lo generó.
- **Un cuaderno gigante que lo hace todo.** Divídelo cuando deje de caber en unas pocas pantallas.
- **Entornos compartidos entre proyectos.** Un entorno separado por proyecto significa que actualizar una biblioteca para un análisis nunca puede cambiar los resultados de otro.

---
**Anterior:** [Prepara tu ordenador](./setup-environment.md) · **Siguiente:** [Trabaja con un agente de IA →](./use-an-agent.md) · [Inicio](./README.md) · [Glosario](./glossary.md)
