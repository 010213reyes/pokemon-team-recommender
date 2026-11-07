# Reglas de Limpieza de Datos

**Proyecto:** Pokémon Team Recommender  
**Fase:** 3 — Análisis de Datos  
**Origen:** `data/processed/`  
**Destino:** `data/clean/`

## 1. Objetivo

Definir criterios reproducibles para preparar los datos utilizados en el análisis exploratorio y las etapas posteriores de Ciencia de Datos, preservando la integridad de la información original.

## 2. Diagnóstico inicial

El análisis de las nueve tablas procesadas identificó:

- Cero valores nulos.
- Cero duplicados exactos.
- Seis valores estadísticamente atípicos, considerados legítimos.
- Seis verificaciones básicas de integridad satisfactorias.

No se identificaron problemas que requieran eliminar o imputar registros.

## 3. Reglas de limpieza

**Regla 1. Preservación de datos originales**

Los archivos RAW y PROCESSED permanecerán sin modificaciones. Los resultados de esta etapa se almacenarán en CLEAN.

**Regla 2. Identificadores**

Los identificadores deben conservarse sin modificaciones y respetar las relaciones entre tablas.

**Regla 3. Valores faltantes**

No se realizará imputación mientras no existan valores faltantes que requieran tratamiento.

**Regla 4. Duplicados**

No se eliminarán registros mientras no se identifiquen duplicados reales. Las relaciones legítimas entre Pokémon, tipos, estadísticas y habilidades deberán conservarse.

**Regla 5. Valores atípicos**

Los seis valores extremos identificados mediante IQR se conservarán. No se aplicará truncamiento, sustitución por promedios ni eliminación automática.

**Regla 6. Tipos de datos**

Se verificarán los tipos numéricos y categóricos, evitando conversiones que alteren los valores originales.

**Regla 7. Integridad referencial**

Se comprobará que los identificadores relacionados existan en sus respectivas tablas de referencia.

**Regla 8. Efectividad de tipos**

Los multiplicadores de efectividad deberán respetar el conjunto de valores permitido por el sistema de tipos utilizado: 0, 0.5, 1 y 2.

**Regla 9. Reproducibilidad**

La generación de CLEAN deberá realizarse mediante un script ejecutable, con validaciones previas y posteriores, sin modificaciones manuales a los archivos.

## 4. Separación entre limpieza y modelado

La limpieza de datos no incluirá normalización estadística, PCA ni selección de características para clustering.

Estas transformaciones corresponden a la preparación de características y modelado, y deberán documentarse en sus respectivas etapas.

## 5. Criterios de aceptación

Para considerar satisfactoria la preparación de CLEAN se requiere:

- Preservar las nueve tablas procesadas.
- Mantener la cantidad de registros cuando no exista una justificación de eliminación.
- Conservar los seis valores extremos legítimos.
- Validar las claves y relaciones entre tablas.
- Comprobar que las tablas CLEAN respetan las reglas definidas.
- Generar un reporte reproducible de validación.

## 6. Resultado esperado

Obtener nueve tablas limpias y validadas que puedan utilizarse como entrada para el análisis exploratorio, sin alterar la información original ni introducir transformaciones de modelado.