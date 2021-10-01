from raven import Client
from app.core.config import settings
import faust


client_sentry = Client(settings.SENTRY_DSN)


app = faust.App(
    'hello-world',
    broker='kafka://kafkabroker:9092',
    value_serializer='raw',
)

greetings_topic = app.topic('greetings')

@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)