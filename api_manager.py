from newsapi import NewsApiClient
import tweepy
import replicate
from typing import Dict, Optional

from cachetools import TTLCache, cached
# from tweepy import Client
from config import Config
from logger import Logger

from utils import fetch_last_since_id

class APIManager:
    def __init__(self, config: Config, logger: Logger):
        # initializing the client class calls `ping` API endpoint, verifying the connection
        self.auth = tweepy.OAuthHandler(config.TWITTER_API_KEY,config.TWITTER_API_KEY_SECRET)
        self.auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
        self.twitter_api = tweepy.API(self.auth)   
        self.ds_model = replicate.Client(api_token=config.REPLICATE_API_KEY)
     
        # self.newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
        self.logger = logger
        self.config = config
        self.last_since_id()
        # self.cache = BinanceCache()
        # self.stream_manager: Optional[BinanceStreamManager] = None
        # self.setup_websockets()

    def last_since_id(self):
        self.config.SINCE_ID = fetch_last_since_id(self.logger,)

    @cached(cache=TTLCache(maxsize=1, ttl=43200))
    def check_connection(self) -> Dict[str, float]:
        return self.twitter_api

    # @cached(cache=TTLCache(maxsize=1, ttl=60))
    # def get_using_bnb_for_fees(self):
    #     return self.binance_client.get_bnb_burn_spot_margin()["spotBNBBurn"]
