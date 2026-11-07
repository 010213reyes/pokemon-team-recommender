
# Fase 2 — Ingeniería de Datos

## Proyecto: Pokémon Team Recommender

**Fuente principal:** PokéAPI v2  
**Fase anterior:** Minería de Datosñ

## 1. Objetivo

Diseñar e implementar un pipeline reproducible para extraer, almacenar, validar y transformar información de Pokémon desde PokéAPI.

El resultado será un conjunto de datos estructurado que permita realizar análisis exploratorio, ingeniería de características, clustering y recomendación de equipos.

## 2. Arquitectura del pipeline

El flujo de procesamiento será:

PokéAPI → RAW → Validación → PROCESSED → Dataset analítico

### Extracción

- Consultar los endpoints necesarios.
- Implementar paginación.
- Controlar errores HTTP.
- Registrar la procedencia de los datos.
- Evitar solicitudes innecesarias.

### RAW

Guardar respuestas originales en formato JSON.

Directorio: `data/raw/`

Los archivos originales no deben modificarse durante las transformaciones.

### Validación

Comprobar:

- Identificadores únicos.
- Campos obligatorios.
- Estructura de estadísticas.
- Relaciones entre entidades.
- Valores faltantes.
- Registros duplicados.

### PROCESSED

Transformar las respuestas JSON en tablas estructuradas.

Directorio: `data/processed/`

Las tablas permitirán trabajar con Pokémon, estadísticas, tipos, habilidades y otras entidades relacionadas.

## 3. Estructura de trabajo

La implementación de esta fase se organizará en:

- `ingenieria/docs/`: documentación técnica.
- `ingenieria/notebooks/`: exploración y validaciones.
- `ingenieria/scripts/`: programas de extracción y transformación.
- `ingenieria/resultados/`: reportes de ejecución.

Se reutilizarán los directorios globales `data/raw/` y `data/processed/`.

## 4. Actividades

1. Definir el contrato de extracción.
2. Implementar un cliente HTTP para PokéAPI.
3. Implementar paginación y manejo de errores.
4. Extraer los recursos seleccionados.
5. Guardar las respuestas originales.
6. Transformar los datos en tablas.
7. Aplicar controles de calidad.
8. Construir un dataset analítico.
9. Documentar resultados y limitaciones.

## 5. Criterios de aceptación

La fase se considerará terminada cuando:

- Las extracciones puedan reproducirse.
- Los datos RAW conserven su estructura original.
- Los registros procesados tengan identificadores consistentes.
- Las relaciones multivaluadas no produzcan duplicaciones accidentales.
- Se genere un reporte de calidad.
- El dataset analítico esté documentado.
- Los scripts y notebooks estén versionados en GitHub.

## 6. Alcance y limitaciones

La ingeniería de datos no incluirá entrenamiento de modelos.

El clustering y el recomendador se desarrollarán en fases posteriores.

La cantidad de Pokémon, las generaciones y el tratamiento de variedades se definirán explícitamente antes de realizar una extracción completa.

## 7. Referencias

- PokéAPI: https://pokeapi.co/
- Documentación oficial: https://pokeapi.co/docs/v2
- Documentación de Requests: https://requests.readthedocs.io/
- Documentación de Pandas: https://pandas.pydata.org/docs/
