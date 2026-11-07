# Resultados del Análisis Exploratorio de Datos (EDA)

## Pokémon Team Recommender — Fase 3

### 1. Objetivo

Analizar las características estadísticas, los tipos y las relaciones defensivas de los 151 Pokémon de primera generación, utilizando datos validados procedentes de PokéAPI.

El propósito es identificar patrones y características que puedan utilizarse posteriormente en el desarrollo de un sistema experimental de recomendación de equipos.

### 2. Datos analizados

Se utilizaron los nueve conjuntos de datos CLEAN generados durante la fase.

Los principales conjuntos empleados en el EDA fueron:

- `pokemon.csv`: identificación de los Pokémon.
- `pokemon_stats.csv`: estadísticas base.
- `pokemon_types.csv`: asignación de tipos.
- `types.csv`: catálogo de tipos.
- `pokemon_defensive_profile.csv`: relaciones defensivas frente a los 18 tipos atacantes.

El conjunto contiene 151 Pokémon únicos y 2,718 relaciones defensivas.

### 3. Diagnóstico de calidad

Los datos fueron revisados antes de realizar el análisis exploratorio.

**Resultados:**

- Sin valores nulos detectados.
- Sin duplicados exactos detectados.
- Relaciones e identificadores validados.
- Nueve conjuntos CLEAN generados.
- Equivalencia entre PROCESSED y CLEAN comprobada mediante SHA-256.
- 53 de 53 validaciones CLEAN satisfactorias.

#### 3.1 Valores atípicos

Se identificaron seis observaciones atípicas mediante el método IQR:

| Pokémon | Estadística | Valor |
|---|---|---:|
| Cloyster | Defense | 180 |
| Onix | Defense | 160 |
| Chansey | HP | 250 |
| Snorlax | HP | 160 |
| Wigglytuff | HP | 140 |
| Mewtwo | Special Attack | 154 |

Estos valores fueron conservados por corresponder a características válidas de los Pokémon.

Un valor estadísticamente atípico no implica necesariamente un error de calidad.

### 4. Análisis de estadísticas base

Se analizaron seis características:

- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

Se calcularon estadísticas descriptivas y se visualizaron sus distribuciones mediante histogramas.

#### 4.1 Correlaciones

Se utilizó el coeficiente de correlación de Pearson.

Entre los resultados observados destacan:

| Variables | Correlación |
|---|---:|
| Special Attack / Special Defense | 0.53 |
| HP / Special Defense | 0.49 |
| Attack / Defense | 0.48 |
| Special Attack / Speed | 0.41 |
| Special Defense / Speed | 0.39 |
| Defense / Speed | -0.05 |
| HP / Speed | -0.04 |

**Interpretación:**

Las correlaciones positivas más altas son moderadas. No se observaron correlaciones extremas que justificaran eliminar automáticamente alguna de las seis estadísticas.

Las seis variables se consideran candidatas para etapas posteriores de ingeniería de características y clustering.

### 5. Distribución de tipos

Se analizaron las frecuencias de los tipos asignados a los Pokémon.

Los tipos más frecuentes fueron:

| Tipo | Apariciones |
|---|---:|
| Poison | 33 |
| Water | 32 |
| Normal | 22 |
| Flying | 19 |
| Ground | 14 |
| Psychic | 14 |
| Grass | 14 |
| Bug | 12 |
| Fire | 12 |

Las frecuencias representan asignaciones de tipos, no Pokémon únicos.

El tipo Dark no aparece entre los Pokémon originales estudiados bajo la clasificación actual de PokéAPI.

#### 5.1 Pokémon de uno y dos tipos

| Clasificación | Pokémon | Porcentaje |
|---|---:|---:|
| Un tipo | 84 | 55.6 % |
| Dos tipos | 67 | 44.4 % |
| Total | 151 | 100 % |

Se identificaron 218 asignaciones de tipos.

**Interpretación:**

La presencia de Pokémon con dos tipos introduce combinaciones defensivas que pueden modificar resistencias, inmunidades y debilidades.

### 6. Distribución de multiplicadores defensivos

Se analizaron 2,718 combinaciones Pokémon–tipo atacante.

| Multiplicador | Interpretación | Registros |
|---|---|---:|
| 0× | Inmunidad | 68 |
| 0.25× | Resistencia doble | 64 |
| 0.5× | Resistencia | 517 |
| 1× | Daño neutral | 1,605 |
| 2× | Debilidad | 433 |
| 4× | Debilidad doble | 31 |
| **Total** | | **2,718** |

El daño neutral representa la categoría más frecuente.

Las relaciones defensivas proporcionan información útil para evaluar la compatibilidad entre integrantes de un equipo.

### 7. Resumen defensivo individual

Se calcularon los conteos de inmunidades, resistencias y debilidades para cada Pokémon.

| Indicador | Promedio | Mediana | Máximo |
|---|---:|---:|---:|
| Inmunidades | 0.45 | 0 | 2 |
| Resistencias | 3.85 | 4 | 11 |
| Debilidades | 3.07 | 3 | 7 |
| Debilidades de 4× | 0.21 | 0 | 2 |

Las resistencias incluyen multiplicadores de 0.25× y 0.5×. Las debilidades incluyen 2× y 4×.

#### 7.1 Pokémon con más resistencias

Magnemite y Magneton presentan:

- 11 resistencias.
- 1 inmunidad.
- 3 debilidades.
- 1 debilidad de 4×.

#### 7.2 Pokémon con más debilidades

Exeggcute y Exeggutor presentan:

- 7 debilidades.
- 6 resistencias.
- 1 debilidad de 4×.

#### 7.3 Pokémon con más inmunidades

Entre los Pokémon con dos inmunidades se encuentran:

- Gastly.
- Haunter.
- Gengar.
- Pidgey.
- Pidgeotto.
- Pidgeot.

Estos resultados no constituyen un ranking general de calidad competitiva.

### 8. Experimento de complementariedad defensiva

Se evaluó un equipo formado por:

1. Blastoise — Water.
2. Charizard — Fire / Flying.
3. Magnemite — Electric / Steel.

Para cada uno de los 18 tipos atacantes se compararon los multiplicadores defensivos de los tres integrantes.

Se definió como tipo cubierto aquel frente al cual al menos un integrante presenta resistencia o inmunidad, es decir, un multiplicador inferior a 1.

#### 8.1 Resultados

| Indicador | Resultado |
|---|---:|
| Tipos atacantes evaluados | 18 |
| Tipos con resistencia o inmunidad disponible | 16 |
| Cobertura defensiva descriptiva | 88.89 % |
| Tipos sin resistencia disponible | 2 |
| Tipos frente a los que los tres son débiles | 0 |

Los tipos sin resistencia disponible fueron Dark y Ghost, frente a los cuales los tres integrantes presentan multiplicador neutral.

#### 8.2 Ejemplos de complementariedad

**Ground:** Magnemite presenta debilidad de 4×, mientras que Charizard es inmune.

**Rock:** Charizard presenta debilidad de 4×, mientras que Magnemite tiene resistencia de 0.5×.

**Electric:** Blastoise y Charizard son vulnerables, mientras que Magnemite presenta resistencia de 0.5×.

**Grass:** Blastoise presenta debilidad de 2×, mientras que Charizard tiene resistencia de 0.25×.

#### 8.3 Interpretación

El experimento muestra que las debilidades individuales pueden compensarse mediante resistencias o inmunidades de otros integrantes.

Sin embargo, la cobertura defensiva calculada no representa una probabilidad de victoria ni garantiza que el equipo sea óptimo.

El experimento se utiliza exclusivamente como evidencia exploratoria de complementariedad defensiva.

### 9. Implicaciones para Ciencia de Datos

Los resultados permiten identificar posibles variables para la siguiente fase:

**Características estadísticas:**
- HP.
- Attack.
- Defense.
- Special Attack.
- Special Defense.
- Speed.

**Características defensivas:**
- Número de inmunidades.
- Número de resistencias.
- Número de debilidades.
- Número de debilidades de 4×.
- Perfil de multiplicadores frente a los 18 tipos atacantes.

Estas variables son candidatas y deberán evaluarse antes de incorporarlas a los modelos.

En la siguiente fase se podrán estudiar normalización, PCA, clustering y criterios de complementariedad para construir un recomendador experimental de tres Pokémon.

### 10. Limitaciones

1. La muestra contiene únicamente 151 Pokémon.
2. Las relaciones defensivas utilizan el sistema actual de PokéAPI.
3. Los perfiles no consideran movimientos, habilidades, objetos ni condiciones de combate.
4. Las estadísticas base no describen por sí solas el rendimiento competitivo.
5. El experimento de complementariedad utiliza una combinación seleccionada manualmente.
6. No se ha demostrado que la combinación analizada sea óptima.
7. No se han entrenado ni evaluado modelos de clustering en esta fase.

### 11. Conclusión

El análisis exploratorio permitió caracterizar las estadísticas, la distribución de tipos y las relaciones defensivas de los Pokémon estudiados.

Los resultados muestran variabilidad entre las estadísticas base, diferencias en la frecuencia de tipos y perfiles defensivos que pueden complementarse entre distintos Pokémon.

La validación de calidad y el análisis descriptivo proporcionan una base reproducible para la siguiente fase del proyecto, orientada al desarrollo de características, agrupamiento y recomendación experimental de equipos.