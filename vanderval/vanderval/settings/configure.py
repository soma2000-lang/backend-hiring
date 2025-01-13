import os
from dotenv import load_dotenv

load_dotenv()

ENV_VAR_NAME = "ENV"
PRODUCTION = "PRODUCTION"
DEVELOPMENT = "DEVELOPMENT"
PRODUCTION_SETTINGS = "vanderval.settings.production"
DEVELOPMENT_SETTINGS = "vanderval.settings.development"
DEFAULT_SETTINGS = DEVELOPMENT_SETTINGS


def configure_settings_module():
    env = os.getenv(ENV_VAR_NAME, DEVELOPMENT).upper()

    django_settings_module = DEVELOPMENT_SETTINGS

    if env == PRODUCTION:
        django_settings_module = PRODUCTION_SETTINGS

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)