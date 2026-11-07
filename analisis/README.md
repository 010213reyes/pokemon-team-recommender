# Fase 3 — Análisis de Datos

## Pokémon Team Recommender

### 1. Descripción

Esta fase tiene como objetivo evaluar la calidad de los datos obtenidos de PokéAPI, preparar un conjunto de datos validado y realizar un análisis exploratorio de las características estadísticas, los tipos y los perfiles defensivos de los 151 Pokémon de la primera generación.

Los resultados proporcionan una base para las siguientes etapas del proyecto: ingeniería de características, reducción de dimensionalidad, clustering y recomendación de equipos de tres Pokémon.

El análisis es descriptivo y exploratorio. No constituye todavía un modelo predictivo ni un sistema de recomendación terminado.

### 2. Objetivos

- Verificar la calidad, integridad y consistencia de los datos procesados.
- Identificar valores faltantes, duplicados y valores atípicos.
- Construir y validar los conjuntos de datos CLEAN.
- Explorar las distribuciones de las seis estadísticas base.
- Analizar las correlaciones entre características.
- Estudiar la distribución de tipos Pokémon.
- Evaluar resistencias, debilidades e inmunidades.
- Explorar la complementariedad defensiva entre tres Pokémon.
- Documentar resultados, limitaciones y decisiones metodológicas.

### 3. Estructura de la fase

```text
analisis/
├── README.md
├── docs/
│   ├── 01_diagnostico_calidad.md
│   ├── 02_reglas_limpieza.md
│   ├── 03_validacion_final.md
│   └── 04_resultados_eda.md
├── notebooks/
│   ├── 01_diagnostico_calidad.ipynb
│   └── 02_analisis_exploratorio.ipynb
├── scripts/
│   ├── build_clean_dataset.py
│   └── validate_clean.py
└── resultados/
```

Los archivos CSV CLEAN se almacenan en `data/clean/` y no se versionan en Git.

### 4. Datos utilizados

Se trabaja con nueve conjuntos de datos provenientes de la fase de Ingeniería de Datos.

| Dataset | Registros |
|---|---:|
| pokemon.csv | 151 |
| pokemon_stats.csv | 906 |
| pokemon_types.csv | 218 |
| pokemon_abilities.csv | 395 |
| species.csv | 151 |
| pokemon_varieties.csv | 238 |
| types.csv | 18 |
| type_effectiveness.csv | 324 |
| pokemon_defensive_profile.csv | 2,718 |

Los 2,718 registros defensivos representan 151 Pokémon evaluados frente a 18 tipos atacantes.

El proyecto utiliza las reglas actuales de PokéAPI, no exclusivamente las reglas históricas de los juegos originales de primera generación.

### 5. Metodología

#### 5.1 Diagnóstico de calidad

Se revisaron valores nulos, duplicados, integridad de identificadores, relaciones entre tablas y valores estadísticos atípicos.

Se detectaron seis valores atípicos mediante el método del rango intercuartílico (IQR). Se conservaron porque corresponden a estadísticas válidas de Pokémon reales.

#### 5.2 Preparación CLEAN

Se construyeron nueve archivos CLEAN a partir de los datos procesados.

No fue necesario modificar los registros, ya que las validaciones no identificaron problemas que justificaran eliminaciones, imputaciones o transformaciones correctivas.

Se verificó la equivalencia mediante hashes SHA-256.

#### 5.3 Validación

La validación CLEAN concluyó con 53 de 53 comprobaciones satisfactorias.

#### 5.4 Análisis exploratorio

Se analizaron:

- Estadísticas descriptivas y distribuciones.
- Correlaciones de Pearson entre estadísticas base.
- Frecuencia de tipos.
- Pokémon de uno y dos tipos.
- Multiplicadores defensivos.
- Rankings de resistencias, debilidades e inmunidades.
- Complementariedad defensiva de un equipo experimental.

### 6. Resultados principales

**Calidad de datos:** no se detectaron valores nulos ni duplicados exactos en los conjuntos revisados.

**Estadísticas:** las correlaciones muestran relaciones moderadas entre algunas variables, sin redundancia extrema.

**Tipos:** 84 Pokémon tienen un tipo y 67 tienen dos tipos.

**Defensa:** el promedio por Pokémon es de 3.85 resistencias, 3.07 debilidades y 0.45 inmunidades.

**Complementariedad:** el equipo experimental Blastoise, Charizard y Magnemite dispone de al menos una resistencia o inmunidad frente a 16 de los 18 tipos atacantes.

Los resultados detallados se encuentran en `docs/04_resultados_eda.md`.

### 7. Ejecución

Desde la raíz del repositorio:

```powershell
python analisis/scripts/build_clean_dataset.py
python analisis/scripts/validate_clean.py
```

Posteriormente, abrir y ejecutar los notebooks en orden:

1. `analisis/notebooks/01_diagnostico_calidad.ipynb`
2. `analisis/notebooks/02_analisis_exploratorio.ipynb`

Los notebooks deben ejecutarse con un entorno Python que tenga instaladas las dependencias del proyecto.

### 8. Limitaciones

- El estudio se limita a los 151 Pokémon originales.
- Las relaciones de tipos corresponden a las reglas actuales de PokéAPI.
- Los perfiles defensivos no consideran habilidades, objetos, movimientos ni condiciones de combate.
- El análisis de complementariedad utiliza un equipo de ejemplo y no demuestra optimalidad.
- No se ha realizado todavía entrenamiento de modelos de clustering ni evaluación del recomendador.

### 9. Conclusión

La fase permitió obtener conjuntos de datos validados y comprender las principales características estadísticas y defensivas de los Pokémon estudiados.

Los resultados proporcionan una base consistente para la siguiente fase de Ciencia de Datos, donde se desarrollarán las características, los modelos de agrupamiento y la lógica experimental de recomendación de equipos.