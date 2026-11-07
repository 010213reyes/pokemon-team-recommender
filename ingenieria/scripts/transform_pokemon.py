
"""
Transformación RAW -> PROCESSED.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos
"""

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

POKEMON_RAW = ROOT / "data/raw/pokemon"
SPECIES_RAW = ROOT / "data/raw/pokemon-species"
PROCESSED = ROOT / "data/processed"

EXPECTED_STATS = {
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
}


def load_json_files(directory):
    """Carga archivos JSON en orden determinista."""

    if not directory.exists():
        raise FileNotFoundError(
            f"No existe el directorio: {directory}"
        )

    files = sorted(
        directory.glob("*.json"),
        key=lambda path: int(path.stem),
    )

    if not files:
        raise ValueError(
            f"No se encontraron archivos JSON en {directory}"
        )

    records = []

    for file in files:
        with file.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo no contiene un objeto JSON: {file}"
            )

        if data.get("id") != int(file.stem):
            raise ValueError(
                f"ID inconsistente en el archivo: {file}"
            )

        records.append(data)

    return records


def resource_id(resource):
    """Obtiene el ID desde una URL de PokéAPI."""

    if not resource:
        return None

    url = resource.get("url", "")
    return int(url.rstrip("/").split("/")[-1])


def transform_pokemon(records):
    """Construye tablas normalizadas de Pokémon."""

    pokemon_rows = []
    stats_rows = []
    types_rows = []
    abilities_rows = []

    for item in records:
        pokemon_id = item["id"]

        pokemon_rows.append({
            "pokemon_id": pokemon_id,
            "pokemon_name": item["name"],
            "species_id": resource_id(item["species"]),
            "is_default": item["is_default"],
            "height_dm": item["height"],
            "weight_hg": item["weight"],
            "base_experience": item.get("base_experience"),
        })

        for stat in item["stats"]:
            stats_rows.append({
                "pokemon_id": pokemon_id,
                "stat_name": stat["stat"]["name"],
                "base_stat": stat["base_stat"],
            })

        for pokemon_type in item["types"]:
            types_rows.append({
                "pokemon_id": pokemon_id,
                "type_id": resource_id(pokemon_type["type"]),
                "type_name": pokemon_type["type"]["name"],
                "slot": pokemon_type["slot"],
            })

        for ability in item["abilities"]:
            abilities_rows.append({
                "pokemon_id": pokemon_id,
                "ability_id": resource_id(ability["ability"]),
                "ability_name": ability["ability"]["name"],
                "is_hidden": ability["is_hidden"],
                "slot": ability["slot"],
            })

    return {
        "pokemon": pd.DataFrame(pokemon_rows),
        "pokemon_stats": pd.DataFrame(stats_rows),
        "pokemon_types": pd.DataFrame(types_rows),
        "pokemon_abilities": pd.DataFrame(abilities_rows),
    }


def transform_species(records):
    """Construye tablas de especies y variedades."""

    species_rows = []
    variety_rows = []

    for item in records:
        species_id = item["id"]

        species_rows.append({
            "species_id": species_id,
            "species_name": item["name"],
            "generation": item["generation"]["name"],
            "is_legendary": item["is_legendary"],
            "is_mythical": item["is_mythical"],
            "capture_rate": item["capture_rate"],
            "habitat": (
                item["habitat"]["name"]
                if item["habitat"] else None
            ),
        })

        for variety in item["varieties"]:
            variety_rows.append({
                "species_id": species_id,
                "pokemon_id": resource_id(variety["pokemon"]),
                "pokemon_name": variety["pokemon"]["name"],
                "is_default": variety["is_default"],
            })

    return {
        "species": pd.DataFrame(species_rows),
        "pokemon_varieties": pd.DataFrame(variety_rows),
    }


def validate_tables(tables):
    """Ejecuta validaciones básicas antes de guardar."""

    pokemon = tables["pokemon"]
    species = tables["species"]
    stats = tables["pokemon_stats"]

    if pokemon["pokemon_id"].duplicated().any():
        raise ValueError("IDs Pokémon duplicados")

    if species["species_id"].duplicated().any():
        raise ValueError("IDs de especies duplicados")

    if stats.duplicated(
        subset=["pokemon_id", "stat_name"]
    ).any():
        raise ValueError("Estadísticas duplicadas")

    for pokemon_id, group in stats.groupby("pokemon_id"):
        observed = set(group["stat_name"])

        if observed != EXPECTED_STATS:
            raise ValueError(
                f"Estadísticas incompletas: Pokémon {pokemon_id}"
            )

    missing_species = (
        set(pokemon["species_id"])
        - set(species["species_id"])
    )

    if missing_species:
        raise ValueError(
            f"Especies faltantes: {sorted(missing_species)}"
        )


def main():
    print("=== TRANSFORMACIÓN RAW -> PROCESSED ===")

    pokemon_records = load_json_files(POKEMON_RAW)
    species_records = load_json_files(SPECIES_RAW)

    tables = {
        **transform_pokemon(pokemon_records),
        **transform_species(species_records),
    }

    validate_tables(tables)

    PROCESSED.mkdir(parents=True, exist_ok=True)

    for name, dataframe in tables.items():
        destination = PROCESSED / f"{name}.csv"

        dataframe.to_csv(
            destination,
            index=False,
            encoding="utf-8",
        )

        print(
            f"[OK] {name}: {len(dataframe)} filas"
        )

    print("\nTransformación completada")


if __name__ == "__main__":
    main()
