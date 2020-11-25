import os

ADDR_RUN_LANG_PY = os.environ.get("ADDR_RUN_LANG_PY")
ADDR_RUN_LANG_JS = os.environ.get("ADDR_RUN_LANG_JS")
ADDR_RUN_LANG_CPP = os.environ.get("ADDR_RUN_LANG_CPP")

RUN_LANG_TABLE = {
    "python": ADDR_RUN_LANG_PY,
    "javascript": ADDR_RUN_LANG_JS,
    "cpp": ADDR_RUN_LANG_CPP,
}
