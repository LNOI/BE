import sys
import logging
import logging.config
import signal
import uvicorn
from pathlib import Path

from src.const.global_map import CONFIG_SET, CONFIG_MAP, RESOURCE_MAP
from src.const import const_map as CONST_MAP
from src.const import config_map, resource_map
from src.api_endpoint import add_api
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
# os.chdir(Path(__file__).parent)

def sigterm_handler(signalNumber, frame):
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, sigterm_handler)
Path("logs").mkdir(parents=True, exist_ok=True)
Path("tmp").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        CONFIG_SET = sys.argv[1]

    config_map.load_all_config(CONFIG_SET, CONFIG_MAP)
    print(CONFIG_MAP['resource'])
    resource_map.load_all_resource(CONFIG_MAP, RESOURCE_MAP)
    print(CONFIG_MAP)
    print()
    print(RESOURCE_MAP)
    print()

    logging.config.dictConfig(CONFIG_MAP["logging"])
    logger = logging.getLogger("utils_logger")

    app = RESOURCE_MAP["fastapi_app"]
    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_api.add_api()
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    print(f"Run app at: {CONFIG_MAP['app']['host']}:{CONFIG_MAP['app']['port']}")
    config = uvicorn.Config(
            app,
            host=CONFIG_MAP["app"]["host"],
            port=CONFIG_MAP["app"]["port"],
            workers=4
    )
    server = uvicorn.Server(config)
    server.run()

