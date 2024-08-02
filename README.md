??? poetry self add pydantic-settings

docker run -d --rm -p 5672:5672 --name test-mq rabbitmq:alpine

poetry run faststream run backend.main:app
poetry run pytest

faststream docs gen backend.main:app
faststream docs serve backend.main:app


durable - свойство назначается для каждого элемента отдельно:
exch, pub, sub, message=persist


.env:
1. ENV=.test.env faststream run serve:app
в config создается объект settings = Settings(_env_file=os.getenv("ENV", ".env"))
2. faststream run backend.main:app --env .env.test
в параметры lifespan передается аргумент env
в lifespan создается объект settings = Settings(_env_file=env)
объект помещается в контекст context.set_global("settings", settings)
