from pydantic.parse import Path

BASE_DIR = Path(__file__).resolve().parent
TESTDATA_DIR = Path(*[BASE_DIR / 'testdata' / 'data'])
SCHEMA_DIR = Path(*[BASE_DIR / 'testdata' / 'schema'])
UTILS_DIR = [BASE_DIR / 'utils']

SERVICE_URL = 'http://async_api:8000'
ELASTIC_HOST = 'http://elasticsearch:9200'