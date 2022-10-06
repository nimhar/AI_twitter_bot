# AI Twitter bot
> AI-reply-tweets bot in any language. 

## Follow me on Twitter :)

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40WhatAIthinks)](https://twitter.com/WhatAIthinks)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40harel_nimrod)](https://twitter.com/harel_nimrod)

## Tool Setup

### Install Python dependencies

Run the following line in the terminal: `pip install -r requirements.txt`.

### Create user configuration

Insert your tokens in the config.py file or edit the usr.cfg file. 
Create a .cfg file named `user.cfg` based off `.user.cfg.example`.

**The configuration file consists of the following fields:**

-   **api_key** - Twitter API key generated in the Binance account setup stage.
-   **api_secret_key** - Binance secret key generated in the Binance account setup stage.
-   **t_api_key** - Twitter API key generated in the twitter developer portal.
-   **t_api_key_secret** - Twitter API secret-key generated in the twitter developer portal.
-   **t_access_token** - Twitter API access token generated in the twitter developer portal.
-   **t_access_token_secret** - Twitter API secret-access token generated in the twitter developer portal.
-   **t_user_name** - Twitter username of the authenticator user.
-   **openai_api_key** - OPENAI API key generated in the openai website.
-   **telegram_api_key** - Telegram API key generated in the telegram website. (for notification only)


### Notifications with Apprise

Apprise allows the bot to send notifications to all of the most popular notification services available such as: Telegram, Discord, Slack, Amazon SNS, Gotify, etc.

To set this up you need to create a apprise.yml file in the config directory.

There is an example version of this file to get you started.

If you are interested in running a Telegram bot, more information can be found at [Telegram's official documentation](https://core.telegram.org/bots).

### Run

```shell
python -m twitter_bot
```

## Acknolegment
The bot structure is heavily aided by binance-trade-bot which you may find in here: [watch this repo](https://github.com/edeng23/binance-trade-bot/subscription)


## Support the Project

<a href="https://www.buymeacoffee.com/nimrodharel?new=1" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
