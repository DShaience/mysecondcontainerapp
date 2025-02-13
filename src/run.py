import streamlit

import streamlit.web.cli as stcli
import os, sys
from utils.consts import STREAMLIT_SERVER_MAX_UPLOAD_SIZE
os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = str(STREAMLIT_SERVER_MAX_UPLOAD_SIZE)


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("webapp/app.py"),
        "--global.developmentMode=false",
        "--browser.gatherUsageStats=false",
        "--server.address=0.0.0.0",
        # f"--server.port={DEFAULT_SERVER_PORT}",
    ]
    sys.exit(stcli.main())






