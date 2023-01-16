from typing import Any, Callable


CONFIG_SET = "dev"
CONFIG_MAP: dict[str, dict[str, Any]] = {}
RESOURCE_MAP: dict[str, Any] = {}
METHOD_MAP: dict[str, Callable] = {}
