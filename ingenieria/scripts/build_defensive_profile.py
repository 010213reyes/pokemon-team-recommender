
"""
Construcción del perfil defensivo por Pokémon.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos

Salida:
data/processed/pokemon_defensive_profile.csv
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"


def load_data():
    """Carga tablas procesadas necesarias."""

    names = [
        "pokemon",
        "pokemon_types",
        "types",
        "type_effectiveness",
    ]

    tables = {}

    for name in names:
        path = PROCESSED / f"{name}.csv"

        if not path.exists():
            raise FileNotFoundError(
                f"Archivo faltante: {path}"
            )

        tables[name] = pd.read_csv(path)

    return tables


def build_profiles(tables):
    """Calcula multiplicadores defensivos combinados."""

    pokemon = tables["pokemon"]
    pokemon_types = tables["pokemon_types"]
    types = tables["types"]
    effectiveness = tables["type_effectiveness"]

    if len(types) != 18 or len(effectiveness) != 324:
        raise ValueError(
            "Catálogo o matriz de efectividad incompletos"
        )

    if pokemon["pokemon_id"].duplicated().any():
        raise ValueError("Pokémon duplicados")

    if pokemon_types.duplicated(
        ["pokemon_id", "type_id"]
    ).any():
        raise ValueError("Tipos Pokémon duplicados")

    if effectiveness.duplicated(
        ["attacking_type_id", "defending_type_id"]
    ).any():
        raise ValueError("Relaciones de efectividad duplicadas")

    if effectiveness["ruleset"].nunique() != 1:
        raise ValueError(
            "Se detectaron múltiples conjuntos de reglas"
        )

    if effectiveness["multiplier"].isna().any():
        raise ValueError("Multiplicadores nulos")

    lookup = effectiveness.set_index(
        ["attacking_type_id", "defending_type_id"]
    )["multiplier"].to_dict()

    rows = []

    for _, poke in pokemon.iterrows():
        pokemon_id = int(poke["pokemon_id"])

        defensive_types = pokemon_types.loc[
            pokemon_types["pokemon_id"] == pokemon_id,
            "type_id",
        ].tolist()

        if not 1 <= len(defensive_types) <= 2:
            raise ValueError(
                f"Cantidad de tipos inválida: {pokemon_id}"
            )

        for _, attacking_type in types.iterrows():
            attacking_id = int(attacking_type["type_id"])

            multiplier = 1.0

            for defending_id in defensive_types:
                key = (attacking_id, int(defending_id))

                if key not in lookup:
                    raise ValueError(
                        f"Relación faltante: {key}"
                    )

                multiplier *= float(lookup[key])

            rows.append({
                "pokemon_id": pokemon_id,
                "pokemon_name": poke["pokemon_name"],
                "attacking_type_id": attacking_id,
                "attacking_type": attacking_type["type_name"],
                "defensive_multiplier": multiplier,
                "ruleset": effectiveness["ruleset"].iloc[0],
            })

    return pd.DataFrame(rows)


def validate_profiles(profiles, pokemon):
    """Comprueba integridad de los perfiles."""

    expected = len(pokemon) * 18

    if len(profiles) != expected:
        raise ValueError(
            f"Se esperaban {expected} filas, "
            f"se obtuvieron {len(profiles)}"
        )

    if profiles.duplicated(
        ["pokemon_id", "attacking_type_id", "ruleset"]
    ).any():
        raise ValueError("Perfiles duplicados")

    allowed = {0.0, 0.25, 0.5, 1.0, 2.0, 4.0}

    if not set(
        profiles["defensive_multiplier"]
    ).issubset(allowed):
        raise ValueError("Multiplicadores inválidos")

    if profiles.isna().any().any():
        raise ValueError("Valores faltantes")


def main():
    print("=== PERFILES DEFENSIVOS ===")

    tables = load_data()

    profiles = build_profiles(tables)

    validate_profiles(
        profiles,
        tables["pokemon"],
    )

    destination = (
        PROCESSED / "pokemon_defensive_profile.csv"
    )

    profiles.to_csv(
        destination,
        index=False,
        encoding="utf-8",
    )

    print("Pokémon:", len(tables["pokemon"]))
    print("Tipos ofensivos:", len(tables["types"]))
    print("Perfiles generados:", len(profiles))

    print("\n=== DISTRIBUCIÓN ===")
    print(
        profiles["defensive_multiplier"]
        .value_counts()
        .sort_index()
    )

    print("\n[OK] Archivo:", destination)


if __name__ == "__main__":
    main()
