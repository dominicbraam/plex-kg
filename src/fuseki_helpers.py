import json
import requests
from pyshacl import validate
from rdflib import Graph
from typing import Dict, List


base = "http://fuseki:3030/plex"
headers = {
    "Accept": "application/json",
}


def get_graph(graph_identifier: str = "") -> Graph:
    """
    Download graph from fuseki.

    Args:
        graph_identifier: str
            Leave empty for the default graph.
            Other options: "relations"

    Returns:
        Graph
    """
    url = f"{base}/data"
    if graph_identifier:
        # Select graph other than default
        graph_param = f"http://plex-kg/{graph_identifier}"
    else:
        graph_param = "default"

    result = requests.get(
        url,
        params={"graph": graph_param},
        headers={**headers, "Accept": "text/turtle"},
        auth=("admin", "admin"),
    )
    result.raise_for_status()

    return Graph().parse(data=result.text, format="turtle")


def _post(path: str, data: str) -> Dict:
    """
    HTTP POST request template.

    Args:
        path: str
            Either /data, /query
        data: str
            File content

    Returns:
        pd.DataFrame: result from request.
    """
    url = f"{base}{path}"
    result = requests.post(url, data=data, headers=headers, timeout=10)
    result.raise_for_status()

    return json.loads(result.text)


def run_query(query_name: str) -> Dict:

    query_path = f"/app/rdf/queries/{query_name}.rq"
    with open(query_path) as f:
        file_contents = f.read()
    f.close()

    query = file_contents

    data = {"query": query}

    result = _post("/query", data)
    return result


def construct_relationships() -> Dict:
    """
    Construct relationships on the default graph with Plex data
    using a SPARQL update query.

    Returns:
        Dict
    """
    query_path = "/app/rdf/queries/construct_relationships.rq"
    with open(query_path) as f:
        file_contents = f.read()
    f.close()

    result = requests.post(
        f"{base}/update",
        data=file_contents,
        headers={
            **headers,
            "Content-Type": "application/sparql-update",
        },
        auth=("admin", "admin"),
        timeout=10,
    )

    return result


def upload_graph(data: str, name: str = "") -> Dict:
    """
    Uoload graph to fuseki.

    Args:
        data: str
            Graph as ttl string.
        name: str
            Leave empty for default graph.

    Returns:
        Dict
    """
    url = f"{base}/data"
    if name:
        # Add to another graph other than default
        url = f"{url}?graph=http://plex-kg/{name}"

    result = requests.put(
        url,
        data=data,
        headers={**headers, "Content-Type": "text/turtle"},
        auth=("admin", "admin"),
        timeout=10,
    )

    return result


def validate_graphs(graphs: Graph, identifiers: List[str]) -> (bool, str):
    """
    Validate graphs with multiple

    Args:
        graphs: Graph
            Concatenated graphs.
        identifiers: List[str]
            Identifiers used to get shape file.

    Returns:
        (bool, str)
    """
    shape_graph = Graph()
    for gi in identifiers:
        shape_file = f"/app/rdf/shapes/{gi}.ttl"
        shape_graph = shape_graph + Graph().parse(shape_file, format="turtle")

    conforms, report_graph, report_text = validate(
        data_graph=graphs,
        shacl_graph=shape_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )

    return conforms, report_graph.serialize(format="turtle")
