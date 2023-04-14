import logging
import pathlib

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services import nmap

LOG = logging.getLogger(__name__)

ROOT_DIR = pathlib.Path(__file__).parent
API_RESOURCES_DIR = pathlib.Path(ROOT_DIR, "api")
HOST = "0.0.0.0"
PORT = 8000
API_URL = f"http://{HOST}:{PORT}"
OPEN_AI_URL = "https://chat.openai.com"


app = FastAPI(
    title="Developer Chat GPT Plugin",
    description="A ChatGPT plugin for the Developer Chat",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        API_URL,
        OPEN_AI_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
def serve_manifest():
    return FileResponse(pathlib.Path(API_RESOURCES_DIR, "ai-plugin.json"))


@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi_yaml():
    yaml_file = pathlib.Path(API_RESOURCES_DIR, "openapi.yaml")
    if not yaml_file.exists():
        LOG.error(f"Could not find {yaml_file}")
        with open(yaml_file, "w") as f:
            openapi_json = app.openapi()
            openapi_json["servers"] = [{"url": "http://localhost:8000"}]
            openapi_yaml = yaml.dump(openapi_json)
            LOG.info(f"Writing {yaml_file}")
            f.write(openapi_yaml)

    return FileResponse(yaml_file)


@app.get("/logo.png", include_in_schema=False)
def get_logo():
    return FileResponse(
        pathlib.Path(API_RESOURCES_DIR, "tibber-logo-small.png"), media_type="image/png"
    )


@app.get("/nmap/list-hosts")
def list_hosts():
    return nmap.list_hosts()


@app.get("/ping", include_in_schema=False)
def ping():
    return "pong"


if __name__ == "__main__":
    print(f"Starting API server at {API_URL}")
    uvicorn.run(app, host=HOST, port=PORT)
