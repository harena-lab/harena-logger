from raven import Client
from app.core.config import settings
from app.core.celery_app import app, topic, Greeting


client_sentry = Client(settings.SENTRY_DSN)

@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f'Hello from {greeting.from_name} to {greeting.to_name}')

@app.timer(interval=10.0)
async def example_sender(app):
    await topic.send(
        value=Greeting(from_name='Faust', to_name='you').dumps()
    )