import json
import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from fuseki_helpers import (
    construct_relationships,
    get_graph,
    run_query,
    upload_graph,
    validate_graphs,
)
from plex_client import PlexClient
from rdf_handler import PlexRDFHandler
from typing import Dict

router = APIRouter()


@router.get("/fuseki/genres/most_watched")
def most_watched_genres():
    return run_query("genres_most_watched")


@router.get("/fuseki/movies/most_watched")
def most_watched_movies():
    return run_query("movies_most_watched")


@router.get("/fuseki/movies/last_watched")
def last_watched_movies():
    return run_query("movies_last_watched")


@router.get("/fuseki/movies/unwatched")
def unwatched_movies():
    return run_query("movies_unwatched")


@router.get("/fuseki/movies/filter/{movie_name}")
def filter_movies_by_name(movie_name: str):
    return run_query("movies_filter", movie_name)


@router.get("/fuseki/movies/most_watched/recommend")
def recommend_movies_based_on_most_watched_movie():
    most_watched_movies = run_query("movies_most_watched")
    top_watched = most_watched_movies["results"]["bindings"][0]["movie"][
        "value"
    ]
    return run_query("recommend_unwatched_by_relation", top_watched)


@router.get("/fuseki/movies/last_watched/recommend")
def recommend_movies_based_on_last_watched_movie():
    last_watched_movies = run_query("movies_last_watched")
    last_watched = last_watched_movies["results"]["bindings"][0]["movie"][
        "value"
    ]
    return run_query("recommend_unwatched_by_relation", last_watched)


@router.get("/fuseki/movies/most_watched/recommend/rewatch")
def recommend_rewatch():
    most_watched_movies = run_query("movies_most_watched")
    top_watched = most_watched_movies["results"]["bindings"][0]["movie"][
        "value"
    ]
    return run_query("recommend_watched_by_relation", top_watched)


@router.get("/fuseki/data/add")
def add_data(section_id: int, account_id: int) -> Dict:
    """
    Add datasets to fuseki: default, relationships, ontology, then
    validate them.

    Datasets are locked to a single Plex sectiona and a single account.

    Args:
        section_id: int
            It is the 'key' for a Plex library.
        account_id: int

    Returns:
        Dict

    Raises:
        HTTPException:
            If any file upload or validation fails.
    """
    pc = PlexClient()
    genres_df, person_df, all_movie_df, history_df = (
        pc.create_structured_datasets(section_id, account_id)
    )

    rdf_handler = PlexRDFHandler()

    try:
        turtle_data = rdf_handler.to_ttl(
            genres_df, person_df, all_movie_df, history_df
        )
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        raise HTTPException(
            status_code=500, detail=f"{e}. Check console log for details."
        )

    # Add main graph
    data_add_response = upload_graph(turtle_data)
    if not data_add_response.ok:
        raise HTTPException(
            status_code=data_add_response.status_code,
            detail=data_add_response.text,
        )

    # Add ontology graph
    with open("/app/rdf/ontology.ttl") as f:
        ontology = f.read()
    f.close()
    ont_add_response = upload_graph(ontology, "ontology")
    if not ont_add_response.ok:
        raise HTTPException(
            status_code=ont_add_response.status_code,
            detail=ont_add_response.text,
        )

    # Add relationships graph... made by SPARQL query and not python logic.
    relations_response = construct_relationships()
    if relations_response.status_code != 204:
        raise HTTPException(
            status_code=relations_response.status_code,
            detail=relations_response.text,
        )

    # Concat main and relationships graph for easier validation.
    default_graph = get_graph()
    relations_graph = get_graph("relations")
    graphs = default_graph + relations_graph
    conforms, report_graph = validate_graphs(graphs, ["default", "relations"])
    if not conforms:
        return Response(
            status_code=400,
            content=report_graph,
            media_type="text/turtle",
            headers={
                "Content-Disposition": "attachment; filename=error_report.ttl"
            },
        )

    return {
        "ontology": json.loads(ont_add_response.text),
        "data": json.loads(data_add_response.text),
        "relationships": "Successfully built.",
    }
