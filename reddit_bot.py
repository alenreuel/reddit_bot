import praw
import sqlite3
import re
import ollama


class RedditAIBot:
    """
    Class representing a Reddit bot powered by Llama3. The bot is able to take in the context of any reddit submission and
    answer any questions you might have about it.
    Instance Attributes
    -------------------
    1) reddit_bot: Crating an authorized reddit instance(requires Client_ID, Client_Secret, Password, Useragent, Username)
    2) reddit_bot_user_name: UserName of the reddit bot
    3) master_name: The user the bot acts as an assistant of.
    4) cache_con: Connection with a SQLite DB is used to create a table which holds the cache of all the comments that the bot has replied to.
    5) cache_cursor: Cursor to execute querys on the SQLite database.

    Methods
    -------
    1) __init__: Constructor of the class.
    2) __create_cache_memory: Helper function to create the cache table in the database.
    3) __comment_reply: Function which replies to the tagged comment.
    4) __llama3_response: Helper function to send inputs and recieve outputs from llama3 via Ollama API.
    5) 
    """
    def __init__(self):        
        """
        Constructor of the class.
        Parameters
        ----------
            None
        """
        bot_log_in_dict = self.__initialization()
        self.reddit_bot = praw.Reddit(client_id=bot_log_in_dict["CLIENT_ID"], client_secret=bot_log_in_dict["CLIENT_SECRET"], 
                             password=bot_log_in_dict["PASSWORD"], user_agent=bot_log_in_dict["USERAGENT"], 
                             username=bot_log_in_dict["USERNAME"]) 
        self.reddit_bot.read_only = False
        self.reddit_bot_user_name = bot_log_in_dict["USERNAME"]
        self.master_name = bot_log_in_dict["MASTER_USERNAME"]
        self.cache_con = sqlite3.connect(bot_log_in_dict["CACHE_DB_NAME"])
        self.cache_cursor = self.cache_con.cursor()
        self.__create_cache_memory()

    def __create_cache_memory(self):
        """
        Helper function to create the cache table in the database.
        Parameters
        ----------
            None
        """
        self.cache_cursor.execute("CREATE TABLE IF NOT EXISTS replied_comments(comment_id VARCHAR(1000));")
        self.cache_cursor.execute("CREATE TABLE IF NOT EXISTS failed_replies(comment_id VARCHAR(1000), reason VARCHAR(1000));")
        self.cache_con.commit()
    
    def __comment_reply(self, comment):
        """
        Function which replies to the tagged comment.
        Parameters
        ----------
            comment: comment object returned by praw library.
        """
        comment_obj = self.reddit_bot.comment(comment.id)
        context = comment_obj.submission.selftext
        reply_message = self.__llama3_response(context, comment.body)
        comment_obj.reply(reply_message)

    def __llama3_response(self, context, question):
        """
        Helper function to send inputs and recieve outputs from llama3 via Ollama API.
        Parameters
        ----------
            1) context
            2) question: question you want to ask with respect to the context
        """
        prefix = f"""I am using you as my assistant to answer any questions I have about a reddit post. Imagine you are my reddit assistant bot 
        and you must answer questions to me about the post I have submitted below. (Remember you are: {self.reddit_bot_user_name}) \n"""
        llm_input = prefix + f"Reddit Post Content: {context} \n" + f"Question: {question} \n" + "Please keep the answer human readable. Thank you!"
        response = ollama.chat(model='llama3', messages=[{ 'role': 'user', 'content': f"{llm_input}"}])
        final_response = response['message']['content'] + "\n" + f"\n Please Note: I am {self.master_name}'s AI assistant bot powered by Meta Llama3." 
        return final_response

    def __initialization(self):
        """
        Helper function to intialize the bot.
        Parameters
        ----------
            None
        """
        config_dict = {}
        with open("config.txt", "r") as config_file:
            for line in config_file:
                key, value = line.strip().split(": ", 1)

                value = value.strip('"')
                config_dict[key] = value

        return config_dict


    def check_mentions(self):    
        """
        Main function of the bot to check for comments made by master user and reply to them accordingly.
        Parameters
        ----------
            None
        """    
        master_redditor = self.reddit_bot.redditor(self.master_name)
        for comment in master_redditor.comments.new():
            if re.search(self.reddit_bot_user_name, comment.body):
                self.cache_cursor.execute(f"SELECT * from replied_comments WHERE comment_id='{comment.id}'")
                data= self.cache_cursor.fetchall()
                if len(data)>0:
                    continue
                else:
                    self.cache_cursor.execute("INSERT into replied_comments values (?)", (comment.id, ))
                    self.cache_con.commit()
                    try:
                        self.__comment_reply(comment)
                    except Exception as e:
                        self.cache_cursor.execute(f"INSERT into failed_replies values (?,?)", (comment.id, str(e)))
                        self.cache_con.commit()

    
    
    