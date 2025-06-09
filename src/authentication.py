from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEYS = {
    "test": "test_key_12345",
    "production": "prod_key_67890",
}

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=True,
)


async def authenticate(api_key: str = Security(api_key_header)) -> None:
    """
    Authenticate the provided API key.

    Args:
        api_key (str): The API key to authenticate.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    if api_key not in API_KEYS.values():
        raise HTTPException(status_code=403, detail="Invalid API key. Access denied.")
