import traceback
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from plex_client import PlexClient
from rdf_handler import PlexRDFHandler

app = FastAPI()


@app.get("/plex-rdf/section/{section_id}/account/{account_id}")
def download_rdf_file(section_id: int, account_id: int):
    """
    Gets structured datasets that represent Plex data and use it to creates a
    graph in the format of RDF.

    Args:
        section_id: int
        account_id: int

    Returns:
        Response: .ttl file
    """
    pc = PlexClient()
    genres_df, person_df, all_movie_df, history_df = (
        pc.create_structured_datasets(section_id, account_id)
    )

    rdf_handler = PlexRDFHandler()

    try:
        conforms, turtle_data = rdf_handler.to_ttl(
            genres_df, person_df, all_movie_df, history_df
        )
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        raise HTTPException(
            status_code=500, detail=f"{e}. Check console log for details."
        )

    status_code = 200
    file_name = "data.ttl"

    if not conforms:
        status_code = 400
        file_name = "error_report.ttl"

    return Response(
        status_code=status_code,
        content=turtle_data,
        media_type="text/turtle",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


@app.get("/library")
def get_plex_libraries():
    pc = PlexClient()
    return pc._get_libraries()


@app.get("/library/section/{section_id}")
def get_plex_sections(section_id: int):
    pc = PlexClient()
    result = pc._get_section_items(section_id)
    result.loc["Metadata", "MediaContainer"] = result["MediaContainer"][
        "Metadata"
    ][:3]

    return result


@app.get("/history/section/{section_id}/account/{account_id}")
def get_playback_history(section_id: int, account_id: int):
    pc = PlexClient()
    result = pc._get_playback_history(section_id, account_id)
    result.loc["Metadata", "MediaContainer"] = result["MediaContainer"][
        "Metadata"
    ][:3]
    return result
