
"""
Validación de calidad e integridad de datos PROCESSED.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "ingenieria" / "resultados"

TABLES = [
    "pokemon",
    "pokemon_stats",
    "pokemon_types",
    "pokemon_abilities",
    "species",
    "pokemon_varieties",
]

EXPECTED_STATS = {
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
}


def load_tables():
    """Carga las tablas procesadas."""

    tables = {}

    for name in TABLES:
        path = PROCESSED / f"{name}.csv"

        if not path.exists():
            raise FileNotFoundError(
                f"No se encontró la tabla: {path}"
            )

        tables[name] = pd.read_csv(path)

    return tables


def validate(tables):
    """Ejecuta controles de calidad y registra hallazgos."""

    checks = []

    def check(name, condition, details=""):
        passed = bool(condition)

        checks.append({
            "check": name,
            "passed": passed,
            "details": details,
        })

        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")

    pokemon = tables["pokemon"]
    stats = tables["pokemon_stats"]
    types = tables["pokemon_types"]
    abilities = tables["pokemon_abilities"]
    species = tables["species"]
    varieties = tables["pokemon_varieties"]

    # 1. Unicidad de entidades principales
    check(
        "pokemon_id único",
        pokemon["pokemon_id"].is_unique,
    )

    check(
        "species_id único",
        species["species_id"].is_unique,
    )

    # 2. Identificadores obligatorios
    for name, column in [
        ("pokemon", "pokemon_id"),
        ("species", "species_id"),
        ("pokemon_stats", "pokemon_id"),
        ("pokemon_types", "pokemon_id"),
        ("pokemon_abilities", "pokemon_id"),
    ]:
        check(
            f"{name}: {column} sin nulos",
            tables[name][column].notna().all(),
        )

    # 3. Integridad de relaciones
    pokemon_ids = set(pokemon["pokemon_id"])
    species_ids = set(species["species_id"])

    check(
        "Pokémon referencian especies existentes",
        set(pokemon["species_id"]).issubset(species_ids),
    )

    for name, table in [
        ("stats", stats),
        ("types", types),
        ("abilities", abilities),
    ]:
        check(
            f"{name}: Pokémon existentes",
            set(table["pokemon_id"]).issubset(pokemon_ids),
        )

    # 4. Estadísticas completas
    stat_groups = stats.groupby("pokemon_id")["stat_name"]

    complete_stats = all(
        set(group) == EXPECTED_STATS
        and len(group) == 6
        for _, group in stat_groups
    )

    check(
        "Seis estadísticas por Pokémon",
        complete_stats
        and set(stat_groups.groups) == pokemon_ids,
    )

    check(
        "Estadísticas no negativas",
        stats["base_stat"].notna().all()
        and (stats["base_stat"] >= 0).all(),
    )

    check(
        "Sin estadísticas duplicadas",
        not stats.duplicated(
            ["pokemon_id", "stat_name"]
        ).any(),
    )

    # 5. Tipos
    check(
        "Todos los Pokémon tienen tipo",
        pokemon_ids.issubset(set(types["pokemon_id"])),
    )

    check(
        "Sin asociaciones de tipo duplicadas",
        not types.duplicated(
            ["pokemon_id", "type_id"]
        ).any(),
    )

    # 6. Habilidades
    check(
        "Todos los Pokémon tienen habilidad",
        pokemon_ids.issubset(
            set(abilities["pokemon_id"])
        ),
    )

    check(
        "Sin asociaciones de habilidad duplicadas",
        not abilities.duplicated(
            ["pokemon_id", "ability_id"]
        ).any(),
    )

    # 7. Variedades
    check(
        "Variedades referencian especies existentes",
        set(varieties["species_id"]).issubset(
            species_ids
        ),
    )

    check(
        "Sin relaciones de variedad duplicadas",
        not varieties.duplicated(
            ["species_id", "pokemon_id"]
        ).any(),
    )

    # Las variedades pueden referenciar Pokémon
    # todavía no descargados. No es un error.
    missing_varieties = (
        set(varieties["pokemon_id"]) - pokemon_ids
    )

    return checks, {
        "variety_pokemon_not_extracted": len(
            missing_varieties
        ),
        "variety_pokemon_ids_not_extracted": sorted(
            int(value) for value in missing_varieties
        ),
    }


def main():
    print("=== VALIDACIÓN PROCESSED ===\n")

    tables = load_tables()
    checks, observations = validate(tables)

    passed = sum(item["passed"] for item in checks)
    failed = len(checks) - passed

    report = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "PASS" if failed == 0 else "FAIL",
        "total_checks": len(checks),
        "passed": passed,
        "failed": failed,
        "table_rows": {
            name: len(table)
            for name, table in tables.items()
        },
        "checks": checks,
        "observations": observations,
    }

    RESULTS.mkdir(parents=True, exist_ok=True)

    destination = RESULTS / "validacion_processed.json"

    with destination.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n=== RESUMEN ===")
    print("Validaciones:", len(checks))
    print("Correctas:", passed)
    print("Fallidas:", failed)
    print("Estado:", report["status"])
    print("Reporte:", destination)

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
