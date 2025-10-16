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

## Limitations

To reduce the project's complexity, the media is limited to a single Plex section and a single user. Note: Movies and TV Shows can be considered Plex sections. The project was developed and tested using only movies so the other sections might not even work.

If you would like to see the available Plex sections, you can use the FastAPI endpoint `/library`, "Get Plex Libraries". I know... confusing names but that's Plex naming scheme. The section ID is called "key" in the dataset.

Another major limitation is that I did not implement any error handling... 😅 I just didn't feel like, lol. You can check docker logs to help clear any blockers you might have.

## Resources

- [Plex Media Server API](https://developer.plex.tv/)
- [rdflib Docs](https://rdflib.readthedocs.io/en/stable/)
