import requests
from typing import Dict, List, Any, Optional

import os

BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://supply-risk-api.onrender.com"
)

TIMEOUT = 240


class APIClientError(Exception):
    """Custom exception for frontend API failures."""
    pass


def _handle_response(response: requests.Response) -> Any:
    """
    Validate HTTP response and safely parse JSON.
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise APIClientError(
            f"Backend request failed: {response.status_code} - {response.text}"
        ) from e

    try:
        return response.json()
    except ValueError as e:
        raise APIClientError("Invalid JSON response from backend.") from e


def get_health() -> Dict[str, Any]:
    """
    Fetch backend health status.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        raise APIClientError(
            f"Unable to connect to backend health endpoint: {str(e)}"
        ) from e


def analyze_region(region: str) -> Dict[str, Any]:
    """
    Run AI risk analysis for a single region.
    """
    if not region.strip():
        raise APIClientError("Region cannot be empty.")

    payload = {
        "region": region.strip()
    }

    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            timeout=TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        raise APIClientError(
            f"Analysis request failed: {str(e)}"
        ) from e


def get_history() -> List[Dict[str, Any]]:
    """
    Fetch historical risk analyses.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/history",
            timeout=TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        raise APIClientError(
            f"Failed to fetch history: {str(e)}"
        ) from e


def get_critical_alerts() -> List[Dict[str, Any]]:
    """
    Fetch critical supply chain alerts.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/critical-alerts",
            timeout=TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        raise APIClientError(
            f"Failed to fetch critical alerts: {str(e)}"
        ) from e


def batch_analyze(regions: List[str]) -> List[Dict[str, Any]]:
    """
    Simulate batch analysis by repeatedly calling /analyze.
    """
    if not regions:
        raise APIClientError("No regions provided.")

    results = []

    for region in regions:
        try:
            result = analyze_region(region)
            results.append(result)

        except APIClientError as e:
            results.append({
                "region": region,
                "error": str(e)
            })

    return results