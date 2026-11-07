
"""
Validación integral del pipeline de Ingeniería de Datos.

Proyecto: Pokémon Team Recommender

Comprueba:
- Existencia y esquema de tablas.
- Cobertura del lote piloto.
- Claves únicas y relaciones.
- Estadísticas y asociaciones.
- Matriz de efectividad.
- Reconstrucción de perfiles defensivos.

Genera:
ingenieria/resultados/validacion_pipeline.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "ingenieria" / "resultados"

EXPECTED_POKEMON = 151
EXPECTED_TYPES = 18

SCHEMAS = {
    "pokemon": [
        "pokemon_id", "pokemon_name", "species_id"
    ],
    "pokemon_stats": [
        "pokemon_id", "stat_name", "base_stat"
    ],
    "pokemon_types": [
        "pokemon_id", "type_id", "type_name", "slot"
    ],
    "pokemon_abilities": [
        "pokemon_id", "ability_id", "ability_name"
    ],
    "species": [
        "species_id", "species_name"
    ],
    "pokemon_varieties": [
        "species_id", "pokemon_id"
    ],
    "types": [
        "type_id", "type_name"
    ],
    "type_effectiveness": [
        "attacking_type_id",
        "defending_type_id",
        "multiplier",
        "ruleset",
    ],
    "pokemon_defensive_profile": [
        "pokemon_id",
        "attacking_type_id",
        "defensive_multiplier",
        "ruleset",
    ],
}

EXPECTED_STATS = {
    "hp", "attack", "defense",
    "special-attack", "special-defense", "speed",
}

ALLOWED_MULTIPLIERS = {
    0.0, 0.25, 0.5, 1.0, 2.0, 4.0
}


class Validator:
    def __init__(self):
        self.checks = []

    def check(self, name, condition, detail=""):
        passed = bool(condition)

        self.checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

        print(
            f"[{'PASS' if passed else 'FAIL'}] {name}"
        )

    def save(self, tables):
        RESULTS.mkdir(parents=True, exist_ok=True)

        failures = sum(
            item["status"] == "FAIL"
            for item in self.checks
        )

        report = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "scope": "first_151_pokemon",
            "total_checks": len(self.checks),
            "passed": len(self.checks) - failures,
            "failed": failures,
            "status": "PASS" if failures == 0 else "FAIL",
            "table_rows": {
                name: len(table)
                for name, table in tables.items()
            },
            "checks": self.checks,
        }

        destination = (
            RESULTS / "validacion_pipeline.json"
        )

        with destination.open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(
                report, file,
                indent=2,
                ensure_ascii=False,
            )

        print("\n=== RESUMEN ===")
        print("Validaciones:", report["total_checks"])
        print("Correctas:", report["passed"])
        print("Fallidas:", report["failed"])
        print("Estado:", report["status"])
        print("Reporte:", destination)

        return failures == 0


def load_tables(validator):
    tables = {}

    for name, columns in SCHEMAS.items():
        path = PROCESSED / f"{name}.csv"

        if not path.exists():
            validator.check(
                f"Existe {name}", False
            )
            continue

        try:
            table = pd.read_csv(path)
        except (OSError, ValueError, pd.errors.ParserError):
            validator.check(
                f"Lectura correcta: {name}", False
            )
            continue

        valid_schema = set(columns).issubset(
            table.columns
        )

        validator.check(
            f"Esquema correcto: {name}",
            valid_schema,
        )

        if valid_schema:
            tables[name] = table

    return tables


def validate_entities(v, t):
    pokemon = t["pokemon"]
    species = t["species"]
    stats = t["pokemon_stats"]
    ptypes = t["pokemon_types"]
    abilities = t["pokemon_abilities"]
    varieties = t["pokemon_varieties"]

    pokemon_ids = set(pokemon["pokemon_id"])
    species_ids = set(species["species_id"])

    v.check(
        "151 Pokémon",
        len(pokemon) == EXPECTED_POKEMON,
    )

    v.check(
        "151 especies",
        len(species) == EXPECTED_POKEMON,
    )

    v.check(
        "IDs Pokémon únicos",
        pokemon["pokemon_id"].is_unique
        and pokemon["pokemon_id"].notna().all(),
    )

    v.check(
        "IDs especies únicos",
        species["species_id"].is_unique
        and species["species_id"].notna().all(),
    )

    v.check(
        "Pokémon referencian especies existentes",
        set(pokemon["species_id"]).issubset(
            species_ids
        ),
    )

    v.check(
        "906 estadísticas",
        len(stats) == EXPECTED_POKEMON * 6,
    )

    v.check(
        "Estadísticas referencian Pokémon",
        set(stats["pokemon_id"]).issubset(
            pokemon_ids
        ),
    )

    v.check(
        "Seis estadísticas distintas por Pokémon",
        all(
            set(group["stat_name"]) == EXPECTED_STATS
            and len(group) == 6
            for _, group in stats.groupby("pokemon_id")
        )
        and set(stats["pokemon_id"]) == pokemon_ids,
    )

    v.check(
        "Estadísticas no negativas",
        pd.to_numeric(
            stats["base_stat"], errors="coerce"
        ).ge(0).all(),
    )

    v.check(
        "Tipos asociados a Pokémon existentes",
        set(ptypes["pokemon_id"]).issubset(
            pokemon_ids
        ),
    )

    v.check(
        "Uno o dos tipos por Pokémon",
        ptypes.groupby("pokemon_id").size()
        .between(1, 2).all()
        and set(ptypes["pokemon_id"]) == pokemon_ids,
    )

    v.check(
        "Sin asociaciones de tipo duplicadas",
        not ptypes.duplicated(
            ["pokemon_id", "type_id"]
        ).any(),
    )

    v.check(
        "Habilidades referencian Pokémon",
        set(abilities["pokemon_id"]).issubset(
            pokemon_ids
        ),
    )

    v.check(
        "Todos los Pokémon tienen habilidad",
        set(abilities["pokemon_id"]) == pokemon_ids,
    )

    v.check(
        "Sin asociaciones de habilidad duplicadas",
        not abilities.duplicated(
            ["pokemon_id", "ability_id"]
        ).any(),
    )

    v.check(
        "Variedades referencian especies",
        set(varieties["species_id"]).issubset(
            species_ids
        ),
    )

    v.check(
        "Sin relaciones de variedad duplicadas",
        not varieties.duplicated(
            ["species_id", "pokemon_id"]
        ).any(),
    )


def validate_type_matrix(v, t):
    types = t["types"]
    matrix = t["type_effectiveness"]

    ids = set(types["type_id"])

    v.check(
        "18 tipos principales",
        len(types) == EXPECTED_TYPES
        and types["type_id"].is_unique
        and types["type_name"].is_unique
        and ids == set(range(1, 19)),
    )

    v.check(
        "324 relaciones de efectividad",
        len(matrix) == EXPECTED_TYPES ** 2,
    )

    v.check(
        "Matriz sin combinaciones duplicadas",
        not matrix.duplicated(
            ["attacking_type_id", "defending_type_id"]
        ).any(),
    )

    v.check(
        "Matriz con cobertura completa",
        set(zip(
            matrix["attacking_type_id"],
            matrix["defending_type_id"],
        )) == {
            (a, d)
            for a in ids
            for d in ids
        },
    )

    v.check(
        "Multiplicadores de tipo válidos",
        pd.to_numeric(
            matrix["multiplier"], errors="coerce"
        ).isin([0.0, 0.5, 1.0, 2.0]).all(),
    )

    v.check(
        "Un único ruleset",
        matrix["ruleset"].nunique() == 1
        and matrix["ruleset"].notna().all(),
    )

    ptypes = t["pokemon_types"]

    v.check(
        "Tipos Pokémon pertenecen al catálogo",
        set(ptypes["type_id"]).issubset(ids),
    )


def validate_defensive_profiles(v, t):
    pokemon = t["pokemon"]
    types = t["types"]
    ptypes = t["pokemon_types"]
    matrix = t["type_effectiveness"]
    profiles = t["pokemon_defensive_profile"]

    pokemon_ids = set(pokemon["pokemon_id"])
    type_ids = set(types["type_id"])

    expected_pairs = {
        (p, a)
        for p in pokemon_ids
        for a in type_ids
    }

    actual_pairs = set(zip(
        profiles["pokemon_id"],
        profiles["attacking_type_id"],
    ))

    v.check(
        "2718 perfiles defensivos",
        len(profiles) == (
            EXPECTED_POKEMON * EXPECTED_TYPES
        ),
    )

    v.check(
        "Cobertura defensiva completa",
        actual_pairs == expected_pairs,
    )

    v.check(
        "Sin perfiles duplicados",
        not profiles.duplicated(
            ["pokemon_id", "attacking_type_id"]
        ).any(),
    )

    v.check(
        "Multiplicadores defensivos válidos",
        pd.to_numeric(
            profiles["defensive_multiplier"],
            errors="coerce"
        ).isin(ALLOWED_MULTIPLIERS).all(),
    )

    v.check(
        "Ruleset consistente",
        profiles["ruleset"].nunique() == 1
        and profiles["ruleset"].notna().all()
        and set(profiles["ruleset"]) == set(
            matrix["ruleset"]
        ),
    )

    # Reconstrucción independiente desde los tipos.
    lookup = {
        (int(row.attacking_type_id),
         int(row.defending_type_id)): float(
             row.multiplier
         )
        for row in matrix.itertuples()
    }

    grouped_types = {
        int(pid): group["type_id"].tolist()
        for pid, group in ptypes.groupby("pokemon_id")
    }

    matches = True

    for row in profiles.itertuples():
        pid = int(row.pokemon_id)
        attacker = int(row.attacking_type_id)

        defensive_types = grouped_types.get(pid, [])

        if not 1 <= len(defensive_types) <= 2:
            matches = False
            break

        expected = 1.0

        for defender in defensive_types:
            key = (attacker, int(defender))

            if key not in lookup:
                matches = False
                break

            expected *= lookup[key]

        if not matches or abs(
            expected - float(row.defensive_multiplier)
        ) > 1e-9:
            matches = False
            break

    v.check(
        "Perfiles reconstruidos correctamente",
        matches,
    )

    # Caso de referencia: Charizard.
    expected_charizard = {
        "rock": 4.0,
        "water": 2.0,
        "grass": 0.25,
        "ground": 0.0,
    }

    charizard = profiles.loc[
        profiles["pokemon_id"] == 6
    ].merge(
        types[["type_id", "type_name"]],
        left_on="attacking_type_id",
        right_on="type_id",
    )

    observed = dict(zip(
        charizard["type_name"],
        charizard["defensive_multiplier"],
    ))

    v.check(
        "Caso de referencia: Charizard",
        all(
            observed.get(name) == value
            for name, value in expected_charizard.items()
        ),
    )


def main():
    print("=== VALIDACIÓN INTEGRAL ===")

    validator = Validator()
    tables = load_tables(validator)

    if len(tables) == len(SCHEMAS):
        try:
            validate_entities(validator, tables)
            validate_type_matrix(validator, tables)
            validate_defensive_profiles(
                validator, tables
            )
        except (KeyError, TypeError, ValueError) as error:
            validator.check(
                "Ejecución de validaciones",
                False,
                str(error),
            )
            print(f"[ERROR] {error}")
    else:
        validator.check(
            "Todas las tablas disponibles",
            False,
        )

    success = validator.save(tables)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
