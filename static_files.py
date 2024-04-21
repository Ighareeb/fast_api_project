# Auto serve static files from a dir
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# mounting means adding a complete independent FastAPI app in a specific path, that handles all its sub-paths. Different to APIRouter as mounted app is completely independent. Auto-generated docs won't include/show anything from the mount app
# where /static refers to sub-path this sub-app will be mounted on. So any path that starts with /static will be handled by it (similar to router)
# where directory='static' is dir name where static files located and name is what FastAPI uses internally.
