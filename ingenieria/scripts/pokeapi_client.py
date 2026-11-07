
"""
Cliente HTTP reutilizable para PokéAPI.

Proyecto: Pokémon Team Recommender
Fase: 2 - Ingeniería de Datos

Responsabilidades:
- Consultar recursos JSON.
- Gestionar timeouts y errores HTTP.
- Aplicar reintentos con espera progresiva.
- Recuperar listados paginados.
"""

import logging
import time
from typing import Any
from urllib.parse import urlparse

import requests


LOGGER = logging.getLogger(__name__)


class PokeAPIError(Exception):
    """Error de consulta o procesamiento de PokéAPI."""


class PokeAPIClient:
    """Cliente HTTP para la API pública de Pokémon."""

    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(
        self,
        timeout: int = 20,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        request_delay: float = 0.2,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.request_delay = request_delay

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "pokemon-team-recommender/0.1",
                "Accept": "application/json",
            }
        )

    def _build_url(self, endpoint: str) -> str:
        """Construye y valida una URL de PokéAPI."""

        endpoint = endpoint.strip()

        if endpoint.startswith(("http://", "https://")):
            url = endpoint
        else:
            url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        parsed = urlparse(url)
        base = urlparse(self.BASE_URL)

        if (
            parsed.scheme != "https"
            or parsed.hostname != base.hostname
            or not parsed.path.startswith("/api/v2/")
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
        ):
            raise PokeAPIError(
                f"URL fuera del dominio permitido: {url}"
            )

        return url

    def get(self, endpoint: str) -> dict[str, Any]:
        """Consulta un recurso y devuelve su contenido JSON."""

        url = self._build_url(endpoint)

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                )

                if response.status_code == 404:
                    raise PokeAPIError(
                        f"Recurso no encontrado: {url}"
                    )

                if response.status_code == 429:
                    retryable = True

                elif 500 <= response.status_code <= 599:
                    retryable = True

                else:
                    retryable = False
                    response.raise_for_status()

                if retryable:
                    if attempt == self.max_retries:
                        raise PokeAPIError(
                            f"Error HTTP {response.status_code} "
                            f"después de {attempt + 1} intentos: {url}"
                        )

                    wait = self.backoff_factor * (2 ** attempt)

                    retry_after = response.headers.get(
                        "Retry-After"
                    )

                    if retry_after and retry_after.isdigit():
                        wait = max(wait, int(retry_after))

                    LOGGER.warning(
                        "HTTP %s. Reintentando en %.1f segundos.",
                        response.status_code,
                        wait,
                    )

                    time.sleep(wait)
                    continue

                data = response.json()

                if not isinstance(data, dict):
                    raise PokeAPIError(
                        f"Respuesta JSON inesperada: {url}"
                    )

                if self.request_delay > 0:
                    time.sleep(self.request_delay)

                return data

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ) as exc:
                if attempt == self.max_retries:
                    raise PokeAPIError(
                        f"Fallo de conexión después de "
                        f"{attempt + 1} intentos: {url}"
                    ) from exc

                wait = self.backoff_factor * (2 ** attempt)

                LOGGER.warning(
                    "Error de conexión. Reintentando en "
                    "%.1f segundos.",
                    wait,
                )

                time.sleep(wait)

            except requests.exceptions.HTTPError as exc:
                raise PokeAPIError(
                    f"Error HTTP no recuperable: {url}"
                ) from exc

            except requests.exceptions.JSONDecodeError as exc:
                raise PokeAPIError(
                    f"Respuesta JSON inválida: {url}"
                ) from exc

        raise PokeAPIError(
            f"No fue posible recuperar el recurso: {url}"
        )

    def get_resource(
        self,
        resource: str,
        identifier: int | str,
    ) -> dict[str, Any]:
        """Consulta un recurso mediante su ID o nombre."""

        return self.get(f"{resource}/{identifier}")

    def get_paginated(
        self,
        resource: str,
        limit: int = 100,
        max_pages: int | None = None,
    ) -> list[dict[str, Any]]:
        """Recupera resultados de un endpoint paginado."""

        if limit < 1:
            raise ValueError("limit debe ser mayor que cero")

        if max_pages is not None and max_pages < 1:
            raise ValueError("max_pages debe ser mayor que cero")

        results = []
        endpoint = f"{resource}?limit={limit}&offset=0"
        pages_read = 0

        while endpoint is not None:
            page = self.get(endpoint)

            if not isinstance(page.get("results"), list):
                raise PokeAPIError(
                    "La respuesta no contiene una lista 'results'"
                )

            results.extend(page["results"])
            pages_read += 1

            LOGGER.info(
                "Página %s recuperada. Registros acumulados: %s",
                pages_read,
                len(results),
            )

            if max_pages is not None and pages_read >= max_pages:
                break

            endpoint = page.get("next")

        return results

    def close(self) -> None:
        """Cierra la sesión HTTP."""

        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
