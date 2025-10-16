from fastapi import FastAPI
from fastapi.responses import Response
from plex_client import PlexClient
from rdf_handler import PlexRDFHandler

app = FastAPI()


@app.get("/plex-rdf")
def download_rdf_file():
    """
    Gets structured datasets that represent Plex data and use it to creates a
    graph in the format of RDF.

    Returns:
        Response: .ttl file
    """
    pc = PlexClient()
    genres_df, person_df, all_movie_df = pc.create_structured_datasets()

    rdf_handler = PlexRDFHandler()
    turtle_data = rdf_handler.to_ttl(genres_df, person_df, all_movie_df)

    return Response(
        content=turtle_data,
        media_type="text/turtle",
        headers={"Content-Disposition": "attachment; filename=data.ttl"},
    )


@app.get("/libraries")
def get_plex_libraries():
    pc = PlexClient()
    return pc._get_libraries()


@app.get("/get-plex-section/{secion_id}")
def get_plex_sections(section_id: str):
    pc = PlexClient()
    return pc._get_section_items(section_id)
