# Diagnóstico de Calidad de Datos

**Proyecto:** Pokémon Team Recommender  
**Fase:** 3 — Análisis de Datos  
**Dataset:** Primera generación, Pokémon 1–151  
**Estado:** Diagnóstico exploratorio inicial completado

## 1. Objetivo

Evaluar la calidad de los datos procesados durante la fase de Ingeniería de Datos, identificando valores faltantes, duplicados exactos y valores estadísticamente atípicos antes de aplicar transformaciones de limpieza.

## 2. Metodología

Se analizaron nueve tablas CSV mediante Python, pandas y NumPy.

Las verificaciones realizadas incluyeron:

- Dimensiones y estructura de las tablas.
- Detección de valores nulos.
- Identificación de duplicados exactos.
- Estadísticas descriptivas.
- Detección de valores atípicos mediante el rango intercuartílico (IQR).

El criterio IQR identifica valores inferiores a Q1 − 1.5 × IQR o superiores a Q3 + 1.5 × IQR.

## 3. Resultados

Se analizaron nueve tablas procesadas, correspondientes a información de Pokémon, especies, estadísticas, tipos, habilidades, variedades, efectividad y perfiles defensivos.

**Valores faltantes:** 0.

**Duplicados exactos:** 0.

**Registros atípicos identificados:** 6.

| Pokémon | Estadística | Valor |
|---|---|---:|
| Cloyster | Defense | 180 |
| Onix | Defense | 160 |
| Chansey | HP | 250 |
| Snorlax | HP | 160 |
| Wigglytuff | HP | 140 |
| Mewtwo | Special Attack | 154 |

Los seis valores son coherentes con las características conocidas de los Pokémon correspondientes.

## 4. Decisiones técnicas

Se determina conservar los seis registros atípicos, debido a que representan diferencias naturales entre Pokémon y no errores evidentes.

No se aplicará imputación, eliminación de filas ni sustitución de estadísticas durante esta etapa.

Las futuras transformaciones para modelado, como el escalado de características, deberán realizarse de manera independiente de la limpieza de errores.

## 5. Limitaciones

Este diagnóstico no constituye una validación exhaustiva de calidad.

Aunque no se encontraron valores faltantes ni duplicados exactos, todavía deben revisarse las restricciones de dominio, las claves únicas y la integridad referencial.

La validación de Ingeniería de Datos se documentó por separado y no sustituye las comprobaciones específicas de esta fase.

## 6. Conclusión

Los resultados iniciales indican que las nueve tablas presentan condiciones favorables para continuar el análisis.

Los valores extremos detectados son coherentes con las características de los Pokémon y deben conservarse.

El siguiente paso será comprobar la integridad lógica y los rangos permitidos antes de generar los conjuntos de datos limpios.