poetry self add pydantic-settings ???

docker run -d --rm -p 5672:5672 --name test-mq rabbitmq:alpine

poetry run faststream run backend.main:app
poetry run pytest

faststream docs gen backend.main:app
faststream docs serve backend.main:app

