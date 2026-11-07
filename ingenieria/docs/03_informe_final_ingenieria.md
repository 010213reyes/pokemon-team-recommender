# Informe final — Fase 2: Ingeniería de Datos

**Proyecto:** Pokémon Team Recommender  
**Versión:** Prototipo experimental  
**Fuente principal:** PokéAPI  
**Alcance:** Primeros 151 Pokémon y sus especies  
**Estado:** Pipeline implementado y validado

## 1. Introducción

La Fase 2 del proyecto Pokémon Team Recommender tuvo como propósito desarrollar un pipeline reproducible para extraer, transformar, normalizar y validar información de Pokémon.

El conjunto de datos procesado servirá como base para las etapas posteriores de limpieza, análisis exploratorio, ingeniería de características, clustering y recomendación de equipos de tres Pokémon.

## 2. Objetivo

Implementar un proceso de ingeniería de datos capaz de obtener información estructurada desde PokéAPI y convertirla en tablas relacionadas, verificando su integridad y consistencia.

## 3. Arquitectura del pipeline

El proceso implementado sigue la arquitectura:

**PokéAPI → RAW → PROCESSED → Validación**

### Extracción

Los recursos de PokéAPI se descargan mediante un cliente HTTP reutilizable que incorpora manejo de errores, reintentos y tiempos de espera.

Se implementaron extractores para:

- Pokémon.
- Especies.
- Tipos.

Los archivos originales se conservan en formato JSON dentro de `data/raw/`.

### Transformación

Los archivos RAW se convierten en tablas CSV mediante pandas.

La normalización separa entidades y relaciones, evitando almacenar estadísticas, habilidades y tipos como estructuras anidadas dentro de una única tabla.

### Validación

Se implementaron controles para comprobar la estructura de las tablas, la unicidad de identificadores, las relaciones referenciales y la consistencia de los cálculos derivados.

## 4. Estructura de datos

El pipeline genera nueve tablas:

| Tabla | Función |
|---|---|
| pokemon | Atributos básicos de Pokémon |
| pokemon_stats | Estadísticas base |
| pokemon_types | Tipos asociados |
| pokemon_abilities | Habilidades asociadas |
| species | Información de especies |
| pokemon_varieties | Relaciones entre especies y variedades |
| types | Catálogo de tipos |
| type_effectiveness | Efectividad entre tipos |
| pokemon_defensive_profile | Perfil defensivo por Pokémon |

Las relaciones se mantienen mediante identificadores de Pokémon, especies y tipos.

## 5. Construcción de la matriz de efectividad

Se utilizaron los 18 tipos principales para construir una matriz de 324 combinaciones ofensivas y defensivas.

Los multiplicadores posibles son:

- 0: inmunidad.
- 0.5: resistencia.
- 1: efectividad neutral.
- 2: supereficacia.

La matriz utiliza las relaciones disponibles en los recursos de tipos descargados desde PokéAPI.

## 6. Construcción de perfiles defensivos

Para cada Pokémon se calculó su respuesta defensiva frente a los 18 tipos de ataque.

Cuando un Pokémon posee dos tipos, sus multiplicadores se combinan mediante multiplicación.

El proceso produjo 2,718 relaciones defensivas.

### Distribución obtenida

| Multiplicador | Registros |
|---|---:|
| 0 | 68 |
| 0.25 | 64 |
| 0.5 | 517 |
| 1 | 1,605 |
| 2 | 433 |
| 4 | 31 |
| **Total** | **2,718** |

Estos resultados describen las interacciones de tipos del conjunto experimental, sin considerar habilidades, objetos ni otras mecánicas de combate.

## 7. Resultados de calidad

Se implementaron dos niveles de validación:

**Validación de tablas procesadas:** 20 verificaciones correctas de 20 ejecutadas.

**Validación integral del pipeline:** 40 verificaciones correctas de 40 ejecutadas.

La validación integral incluyó:

- Comprobación de esquemas.
- Verificación de claves y relaciones.
- Control de estadísticas y asociaciones.
- Cobertura completa de la matriz de efectividad.
- Verificación de perfiles defensivos.
- Reconstrucción de multiplicadores desde las relaciones originales.
- Prueba funcional con Charizard.

No se detectaron fallos en los controles implementados.

## 8. Reproducibilidad

Los principales scripts se encuentran en `ingenieria/scripts/`.

| Script | Responsabilidad |
|---|---|
| pokeapi_client.py | Cliente HTTP |
| extract_pokemon.py | Extracción de Pokémon |
| extract_species.py | Extracción de especies |
| extract_types.py | Extracción de tipos |
| transform_pokemon.py | Normalización de entidades |
| transform_types.py | Matriz de efectividad |
| build_defensive_profile.py | Perfiles defensivos |
| validate_processed.py | Validación de tablas |
| validate_pipeline.py | Validación integral |

Para reconstruir el conjunto experimental desde la raíz del repositorio:

```powershell
python ingenieria/scripts/extract_pokemon.py --start 1 --end 151
python ingenieria/scripts/extract_species.py --start 1 --end 151
python ingenieria/scripts/extract_types.py

python ingenieria/scripts/transform_pokemon.py
python ingenieria/scripts/transform_types.py
python ingenieria/scripts/build_defensive_profile.py

python ingenieria/scripts/validate_processed.py
python ingenieria/scripts/validate_pipeline.py
```

Los extractores permiten reutilizar archivos descargados previamente. Las transformaciones generan nuevamente las tablas procesadas a partir de los archivos RAW.

## 9. Limitaciones

El alcance actual comprende los primeros 151 Pokémon, no el catálogo completo.

Las relaciones de tipos corresponden al conjunto actual utilizado por PokéAPI, identificado en el proyecto como `pokeapi_current`.

No se representan las reglas históricas originales de la primera generación.

Las variedades identificadas en los recursos de especies no necesariamente cuentan con todos sus datos individuales descargados.

El pipeline todavía no incorpora información completa de movimientos, objetos, condiciones de combate ni mecanismos competitivos.

Las verificaciones realizadas no sustituyen una evaluación posterior de calidad semántica, cobertura, sesgos o utilidad predictiva.

## 10. Relación con las siguientes fases

Los resultados de Ingeniería de Datos permiten continuar con:

**Fase 3 — Limpieza de Datos:** evaluación de valores faltantes, rangos, consistencia, duplicados y tratamiento de atributos.

**Fase 4 — Análisis Exploratorio:** distribución de estadísticas, tipos, habilidades y relaciones entre variables.

**Fase 5 — Ingeniería de Características:** creación de variables numéricas y categóricas para representar perfiles Pokémon.

**Fase 6 — Modelado:** reducción de dimensionalidad, clustering y evaluación de agrupaciones.

**Fase 7 — Recomendación:** selección de equipos de tres Pokémon considerando complementariedad estadística y cobertura de tipos.

La numeración de estas etapas deberá mantenerse consistente con el plan general del repositorio.

## 11. Conclusión

La Fase 2 permitió construir un pipeline reproducible para la obtención, normalización y validación de datos de Pokémon.

Se procesaron 151 Pokémon y sus especies, se construyó una matriz de efectividad de 324 relaciones y se generaron 2,718 perfiles defensivos.

Los 40 controles de validación integral se completaron correctamente.

Por tanto, el pipeline cumple los criterios técnicos implementados para este primer ciclo experimental y proporciona una base estructurada para continuar con la limpieza y el análisis de datos.