
"""
Extracción RAW de tipos Pokémon.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos

Descarga los 18 tipos principales desde PokéAPI
y genera un reporte de ejecución.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pokeapi_client import PokeAPIClient, PokeAPIError


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "raw" / "type"
RESULTS_DIR = ROOT / "ingenieria" / "resultados"

# Tipos principales del sistema moderno.
# Se excluyen tipos especiales como unknown y shadow.
TYPE_IDS = list(range(1, 19))


def save_json(data: dict, destination: Path) -> None:
    """Guarda un JSON mediante escritura temporal."""

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = destination.with_suffix(".json.tmp")

    try:
        with temporary.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temporary.replace(destination)

    finally:
        temporary.unlink(missing_ok=True)


def extract_types(overwrite: bool = False) -> dict:
    """Descarga los 18 tipos principales."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(timezone.utc)

    report = {
        "resource": "type",
        "started_at": started_at.isoformat(),
        "finished_at": None,
        "expected_types": len(TYPE_IDS),
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "records": [],
    }

    with PokeAPIClient() as client:

        for type_id in TYPE_IDS:

            destination = RAW_DIR / f"{type_id}.json"

            if destination.exists() and not overwrite:

                print(f"[SKIP] Tipo {type_id}")

                report["skipped"] += 1

                report["records"].append({
                    "type_id": type_id,
                    "status": "skipped",
                })

                continue

            try:
                data = client.get_resource(
                    "type",
                    type_id,
                )

                if data.get("id") != type_id:
                    raise ValueError(
                        f"ID inesperado para tipo {type_id}"
                    )

                if not isinstance(
                    data.get("damage_relations"),
                    dict,
                ):
                    raise ValueError(
                        f"Relaciones ausentes: tipo {type_id}"
                    )

                save_json(data, destination)

                print(
                    f"[OK] {type_id}: {data['name']}"
                )

                report["success"] += 1

                report["records"].append({
                    "type_id": type_id,
                    "name": data["name"],
                    "status": "success",
                    "path": str(
                        destination.relative_to(ROOT)
                    ),
                })

            except (
                PokeAPIError,
                ValueError,
                OSError,
            ) as error:

                print(
                    f"[ERROR] Tipo {type_id}: {error}"
                )

                report["failed"] += 1

                report["records"].append({
                    "type_id": type_id,
                    "status": "failed",
                    "error": str(error),
                })

    report["finished_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    report_name = (
        "extraccion_types_"
        f"{started_at.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    )

    report_path = RESULTS_DIR / report_name

    save_json(report, report_path)

    print("\n=== RESUMEN DE TIPOS ===")
    print("Esperados:", len(TYPE_IDS))
    print("Descargados:", report["success"])
    print("Omitidos:", report["skipped"])
    print("Fallidos:", report["failed"])
    print("Reporte:", report_path)

    return report


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Extraer tipos Pokémon"
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribir archivos existentes",
    )

    args = parser.parse_args()

    extract_types(
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
