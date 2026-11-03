
# 02 — Diccionario de Datos

## Proyecto: Pokémon Team Recommender

**Fase:** Minería de Datos  
**Estado:** Preliminar, pendiente de validación empírica  
**Fuente principal:** PokéAPI v2  
**Documentación:** https://pokeapi.co/docs/v2

---

## 1. Objetivo

Documentar las variables candidatas que se utilizarán durante las etapas de adquisición, transformación, análisis exploratorio, Feature Engineering, clustering y recomendación de equipos Pokémon.

El diccionario establece:

- Nombre de cada variable.
- Entidad de origen.
- Tipo de dato esperado.
- Unidad de medida.
- Significado.
- Condiciones de nulidad.
- Utilidad analítica.
- Reglas preliminares de validación.

Las variables descritas no constituyen todavía el esquema definitivo del dataset.

Su disponibilidad y comportamiento deberán verificarse mediante consultas reales a PokéAPI.

---

## 2. Unidad de análisis

Se propone utilizar como unidad principal una entrada del recurso Pokémon, identificada mediante `pokemon_id`.

Una entrada Pokémon puede representar una variedad específica de una especie.

Por lo tanto, se distinguirán dos identificadores:

| Identificador | Entidad | Función |
|---|---|---|
| `pokemon_id` | Pokémon | Identificar una entrada con estadísticas y características de combate |
| `species_id` | Pokémon Species | Identificar la especie relacionada |

No se asumirá que ambos identificadores son equivalentes.

### Granularidad propuesta

El dataset analítico principal tendrá una fila por `pokemon_id`.

Las relaciones multivaluadas se almacenarán separadamente antes de construir las variables finales.

---

## 3. Identificación de Pokémon

**Endpoint de origen:** `/pokemon/{id}`

| Variable | Tipo esperado | Nulo | Descripción |
|---|---|---|---|
| `pokemon_id` | int | No | Identificador de entrada Pokémon |
| `pokemon_name` | string | No | Nombre de la entrada |
| `species_name` | string | No | Nombre de la especie asociada |
| `is_default` | bool | No | Indica si es la variedad predeterminada |
| `base_experience` | int/null | Sí | Experiencia base otorgada |
| `height_dm` | int | No | Altura expresada en decímetros |
| `weight_hg` | int | No | Peso expresado en hectogramos |

### Reglas preliminares

- `pokemon_id` debe ser único en la tabla principal.
- `pokemon_name` no debe estar vacío.
- `height_dm` y `weight_hg` deben ser no negativos.
- `base_experience` puede ser nulo.
- `is_default` debe contener valores booleanos.

---

## 4. Estadísticas base

**Endpoint:** `/pokemon/{id}`  
**Campo JSON:** `stats`

Las estadísticas constituyen uno de los principales grupos de variables para el análisis multivariado.

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `hp` | int | Puntos base | Salud base |
| `attack` | int | Puntos base | Ataque físico base |
| `defense` | int | Puntos base | Defensa física base |
| `special_attack` | int | Puntos base | Ataque especial base |
| `special_defense` | int | Puntos base | Defensa especial base |
| `speed` | int | Puntos base | Velocidad base |

### Transformación prevista

El arreglo JSON de estadísticas se convertirá a columnas independientes.

Ejemplo conceptual:

```text
pokemon_id | hp | attack | defense | special_attack | special_defense | speed
1          | 45 | 49     | 49      | 65             | 65              | 45
```

### Consideraciones

Las estadísticas base no representan directamente las estadísticas finales durante un combate.

El resultado real depende de otros factores, como nivel, naturaleza, valores individuales, valores de esfuerzo y mecánicas aplicables.

Por tanto, estas variables se utilizarán inicialmente para caracterización estadística.

---

## 5. Características físicas

| Variable original | Variable transformada | Unidad original | Unidad final |
|---|---|---|---|
| `height` | `height_m` | Decímetros | Metros |
| `weight` | `weight_kg` | Hectogramos | Kilogramos |

### Fórmulas

```python
height_m = height_dm / 10
weight_kg = weight_hg / 10
```

Las conversiones se realizarán durante la ingeniería de datos.

Las variables originales deberán conservarse en los datos raw.

---

## 6. Información de especie

**Endpoint:** `/pokemon-species/{id}`

| Variable | Tipo esperado | Nulo | Descripción |
|---|---|---|---|
| `species_id` | int | No | Identificador de especie |
| `species_name` | string | No | Nombre de especie |
| `generation` | string | No | Generación de introducción |
| `is_legendary` | bool | No | Clasificación legendaria |
| `is_mythical` | bool | No | Clasificación mítica |
| `capture_rate` | int | No* | Valor de captura |
| `base_happiness` | int/null | Sí | Valor base de amistad, si está disponible |
| `habitat` | string/null | Sí | Hábitat |
| `growth_rate` | string | No* | Grupo de crecimiento |
| `evolution_chain_id` | int/null | Sí | Referencia a cadena evolutiva |

*Las condiciones exactas de disponibilidad se verificarán durante la exploración.

### Consideraciones

Las variables de especie podrán utilizarse para:

- Comparaciones entre generaciones.
- Caracterización de grupos.
- Análisis de Pokémon legendarios y míticos.
- Análisis evolutivo.
- Evaluación de posibles sesgos.

No todas estas variables necesariamente formarán parte del modelo de clustering.

---

## 7. Tipos Pokémon

**Endpoint de origen:** `/pokemon/{id}`  
**Campo JSON:** `types`

Una entrada Pokémon puede tener uno o dos tipos en las mecánicas habituales del juego.

### Estructura propuesta

Tabla: `pokemon_types`

| Variable | Tipo | Descripción |
|---|---|---|
| `pokemon_id` | int | Referencia al Pokémon |
| `type_name` | string | Nombre del tipo |
| `slot` | int | Posición del tipo |

### Ejemplo

```text
pokemon_id | type_name | slot
1          | grass     | 1
1          | poison    | 2
```

### Consideraciones

Los tipos son variables categóricas.

Para clustering podrán representarse mediante codificación binaria.

Para recomendación se utilizarán en el cálculo de cobertura, resistencias y debilidades.

---

## 8. Efectividad de tipos

**Endpoint:** `/type/{id}`

El recurso de tipos proporciona relaciones de daño que permiten construir una matriz de efectividad.

### Estructura propuesta

Tabla: `type_effectiveness`

| Variable | Tipo | Descripción |
|---|---|---|
| `attacking_type` | string | Tipo del ataque |
| `defending_type` | string | Tipo del defensor |
| `multiplier` | float | Multiplicador de daño por tipo |

### Multiplicadores habituales

| Multiplicador | Interpretación |
|---|---|
| 0.0 | Inmunidad |
| 0.5 | Resistencia |
| 1.0 | Daño neutral |
| 2.0 | Debilidad |

Para un Pokémon con dos tipos, el multiplicador defensivo se obtiene combinando los multiplicadores correspondientes a ambos tipos.

Ejemplos posibles:

- 0.25
- 0.5
- 1.0
- 2.0
- 4.0

### Limitación

La matriz debe corresponder a las reglas de una generación o formato definido.

No se mezclarán relaciones de efectividad incompatibles entre generaciones.

---

## 9. Habilidades

**Endpoint de relación:** `/pokemon/{id}`  
**Recurso complementario:** `/ability/{id}`

Tabla propuesta: `pokemon_abilities`

| Variable | Tipo | Descripción |
|---|---|---|
| `pokemon_id` | int | Pokémon asociado |
| `ability_name` | string | Nombre de habilidad |
| `is_hidden` | bool | Indica habilidad oculta |
| `slot` | int | Posición de habilidad |

### Uso previsto

Las habilidades se conservarán inicialmente como información descriptiva.

Su incorporación al recomendador requerirá interpretar sus efectos bajo reglas de combate específicas.

No se asignará automáticamente una puntuación numérica a cada habilidad.

---

## 10. Movimientos

**Endpoint de relación:** `/pokemon/{id}`  
**Recurso complementario:** `/move/{id}`

### Tabla propuesta: `moves`

| Variable | Tipo | Nulo | Descripción |
|---|---|---|---|
| `move_name` | string | No | Nombre del movimiento |
| `move_type` | string | No | Tipo |
| `power` | int/null | Sí | Poder base |
| `accuracy` | int/null | Sí | Precisión |
| `pp` | int/null | Sí | Puntos de poder |
| `priority` | int | No | Prioridad |
| `damage_class` | string | No | Físico, especial o estado |

### Tabla propuesta: `pokemon_moves`

| Variable | Tipo | Descripción |
|---|---|---|
| `pokemon_id` | int | Pokémon |
| `move_name` | string | Movimiento |
| `version_group` | string | Grupo de versiones |
| `learn_method` | string | Método de aprendizaje |
| `level_learned_at` | int | Nivel de aprendizaje |

### Consideraciones

La lista de movimientos disponibles no equivale a un conjunto de movimientos equipados.

Para una recomendación basada en movimientos será necesario establecer un formato y restricciones de aprendizaje.

---

## 11. Evoluciones

**Endpoint:** `/evolution-chain/{id}`

### Variables candidatas

| Variable | Tipo | Descripción |
|---|---|---|
| `evolution_chain_id` | int | Identificador de cadena |
| `species_id` | int | Especie |
| `parent_species_id` | int/null | Especie anterior |
| `evolution_depth` | int | Profundidad dentro de la cadena |
| `branch_count` | int | Número de ramificaciones, según definición |

La estructura de evolución podrá utilizarse para estudiar patrones entre etapas evolutivas.

Las cadenas ramificadas requieren tratamiento específico.

---

## 12. Variables derivadas candidatas

Las siguientes variables no provienen directamente de la API.

Se construirán en Feature Engineering.

| Variable | Tipo | Definición preliminar |
|---|---|---|
| `total_stats` | int | Suma de seis estadísticas base |
| `physical_offense` | float | Indicador basado en Attack |
| `special_offense` | float | Indicador basado en Special Attack |
| `physical_bulk_proxy` | float | HP × Defense |
| `special_bulk_proxy` | float | HP × Special Defense |
| `speed_score` | float | Velocidad normalizada |
| `type_count` | int | Número de tipos |
| `weakness_count` | int | Cantidad de tipos ofensivos super efectivos |
| `resistance_count` | int | Cantidad de tipos ofensivos resistidos |
| `immunity_count` | int | Cantidad de inmunidades |
| `offensive_coverage` | float | Cobertura ofensiva según reglas definidas |
| `cluster_id` | int | Etiqueta de clustering |
| `profile_name` | string | Interpretación del cluster |

### Advertencia metodológica

Estas variables son candidatas.

Su definición final dependerá de:

- Disponibilidad de datos.
- Correlación.
- Redundancia.
- Escalado.
- Interpretabilidad.
- Utilidad para los objetivos.

---

## 13. Selección preliminar de variables por etapa

| Grupo | EDA | Clustering | Recomendación |
|---|---|---|---|
| Estadísticas base | Sí | Candidato | Sí |
| Altura y peso | Sí | Candidato | Opcional |
| Generación | Sí | Opcional | Filtro |
| Legendario/mítico | Sí | Opcional | Filtro |
| Tipos | Sí | Candidato | Sí |
| Efectividad de tipos | Sí | Opcional | Sí |
| Habilidades | Sí | Opcional | Futuro |
| Movimientos | Sí | Opcional | Futuro |
| Evoluciones | Sí | Candidato | Opcional |
| Perfiles de clustering | Resultado | Resultado | Sí |

La tabla no implica que todas las variables deban introducirse simultáneamente al clustering.

---

## 14. Reglas preliminares de calidad

### Identificadores

- `pokemon_id` debe ser único en la tabla principal.
- `species_id` debe permitir relacionar la especie.
- Las relaciones no deben contener referencias inexistentes.

### Estadísticas

- Deben ser numéricas.
- No deben contener valores negativos.
- Se verificará la presencia de las seis estadísticas esperadas.

### Tipos

- Deben corresponder a tipos reconocidos.
- No deben duplicarse dentro de una misma entrada.
- Deben conservar su posición original.

### Movimientos

- Se deben conservar las relaciones con versión y método.
- Los valores nulos permitidos deben documentarse.

### Datos faltantes

- No se imputarán automáticamente.
- Se cuantificarán por variable y entidad.
- Se distinguirá entre ausencia válida y error de extracción.

---

## 15. Esquema analítico preliminar

El dataset principal podrá contener:

```text
pokemon_id
pokemon_name
species_id
species_name
generation
is_default
hp
attack
defense
special_attack
special_defense
speed
total_stats
height_m
weight_kg
base_experience
is_legendary
is_mythical
type_count
```

Las variables de cobertura, resistencias y perfiles se incorporarán posteriormente.

El dataset deberá mantener una fila por `pokemon_id`.

---

## 16. Decisiones pendientes

Antes de cerrar esta fase deberán resolverse:

1. Qué generaciones se incluirán.
2. Qué variedades serán elegibles.
3. Qué reglas de tipos se utilizarán.
4. Qué campos son obligatorios.
5. Cómo se representarán los tipos.
6. Cómo se almacenarán los movimientos.
7. Qué características participarán en clustering.
8. Qué características utilizará el recomendador.

---

## 17. Conclusión preliminar

PokéAPI proporciona una estructura candidata para construir un dataset analítico con variables numéricas, categóricas y relacionales.

Las estadísticas base constituyen una base inicial para análisis multivariado y clustering.

Las relaciones de tipos ofrecen información útil para construir medidas de complementariedad.

Sin embargo, la selección definitiva de variables deberá realizarse después de verificar los recursos mediante consultas reales.

---

## 18. Referencias

- PokéAPI — Documentación oficial: https://pokeapi.co/docs/v2
- Pokémon: https://pokeapi.co/docs/v2#pokemon
- Pokémon Species: https://pokeapi.co/docs/v2#pokemon-species
- Types: https://pokeapi.co/docs/v2#types
- Moves: https://pokeapi.co/docs/v2#moves
