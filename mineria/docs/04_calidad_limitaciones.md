
# 04 — Calidad y Limitaciones de los Datos

## Proyecto: Pokémon Team Recommender

**Fase:** Minería de Datos  
**Estado:** Evaluación preliminar  
**Fuente principal:** PokéAPI v2  
**Documentación:** https://pokeapi.co/docs/v2

---

## 1. Objetivo

Identificar los riesgos de calidad, integridad, consistencia y representatividad de los datos disponibles en PokéAPI.

Definir criterios de validación que permitan construir posteriormente un dataset confiable para análisis exploratorio, reducción dimensional, clustering y recomendación de equipos Pokémon.

Este documento describe controles propuestos. Los resultados reales de calidad se obtendrán durante la exploración y la ingeniería de datos.

---

## 2. Dimensiones de calidad

La evaluación considerará seis dimensiones principales.

| Dimensión | Definición | Control propuesto |
|---|---|---|
| Completitud | Presencia de datos esperados | Porcentaje de nulos |
| Unicidad | Ausencia de duplicados indebidos | Verificación de identificadores |
| Consistencia | Coherencia entre entidades | Comparación de relaciones |
| Validez | Cumplimiento de tipos y rangos | Reglas por variable |
| Integridad referencial | Existencia de referencias relacionadas | Validación de claves |
| Trazabilidad | Identificación del origen de los datos | Registro de endpoints y extracción |

La calidad no se evaluará únicamente mediante la ausencia de valores nulos.

---

## 3. Completitud

La completitud representa la proporción de valores disponibles respecto a los esperados.

### Fórmula

\[
Completitud = \frac{Valores\ no\ nulos}{Valores\ esperados}\times100
\]

### Variables críticas

- `pokemon_id`
- `pokemon_name`
- `species_id`
- `hp`
- `attack`
- `defense`
- `special_attack`
- `special_defense`
- `speed`
- `types`

### Variables opcionales

- `base_experience`
- `habitat`
- `base_happiness`
- `power`
- `accuracy`
- `evolution_chain_id`

Los valores nulos de variables opcionales no se considerarán automáticamente errores.

### Criterios preliminares

- Los identificadores principales deberán estar presentes.
- Las estadísticas necesarias para clustering deberán verificarse individualmente.
- Se documentará la proporción de valores faltantes por variable.
- No se realizará imputación sin justificación metodológica.

---

## 4. Unicidad

El dataset analítico tendrá como unidad de análisis una entrada Pokémon identificada por `pokemon_id`.

### Reglas

1. `pokemon_id` debe ser único en la tabla principal.
2. `species_id` debe ser único en la tabla de especies.
3. Las tablas relacionales deben respetar sus claves compuestas.
4. Las uniones no deben multiplicar accidentalmente las observaciones.

### Riesgo identificado

Un Pokémon puede tener varios tipos, habilidades y movimientos.

Si estas relaciones se unen directamente, pueden generarse múltiples filas para un mismo Pokémon.

### Control

Verificar la cantidad de identificadores únicos antes y después de cada integración.

---

## 5. Consistencia

La consistencia evalúa si la información mantiene coherencia entre diferentes recursos.

### Validaciones propuestas

- El identificador de especie de Pokémon debe corresponder a una especie existente.
- Los nombres de tipos deben corresponder al catálogo seleccionado.
- Los movimientos deben conservar sus identificadores.
- Las estadísticas deben asociarse al Pokémon correcto.
- Las variedades deben relacionarse con su especie correspondiente.

### Consideración especial

Las formas y variedades pueden representar configuraciones diferentes.

No deben eliminarse automáticamente por compartir especie.

---

## 6. Validez

La validez evalúa si los valores cumplen restricciones esperadas.

### Reglas preliminares

| Variable | Regla |
|---|---|
| `pokemon_id` | Entero positivo |
| `species_id` | Entero positivo |
| Estadísticas base | Enteros no negativos |
| `height_dm` | Entero no negativo |
| `weight_hg` | Entero no negativo |
| `is_default` | Booleano |
| `is_legendary` | Booleano |
| `is_mythical` | Booleano |
| `slot` | Entero positivo |
| `multiplier` | Valor permitido por las reglas seleccionadas |

Estas restricciones deberán contrastarse con los valores reales.

### Valores extremos

Un valor estadístico muy alto no constituye necesariamente un error.

Los valores extremos deberán distinguirse entre:

- Valores válidos del universo Pokémon.
- Errores de extracción.
- Errores de transformación.
- Inconsistencias de integración.

---

## 7. Integridad referencial

Se verificarán las siguientes relaciones:

| Origen | Destino | Validación |
|---|---|---|
| pokemon | species | Existencia de especie |
| pokemon_stats | pokemon | Existencia de Pokémon |
| pokemon_types | pokemon | Existencia de Pokémon |
| pokemon_abilities | pokemon | Existencia de Pokémon |
| pokemon_moves | pokemon | Existencia de Pokémon |
| pokemon_moves | moves | Existencia de movimiento |
| species | evolution_chains | Existencia de cadena cuando aplique |

Las referencias ausentes deberán registrarse antes de decidir su tratamiento.

---

## 8. Calidad de la fuente

PokéAPI proporciona información estructurada mediante recursos REST.

Sin embargo, deben considerarse los siguientes riesgos:

### 8.1 Disponibilidad

Las solicitudes pueden fallar temporalmente.

Posibles problemas:

- Errores HTTP.
- Tiempo de espera agotado.
- Problemas de conectividad.
- Respuestas incompletas.

### 8.2 Cambios en la fuente

La información disponible puede modificarse conforme se actualiza la API.

Por ello, los resultados deberán registrar fecha de extracción y procedencia.

### 8.3 Diferencias entre recursos

Los endpoints representan entidades diferentes.

Una integración incorrecta puede producir duplicados o pérdida de información.

### 8.4 Paginación

Los endpoints de listado pueden devolver resultados paginados.

La extracción completa deberá comprobar que se hayan recuperado todas las páginas previstas.

---

## 9. Limitaciones metodológicas

### 9.1 Ausencia de resultados de combate

La fuente no proporciona, por sí sola, un conjunto completo de resultados competitivos de equipos de tres Pokémon.

Por tanto, el proyecto no podrá afirmar inicialmente que sus equipos tienen mayor probabilidad real de victoria.

### 9.2 Estadísticas base

Las estadísticas base no representan directamente el rendimiento final en combate.

No incluyen necesariamente:

- Nivel.
- Naturaleza.
- Valores individuales.
- Valores de esfuerzo.
- Objetos equipados.
- Estrategia del jugador.
- Condiciones del combate.

### 9.3 Habilidades

Las habilidades tienen efectos heterogéneos y dependientes del contexto.

No se asumirá que pueden reducirse a una única puntuación universal.

### 9.4 Movimientos

Los movimientos disponibles pueden variar entre versiones y métodos de aprendizaje.

No se considerará válida cualquier combinación arbitraria de movimientos.

### 9.5 Reglas generacionales

Las mecánicas Pokémon pueden variar entre generaciones.

La efectividad de tipos y otras reglas deberán corresponder a un formato definido.

---

## 10. Sesgos potenciales

### 10.1 Sesgo por selección

Seleccionar únicamente Pokémon populares, legendarios o de estadísticas elevadas puede distorsionar la distribución de características.

### 10.2 Sesgo por generación

Las distribuciones de estadísticas y mecánicas pueden diferir entre generaciones.

### 10.3 Sesgo por variedades

Incluir múltiples variedades de ciertas especies puede otorgarles mayor representación dentro del clustering.

### 10.4 Sesgo por variables

Las características numéricas con mayor escala pueden dominar los algoritmos basados en distancias.

### 10.5 Sesgo por diseño de evaluación

Si el recomendador se optimiza y evalúa utilizando exactamente la misma puntuación de complementariedad, los resultados pueden favorecer artificialmente al propio método.

---

## 11. Riesgos para Machine Learning

### 11.1 Escalado

Las variables numéricas deberán analizarse antes de aplicar algoritmos basados en distancias.

### 11.2 Redundancia

Variables como `total_stats` están relacionadas matemáticamente con las seis estadísticas base.

Su inclusión simultánea puede introducir ponderaciones no deseadas.

### 11.3 Variables categóricas

Los tipos y otras categorías requieren una representación apropiada.

### 11.4 Interpretación de clusters

Los clusters representan agrupamientos estadísticos.

No necesariamente equivalen a roles competitivos oficiales.

### 11.5 Validación

La selección del algoritmo deberá justificarse mediante métricas, estabilidad e interpretación.

No se asumirá que un algoritmo específico es superior antes de experimentar.

---

## 12. Riesgos para el recomendador

El recomendador deberá evitar:

- Seleccionar tres Pokémon únicamente por estadísticas totales.
- Repetir debilidades sin considerar complementariedad.
- Confundir diversidad estadística con sinergia competitiva demostrada.
- Recomendar variedades incompatibles con el formato seleccionado.
- Evaluarse exclusivamente mediante la función que optimiza.

### Evaluación propuesta

Comparar el recomendador con:

1. Selección aleatoria.
2. Selección por estadísticas totales.
3. Selección basada en complementariedad.

Las métricas definitivas se establecerán durante la fase de evaluación.

---

## 13. Controles de adquisición

Durante la ingeniería de datos se recomienda implementar:

- Reintentos limitados ante errores temporales.
- Tiempo máximo por solicitud.
- Identificación de respuestas HTTP incorrectas.
- Validación de estructura JSON.
- Registro de recursos fallidos.
- Almacenamiento de respuestas originales.
- Registro de fecha de extracción.
- Control de paginación.
- Verificación de identificadores recuperados.

No se realizará extracción masiva durante la fase de minería.

---

## 14. Matriz preliminar de riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Duplicados por uniones | Alto | Modelo normalizado |
| Datos faltantes | Medio/Alto | Perfilado de completitud |
| Errores HTTP | Medio | Reintentos y registro |
| Variedades inconsistentes | Alto | Política de inclusión |
| Mezcla de generaciones | Alto | Definir reglas de referencia |
| Variables redundantes | Medio | Análisis de correlación |
| Clusters poco interpretables | Medio | Perfilamiento y estabilidad |
| Evaluación circular | Alto | Baselines y métricas independientes |
| Ausencia de combates reales | Alto | Limitar afirmaciones competitivas |

Los niveles de impacto son una clasificación cualitativa preliminar.

---

## 15. Plan de validación

### Durante minería de datos

- Verificar conectividad.
- Inspeccionar respuestas JSON.
- Revisar ejemplos de especies y variedades.
- Confirmar estadísticas disponibles.
- Revisar relaciones de tipos.
- Documentar valores nulos observados en una muestra.

### Durante ingeniería de datos

- Validar integridad de archivos.
- Comprobar unicidad.
- Verificar relaciones.
- Medir completitud.
- Detectar duplicados.
- Registrar errores de extracción.

### Durante análisis de datos

- Estudiar distribuciones.
- Detectar valores extremos.
- Analizar correlaciones.
- Identificar sesgos de representación.

### Durante Machine Learning

- Evaluar sensibilidad al escalado.
- Comparar algoritmos.
- Analizar estabilidad de clusters.
- Interpretar perfiles.
- Comparar baselines del recomendador.

---

## 16. Criterios de aceptación

- [ ] Dimensiones de calidad definidas.
- [ ] Variables críticas identificadas.
- [ ] Reglas de unicidad documentadas.
- [ ] Relaciones de integridad definidas.
- [ ] Riesgos de la fuente identificados.
- [ ] Limitaciones competitivas documentadas.
- [ ] Sesgos potenciales identificados.
- [ ] Controles de adquisición propuestos.
- [ ] Riesgos para clustering documentados.
- [ ] Riesgos para recomendación documentados.
- [ ] Validaciones exploratorias ejecutadas.

---

## 17. Conclusión preliminar

PokéAPI constituye una fuente viable para desarrollar un dataset estructurado de características Pokémon.

Sin embargo, la confiabilidad del proyecto dependerá de la correcta integración de entidades, el tratamiento de variedades, la definición de reglas de combate y la validación de los datos.

La fase de minería permitirá identificar estos riesgos antes de construir el pipeline definitivo.

La calidad deberá comprobarse empíricamente y no asumirse únicamente por utilizar una API pública.

---

## 18. Referencias

- PokéAPI — Documentación oficial: https://pokeapi.co/docs/v2
- PokéAPI — Pokémon: https://pokeapi.co/docs/v2#pokemon
- PokéAPI — Pokémon Species: https://pokeapi.co/docs/v2#pokemon-species
- PokéAPI — Types: https://pokeapi.co/docs/v2#types
- scikit-learn — Preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html
- scikit-learn — Clustering: https://scikit-learn.org/stable/modules/clustering.html
