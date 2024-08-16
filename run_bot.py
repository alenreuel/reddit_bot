import reddit_bot

x = reddit_bot.RedditBot()


while True:
    try:
        x.check_mentions()
    except:
        continue
    