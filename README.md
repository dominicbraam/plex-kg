# Plex Knowledge Graph

Plex KG transforms Plex media data into a connected web of knowledge, showing how the data can be linked, queried, and understood semantically.

## Tools

- PlexAPI: collect Plex data.
- rdflib: extract/map Plex data to turtle only. Doesn't handle large graphs well because it runs in memory.
- Fuseki: handle RDF storage, query and reasoning.
- FastAPI: easily access user facing functions.

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

URLs:

- `http://localhost:3030/` - Fuseki
- `http://localhost:8000/` - FastAPI

## Resources

- [Plex Media Server API](https://developer.plex.tv/)
- [rdflib Docs](https://rdflib.readthedocs.io/en/stable/)
