
"""
Fase 3 — Análisis de Datos
Generación reproducible de datos CLEAN.

Valida los CSV procesados y genera copias verificadas
sin modificar RAW ni PROCESSED.
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


def sha256_file(path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024), b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def validate_sources() -> dict:
    """Valida que las nueve tablas existan y sean legibles."""
    report = {}

    for name in TABLES:
        path = PROCESSED / f"{name}.csv"

        if not path.is_file():
            raise FileNotFoundError(
                f"No existe la tabla: {path}"
            )

        df = pd.read_csv(path)

        if df.empty:
            raise ValueError(
                f"La tabla {name} está vacía."
            )

        if df.isna().any().any():
            raise ValueError(
                f"La tabla {name} contiene valores nulos."
            )

        if df.duplicated().any():
            raise ValueError(
                f"La tabla {name} contiene duplicados exactos."
            )

        report[name] = {
            "rows": len(df),
            "columns": len(df.columns),
            "source_sha256": sha256_file(path),
        }

        print(
            f"[PASS] {name}: "
            f"{len(df)} filas, "
            f"{len(df.columns)} columnas"
        )

    return report


def build_clean(report: dict) -> None:
    """Copia los CSV validados sin modificar su contenido."""
    CLEAN.mkdir(parents=True, exist_ok=True)

    for name in TABLES:
        source = PROCESSED / f"{name}.csv"
        target = CLEAN / f"{name}.csv"

        # Preserva exactamente el contenido original.
        target.write_bytes(source.read_bytes())

        source_hash = report[name]["source_sha256"]
        target_hash = sha256_file(target)

        if source_hash != target_hash:
            raise RuntimeError(
                f"Error de integridad en {name}."
            )

        report[name]["clean_sha256"] = target_hash
        report[name]["hash_match"] = True

        print(f"[OK] CLEAN generado: {name}.csv")


def save_report(report: dict) -> None:
    """Guarda el reporte de generación."""
    RESULTS.mkdir(parents=True, exist_ok=True)

    output = RESULTS / "build_clean_report.json"

    payload = {
        "phase": "analisis_datos",
        "operation": "validated_copy",
        "tables": report,
        "total_tables": len(report),
        "all_hashes_match": all(
            item.get("hash_match", False)
            for item in report.values()
        ),
    }

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nReporte generado: {output}")


def main() -> None:
    print("=== VALIDACIÓN DE PROCESSED ===")
    report = validate_sources()

    print("\n=== GENERACIÓN DE CLEAN ===")
    build_clean(report)

    save_report(report)

    print("\n[PASS] Generación CLEAN completada.")


if __name__ == "__main__":
    main()
