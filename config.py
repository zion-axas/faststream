import logging
import os

from pydantic_settings import BaseSettings


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)d] %(module)s:%(lineno)d %(levelname)s - %(funcName)s() - %(message)s",
    )


class Settings(BaseSettings):
    TEST_ID: int = 0


settings = Settings(_env_file=os.getenv("ENV", ".env"))


# ENV=.local.env faststream run serve:app
# ENV=.test.env pytest
