
"""
Transformación de tipos Pokémon.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos

Genera:
- types.csv
- type_effectiveness.csv
"""

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "raw" / "type"
PROCESSED_DIR = ROOT / "data" / "processed"

EXPECTED_TYPE_IDS = set(range(1, 19))
RULESET = "pokeapi_current"


def load_types() -> list[dict]:
    """Carga y verifica los 18 recursos RAW."""

    records = []

    for type_id in sorted(EXPECTED_TYPE_IDS):
        path = RAW_DIR / f"{type_id}.json"

        if not path.exists():
            raise FileNotFoundError(
                f"Falta el recurso: {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if data.get("id") != type_id:
            raise ValueError(
                f"ID inconsistente: {path}"
            )

        if not isinstance(
            data.get("damage_relations"), dict
        ):
            raise ValueError(
                f"Relaciones ausentes: {path}"
            )

        records.append(data)

    return records


def build_catalog(records: list[dict]) -> pd.DataFrame:
    """Construye el catálogo de tipos."""

    rows = [
        {
            "type_id": item["id"],
            "type_name": item["name"],
        }
        for item in records
    ]

    return pd.DataFrame(rows)


def build_effectiveness(
    records: list[dict],
) -> pd.DataFrame:
    """Construye las 324 relaciones ofensivas."""

    names = {
        item["name"]: item["id"]
        for item in records
    }

    rows = []

    for attacker in records:
        attacker_id = attacker["id"]
        attacker_name = attacker["name"]

        relations = attacker["damage_relations"]

        double = {
            item["name"]
            for item in relations["double_damage_to"]
        }

        half = {
            item["name"]
            for item in relations["half_damage_to"]
        }

        zero = {
            item["name"]
            for item in relations["no_damage_to"]
        }

        for defender_name, defender_id in names.items():

            memberships = sum([
                defender_name in double,
                defender_name in half,
                defender_name in zero,
            ])

            if memberships > 1:
                raise ValueError(
                    "Relación contradictoria: "
                    f"{attacker_name} -> {defender_name}"
                )

            multiplier = 1.0

            if defender_name in double:
                multiplier = 2.0

            elif defender_name in half:
                multiplier = 0.5

            elif defender_name in zero:
                multiplier = 0.0

            rows.append({
                "attacking_type_id": attacker_id,
                "attacking_type": attacker_name,
                "defending_type_id": defender_id,
                "defending_type": defender_name,
                "multiplier": multiplier,
                "ruleset": RULESET,
            })

    return pd.DataFrame(rows)


def validate(
    catalog: pd.DataFrame,
    effectiveness: pd.DataFrame,
) -> None:
    """Valida cobertura, unicidad y multiplicadores."""

    if len(catalog) != 18:
        raise ValueError(
            "El catálogo no contiene 18 tipos"
        )

    if set(catalog["type_id"]) != EXPECTED_TYPE_IDS:
        raise ValueError(
            "Los identificadores de tipos no coinciden"
        )

    if not catalog["type_name"].is_unique:
        raise ValueError(
            "Existen nombres de tipo duplicados"
        )

    if len(effectiveness) != 324:
        raise ValueError(
            "La matriz no contiene 324 combinaciones"
        )

    keys = [
        "attacking_type_id",
        "defending_type_id",
        "ruleset",
    ]

    if effectiveness.duplicated(keys).any():
        raise ValueError(
            "Existen combinaciones duplicadas"
        )

    allowed = {0.0, 0.5, 1.0, 2.0}

    if not set(
        effectiveness["multiplier"]
    ).issubset(allowed):
        raise ValueError(
            "Se detectaron multiplicadores inválidos"
        )

    if effectiveness.isna().any().any():
        raise ValueError(
            "Existen valores faltantes"
        )


def main() -> None:
    print("=== TRANSFORMACIÓN DE TIPOS ===")

    records = load_types()

    catalog = build_catalog(records)
    effectiveness = build_effectiveness(records)

    validate(catalog, effectiveness)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    catalog.to_csv(
        PROCESSED_DIR / "types.csv",
        index=False,
        encoding="utf-8",
    )

    effectiveness.to_csv(
        PROCESSED_DIR / "type_effectiveness.csv",
        index=False,
        encoding="utf-8",
    )

    print(f"[OK] types: {len(catalog)} filas")
    print(
        "[OK] type_effectiveness: "
        f"{len(effectiveness)} filas"
    )

    print("\n=== DISTRIBUCIÓN DE MULTIPLICADORES ===")

    print(
        effectiveness["multiplier"]
        .value_counts()
        .sort_index()
    )

    print("\nTransformación completada")


if __name__ == "__main__":
    main()
