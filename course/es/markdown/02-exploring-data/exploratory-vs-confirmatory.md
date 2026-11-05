# Análisis exploratorio vs. confirmatorio

**En pocas palabras:** el análisis confirmatorio contrasta una idea concreta a la que te comprometiste *antes* de ver los datos, idealmente en un experimento bien diseñado. El análisis exploratorio consiste en rastrear los datos en busca de patrones que no habías especificado de antemano. Las garantías que promete un valor p (*p-value*) solo se cumplen en el primer caso: no es cuestión de fiarte más o menos de él, sino de si es siquiera la herramienta adecuada para aprender de los datos.

## El ejemplo de Mia, de dos maneras

- **Confirmatorio**: Mia diseñó un estudio de cohortes específicamente para comparar el colesterol LDL entre portadores y no portadores de una variante del gen LDLR (un "portador" tiene al menos una copia de la variante), decidió de antemano esa única comparación y ahora analiza los resultados. Este es el escenario de manual para el que se crearon las pruebas de hipótesis clásicas, aunque incluso aquí, presentar la diferencia de LDL con un intervalo de confianza enseña más que un veredicto de significativo/no significativo por sí solo.
- **Exploratorio**: Mia tiene una gran hoja de cálculo con datos de la clínica —edad, sexo, IMC, puntuación de dieta, genotipos de muchas variantes, LDL y una docena de columnas más— y quiere saber "¿qué se asocia con un LDL más alto?" sin ninguna comparación decidida de antemano.

Ambas son formas legítimas de trabajar con datos. El error es tratar la segunda como si fuera la primera.

## Por qué importa: el "jardín de los senderos que se bifurcan"

Si miras un conjunto de datos con 10 variables y contrastas todas las relaciones entre pares, es muy probable que encuentres algo que parezca "significativo" solo por azar, aunque nada en los datos esté relacionado con nada. El peligro no es solo elegir a propósito tu resultado favorito (*p-hacking*); es que *cualquier* investigador, de buena fe, toma decenas de pequeñas decisiones sin registrar mientras explora (qué valores atípicos excluir, qué agrupación usar, en qué subgrupo centrarse) y cada una puede empujar un resultado hacia lo "significativo". A esto se le llama a veces el **jardín de los senderos que se bifurcan** (*garden of forking paths*): incluso sin intención de hacer trampa, los muchos caminos que no tomaste siguen inflando la frecuencia con la que tropezarás con un patrón falso.

## Qué hacer en su lugar, si estás explorando

- No presentes un valor p de una pasada exploratoria como si zanjara la cuestión. Llámalo por lo que es: una hipótesis que habrá que contrastar bien más adelante, no un hallazgo confirmado.
- Apóyate primero en la visualización (véase [Fundamentos del EDA](./eda-basics.md)) en lugar de en una batería de pruebas.
- Si un patrón parece prometedor, el siguiente paso apropiado es recoger datos nuevos e independientes (o reservar una parte de los datos de antemano) para contrastarlo como es debido; eso es lo que convierte un hallazgo exploratorio en uno confirmatorio.

## Una forma rápida de saber cuál de los dos estás haciendo

Pregúntate: **¿se decidió esta comparación concreta antes de que viera estos datos?** Si la respuesta es sí —un experimento preregistrado, un ensayo diseñado en torno a una hipótesis—, estás en terreno confirmatorio. Si la comparación solo te resultó interesante *después* de mirar los datos, estás explorando, aparezca o no la palabra "prueba".

Ten en cuenta que esta es una cuestión distinta de si los datos proceden de un experimento aleatorizado: un ensayo aleatorizado bien diseñado también puede analizarse de forma exploratoria (por ejemplo, revisando muchos criterios de valoración secundarios o subgrupos que no estaba diseñado específicamente para contrastar); la aleatorización resuelve la *confusión*, no *qué comparaciones sales a buscar*.

> **Para saber más**
>
> - Gelman & Loken (2014), "The statistical crisis in science," *American Scientist* 102(6), 460–465 — el "jardín de los senderos que se bifurcan" en lenguaje llano.
> - Simmons, Nelson & Simonsohn (2011), "False-positive psychology," *Psychological Science* 22(11), 1359–1366 — cómo las decisiones flexibles de análisis inflan los falsos positivos.
> - Wagenmakers et al. (2012), "An agenda for purely confirmatory research," *Perspectives on Psychological Science* 7(6), 632–638 — por qué importa la frontera entre lo exploratorio y lo confirmatorio.

---
**Anterior:** [Inicio del módulo](./README.md) · **Siguiente:** [Fundamentos del EDA →](./eda-basics.md) · [Glosario](../glossary.md)
