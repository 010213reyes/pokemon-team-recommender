# Validación Final de Datos CLEAN

**Proyecto:** Pokémon Team Recommender  
**Fase:** 3 — Análisis de Datos  
**Estado:** Validación CLEAN completada

## 1. Objetivo

Verificar que los datos almacenados en `data/clean/` conservan su integridad y cumplen los criterios de calidad definidos durante el diagnóstico inicial.

## 2. Metodología

Se desarrollaron dos scripts reproducibles:

- `build_clean_dataset.py`: valida los archivos procesados, genera las tablas CLEAN y compara sus hashes SHA-256.
- `validate_clean.py`: comprueba la existencia de archivos, conservación de registros, ausencia de nulos y duplicados exactos, y determinadas restricciones de integridad.

La validación se realizó mediante Python y pandas.

## 3. Resultados

Se generaron nueve tablas CLEAN con un total de 5,119 registros distribuidos entre entidades y relaciones.

| Tabla | Registros |
|---|---:|
| pokemon | 151 |
| pokemon_stats | 906 |
| pokemon_types | 218 |
| pokemon_abilities | 395 |
| species | 151 |
| pokemon_varieties | 238 |
| types | 18 |
| type_effectiveness | 324 |
| pokemon_defensive_profile | 2,718 |
| **Total** | **5,119** |

Se ejecutaron **53 verificaciones automatizadas**, con los siguientes resultados:

- 53 PASS.
- 0 FAIL.
- Nueve comparaciones SHA-256 satisfactorias.
- Sin valores faltantes.
- Sin duplicados exactos.
- Conservación de los registros originales.
- Validaciones básicas de identificadores, relaciones y multiplicadores satisfactorias.

El reporte `validacion_clean.json` se generó correctamente y su sintaxis JSON fue verificada.

## 4. Tratamiento de valores atípicos

El diagnóstico exploratorio identificó seis estadísticas atípicas mediante IQR, correspondientes a Cloyster, Onix, Chansey, Snorlax, Wigglytuff y Mewtwo.

Se decidió conservar estos valores por ser coherentes con las características conocidas de los Pokémon.

No se realizaron imputaciones, eliminaciones ni modificaciones de estadísticas.

## 5. Limitaciones

CLEAN corresponde a una copia validada de PROCESSED, sin transformaciones correctivas.

Las 53 comprobaciones verifican las condiciones implementadas, pero no constituyen una auditoría exhaustiva de todas las restricciones posibles.

Las transformaciones de escalado, selección de características y reducción de dimensionalidad se realizarán posteriormente, durante Ciencia de Datos.

## 6. Conclusión

La preparación de datos CLEAN finalizó satisfactoriamente.

Las nueve tablas conservaron su contenido y superaron las 53 comprobaciones automatizadas.

Los datos están disponibles para continuar con el análisis exploratorio y la evaluación de características relevantes para el recomendador.