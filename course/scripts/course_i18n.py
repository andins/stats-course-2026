"""Per-language settings for building the course: UI strings, page titles and the markers the builder looks for.

English is the reference language and lives in course/en/markdown/. Every other language lives in
course/<lang>/markdown/ with the same file names, and is built into course/<lang>/ (index.html and pages/).
To add a language, add an entry to UI and TITLES below (including a flag_svg), then translate the markdown
and run `COURSE_LANG=<lang> python3 build_explainers_html.py`.
"""

DEFAULT_LANG = "en"

# Small decorative flags shown next to the language name in the language switch (inline SVG, so they
# render on every platform, unlike emoji flags).
FLAG_ES = (
    '<svg viewBox="0 0 3 2" aria-hidden="true" focusable="false"><rect width="3" height="2" fill="#c60b1e"/>'
    '<rect y=".5" width="3" height="1" fill="#ffc400"/></svg>'
)
FLAG_EN = (
    '<svg viewBox="0 0 60 40" aria-hidden="true" focusable="false"><rect width="60" height="40" fill="#012169"/>'
    '<path d="M0 0L60 40M60 0L0 40" stroke="#fff" stroke-width="8"/>'
    '<path d="M0 0L60 40M60 0L0 40" stroke="#c8102e" stroke-width="3"/>'
    '<path d="M30 0V40M0 20H60" stroke="#fff" stroke-width="12"/>'
    '<path d="M30 0V40M0 20H60" stroke="#c8102e" stroke-width="7"/></svg>'
)

UI = {
    "en": {
        "html_lang": "en",
        "site_title": "Statistics Explainers",
        "search_placeholder": "Search topics...",
        "search_label": "Search topics",
        "expand_all": "Expand all",
        "expand_all_title": "Expand all navigation groups",
        "collapse_all": "Collapse all",
        "collapse_all_title": "Collapse all navigation groups",
        "theme_title": "Toggle dark/light theme",
        "toggle_navigation": "Toggle navigation",
        "toggle_group": "Toggle {title} topics",
        "back_to_top": "Back to top",
        "learn_more": "Learn more",
        "learn_more_aria": "Further reading",
        "do_it_yourself": "Do it yourself",
        "do_it_yourself_aria": "Hands-on guide",
        "previous": "Previous",
        "next": "Next",
        "next_module": "Next module",
        "previous_module": "Previous module",
        "language_name": "English",
        "course_title": "Statistics Course for Life Scientists",
        "flag_svg": FLAG_EN,
        "legend_decision": "A question to answer",
        "legend_process": "Something to do",
        "legend_terminal": "Where you end up",
        "legend_hint": "Click any box to open its page.",
        "edge_default": "Next",
    },
    "es": {
        "html_lang": "es",
        "site_title": "Explicaciones de estadística",
        "search_placeholder": "Buscar temas...",
        "search_label": "Buscar temas",
        "expand_all": "Expandir todo",
        "expand_all_title": "Expandir todos los grupos de navegación",
        "collapse_all": "Contraer todo",
        "collapse_all_title": "Contraer todos los grupos de navegación",
        "theme_title": "Cambiar entre tema oscuro y claro",
        "toggle_navigation": "Mostrar u ocultar la navegación",
        "toggle_group": "Mostrar u ocultar los temas de {title}",
        "back_to_top": "Volver arriba",
        "learn_more": "Para saber más",
        "learn_more_aria": "Lecturas recomendadas",
        "do_it_yourself": "Hazlo tú mismo",
        "do_it_yourself_aria": "Guía práctica",
        "previous": "Anterior",
        "next": "Siguiente",
        "next_module": "Módulo siguiente",
        "previous_module": "Módulo anterior",
        "language_name": "Español",
        "course_title": "Curso de estadística para científicos de la vida",
        "flag_svg": FLAG_ES,
        "legend_decision": "Una pregunta que responder",
        "legend_process": "Algo que hacer",
        "legend_terminal": "Dónde terminas",
        "legend_hint": "Haz clic en cualquier caja para abrir su página.",
        "edge_default": "Siguiente",
    },
}

# Navigation titles by page id (see STRUCTURE in build_explainers_html.py). English titles live in STRUCTURE itself.
TITLES = {
    "en": {},
    "es": {
        "home": "Inicio",
        "setup-environment": "Prepara tu ordenador",
        "project-structure": "Organiza tu proyecto",
        "use-an-agent": "Trabaja con un agente de IA",
        "workflow": "Guía rápida del flujo de trabajo",
        "glossary": "Glosario",
        "m1": "1. Planificar tu estudio",
        "m1-sample-size-and-power": "Tamaño muestral y potencia",
        "m1-effect-size": "Tamaño del efecto",
        "m1-design-considerations": "Consideraciones de diseño",
        "m1-howto-plan-a-sample-size": "Cómo: planificar un tamaño muestral",
        "m2": "2. Explorar tus datos",
        "m2-exploratory-vs-confirmatory": "Exploratorio vs. confirmatorio",
        "m2-eda-basics": "Fundamentos del EDA",
        "m2-missing-data": "Datos faltantes",
        "m2-howto-explore-a-dataset": "Cómo: explorar un conjunto de datos",
        "m3": "3. Contraste de hipótesis",
        "m3-p-values-and-significance": "Valores p y significación",
        "m3-common-tests": "Pruebas habituales",
        "m3-checking-assumptions": "Comprobar los supuestos",
        "m3-multiple-comparisons": "Comparaciones múltiples",
        "m3-howto-run-a-common-test": "Cómo: ejecutar una prueba habitual",
        "m3-howto-check-test-assumptions": "Cómo: comprobar los supuestos de una prueba",
        "m4": "4. Fundamentos de regresión",
        "m4-what-is-regression": "Qué es la regresión",
        "m4-tests-as-regressions": "Pruebas como regresiones",
        "m4-generalized-linear-models": "Modelos lineales generalizados",
        "m4-howto-run-a-test-as-a-regression": "Cómo: ejecutar una prueba como regresión",
        "m5": "5. Predicción vs. causalidad",
        "m5-prediction-vs-explanation": "Predicción vs. explicación",
        "m5-experiments-vs-observational-data": "Experimentos vs. datos observacionales",
        "m5-causal-diagrams": "Diagramas causales",
        "m5-howto-draw-and-use-a-causal-diagram": "Cómo: dibujar un diagrama causal",
        "m6": "6. Construir modelos",
        "m6-overfitting-and-regularization": "Sobreajuste y regularización",
        "m6-cross-validation-and-model-checking": "Validación cruzada y revisión del modelo",
        "m6-multicollinearity": "Multicolinealidad",
        "m6-measurement-error": "Error de medición",
        "m6-howto-validate-a-predictive-model": "Cómo: validar un modelo predictivo",
        "m6-howto-check-multicollinearity": "Cómo: comprobar la multicolinealidad",
        "m6-howto-handle-measurement-error": "Cómo: corregir el error de medición",
        "m7": "7. Estructuras de datos especiales",
        "m7-clustered-and-hierarchical-data": "Datos agrupados y jerárquicos",
        "m7-time-series-data": "Series temporales",
        "m7-meta-analysis": "Metaanálisis",
        "m7-meta-analysis-pitfalls": "Metaanálisis: sesgos y trampas",
        "m7-bayesian-methods": "Métodos bayesianos",
        "m7-howto-analyze-clustered-data": "Cómo: analizar datos agrupados",
        "m7-howto-run-a-meta-analysis": "Cómo: realizar un metaanálisis",
    },
}
