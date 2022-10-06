#!python3
import time

from api_manager import APIManager
from config import Config
from logger import Logger
from scheduler import SafeScheduler
from utils import run_mentions, run_reply, run_tweet

def main():
    logger = Logger()
    logger.info("Initializing the AUTO-TWEET BOT")

    config = Config()
    manager = APIManager(config, logger)
    # check if we can access API feature that require valid config
    try:
        _ = manager.check_connection()
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Couldn't access API - API keys may be wrong or lack sufficient permissions")
        logger.error(e)
        return

    schedule = SafeScheduler(logger)
    # schedule.every(int(config.TWEET_SLEEP_TIME)).seconds.do(run_tweet, manager, logger, config).tag("tweet")
    schedule.every(20).minutes.do(run_reply, manager, logger, config).tag("reply or retweet")
    schedule.every(1).minutes.do(run_mentions, manager, logger, config).tag("check for mentions")
    # schedule.every(int(config.REPLY_SLEEP_TIME)).seconds.do(run_reply, manager, logger, config).tag("reply or retweet")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        # manager.stream_manager.close()
        logger.info('END')
        print('END')
