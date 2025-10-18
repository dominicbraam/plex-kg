from fastapi import FastAPI
from routers.debug import router as debug
from routers.plex_kg import router as plex


app = FastAPI()
app.include_router(plex, tags=["Plex KG"])
app.include_router(debug, tags=["Debug"])
