import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.kafka_app import synchronousSend, Greeting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 30  # 5 minutes
wait_seconds = 4

# TODO: fix pre start worker
@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        synchronousSend("boot", Greeting(from_name='Action Worker', to_name='Boot'))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing Action Worker")
    init()
    logger.info("Action Worker finished initializing")


if __name__ == "__main__":
    main()
