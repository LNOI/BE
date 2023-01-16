import logging
from src.const.global_map import RESOURCE_MAP
from fastapi.templating import Jinja2Templates
app_logger = logging.getLogger("app_logger")

app = RESOURCE_MAP["fastapi_app"]

templates = Jinja2Templates(directory='src/templates/')






