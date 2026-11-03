
# Fase 1 — Minería de Datos

## Pokémon Team Recommender

### 1. Descripción

Esta fase tiene como propósito investigar, identificar y evaluar las fuentes de datos necesarias para desarrollar el proyecto Pokémon Team Recommender.

El proyecto busca descubrir perfiles estadísticos y estructurales de Pokémon mediante técnicas de Data Science y Machine Learning no supervisado, para posteriormente construir un sistema de recomendación de equipos de tres integrantes.

La minería de datos constituye la etapa inicial del proceso y permitirá determinar qué información se encuentra disponible, cómo está organizada, qué limitaciones presenta y cómo puede utilizarse en las siguientes fases.

---

## 2. Objetivo general

Analizar las fuentes de datos del universo Pokémon, principalmente PokéAPI, para identificar las variables, entidades, relaciones y criterios de calidad necesarios para construir un conjunto de datos confiable y adecuado para el análisis multivariado, clustering y recomendación de equipos.

## 3. Objetivos específicos

1. Investigar la estructura y funcionamiento de PokéAPI.
2. Identificar los endpoints relevantes.
3. Documentar las variables disponibles.
4. Analizar las relaciones entre Pokémon, especies, tipos, habilidades, movimientos y evoluciones.
5. Definir una unidad de análisis.
6. Identificar problemas potenciales de calidad de datos.
7. Establecer criterios de inclusión y exclusión.
8. Diseñar un modelo conceptual de datos.
9. Evaluar la viabilidad de utilizar los datos para clustering y recomendación.

---

## 4. Fuente principal

**PokéAPI**

- Tipo: API REST pública.
- Formato: JSON.
- URL base: https://pokeapi.co/api/v2/
- Documentación: https://pokeapi.co/docs/v2
- Autenticación: no requerida para las consultas públicas.

La API permite consultar información relacionada con estadísticas, tipos, especies, habilidades, movimientos, generaciones y cadenas evolutivas.

La selección definitiva de recursos dependerá de la exploración técnica.

---

## 5. Alcance de la fase

### Actividades incluidas

- Investigación documental.
- Exploración de endpoints.
- Consultas controladas a la API.
- Identificación de entidades.
- Diccionario preliminar de datos.
- Análisis de calidad.
- Diseño conceptual.
- Diagnóstico de viabilidad.

### Actividades excluidas

- Extracción masiva.
- Construcción del ETL definitivo.
- Limpieza completa del dataset.
- Entrenamiento de modelos.
- Aplicación de PCA.
- Clustering.
- Desarrollo del recomendador.
- Evaluación de equipos.

Estas actividades corresponden a fases posteriores.

---

## 6. Metodología

### Etapa 1 — Investigación de fuentes

Estudiar la documentación oficial y seleccionar los recursos relevantes.

### Etapa 2 — Exploración técnica

Realizar solicitudes HTTP controladas para inspeccionar las respuestas JSON y comprobar la estructura de los datos.

### Etapa 3 — Diccionario de datos

Identificar variables, tipos, unidades, valores opcionales y procedencia.

### Etapa 4 — Modelado conceptual

Definir entidades, identificadores, relaciones y granularidad del dataset.

### Etapa 5 — Evaluación de calidad

Identificar riesgos de duplicación, valores faltantes, inconsistencias y limitaciones.

### Etapa 6 — Diagnóstico final

Consolidar los hallazgos y establecer los requisitos de la siguiente fase.

---

## 7. Organización

```text
mineria/
├── README.md
├── docs/
│   ├── 01_analisis_fuentes.md
│   ├── 02_diccionario_datos.md
│   ├── 03_modelo_datos.md
│   ├── 04_calidad_limitaciones.md
│   └── 05_diagnostico_final.md
├── notebooks/
├── scripts/
└── resultados/
```

### Responsabilidades

**docs/**

Documentación técnica, investigación y diagnóstico.

**notebooks/**

Exploración interactiva de datos y respuestas de la API.

**scripts/**

Código reutilizable para comprobaciones exploratorias, si resulta necesario.

**resultados/**

Resultados y evidencias de las verificaciones realizadas.

---

## 8. Preguntas de investigación

1. ¿Qué información proporciona PokéAPI?
2. ¿Qué diferencias existen entre especies, variedades y formas?
3. ¿Cuáles son las estadísticas relevantes para caracterizar Pokémon?
4. ¿Cómo se representan los tipos y sus relaciones de efectividad?
5. ¿Qué variables pueden utilizarse en Machine Learning?
6. ¿Qué información adicional necesita un recomendador de equipos?
7. ¿Cuáles son las limitaciones de la fuente?
8. ¿Qué estructura de datos permitirá integrar correctamente los recursos?

---

## 9. Entregables

| Entregable | Descripción |
|---|---|
| Análisis de fuentes | Endpoints y recursos disponibles |
| Diccionario de datos | Variables, tipos y unidades |
| Modelo conceptual | Entidades, claves y relaciones |
| Informe de calidad | Riesgos y controles |
| Notebook exploratorio | Verificación mediante consultas reales |
| Diagnóstico final | Viabilidad y requisitos para ingeniería de datos |

---

## 10. Criterios de aceptación

La fase estará completada cuando:

- [ ] Se identifiquen los endpoints necesarios.
- [ ] Se verifiquen respuestas reales de PokéAPI.
- [ ] Se documenten las variables candidatas.
- [ ] Se determine la unidad de análisis.
- [ ] Se definan las relaciones entre entidades.
- [ ] Se identifiquen los riesgos de calidad.
- [ ] Se establezcan reglas preliminares de inclusión.
- [ ] Se documente la viabilidad del clustering.
- [ ] Se documente la viabilidad del recomendador.
- [ ] Se complete el diagnóstico final.

---

## 11. Resultado esperado

Al concluir esta fase se dispondrá de un diagnóstico técnico que permita comenzar la ingeniería de datos con una estructura definida.

El resultado principal no será todavía un modelo de Machine Learning, sino una especificación de datos fundamentada en la investigación y exploración de la fuente.

---

## 12. Estado

**En desarrollo**

Rama de trabajo: `feature/mineria-datos`.

La fase se considerará finalizada únicamente después de revisar los resultados de exploración y validar los entregables.
