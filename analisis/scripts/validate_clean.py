
"""
Fase 3 — Análisis de Datos
Validación final de tablas CLEAN.
"""

from pathlib import Path
import hashlib
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
CLEAN = ROOT / "data" / "clean"
RESULTS = ROOT / "analisis" / "resultados"

TABLES = [
    "pokemon",
    "pokemon_stats",
    "pokemon_types",
    "pokemon_abilities",
    "species",
    "pokemon_varieties",
    "types",
    "type_effectiveness",
    "pokemon_defensive_profile",
]


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024), b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def main():
    checks = []
    loaded = {}

    for name in TABLES:
        source = PROCESSED / f"{name}.csv"
        target = CLEAN / f"{name}.csv"

        exists = source.is_file() and target.is_file()

        checks.append({
            "check": f"{name}: archivos existentes",
            "passed": exists,
        })

        if not exists:
            continue

        source_df = pd.read_csv(source)
        clean_df = pd.read_csv(target)
        loaded[name] = clean_df

        checks.extend([
            {
                "check": f"{name}: SHA-256",
                "passed": (
                    sha256_file(source)
                    == sha256_file(target)
                ),
            },
            {
                "check": f"{name}: filas conservadas",
                "passed": (
                    len(source_df) == len(clean_df)
                ),
            },
            {
                "check": f"{name}: sin nulos",
                "passed": not clean_df.isna().any().any(),
            },
            {
                "check": f"{name}: sin duplicados exactos",
                "passed": not clean_df.duplicated().any(),
            },
        ])

    if len(loaded) == len(TABLES):
        pokemon = loaded["pokemon"]
        stats = loaded["pokemon_stats"]
        species = loaded["species"]
        pokemon_types = loaded["pokemon_types"]
        types = loaded["types"]
        effectiveness = loaded["type_effectiveness"]
        defensive = loaded["pokemon_defensive_profile"]

        checks.extend([
            {
                "check": "151 Pokémon",
                "passed": len(pokemon) == 151,
            },
            {
                "check": "IDs Pokémon únicos",
                "passed": pokemon["pokemon_id"].is_unique,
            },
            {
                "check": "6 estadísticas por Pokémon",
                "passed": (
                    stats.groupby("pokemon_id")["stat_name"]
                    .nunique()
                    .reindex(
                        pokemon["pokemon_id"],
                        fill_value=0,
                    )
                    .eq(6)
                    .all()
                ),
            },
            {
                "check": "Species referenciadas",
                "passed": pokemon["species_id"].isin(
                    species["species_id"]
                ).all(),
            },
            {
                "check": "Tipos de Pokémon válidos",
                "passed": pokemon_types["type_id"].isin(
                    types["type_id"]
                ).all(),
            },
            {
                "check": "324 relaciones de tipos",
                "passed": len(effectiveness) == 324,
            },
            {
                "check": "Multiplicadores válidos",
                "passed": effectiveness["multiplier"].isin(
                    [0, 0.5, 1, 2]
                ).all(),
            },
            {
                "check": "2718 perfiles defensivos",
                "passed": len(defensive) == 2718,
            },
        ])

        
# Convertir los resultados a booleanos nativos de Python
# para garantizar compatibilidad con JSON.

    for item in checks:
        item["passed"] = bool(item["passed"])

    passed = sum(item["passed"] for item in checks)
    total = len(checks)


   

    for item in checks:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['check']}")

    RESULTS.mkdir(parents=True, exist_ok=True)

    report = {
        "phase": "analisis_datos",
        "passed": passed,
        "total": total,
        "all_passed": passed == total,
        "checks": checks,
    }

    output = RESULTS / "validacion_clean.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nResultado: {passed}/{total} PASS")
    print(f"Reporte: {output}")

    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
