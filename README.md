# Plex Knowledge Graph

Plex KG builds a knowledge graph from Plex media data, linking movies, genres, and people through semantic relationships. It enables querying and simple recommendations.

## Tools

- **PlexAPI**: collect Plex data.
- **rdflib**: extract/map Plex data to turtle only. Doesn't handle large graphs well because it runs in memory.
- **Fuseki**: handle RDF storage, query and reasoning.
- **FastAPI**: easily access user facing functions.

## Data Flow

1. Get data from Plex.
2. Transform Plex data to a graph in the Turtle format.
3. Validate graph against expected shape: `./rdf/shape.ttl`.

## Setup

Developed on Python 3.12.

1. Generate `X-Plex-Client-Identifier` for the python client. You can generate it in many different ways but I prefer to do it on the CLI using `uuidgen`.
2. Get your `authToken` by sending a request to `https://plex.tv/api/v2/users/signin` with the following items in your request body:
    - `X-Plex-Client-Identifier`: from step 1.
    - `login`: email
    - `password`: password
3. Add `X-Plex-Client-Identifier` and `authToken` to your `.env`.
4. You might need to change the permission for the directories inside `./fuseki-data/` to 100:100 (fuseki UID and GID).

```bash
chown -R 100:100 ./fuseki-data/*
```

## Run

```bash
docker compose up
```

**URLs:**

- `http://localhost:3030/` - Fuseki
- `http://localhost:8000/` - FastAPI

**Run queries using fuseki API:**

> [!NOTE]
> The docker compose automagically creates a dataset called 'plex' and will be used as the dataset throughout the project.

```bash
curl POST \
    --data-urlencode "query@{path-to-rq-file}" \
    http://localhost:3030/plex/query | jq
```

- If it's saying unauthorized, use curl's -u parameter: `curl -u user:pw ...`
- If you get an error saying that the URL doesn't support POST requests, ensure that the dataset name is correct.

## Limitations

To reduce the project's complexity, the media is limited to a single Plex section and a single user. Note: Movies and TV Shows can be considered Plex sections. The project was developed and tested using only movies so the other sections might not even work.

If you would like to see the available Plex sections, you can use the FastAPI endpoint `/library`, "Get Plex Libraries". I know... confusing names but that's Plex naming scheme. The section ID is called "key" in the dataset.

Another major limitation is that I did not implement any error handling... 😅 I just didn't feel like, lol. You can check docker logs to help clear any blockers you might have.

## Resources

- [Plex Media Server API](https://developer.plex.tv/)
- [rdflib Docs](https://rdflib.readthedocs.io/en/stable/)

> [!NOTE]
> Check out `prereqs.md` for some key points on Semantic Web.
