
# 05 — Diagnóstico Final de Minería de Datos

## Proyecto: Pokémon Team Recommender

**Fase:** 1 — Minería de Datos  
**Fuente:** PokéAPI v2  
**Fecha:** 03/11/2026  
**Estado:** Diagnóstico preliminar basado en exploración controlada

---

## 1. Objetivo

Consolidar los resultados de la investigación documental y la exploración técnica de PokéAPI, identificando la viabilidad de construir un dataset para análisis estadístico, clustering y recomendación de equipos Pokémon.

---

## 2. Metodología aplicada

La fase se desarrolló mediante:

1. Investigación de los recursos disponibles en PokéAPI.
2. Identificación de variables y entidades.
3. Elaboración del diccionario de datos.
4. Diseño de un modelo conceptual.
5. Definición de criterios de calidad.
6. Construcción y ejecución de un notebook exploratorio.
7. Evaluación preliminar de viabilidad.

La exploración se realizó mediante Python, Requests y Pandas.

No se efectuó una extracción masiva.

---

## 3. Fuente de datos

La fuente principal es PokéAPI v2.

URL: https://pokeapi.co/api/v2/

Recursos considerados:

| Recurso | Aplicación |
|---|---|
| Pokémon | Estadísticas y atributos |
| Pokémon Species | Clasificación y variedades |
| Type | Efectividad de tipos |
| Ability | Habilidades |
| Move | Movimientos |
| Evolution Chain | Evoluciones |
| Generation | Generaciones |
| Pokémon Form | Formas |

La disponibilidad general de estos recursos se documentó a partir de la estructura de la API.

---

## 4. Resultados de exploración

### 4.1 Ejecución

El notebook exploratorio se ejecutó sin errores, según la prueba reportada.

### 4.2 Muestra evaluada

Se consultaron seis entradas Pokémon:

| ID | Pokémon | Estadísticas completas | Número de estadísticas | Tipos | Habilidades | Movimientos |
|---|---|---|---|---|---|---|
| 1 | Bulbasaur | Sí | 6 | 2 | 2 | 86 |
| 4 | Charmander | Sí | 6 | 1 | 2 | 105 |
| 7 | Squirtle | Sí | 6 | 1 | 2 | 105 |
| 25 | Pikachu | Sí | 6 | 1 | 2 | 109 |
| 133 | Eevee | Sí | 6 | 1 | 3 | 74 |
| 150 | Mewtwo | Sí | 6 | 1 | 2 | 167 |

Las seis entradas están marcadas como variedades predeterminadas.

### 4.3 Resultados de calidad

| Indicador | Resultado |
|---|---|
| Entradas evaluadas | 6 |
| Entradas con estadísticas completas | 6 |
| Completitud de estadísticas esperadas en la muestra | 100 % |
| Entradas con al menos un tipo | 6 |
| Entradas con al menos una habilidad | 6 |
| Entradas predeterminadas | 6 |

Los identificadores reportados son distintos entre sí.

Estos resultados corresponden exclusivamente a la muestra exploratoria.

---

## 5. Hallazgos principales

### 5.1 Disponibilidad de estadísticas

Las seis estadísticas base se encuentran disponibles en todas las entradas de la muestra.

Esto permite continuar con la propuesta de caracterización multivariada.

### 5.2 Información relacional

La estructura de PokéAPI permite identificar relaciones entre Pokémon, especies, tipos, habilidades y movimientos.

Estas relaciones requieren un modelo de integración que evite duplicaciones.

### 5.3 Variabilidad de características

La muestra presenta diferencias en cantidades de tipos, habilidades y movimientos asociados.

Esto confirma que no todas las entradas poseen la misma estructura multivaluada.

### 5.4 Unidad de análisis

Se mantiene provisionalmente `pokemon_id` como unidad principal.

Las especies y variedades se relacionarán mediante identificadores explícitos.

---

## 6. Viabilidad por componente

| Componente | Evaluación preliminar |
|---|---|
| Extracción mediante API | Viable en la exploración |
| Integración de estadísticas | Viable |
| Caracterización de tipos | Viable |
| Análisis exploratorio | Viable |
| Clustering | Técnicamente plausible |
| Recomendación estructural | Técnicamente plausible |
| Predicción de victorias | No demostrada |

La viabilidad de clustering y recomendación requiere experimentación posterior.

---

## 7. Limitaciones

1. La muestra utilizada contiene únicamente seis entradas.
2. No representa toda la población disponible.
3. No se ha ejecutado el ETL completo.
4. No se ha evaluado la completitud global.
5. No se ha seleccionado un formato competitivo definitivo.
6. No se han entrenado modelos de clustering.
7. No se ha construido ni evaluado el recomendador.
8. No existen resultados de combates que validen una mejora en la probabilidad de victoria.

---

## 8. Riesgos identificados

| Riesgo | Medida propuesta |
|---|---|
| Duplicación por uniones | Normalización de entidades |
| Variedades múltiples | Identificación mediante pokemon_id |
| Valores faltantes | Perfilado de completitud |
| Errores HTTP | Reintentos y registros |
| Mezcla de reglas | Definir generación o formato |
| Variables redundantes | Análisis de correlación |
| Clusters inestables | Comparación y validación |
| Evaluación circular | Baselines y métricas independientes |

---

## 9. Requisitos para ingeniería de datos

La siguiente fase deberá implementar:

1. Extracción reproducible de recursos.
2. Conservación de respuestas JSON originales.
3. Paginación controlada.
4. Registro de errores HTTP.
5. Separación de entidades relacionales.
6. Validación de identificadores.
7. Transformación de estadísticas a columnas.
8. Tratamiento explícito de variedades.
9. Generación de datasets procesados.
10. Pruebas de calidad e integridad.

Los datos originales se almacenarán en `data/raw/` y los procesados en `data/processed/`, respetando la arquitectura existente.

---

## 10. Decisiones pendientes

Antes de cerrar definitivamente el diseño de ingeniería deberán establecerse:

- Generaciones incluidas.
- Inclusión de variedades alternativas.
- Tratamiento de legendarios y míticos.
- Formato o conjunto de reglas de combate.
- Alcance inicial de movimientos y habilidades.
- Variables obligatorias para el dataset analítico.

---

## 11. Conclusión

La exploración inicial demuestra que es posible consultar PokéAPI mediante Python y obtener características estructuradas de Pokémon.

En la muestra evaluada, las seis entradas presentaron las estadísticas base esperadas y relaciones de tipos y habilidades.

Los resultados respaldan continuar hacia ingeniería de datos para construir un conjunto de datos reproducible.

La viabilidad de clustering y recomendación es preliminar y deberá evaluarse mediante experimentos posteriores.

No se afirma todavía que el sistema permita generar equipos competitivamente superiores.

---

## 12. Evidencia

Notebook:

`mineria/notebooks/01_exploracion_pokeapi.ipynb`

Documentación relacionada:

- `01_analisis_fuentes.md`
- `02_diccionario_datos.md`
- `03_modelo_datos.md`
- `04_calidad_limitaciones.md`

Fuente:

https://pokeapi.co/docs/v2
