# Pokémon Team Recommender

## Análisis multivariado, Data Mining y recomendación de equipos de combate

---

## 1. Descripción del proyecto

**Pokémon Team Recommender** es un proyecto de análisis de datos y Machine Learning orientado al descubrimiento de patrones dentro de un conjunto de datos de Pokémon y a la construcción de un sistema de recomendación de equipos de combate de tres integrantes.

El proyecto utilizará información estructurada proveniente de fuentes de datos públicas, principalmente **PokéAPI**, para construir un conjunto de datos analítico que permita estudiar las características físicas, estadísticas, tipos, habilidades, movimientos, evoluciones y demás atributos disponibles de los Pokémon.

A partir de este conjunto de datos se desarrollará un flujo de trabajo de punta a punta que abarcará:

```text
Data Engineering
       ↓
Data Mining
       ↓
Data Analysis
       ↓
Feature Engineering
       ↓
Dimensionality Reduction
       ↓
Clustering
       ↓
Perfilamiento de Pokémon
       ↓
Team Recommendation
       ↓
Evaluation
```

El objetivo no es simplemente identificar cuáles son los Pokémon con mejores estadísticas, sino **descubrir estructuras y perfiles dentro del conjunto de Pokémon y utilizar dichos patrones para construir equipos de tres integrantes con características complementarias**.

---

# 2. Problema

La selección de un equipo Pokémon puede realizarse de diferentes maneras: mediante preferencias personales, popularidad, estadísticas individuales o experiencia del jugador.

Sin embargo, seleccionar los tres Pokémon con mayores estadísticas no garantiza que formen un equipo equilibrado.

Un equipo puede presentar:

- debilidades compartidas;
- redundancia de tipos;
- poca cobertura ofensiva;
- ausencia de determinados perfiles estadísticos;
- exceso de Pokémon con funciones similares;
- poca diversidad estructural.

Por esta razón, el proyecto plantea el siguiente problema:

> **¿Es posible identificar perfiles estadísticos y estructurales de Pokémon mediante técnicas de Data Mining y Machine Learning, y utilizar dichos perfiles para recomendar equipos de tres Pokémon con mayor complementariedad?**

---

# 3. Objetivo general

Desarrollar un sistema de análisis y recomendación capaz de descubrir perfiles de Pokémon mediante técnicas de análisis multivariado y clustering, para posteriormente utilizar dichos perfiles junto con información estadística y de tipos en la construcción de equipos de tres Pokémon complementarios.

---

# 4. Objetivos específicos

### OE1 — Adquisición de datos

Obtener información estructurada de Pokémon mediante APIs y fuentes de datos públicas.

### OE2 — Data Engineering

Diseñar un proceso reproducible de extracción, transformación, limpieza y almacenamiento de los datos.

### OE3 — Data Mining

Explorar patrones, relaciones, distribuciones y estructuras presentes en los datos.

### OE4 — Data Analysis

Realizar un análisis exploratorio de las características estadísticas, físicas, tipológicas y evolutivas de los Pokémon.

### OE5 — Feature Engineering

Construir variables derivadas que representen características relevantes para el análisis y la recomendación.

### OE6 — Machine Learning no supervisado

Aplicar técnicas de reducción dimensional y clustering para descubrir grupos naturales de Pokémon.

### OE7 — Perfilamiento

Interpretar los clusters obtenidos y definir perfiles de Pokémon basados en sus características.

### OE8 — Recomendación

Desarrollar un algoritmo capaz de seleccionar un equipo de tres Pokémon considerando complementariedad y cobertura.

### OE9 — Evaluación

Comparar el sistema propuesto contra diferentes estrategias base para determinar si la metodología genera equipos con mejores propiedades de complementariedad.

---

# 5. Hipótesis

### H1 — Existencia de perfiles

Los Pokémon pueden agruparse en perfiles diferenciables mediante sus características estadísticas y estructurales.

### H2 — Utilidad del clustering

Los grupos obtenidos mediante técnicas de clustering proporcionan información útil para caracterizar diferentes roles o perfiles de Pokémon.

### H3 — Complementariedad

La combinación de Pokémon pertenecientes a diferentes perfiles puede generar equipos con mayor diversidad y complementariedad que la selección basada únicamente en estadísticas individuales.

### H4 — Recomendación

Un algoritmo que considere estadísticas, tipos, resistencias, cobertura y diversidad de perfiles puede producir equipos de tres Pokémon más equilibrados que estrategias de selección simples.

---

# 6. Alcance

El proyecto abarcará principalmente:

- adquisición de datos;
- ingeniería de datos;
- limpieza;
- transformación;
- análisis exploratorio;
- minería de datos;
- feature engineering;
- reducción dimensional;
- clustering;
- perfilamiento;
- recomendación;
- evaluación cuantitativa;
- documentación técnica.

El proyecto **no requiere despliegue de una aplicación web** como parte del alcance principal.

El producto final será principalmente un **proyecto reproducible de Data Science publicado en GitHub**, acompañado de notebooks, código modular, datasets procesados, modelos y documentación.

---

# 7. Fuente principal de datos

La fuente inicial será **PokéAPI**, una API pública que proporciona información estructurada relacionada con el universo Pokémon.

Entre los recursos que podrán utilizarse se encuentran:

- Pokémon;
- especies;
- estadísticas;
- tipos;
- habilidades;
- movimientos;
- cadenas evolutivas;
- generaciones;
- regiones;
- hábitats;
- características adicionales disponibles mediante la API.

La selección definitiva de variables se realizará después de estudiar la estructura real de la API.

No se asumirán variables antes de analizar la fuente.

---

# 8. Arquitectura general del proyecto

```text
                    ┌──────────────────┐
                    │     PokéAPI      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Data Ingestion   │
                    │    Extraction    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Raw Dataset    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Cleaning & ETL │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Processed Dataset│
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌─────────────────┐          ┌──────────────────┐
     │ Exploratory     │          │ Feature          │
     │ Data Analysis   │          │ Engineering      │
     └────────┬────────┘          └─────────┬────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌──────────────────┐
                    │       PCA        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Clustering    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Pokémon Profiles │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Team Recommender │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Evaluation    │
                    └──────────────────┘
```

---

# 9. Plan de desarrollo

## Fase 0 — Configuración del entorno

### Objetivo

Preparar un entorno reproducible para el desarrollo.

### Actividades

- Crear entorno virtual.
- Configurar Python.
- Instalar dependencias.
- Crear `requirements.txt`.
- Configurar `.gitignore`.
- Inicializar Git.
- Crear repositorio remoto.
- Configurar rama `main`.

### Estado

**Completada.**

---

# Fase 1 — Exploración de la fuente de datos

### Objetivo

Comprender la estructura de PokéAPI antes de diseñar el proceso de extracción.

### Actividades

- Analizar endpoints disponibles.
- Identificar recursos relevantes.
- Revisar relaciones entre recursos.
- Determinar variables disponibles.
- Identificar datos redundantes.
- Identificar posibles limitaciones.
- Definir el esquema inicial del dataset.

### Resultado esperado

Un diseño inicial del modelo de datos y de las entidades que serán extraídas.

---

# Fase 2 — Data Engineering / Data Ingestion

### Objetivo

Construir un proceso reproducible para obtener los datos.

### Actividades

- Implementar cliente para la API.
- Realizar extracción.
- Manejar respuestas HTTP.
- Manejar errores.
- Controlar solicitudes.
- Guardar información raw.
- Separar extracción de transformación.

### Resultado esperado

Dataset raw reproducible.

```text
data/
└── raw/
    └── ...
```

---

# Fase 3 — Data Cleaning & Transformation

### Objetivo

Transformar los datos obtenidos desde la API en un dataset analítico consistente.

### Actividades

- Normalización.
- Eliminación de duplicados.
- Manejo de valores faltantes.
- Conversión de tipos.
- Integración de entidades.
- Estandarización de nombres.
- Resolución de relaciones.
- Validación de registros.

### Resultado esperado

Dataset procesado preparado para análisis.

```text
data/
├── raw/
└── processed/
    └── pokemon_dataset.csv
```

---

# Fase 4 — Exploratory Data Analysis

### Objetivo

Comprender el comportamiento de los datos antes de aplicar Machine Learning.

### Análisis

Se estudiarán variables como:

- HP;
- Attack;
- Defense;
- Special Attack;
- Special Defense;
- Speed;
- estadísticas totales;
- peso;
- altura;
- experiencia base;
- tipos;
- habilidades;
- evolución;
- generación;
- legendario/mítico;
- otras variables disponibles.

### Preguntas de análisis

- ¿Cómo se distribuyen las estadísticas?
- ¿Qué relaciones existen entre estadísticas?
- ¿Qué tipos aparecen con mayor frecuencia?
- ¿Existen perfiles estadísticos visibles?
- ¿Existen correlaciones?
- ¿Existen valores extremos?
- ¿Cómo evolucionan las características entre generaciones?
- ¿Existen diferencias entre grupos de Pokémon?

---

# Fase 5 — Feature Engineering

### Objetivo

Construir variables que representen de mejor manera las características relevantes de cada Pokémon.

Además de las variables originales, se podrán generar características derivadas.

### Ejemplos

```text
total_stats
offensive_score
defensive_score
special_offense
special_defense
speed_score
physical_bulk
special_bulk
type_count
evolution_stage
is_legendary
is_mythical
```

También se estudiarán características relacionadas con tipos:

```text
weakness_count
resistance_count
immunity_count
offensive_type_coverage
defensive_type_coverage
```

Las variables definitivas dependerán del análisis realizado en las fases anteriores.

---

# Fase 6 — Reducción dimensional

### Objetivo

Reducir la dimensionalidad de las variables numéricas para facilitar el análisis y visualización de la estructura de los datos.

Se utilizará principalmente:

**Principal Component Analysis — PCA**

### Actividades

- Estandarización.
- Ajuste de PCA.
- Análisis de varianza explicada.
- Selección de componentes.
- Visualización.
- Interpretación de componentes.

### Resultado esperado

Una representación de menor dimensionalidad que permita observar estructuras y relaciones entre Pokémon.

---

# Fase 7 — Clustering / Data Mining

### Objetivo

Descubrir grupos naturales de Pokémon con características similares.

Se evaluarán diferentes técnicas de clustering, por ejemplo:

- K-Means;
- DBSCAN;
- clustering jerárquico.

La selección del método no estará predeterminada.

Se compararán los resultados mediante métricas como:

- Silhouette Score;
- Davies-Bouldin Index;
- Calinski-Harabasz Index.

También se analizará la interpretabilidad de los grupos.

---

# Fase 8 — Perfilamiento de Pokémon

### Objetivo

Interpretar los clusters obtenidos y convertirlos en perfiles comprensibles.

Ejemplos hipotéticos:

```text
Perfil A
Pokémon rápidos y ofensivos

Perfil B
Pokémon defensivos

Perfil C
Pokémon con alto ataque especial

Perfil D
Pokémon equilibrados

Perfil E
Pokémon especializados
```

Estos nombres **no serán definidos previamente**.

Los perfiles serán determinados a partir de los resultados obtenidos.

### Resultado esperado

Cada Pokémon tendrá asociado un perfil estadístico/estructural.

```text
Pokémon → Cluster → Perfil
```

---

# Fase 9 — Diseño del sistema de recomendación

### Objetivo

Diseñar el mecanismo que seleccionará equipos de tres Pokémon.

El recomendador no buscará simplemente:

```text
Pokémon con mayor estadística
```

En su lugar, buscará:

```text
A + B + C
```

donde el conjunto presente características complementarias.

---

# 10. Concepto de complementariedad

La función de recomendación podrá considerar diferentes dimensiones.

### 10.1 Cobertura de tipos

Evaluar qué tipos ofensivos puede cubrir el equipo.

### 10.2 Resistencias

Evaluar las resistencias e inmunidades disponibles.

### 10.3 Debilidades compartidas

Penalizar equipos donde los tres Pokémon compartan demasiadas debilidades.

### 10.4 Diversidad estadística

Evitar seleccionar tres Pokémon con perfiles estadísticos prácticamente idénticos.

### 10.5 Diversidad de clusters

Favorecer combinaciones provenientes de perfiles diferentes cuando esto produzca una mayor complementariedad.

### 10.6 Roles

Considerar diferentes funciones estadísticas:

```text
Ofensivo
Defensivo
Velocidad
Ataque especial
Balanceado
```

### 10.7 Redundancia

Penalizar características excesivamente repetidas entre integrantes.

---

# 11. Modelo conceptual del recomendador

La recomendación podrá representarse mediante una función de puntuación:

```text
Team Score =
    Type Coverage
  + Resistance Coverage
  + Role Diversity
  + Cluster Diversity
  + Statistical Complementarity
  - Shared Weaknesses
  - Redundancy
```

Los pesos definitivos serán determinados durante la fase de experimentación.

La intención es construir un sistema interpretable, donde pueda explicarse **por qué** un equipo fue recomendado.

---

# Fase 10 — Generación de equipos

### Objetivo

Generar diferentes combinaciones de tres Pokémon y calcular su puntuación de complementariedad.

Conceptualmente:

```text
Pokémon A
    +
Pokémon B
    +
Pokémon C
    ↓
Team Scoring
    ↓
Complementarity Score
```

El sistema deberá ser capaz de devolver un equipo y explicar sus principales fortalezas y debilidades.

Ejemplo conceptual:

```text
Equipo recomendado

1. Pokémon A
   Perfil: ofensivo
   Tipo: X

2. Pokémon B
   Perfil: defensivo
   Tipo: Y

3. Pokémon C
   Perfil: velocidad
   Tipo: Z

Score: 0.87
```

---

# Fase 11 — Evaluación

### Objetivo

Determinar si el sistema propuesto realmente mejora sobre estrategias simples.

Se utilizarán diferentes baselines.

### Baseline 1 — Random

Equipo formado aleatoriamente.

### Baseline 2 — Statistical

Equipo formado utilizando únicamente estadísticas individuales.

### Baseline 3 — Proposed

Equipo generado mediante el algoritmo de complementariedad desarrollado en el proyecto.

---

## Métricas de evaluación

Dependiendo de las variables disponibles, se podrán evaluar:

- cobertura de tipos;
- número de resistencias;
- número de debilidades compartidas;
- diversidad estadística;
- diversidad de clusters;
- redundancia;
- score global de complementariedad.

La comparación permitirá determinar si el método propuesto presenta mejores propiedades estructurales que los métodos base.

---

# Fase 12 — Interpretación y conclusiones

### Objetivo

Analizar los resultados obtenidos desde una perspectiva de Data Science.

Se documentará:

- comportamiento de los datos;
- patrones encontrados;
- calidad de los clusters;
- perfiles descubiertos;
- comportamiento del recomendador;
- comparación con baselines;
- limitaciones;
- posibles mejoras.

La conclusión deberá responder principalmente:

> ¿Los datos permiten descubrir perfiles diferenciables de Pokémon?

y:

> ¿La utilización de dichos perfiles junto con características de tipos y estadísticas permite construir equipos de tres Pokémon más complementarios?

---

# 13. Estructura final esperada

```text
pokemon-team-recommender/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_dimensionality_reduction.ipynb
│   ├── 06_clustering.ipynb
│   ├── 07_team_recommendation.ipynb
│   └── 08_evaluation.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── clustering/
│   ├── recommendation/
│   └── evaluation/
│
├── models/
│
├── reports/
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 14. Principios de desarrollo

El proyecto seguirá los siguientes principios:

### Reproducibilidad

Los procesos de extracción y transformación deberán poder ejecutarse nuevamente.

### Modularidad

La lógica principal se separará de los notebooks.

### Trazabilidad

Se conservará la separación entre datos raw y procesados.

### Interpretabilidad

Los resultados del clustering y del recomendador deberán poder explicarse.

### Validación

Las decisiones metodológicas se respaldarán mediante métricas y comparaciones.

### Experimentación

No se asumirá de antemano cuál algoritmo de clustering o configuración será mejor.

### Data-driven approach

Las conclusiones deberán derivarse de los datos y resultados obtenidos, no de suposiciones sobre el universo Pokémon.

---

# 15. Limitaciones

El proyecto deberá reconocer algunas limitaciones importantes.

La recomendación de equipos no necesariamente representa una estrategia óptima para combates competitivos reales.

El sistema estará principalmente orientado a **complementariedad estadística y estructural**.

Para construir un modelo capaz de predecir resultados reales de combates sería necesario incorporar datos adicionales como:

- registros históricos de combates;
- movimientos utilizados;
- decisiones de jugadores;
- sets competitivos;
- objetos;
- habilidades utilizadas;
- formatos;
- resultados de partidas.

Por lo tanto, el proyecto inicial se enfocará en:

> **descubrir estructura en los datos y recomendar equipos complementarios.**

---

# 16. Evolución futura

El proyecto podrá evolucionar posteriormente hacia un sistema más avanzado.

Una posible segunda etapa sería incorporar datos históricos de combates y transformar el recomendador en un problema de optimización o predicción.

La evolución conceptual sería:

```text
Versión 1
Pokémon Data
     ↓
Clustering
     ↓
Complementarity
     ↓
Team Recommendation
```

Posteriormente:

```text
Versión 2
Pokémon Data
     +
Battle Data
     ↓
Feature Engineering
     ↓
Machine Learning
     ↓
Battle Prediction
     ↓
Team Optimization
```

Esto permitiría pasar de:

**"¿Qué equipo parece estadísticamente complementario?"**

a:

**"¿Qué equipo tiene mayor probabilidad de obtener un determinado resultado bajo condiciones específicas?"**

---

# 17. Tecnologías

### Lenguaje

- Python

### Data Engineering

- Requests
- Pandas
- APIs REST
- CSV / JSON

### Data Analysis

- Pandas
- NumPy
- Matplotlib
- Seaborn

### Machine Learning

- Scikit-learn
- PCA
- K-Means
- DBSCAN
- Clustering jerárquico

### Entorno

- Python Virtual Environment
- Jupyter
- Git
- GitHub

---

# 18. Resultado final

Al finalizar el proyecto se espera contar con:

1. Un proceso reproducible de extracción de datos.
2. Un dataset Pokémon procesado.
3. Un análisis exploratorio documentado.
4. Un conjunto de características diseñado para Machine Learning.
5. Una representación dimensional reducida.
6. Un modelo de clustering.
7. Perfiles de Pokémon descubiertos mediante Data Mining.
8. Un algoritmo de recomendación de equipos.
9. Una función de puntuación de complementariedad.
10. Comparación contra baselines.
11. Evaluación cuantitativa.
12. Documentación técnica completa.

---

# 19. Estado del proyecto

| Fase | Estado |
|---|---|
| Configuración del entorno | ✅ Completada |
| Repositorio Git/GitHub | ✅ Completado |
| Exploración de PokéAPI | ⏳ Pendiente |
| Data Ingestion | ⏳ Pendiente |
| Data Cleaning | ⏳ Pendiente |
| Exploratory Data Analysis | ⏳ Pendiente |
| Feature Engineering | ⏳ Pendiente |
| PCA | ⏳ Pendiente |
| Clustering | ⏳ Pendiente |
| Perfilamiento | ⏳ Pendiente |
| Team Recommendation | ⏳ Pendiente |
| Evaluación | ⏳ Pendiente |
| Conclusiones | ⏳ Pendiente |

---

# 20. Flujo completo del proyecto

```text
                         POKÉAPI
                           │
                           ▼
                  ┌─────────────────┐
                  │ DATA INGESTION  │
                  └────────┬────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  RAW DATA   │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ CLEANING / ETL  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ PROCESSED DATA  │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        ┌────────────┐           ┌──────────────┐
        │ DATA       │           │ FEATURE      │
        │ ANALYSIS   │           │ ENGINEERING  │
        └─────┬──────┘           └──────┬───────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                         PCA
                           │
                           ▼
                      CLUSTERING
                           │
                           ▼
                  POKÉMON PROFILES
                           │
                           ▼
                 TEAM RECOMMENDER
                           │
                           ▼
                 TEAM OF 3 POKÉMON
                           │
                           ▼
                      EVALUATION
                           │
                           ▼
                      CONCLUSIONS
```

---

# 21. Propósito del proyecto

Aunque el dominio utilizado corresponde al universo Pokémon, el proyecto está diseñado como un ejercicio completo de **Data Science aplicado a datos estructurados**.

La intención es demostrar la capacidad de construir un flujo que comienza con una fuente de datos externa y termina con un producto analítico basado en Machine Learning:

```text
Fuente de datos
      ↓
Ingeniería de datos
      ↓
Datos confiables
      ↓
Análisis
      ↓
Minería de datos
      ↓
Machine Learning
      ↓
Modelo interpretable
      ↓
Sistema de recomendación
      ↓
Evaluación
```

El valor principal del proyecto estará en la **metodología, el tratamiento de datos, la construcción de variables, el descubrimiento de patrones y la evaluación del sistema**, no únicamente en el dominio utilizado.
