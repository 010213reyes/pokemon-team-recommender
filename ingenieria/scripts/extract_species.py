
"""
Extracción RAW de especies Pokémon.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pokeapi_client import PokeAPIClient, PokeAPIError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "pokemon-species"
RESULTS_DIR = PROJECT_ROOT / "ingenieria" / "resultados"


def save_json(data: dict, destination: Path) -> None:
    """Guarda datos JSON de forma atómica."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".json.tmp")

    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def extract_species(
    start_id: int = 1,
    end_id: int = 15,
    overwrite: bool = False,
) -> dict:
    """Extrae especies y genera un reporte de ejecución."""

    if start_id < 1 or end_id < start_id:
        raise ValueError("Rango de IDs inválido")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(timezone.utc)

    report = {
        "resource": "pokemon-species",
        "started_at": started_at.isoformat(),
        "finished_at": None,
        "start_id": start_id,
        "end_id": end_id,
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "records": [],
    }

    with PokeAPIClient() as client:
        for species_id in range(start_id, end_id + 1):
            destination = RAW_DIR / f"{species_id}.json"

            if destination.exists() and not overwrite:
                print(f"[SKIP] Especie {species_id}")
                report["skipped"] += 1
                report["records"].append({
                    "species_id": species_id,
                    "status": "skipped",
                })
                continue

            try:
                data = client.get_resource(
                    "pokemon-species",
                    species_id,
                )

                if data.get("id") != species_id:
                    raise ValueError("ID de especie inesperado")

                save_json(data, destination)

                print(f"[OK] {species_id}: {data['name']}")

                report["success"] += 1
                report["records"].append({
                    "species_id": species_id,
                    "status": "success",
                })

            except (
                PokeAPIError,
                ValueError,
                OSError,
            ) as error:
                print(f"[ERROR] {species_id}: {error}")

                report["failed"] += 1
                report["records"].append({
                    "species_id": species_id,
                    "status": "failed",
                    "error": str(error),
                })

    report["finished_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    report_name = (
        "extraccion_species_"
        f"{started_at.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    )

    report_path = RESULTS_DIR / report_name
    save_json(report, report_path)

    print("\n=== RESUMEN DE ESPECIES ===")
    print("Descargadas:", report["success"])
    print("Omitidas:", report["skipped"])
    print("Fallidas:", report["failed"])
    print("Reporte:", report_path)

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Extraer especies desde PokéAPI"
    )

    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=15)
    parser.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    extract_species(
        start_id=args.start,
        end_id=args.end,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
