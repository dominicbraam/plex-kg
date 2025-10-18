import pandas as pd
from fastapi import APIRouter
from plex_client import PlexClient
from typing import Dict

router = APIRouter()


@router.get("/library")
def get_plex_libraries() -> Dict:
    """
    Get all Plex libraries on Plex server.

    Returns:
        Dict
    """
    pc = PlexClient()
    return pc._get_libraries()


@router.get("/library/section/{section_id}")
def get_plex_sections(section_id: int) -> Dict:
    """
    Get the first 3 items in a Plex section.
    A plex section is locked to a content type like movies, tv shows, etc.

    Args:
        section_id: int
            This value can be found in the libraries data as the 'key'.

    Returns:
        Dict
    """
    pc = PlexClient()
    result = pc._get_section_items(section_id)
    result = pd.DataFrame(result)
    result.loc["Metadata", "MediaContainer"] = result["MediaContainer"][
        "Metadata"
    ][:3]

    return result


@router.get("/history/section/{section_id}/account/{account_id}")
def get_playback_history(section_id: int, account_id: int) -> Dict:
    """
    Get the first 3 items in the playback history for an account.

    Args:
        section_id: int
        account_id: int

    Returns:
        Dict
    """
    pc = PlexClient()
    result = pc._get_playback_history(section_id, account_id)
    result = pd.DataFrame(result)
    result.loc["Metadata", "MediaContainer"] = result["MediaContainer"][
        "Metadata"
    ][:3]

    return result
