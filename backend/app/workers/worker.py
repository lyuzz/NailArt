from rq import Worker
from redis import Redis

from app.core.config import REDIS_URL, QUEUE_NAME
from app.core.logging import configure_logging


def main() -> None:
    configure_logging()
    redis_conn = Redis.from_url(REDIS_URL)
    worker = Worker([QUEUE_NAME], connection=redis_conn)
    worker.work()


if __name__ == "__main__":
    main()
