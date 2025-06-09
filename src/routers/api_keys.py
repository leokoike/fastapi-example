from fastapi import APIRouter

from src.authentication import API_KEYS


router = APIRouter()


@router.get(
    "/api-keys",
    summary="List API Keys",
    description="Retrieve a list of available API keys.",
)
async def list_api_keys():
    """
    List all available API keys.
    """
    return API_KEYS
