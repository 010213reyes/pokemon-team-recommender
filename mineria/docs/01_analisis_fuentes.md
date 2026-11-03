
# 01 — Análisis de Fuentes de Datos

## Proyecto: Pokémon Team Recommender

### 1. Objetivo

Identificar y evaluar las fuentes de información disponibles para el proyecto Pokémon Team Recommender, con énfasis en la estructura de PokéAPI, sus recursos, relaciones y utilidad para las etapas posteriores de ingeniería de datos, análisis exploratorio, Machine Learning y recomendación de equipos.

---

## 2. Fuente principal: PokéAPI

PokéAPI es una API REST pública que proporciona datos estructurados relacionados con el universo Pokémon.

**Características generales:**

| Característica | Descripción |
|---|---|
| Nombre | PokéAPI |
| Tipo | API REST |
| Formato | JSON |
| URL base | https://pokeapi.co/api/v2/ |
| Documentación | https://pokeapi.co/docs/v2 |
| Autenticación | No requerida |
| Método principal | HTTP GET |
| Tipo de información | Descriptiva y mecánicas de Pokémon |
| Actualización | Dependiente del mantenimiento de la fuente |

PokéAPI será considerada la fuente primaria del proyecto.

No se utilizarán inicialmente datos históricos de combates, por lo que las recomendaciones se basarán en características estadísticas y estructurales.

---

## 3. Recursos relevantes

### 3.1 Pokémon

**Endpoint:**

`GET /pokemon/{id}`

Contiene información asociada a una entrada Pokémon.

Variables principales:

- Identificador.
- Nombre.
- Altura.
- Peso.
- Experiencia base.
- Estadísticas.
- Tipos.
- Habilidades.
- Movimientos.
- Especie asociada.
- Indicador de variedad predeterminada.

**Utilidad:**

Será uno de los recursos centrales para construir el dataset analítico.

Las estadísticas base permitirán estudiar perfiles ofensivos, defensivos y de velocidad.

---

### 3.2 Pokémon Species

**Endpoint:**

`GET /pokemon-species/{id}`

Proporciona información asociada a una especie.

Variables relevantes:

- Identificador de especie.
- Nombre.
- Generación.
- Clasificación legendaria.
- Clasificación mítica.
- Tasa de captura.
- Hábitat.
- Cadena evolutiva.
- Variedades relacionadas.

**Utilidad:**

Permitirá complementar la información estadística con atributos de clasificación y evolución.

**Consideración:**

Una especie puede relacionarse con varias entradas Pokémon. Por ello, `species_id` y `pokemon_id` no deben tratarse como identificadores equivalentes.

---

### 3.3 Pokémon Form

**Endpoint:**

`GET /pokemon-form/{id}`

Contiene información relacionada con formas de Pokémon.

**Utilidad:**

Permitirá estudiar si las diferencias entre formas son relevantes para la selección de entidades.

**Consideración:**

Las formas, las variedades y las especies representan conceptos diferentes. Su integración deberá definirse explícitamente.

---

### 3.4 Type

**Endpoint:**

`GET /type/{id}`

Contiene información sobre tipos y relaciones de efectividad.

Relaciones relevantes:

- `double_damage_to`
- `half_damage_to`
- `no_damage_to`
- `double_damage_from`
- `half_damage_from`
- `no_damage_from`

**Utilidad:**

Será fundamental para construir variables relacionadas con:

- Cobertura ofensiva.
- Debilidades defensivas.
- Resistencias.
- Inmunidades.
- Redundancia de tipos.

La efectividad de tipos deberá calcularse mediante reglas consistentes con la generación o formato seleccionado.

---

### 3.5 Ability

**Endpoint:**

`GET /ability/{id}`

Contiene información sobre habilidades.

**Utilidad:**

Permitirá identificar habilidades disponibles y estudiar su posible incorporación a futuras versiones del recomendador.

**Limitación:**

La presencia de una habilidad no significa que sus efectos puedan representarse correctamente mediante una única variable numérica.

---

### 3.6 Move

**Endpoint:**

`GET /move/{id}`

Contiene información sobre movimientos.

Variables relevantes:

- Nombre.
- Tipo.
- Poder.
- Precisión.
- Puntos de poder.
- Clase de daño.
- Prioridad.
- Efectos.
- Generación.

**Utilidad:**

Podrá utilizarse para analizar cobertura ofensiva y diversidad de movimientos.

**Consideración:**

Los movimientos que puede aprender un Pokémon dependen de condiciones como versión, método de aprendizaje y otras restricciones del juego.

No se asumirá que todos los movimientos asociados a una entrada Pokémon pueden utilizarse simultáneamente.

---

### 3.7 Evolution Chain

**Endpoint:**

`GET /evolution-chain/{id}`

Contiene la estructura de las cadenas evolutivas.

**Utilidad:**

Permitirá identificar:

- Relaciones evolutivas.
- Evoluciones ramificadas.
- Etapas evolutivas.
- Posibles características derivadas.

---

### 3.8 Generation

**Endpoint:**

`GET /generation/{id}`

Proporciona información relacionada con generaciones Pokémon.

**Utilidad:**

Permitirá clasificar especies según su generación de introducción y definir filtros de alcance.

La generación de introducción no debe confundirse con la generación cuyas reglas de combate se están utilizando.

---

## 4. Tabla de selección de recursos

| Recurso | Prioridad | Uso principal |
|---|---|---|
| Pokémon | Alta | Estadísticas y atributos de combate |
| Pokémon Species | Alta | Clasificación y relaciones |
| Type | Alta | Efectividad y complementariedad |
| Pokémon Form | Media | Tratamiento de formas |
| Ability | Media | Caracterización adicional |
| Move | Media | Cobertura y movimientos |
| Evolution Chain | Media | Estructura evolutiva |
| Generation | Media | Clasificación temporal |

La prioridad corresponde a una evaluación preliminar, no a una decisión definitiva de extracción.

---

## 5. Relaciones entre recursos

El modelo conceptual inicial considera las siguientes relaciones:

```text
Pokémon Species
       |
       | Una especie puede tener
       | varias entradas Pokémon
       v
     Pokémon
       |
       +---- Estadísticas
       |
       +---- Tipos
       |
       +---- Habilidades
       |
       +---- Movimientos
       |
       +---- Formas

Pokémon Species
       |
       +---- Generación
       |
       +---- Cadena evolutiva

Type
       |
       +---- Relaciones de efectividad
```

Estas relaciones deberán comprobarse durante la exploración de la API.

---

## 6. Unidad de análisis preliminar

Se propone utilizar una entrada del recurso Pokémon como unidad de análisis, identificada mediante `pokemon_id`.

Esta decisión permitirá estudiar variedades con estadísticas o tipos diferentes sin asumir que cada especie tiene una única configuración de combate.

La unidad de análisis deberá mantenerse consistente en las fases de ingeniería de datos y Machine Learning.

**Decisión pendiente:**

Determinar si se incluirán todas las variedades disponibles o únicamente las variedades predeterminadas.

---

## 7. Variables candidatas

### 7.1 Estadísticas base

- HP.
- Attack.
- Defense.
- Special Attack.
- Special Defense.
- Speed.

### 7.2 Características físicas

- Altura.
- Peso.
- Experiencia base.

### 7.3 Clasificación

- Especie.
- Generación.
- Legendario.
- Mítico.
- Cadena evolutiva.

### 7.4 Mecánicas de combate

- Tipos.
- Habilidades.
- Movimientos.
- Efectividad de tipos.

### 7.5 Variables derivadas propuestas

- Total de estadísticas base.
- Perfil ofensivo.
- Perfil defensivo.
- Velocidad relativa.
- Número de debilidades.
- Número de resistencias.
- Número de inmunidades.
- Cobertura ofensiva.
- Diversidad de tipos.

Estas variables derivadas se implementarán y validarán en la fase de Feature Engineering.

---

## 8. Evaluación preliminar de viabilidad

### Data Engineering

PokéAPI proporciona recursos estructurados que pueden consultarse mediante solicitudes HTTP y transformarse a un modelo tabular.

**Viabilidad preliminar:** favorable.

### Data Analysis

Las estadísticas y atributos permiten formular preguntas descriptivas, estudiar distribuciones y analizar relaciones.

**Viabilidad preliminar:** favorable.

### Clustering

Las estadísticas numéricas ofrecen una base para construir representaciones multivariadas y experimentar con algoritmos de agrupamiento.

**Viabilidad preliminar:** favorable, condicionada al preprocesamiento y a la evaluación de resultados.

### Recomendación

Los tipos y estadísticas permiten diseñar medidas de complementariedad.

Sin embargo, la evaluación de rendimiento competitivo requiere información adicional.

**Viabilidad preliminar:** favorable para recomendación estructural; no demostrada para predicción de victorias.

---

## 9. Riesgos identificados

1. Confundir especies, variedades y formas.
2. Generar duplicados durante la integración.
3. Mezclar mecánicas de generaciones diferentes.
4. Interpretar estadísticas base como rendimiento real.
5. Utilizar movimientos sin considerar restricciones.
6. Introducir sesgos mediante la selección de Pokémon.
7. Evaluar el recomendador únicamente con su propia función objetivo.

---

## 10. Decisiones pendientes

Antes de implementar la extracción completa deberán definirse:

- Alcance de generaciones.
- Generación o formato de referencia para las reglas.
- Tratamiento de variedades.
- Inclusión de legendarios y míticos.
- Recursos obligatorios y opcionales.
- Granularidad del dataset.
- Reglas de calidad.
- Política de manejo de campos faltantes.

---

## 11. Conclusión preliminar

PokéAPI constituye una fuente candidata adecuada para el desarrollo de Pokémon Team Recommender.

Su estructura permite plantear un proceso de adquisición e integración de datos, así como el análisis de características estadísticas y estructurales.

La disponibilidad de estadísticas y relaciones de tipos permite justificar la experimentación con clustering y el diseño de un recomendador de complementariedad.

No obstante, estas posibilidades deberán verificarse mediante consultas reales antes de cerrar la fase.

---

## 12. Referencias

1. PokéAPI. Documentación oficial de la API v2.  
   https://pokeapi.co/docs/v2

2. PokéAPI. Recurso Pokémon.  
   https://pokeapi.co/docs/v2#pokemon

3. PokéAPI. Recurso Pokémon Species.  
   https://pokeapi.co/docs/v2#pokemon-species

4. PokéAPI. Recurso Type.  
   https://pokeapi.co/docs/v2#types

5. PokéAPI. Recurso Move.  
   https://pokeapi.co/docs/v2#moves
