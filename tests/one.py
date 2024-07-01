import os
from dotenv import load_dotenv
from pathlib import Path

project_dir = Path(__file__).parent
# load_dotenv(dotenv_path=project_dir+".env.test")
path_conf = Path.joinpath(project_dir.absolute(), ".env.test").as_posix()
load_dotenv(dotenv_path=path_conf)
print(os.getenv('APP_DB_URL_TEST'))
print(Path.joinpath(project_dir.absolute(), "migrations").as_posix())