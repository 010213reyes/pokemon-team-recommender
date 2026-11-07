
# 01 — Contrato de Extracción de Datos

## Proyecto: Pokémon Team Recommender

**Fase:** 2 — Ingeniería de Datos  
**Fuente:** PokéAPI v2  
**Versión del contrato:** 1.0  
**Estado:** Propuesta para implementación

---

## 1. Objetivo

Definir las reglas técnicas para obtener, almacenar y validar información de PokéAPI, garantizando trazabilidad, consistencia e integridad durante la construcción del dataset analítico.

Este contrato establece las condiciones mínimas que deberán cumplir los scripts de extracción y procesamiento.

---

## 2. Fuente de información

### API principal

URL base:

https://pokeapi.co/api/v2/

La API proporciona información estructurada mediante recursos JSON accesibles por HTTP.

### Estrategia de consulta

Se utilizarán solicitudes GET con:

- Tiempo máximo de espera.
- Identificación del cliente mediante User-Agent.
- Manejo de errores HTTP.
- Reintentos limitados con espera progresiva.
- Registro de solicitudes fallidas.
- Paginación cuando corresponda.
- Conservación de los identificadores originales.

No se realizará extracción concurrente masiva durante la implementación inicial.

---

## 3. Recursos seleccionados

### 3.1 Pokémon

Endpoint:

`GET /pokemon/{id}`

**Identificador:** `pokemon_id`

Campos prioritarios:

| Campo | Tipo esperado | Obligatorio |
|---|---|---|
| id | entero | Sí |
| name | cadena | Sí |
| species.name | cadena | Sí |
| species.url | cadena | Sí |
| is_default | booleano | Sí |
| height | entero | Sí |
| weight | entero | Sí |
| base_experience | entero o nulo | No |
| stats | lista | Sí |
| types | lista | Sí |
| abilities | lista | Sí |
| moves | lista | No |

Las estadísticas esperadas son:

- hp
- attack
- defense
- special-attack
- special-defense
- speed

Cada estadística contiene un nombre y un valor base.

### 3.2 Pokémon Species

Endpoint:

`GET /pokemon-species/{id}`

**Identificador:** `species_id`

Campos prioritarios:

- id
- name
- generation
- is_legendary
- is_mythical
- capture_rate
- habitat
- evolution_chain
- varieties

El campo `habitat` puede ser nulo.

Las especies y las entradas Pokémon no deben considerarse equivalentes.

### 3.3 Type

Endpoint:

`GET /type/{id}`

Campos prioritarios:

- id
- name
- damage_relations

Relaciones necesarias:

- double_damage_to
- half_damage_to
- no_damage_to
- double_damage_from
- half_damage_from
- no_damage_from

Estas relaciones permitirán construir una matriz de efectividad.

El formato o conjunto de reglas utilizado deberá documentarse antes de calcular complementariedad competitiva.

### 3.4 Ability

Endpoint:

`GET /ability/{id}`

Campos prioritarios:

- id
- name
- generation
- is_main_series

Las habilidades asociadas a cada Pokémon se identificarán desde el recurso Pokémon.

### 3.5 Move

Endpoint:

`GET /move/{id}`

Campos prioritarios:

- id
- name
- type
- damage_class
- power
- accuracy
- pp
- priority
- generation

Algunos campos pueden ser nulos dependiendo del movimiento.

### 3.6 Evolution Chain

Endpoint:

`GET /evolution-chain/{id}`

Campos prioritarios:

- id
- chain

La estructura evolutiva es jerárquica y puede contener múltiples ramas.

Su transformación deberá preservar las relaciones entre especies.

---

## 4. Unidad de extracción y análisis

### Unidad de extracción

Cada respuesta corresponde a un recurso individual identificado por su endpoint y su ID.

### Unidad analítica principal

`pokemon_id`

### Identificador complementario

`species_id`

La relación entre Pokémon y especie será explícita.

### Variedades

Las variedades alternativas no se eliminarán automáticamente.

Se conservará el indicador `is_default`.

La decisión sobre cuáles variedades participarán en el clustering se tomará durante la construcción del dataset analítico.

---

## 5. Alcance inicial

La primera implementación utilizará un subconjunto controlado de identificadores para validar el funcionamiento del pipeline.

La extracción completa se realizará únicamente después de comprobar:

1. Conectividad.
2. Manejo de errores.
3. Persistencia RAW.
4. Transformación correcta.
5. Integridad de relaciones.
6. Ausencia de duplicaciones accidentales.

El número definitivo de recursos y generaciones será configurable.

No se utilizará una cantidad fija de Pokémon sin justificar el criterio de selección.

---

## 6. Formato RAW

Directorio:

`data/raw/`

Estructura propuesta:

```text
data/raw/
├── pokemon/
├── pokemon-species/
├── type/
├── ability/
├── move/
└── evolution-chain/
```

Cada recurso se guardará como JSON.

Convención de nombres:

`{id}.json`

Ejemplo:

`data/raw/pokemon/25.json`

El contenido JSON original no deberá modificarse durante el procesamiento.

La fecha de extracción, URL, resultado HTTP y otros metadatos se registrarán por separado.

---

## 7. Formato PROCESSED

Directorio:

`data/processed/`

Tablas previstas:

| Tabla | Clave principal |
|---|---|
| pokemon | pokemon_id |
| pokemon_stats | pokemon_id + stat_name |
| pokemon_types | pokemon_id + type_id |
| pokemon_abilities | pokemon_id + ability_id |
| pokemon_moves | pokemon_id + move_id |
| species | species_id |
| type_effectiveness | attacking_type_id + defending_type_id + ruleset |
| moves | move_id |
| abilities | ability_id |
| evolution_relations | species_id + evolved_species_id + relation_id |

La clave `relation_id` será una clave técnica para distinguir relaciones evolutivas cuando sea necesario.

Las tablas relacionales deberán conservar las asociaciones múltiples sin generar duplicaciones accidentales.

Los datos procesados se almacenarán inicialmente en CSV o Parquet, según las necesidades de la siguiente etapa.

---

## 8. Validaciones de calidad

### 8.1 Identificadores

- `pokemon_id` no debe ser nulo.
- `species_id` no debe ser nulo en la tabla de especies.
- Los identificadores deben tener tipos válidos.
- Las claves primarias deben ser únicas.

### 8.2 Estadísticas

Cada entrada Pokémon deberá contener las seis estadísticas esperadas para considerarse completa.

Los valores deben ser numéricos y no negativos.

### 8.3 Tipos

Cada Pokémon deberá tener al menos un tipo.

No deberán repetirse asociaciones idénticas entre Pokémon y tipo.

### 8.4 Relaciones

Las referencias entre tablas deberán corresponder a identificadores válidos.

Las relaciones faltantes se registrarán como incidencias.

### 8.5 Valores faltantes

Se distinguirá entre:

- Campos obligatorios faltantes.
- Campos opcionales nulos.
- Recursos no recuperados.
- Relaciones incompletas.

No se imputarán automáticamente valores durante la extracción.

---

## 9. Manejo de errores

El cliente HTTP deberá contemplar:

| Situación | Acción |
|---|---|
| HTTP 200 | Procesar respuesta |
| HTTP 404 | Registrar recurso inexistente |
| HTTP 429 | Respetar espera y reintentar de forma limitada |
| HTTP 500–599 | Reintentar con espera progresiva |
| Timeout | Reintentar de forma limitada |
| JSON inválido | Registrar error y no guardar como recurso válido |

Los reintentos deberán tener un máximo configurable.

Los errores persistentes no deberán interrumpir innecesariamente toda la extracción, pero sí quedar documentados.

---

## 10. Trazabilidad

Cada ejecución deberá registrar:

- Identificador de ejecución.
- Fecha y hora de inicio.
- Fecha y hora de finalización.
- Endpoint consultado.
- Identificador solicitado.
- Estado HTTP.
- Resultado de la extracción.
- Ruta del archivo guardado.
- Mensaje de error, si corresponde.

Los registros de ejecución se almacenarán en `ingenieria/resultados/`.

No se incluirán credenciales ni datos sensibles en los logs.

---

## 11. Reproducibilidad

Los scripts deberán permitir:

- Configurar el rango o lista de identificadores.
- Ejecutar una muestra pequeña.
- Reanudar una extracción cuando sea posible.
- Evitar descargas repetidas innecesarias.
- Separar extracción de transformación.
- Ejecutar validaciones independientemente.
- Registrar la versión de dependencias.

La información de PokéAPI puede cambiar con el tiempo.

Por ello, cada extracción deberá quedar asociada con su fecha y parámetros de ejecución.

---

## 12. Criterios de aceptación

El contrato se considerará implementado cuando:

1. El cliente HTTP consulte correctamente los recursos seleccionados.
2. Las respuestas válidas se almacenen en RAW.
3. Los errores queden registrados.
4. Los identificadores originales se conserven.
5. Los datos procesados respeten el modelo definido.
6. Las validaciones detecten inconsistencias.
7. El pipeline pueda ejecutarse nuevamente sin alterar innecesariamente los datos originales.
8. Se genere evidencia de ejecución.

---

## 13. Decisiones pendientes

Antes de una extracción completa se definirán:

- Generaciones incluidas.
- Tratamiento de variedades alternativas.
- Inclusión de legendarios y míticos.
- Versión o conjunto de reglas de tipos.
- Alcance de movimientos y habilidades.
- Formato definitivo de almacenamiento procesado.

---

## 14. Referencias

- PokéAPI: https://pokeapi.co/
- Documentación oficial: https://pokeapi.co/docs/v2
- Requests: https://requests.readthedocs.io/
- Pandas: https://pandas.pydata.org/docs/
