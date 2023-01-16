import logging

from src.utils.load_method.load_utils import register_load_method
from src.utils.load_method.common_resource import load_json
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
logger = logging.getLogger("utils_logger")


@register_load_method
def init_db_engine(credential_path: str) -> Engine:
    """
    Create database engine

    Args:
        credential_path (str): relative path to credential file

    Returns:
        Engine: sqlalchemy engine
    """
    args = load_json(credential_path)

    username, password, host, port, dbname = args["username"], args["password"], args["host"], args["port"], args["dbname"]
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    timeout_config_string = f"-c statement_timeout={args['statement_timeout']}s"
    engine = create_engine(connection_string)

    return engine