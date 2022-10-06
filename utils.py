import numpy as np
import openai
from dateutil.parser import parse
import re
import random
from googletrans import Translator
import math
import requests
import tweepy
import os

def run_tweet(manager, logger, config):
    #authentication
    api = manager.twitter_api
    # newsapi = manager.newsapi
    openai.api_key = config.OPENAI_API_KEY
    tweets = api.home_timeline()
    for tweet in tweets:
        if tweet.lang in config.LANG:
            logger.info(f'Tweet ID: {tweet.id}')
            logger.info(f'Tweet text: {tweet.text}')
            response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=clean_tweet(tweet.text),
                    temperature=float(config.TEMPERATURE),
                    max_tokens=int(config.MAX_TOKENS),
                    top_p=1,
                    frequency_penalty=0.1,
                    presence_penalty=0.1
                    )
            response = response.choices[0].text
            response = clean_tweet(response)
            try:
                if len(response)>1:
                    response += f" @{tweet.user.screen_name}"
                else:
                    raise Exception("Tweet is empty")
                logger.info(f"response: {response}")
                print('Are you sure? y/n:')
                if input()=='y':
                    if np.random.randint(10)>8:
                        api.update_status(status=response, in_reply_to_status_id=tweet.id)
                        logger.info('Response has been TWEETED')
                    # else:
                    #     api.retweet(id=tweet.id, )
                else:
                    logger.info('Response has been CENSORED')
            except:
                logger.info('The tweet has not been succeed.')

def run_mentions(manager, logger, config):
    api = manager.twitter_api
    model_api = manager.ds_model
    # model = model_api.models.get("stability-ai/stable-diffusion")
    # model = model_api.models.get("pixray/text2image")
    logger.info("Retrieving mentions")
    # config.TWEET_COUNT_TIME+=1
    # if config.TWEET_COUNT_TIME >int(config.REPLY_SLEEP_TIME):
    #     config.TWEET_COUNT_TIME=0
    #     run_reply(manager, logger, config)
    # keywords=["interesting, imagine"]
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=config.SINCE_ID).items():
        config.SINCE_ID = max(tweet.id, int(config.SINCE_ID))
        if tweet.lang!='en':
            translator = Translator()
            translation = translator.translate(tweet.text, dest='en')
            trigger = translation.text.lower()
        else:
            trigger = tweet.text.lower()
        if any(keyword in trigger for keyword in ['interesting']):
            logger.info(f"{tweet.user.screen_name} asked for a response")
            org_tweet = api.get_status(tweet.in_reply_to_status_id)
            response = tweet_process(org_tweet, api,  logger, config)
            update_status(response, tweet, api, logger,config, mode='mention')
        elif any(keyword in trigger for keyword in ['draw','drew','paint']):
            logger.info(f"{tweet.user.screen_name} asked for an image")
            org_tweet = api.get_status(tweet.in_reply_to_status_id)
            prompt = tweet_to_prompt(org_tweet, api,  logger, config)
            logger.info(f'Prompt for image is: {prompt}')
            # output = model.predict(prompt=prompt)
            
            upload_media_tweet(tweet, output, api, logger, config)

def run_reply(manager, logger, config):
    #authentication
    api = manager.twitter_api
    tweets = []
    while len(tweets)<=0:
        query = get_random_query(manager, logger, config)
        tweets = api.search_tweets(q=query, result_type='popular')
    tweet = tweets[0]
    response = tweet_process(tweet, api,  logger, config)
    if len(response)>1:
        if len(response) < 250 and np.random.randint(10)>9:
            update_status(response, tweet, api, logger, config, mode='retweet')
        else:
            update_status(response, tweet, api, logger, config)

def get_random_query(manager, logger, config):
    openai.api_key = config.OPENAI_API_KEY
    query = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Answer in a few words a random trendy topic to chat about: ",
                    temperature=float(config.TEMPERATURE),
                    max_tokens=int(config.MAX_TOKENS),
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0.2,
                    )
    query = query.choices[0].text
    logger.info(f'Sampled query: {query}')
    return query  


def upload_media_tweet(tweet, output, api, logger, config):
    url = output[0]
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        media = api.simple_upload(filename)
        api.update_status(status="AI draw this tweet", media_ids= [media.media_id_string], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        logger.info("Tweet has been draw!")
        os.remove(filename)
        logger.info(f"Since ID: {config.SINCE_ID}")
    else:
        logger.info("Unable to download image")

def tweet_to_prompt(tweet, api, logger, config):
    openai.api_key = config.OPENAI_API_KEY
    logger.info(f'Tweet ID: {tweet.id}')
    logger.info(f'Tweet text: {tweet.text}')
    if tweet.lang=='en':
        prompt = clean_tweet(tweet.text) 
    else:
        translator = Translator()
        translation = translator.translate(clean_tweet(tweet.text), dest='en')
        prompt = translation.text 
    response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Summarize \"{prompt}\" in less than fifteen words:",
                temperature=float(config.TEMPERATURE),
                max_tokens=int(config.MAX_TOKENS)-70,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.2,
                )
    response = response.choices[0].text
    response = translator.translate(clean_tweet(response), dest=translation.src).text if tweet.lang!='en' else response
    return response

    
def tweet_process(tweet, api, logger, config):
    emotional_bank = [
        'Sarcastic', 
        'Pungent',
        'Sharp', 
        'Cuspidal',
        'Cutting', 
        'Waspish',
        'Full of humor'
        'Funny',
        'Bizarre',
        'Witty',
        'Smart', 
        'Clever',
        'Creative'
        # 'Question', 
        # 'Dramatic', 
        # 'Tragic',
        # 'Axiomatic', 
        # 'Dogmatic', 
        # 'Scary', 
        # 'Sad', 
        # 'Weird', 
        # 'Straigth', 
        # 'Intelligent',
        # 'Emphaty', 
        # 'Angry',
        # 'Suspicious',
        # 'Admire',
        # 'Full of lust',
        # 'Full of love', 
        # 'Crazy',
        # 'Unique', 
        # ''
    ]
    openai.api_key = config.OPENAI_API_KEY
    if tweet.user.name != config.TWITTER_USER_NAME:
            logger.info(f'Tweet ID: {tweet.id}')
            logger.info(f'Tweet text: {tweet.text}')
            chosen_emotion=random.choice(emotional_bank)
            logger.info(f'Emotion: {chosen_emotion}')
            if tweet.lang=='en':
                prompt = clean_tweet(tweet.text) 
            else:
                translator = Translator()
                translation = translator.translate(clean_tweet(tweet.text), dest='en')
                prompt = translation.text 
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{chosen_emotion} response to \"{prompt}\"",
                temperature=float(config.TEMPERATURE),
                max_tokens=int(config.MAX_TOKENS),
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.2,
                )
            response = response.choices[0].text
            response = translator.translate(clean_tweet(response), dest=translation.src).text if tweet.lang!='en' else response
    return response

def update_status(response,tweet, api, logger, config, mode=False):
    n = 280 
    total=len(response)
    logger.info(f"response: {response}")
    if total>n:
        total_parts=int(math.ceil(total/n))
    
        words = iter(response.split())
        lines, current = [], next(words)
        for word in words:
            if len(current) + 1 + len(word) > n:
                lines.append(current)
                current = word
            else:
                current += " " + word

        lines.append(current)

        for a in range(total_parts):                       
            part=lines[a]
            try:
                if a==0:
                    # part = part + f" @{tweet.user.screen_name}"
                    result=api.update_status(status=part, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                else:
                    result=api.update_status(status=part,in_reply_to_status_id = tweetid , auto_populate_reply_metadata=True)

                tweetid=result.id
                    
                logger.debug(" - tweet sent: "+part)    
                    
            except:
                logger.error(" - Error while sending a Twitter")            
    else:
        try:
            if mode == 'retweet':
                    print(api.update_status(status=response, attachment_url=f"https://www.twitter.com/user/status/{tweet.id}"), auto_populate_reply_metadata=True)
                    logger.info('Response has been RE-TWEETED')     
            else:
                print(api.update_status(status=response, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True))
                if mode=='mention':
                    logger.info(f"Mention Reply: {response}")
                    logger.info(f"Since ID: {config.SINCE_ID}")
                # response = response + f" @{tweet.user.screen_name}"    
                else:
                    logger.info('Response has been TWEETED')           
                # logger.debug(" - tweet sent: "+part)    
            
        except Exception as e:
            logger.error(" - Error while sending a Twitter")            
           


def clean_tweet(tweet, response = True):
    tweet = re.sub('[a-zA-Z]*@[a-zA-Z]*','', tweet)
    # tweet = re.sub('[a-zA-Z]*[][a-zA-Z]*','', tweet)
    tweet = re.sub('[a-zA-Z]*pic.twitter[a-zA-Z]*','', tweet)
    # tweet = re.sub('[a-zA-Z]*.co/[a-zA-Z]*','', tweet)
    # tweet = re.sub('[a-zA-Z]*.com/[a-zA-Z]*','', tweet)
    # tweet = re.sub('[a-zA-Z]*://[a-zA-Z]*','', tweet)
    tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)
    tweet = tweet[:tweet.rfind('.')]
    try:
        tweet = ''.join(parse(tweet, fuzzy_with_tokens=True)[1])
    except:
        print('')    
    # tweet = ''.join(tweet.split('.')[:-1]) if len(tweet.split('.'))>1 else tweet
    return tweet


def fetch_last_since_id(logger):
    import pandas as pd
    df_log = pd.read_csv('logs/twitter_bot.log', on_bad_lines='skip')
    df_log = df_log.iloc[:,-1]
    df_log = df_log.dropna()
    return int(df_log.loc[df_log.str.contains('Since ID:')].iat[-1].split('Since ID: ')[-1])