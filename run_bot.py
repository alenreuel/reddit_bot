import reddit_bot
import time
import requests



# check if internet is operational 


# outer-loop: checks for internet connection
# inner-loop: first logs in and the bot runs forever/ until the user does 
# not want it to run :) 
while True:
    random_url = "https://www.reddit.com/"
    timeout = 10
    try:
        # requesting URL
        request = requests.get(random_url,timeout=timeout)
        # if runs through without issues, run main code block
        x = reddit_bot.RedditAIBot()
        while True:
            x.check_mentions()
            time.sleep(30) 
 
    # catching exception for when internet is not running
    except (requests.ConnectionError,requests.Timeout) as exception:
        time.sleep(300)
    