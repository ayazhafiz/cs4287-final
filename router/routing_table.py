import os

ADDR_RUN_LANG_PY = os.environ.get("ADDR_RUN_LANG_PY")
ADDR_RUN_LANG_JS = os.environ.get("ADDR_RUN_LANG_JS")
ADDR_RUN_LANG_CPP = os.environ.get("ADDR_RUN_LANG_CPP")
ADDR_RUN_LANG_RUST = os.environ.get("ADDR_RUN_LANG_RUST")

RUN_LANG_TABLE = {
    "python": ADDR_RUN_LANG_PY,
    "javascript": ADDR_RUN_LANG_JS,
    "cpp": ADDR_RUN_LANG_CPP,
    "rust": ADDR_RUN_LANG_RUST,
}
