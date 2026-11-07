
"""
Prueba de conectividad y paginación de PokéAPI.
"""

from pokeapi_client import PokeAPIClient, PokeAPIError


def main():
    try:
        with PokeAPIClient() as client:

            print("=== PRUEBA 1: RECURSO INDIVIDUAL ===")

            pokemon = client.get_resource("pokemon", 25)

            print("ID:", pokemon["id"])
            print("Nombre:", pokemon["name"])
            print("Estadísticas:", len(pokemon["stats"]))
            print("Tipos:", len(pokemon["types"]))

            assert pokemon["id"] == 25
            assert pokemon["name"] == "pikachu"

            print("\n=== PRUEBA 2: PAGINACIÓN ===")

            results = client.get_paginated(
                resource="pokemon",
                limit=5,
                max_pages=2,
            )

            print("Registros recuperados:", len(results))

            for item in results:
                print("-", item["name"])

            assert len(results) == 10

            print("\n=== PRUEBAS COMPLETADAS ===")

    except (PokeAPIError, AssertionError) as exc:
        print("Error durante la prueba:", exc)
        raise


if __name__ == "__main__":
    main()
