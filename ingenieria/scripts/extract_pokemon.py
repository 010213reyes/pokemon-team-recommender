
"""
Extracción RAW de Pokémon desde PokéAPI.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from pokeapi_client import PokeAPIClient, PokeAPIError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "pokemon"
RESULTS_DIR = PROJECT_ROOT / "ingenieria" / "resultados"


def save_json(data: dict, destination: Path) -> None:
    """Guarda una respuesta JSON sin transformar sus campos."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    temporary = destination.with_suffix(".json.tmp")

    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def extract_pokemon(
    start_id: int = 1,
    end_id: int = 10,
    overwrite: bool = False,
) -> dict:
    """Extrae Pokémon individuales y registra los resultados."""

    if start_id < 1 or end_id < start_id:
        raise ValueError("El rango de IDs no es válido")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(timezone.utc)

    report = {
        "started_at": started_at.isoformat(),
        "finished_at": None,
        "resource": "pokemon",
        "start_id": start_id,
        "end_id": end_id,
        "overwrite": overwrite,
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "records": [],
    }

    with PokeAPIClient() as client:
        for pokemon_id in range(start_id, end_id + 1):
            destination = RAW_DIR / f"{pokemon_id}.json"

            if destination.exists() and not overwrite:
                print(f"[SKIP] Pokémon {pokemon_id}: ya existe")
                report["skipped"] += 1
                report["records"].append({
                    "pokemon_id": pokemon_id,
                    "status": "skipped",
                    "path": str(destination.relative_to(PROJECT_ROOT)),
                })
                continue

            try:
                data = client.get_resource("pokemon", pokemon_id)

                if data.get("id") != pokemon_id:
                    raise ValueError(
                        f"ID inesperado: {data.get('id')}"
                    )

                save_json(data, destination)

                report["success"] += 1
                report["records"].append({
                    "pokemon_id": pokemon_id,
                    "status": "success",
                    "path": str(destination.relative_to(PROJECT_ROOT)),
                })

                print(f"[OK] {pokemon_id}: {data['name']}")

            except (
                PokeAPIError,
                ValueError,
                OSError,
            ) as error:
                report["failed"] += 1
                report["records"].append({
                    "pokemon_id": pokemon_id,
                    "status": "failed",
                    "error": str(error),
                })

                print(f"[ERROR] {pokemon_id}: {error}")

    report["finished_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    report_name = (
        f"extraccion_pokemon_"
        f"{started_at.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    )

    report_path = RESULTS_DIR / report_name
    save_json(report, report_path)

    print("\n=== RESUMEN DE EXTRACCIÓN ===")
    print("Descargados:", report["success"])
    print("Omitidos:", report["skipped"])
    print("Fallidos:", report["failed"])
    print("Reporte:", report_path)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extraer Pokémon desde PokéAPI"
    )

    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    extract_pokemon(
        start_id=args.start,
        end_id=args.end,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
