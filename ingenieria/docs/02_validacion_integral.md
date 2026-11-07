# Validación integral del pipeline de Ingeniería de Datos

## 1. Objetivo

Verificar la integridad estructural, referencial y lógica de los datos obtenidos de PokéAPI, garantizando que las tablas procesadas sean consistentes y puedan utilizarse en las siguientes fases del proyecto Pokémon Team Recommender.

## 2. Alcance

La validación corresponde al conjunto experimental de los primeros 151 Pokémon y sus respectivas especies.

Se utilizaron los 18 tipos principales del sistema moderno de Pokémon para construir una matriz de efectividad ofensiva y calcular perfiles defensivos individuales.

El conjunto de datos no representa el catálogo completo de PokéAPI ni las reglas competitivas originales de la primera generación.

## 3. Arquitectura validada

El pipeline implementado sigue las etapas:

1. Extracción desde PokéAPI.
2. Almacenamiento RAW en archivos JSON.
3. Transformación y normalización mediante pandas.
4. Generación de tablas CSV en `data/processed/`.
5. Cálculo de efectividad de tipos.
6. Construcción de perfiles defensivos.
7. Validación integral de consistencia.

## 4. Tablas procesadas

| Tabla | Descripción |
|---|---|
| pokemon | Identificación y atributos básicos |
| pokemon_stats | Seis estadísticas base por Pokémon |
| pokemon_types | Asociaciones entre Pokémon y tipos |
| pokemon_abilities | Asociaciones entre Pokémon y habilidades |
| species | Información de especies |
| pokemon_varieties | Relaciones entre especies y variedades |
| types | Catálogo de 18 tipos principales |
| type_effectiveness | Matriz de efectividad ofensiva |
| pokemon_defensive_profile | Multiplicadores defensivos individuales |

## 5. Resultados de validación

La ejecución de `validate_pipeline.py` produjo los siguientes resultados:

- Validaciones ejecutadas: **40**
- Validaciones correctas: **40**
- Validaciones fallidas: **0**
- Estado general: **PASS**

Se verificaron los siguientes conteos principales:

| Componente | Registros |
|---|---:|
| Pokémon | 151 |
| Especies | 151 |
| Estadísticas base | 906 |
| Tipos principales | 18 |
| Relaciones de efectividad | 324 |
| Perfiles defensivos | 2,718 |

## 6. Integridad y consistencia

Se verificaron:

- Existencia y estructura de nueve tablas.
- Unicidad de identificadores principales.
- Relaciones entre Pokémon, especies, estadísticas, tipos y habilidades.
- Existencia de seis estadísticas distintas por Pokémon.
- Ausencia de asociaciones duplicadas en los controles implementados.
- Cobertura completa de la matriz de tipos.
- Validez de multiplicadores.
- Consistencia del conjunto de reglas utilizado.
- Reconstrucción de perfiles defensivos desde los tipos originales.

Como prueba funcional se utilizó Charizard, cuyo perfil mostró:

| Ataque recibido | Multiplicador |
|---|---:|
| Roca | 4.0 |
| Agua | 2.0 |
| Planta | 0.25 |
| Tierra | 0.0 |

## 7. Limitaciones

La validación confirma el cumplimiento de los controles implementados, pero no demuestra que todos los valores de origen sean correctos ni que el sistema esté listo para uso competitivo.

Los perfiles defensivos no consideran habilidades, objetos, movimientos, clima ni otras condiciones de combate.

Las relaciones de efectividad corresponden al conjunto de reglas identificado como `pokeapi_current`, no a las reglas históricas de la primera generación.

La evaluación del recomendador, el análisis estadístico y la selección de modelos quedan fuera de esta fase.

## 8. Reproducibilidad

Para ejecutar la validación desde la raíz del repositorio:

```powershell
python ingenieria/scripts/validate_pipeline.py
```

El programa genera:

`ingenieria/resultados/validacion_pipeline.json`

El código fuente se encuentra versionado en la rama `feature/ingenieria-datos`.

Commit de referencia: `ed359fa`.

## 9. Conclusión

El conjunto experimental superó las 40 verificaciones de integridad implementadas, sin errores detectados.

Los datos procesados cuentan con una estructura consistente para continuar con la revisión de calidad, limpieza, análisis exploratorio e ingeniería de características.

La validación se considera satisfactoria dentro del alcance experimental definido.