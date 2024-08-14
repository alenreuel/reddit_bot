import praw
import sqlite3
import re
import ollama


class RedditAIBot:

    def __init__(self):        
        bot_log_in_dict, master_user_name, cache_db = self.initialization()
        self.reddit_bot = praw.Reddit(client_id=bot_log_in_dict["CLIENT_ID"], client_secret=bot_log_in_dict["CLIENT_SECRET"], 
                             password=bot_log_in_dict["PASSWORD"], user_agent=bot_log_in_dict["USERAGENT"], 
                             username=bot_log_in_dict["USERNAME"]) 
        self.reddit_bot.read_only = False
        self.reddit_bot_user_name = bot_log_in_dict["USERNAME"]
        self.master_name = master_user_name
        self.cache_con = sqlite3.connect(cache_db)
        self.cahce_cursor = self.cache_con.cursor()
        self.__create_cache_memory()

    def __create_cache_memory(self):
        self.cahce_cursor.execute("CREATE TABLE IF NOT EXISTS replied_comments(comment_id VARCHAR(1000));")
        self.cache_con.commit()

    def check_mentions(self):        
        master_redditor = self.reddit_bot.redditor(self.master_name)
        for comment in master_redditor.comments.new():
            if re.search(self.reddit_bot_user_name, comment.body):
                self.cahce_cursor.execute(f"SELECT * from replied_comments WHERE comment_id='{comment.id}'")
                data= self.cahce_cursor.fetchall()
                if len(data)>0:
                    continue
                else:
                    self.__comment_reply(comment)
                    self.cahce_cursor.execute(f"INSERT into replied_comments values ('{comment.id}')")
                    self.cache_con.commit()

    def __comment_reply(self, comment, trigger_word):
        
        comment_obj = self.reddit_bot.comment(comment.id)
        context = comment_obj.submission.selftext
        reply_message = self.__llama3_response(context, comment.body)
        comment_obj.reply(reply_message)

    def __llama3_response(self, context, question):
        prefix = f"I am using you as my assistant to answer any questions about a reddit post. Imagine you are my reddit assistant bot and you must answer questions to me about the post I have submitted below. (Remember you are: {self.reddit_bot_user_name})\n"
        llm_input = prefix + f"Reddit Post Content: {context} \n" + f"Question: {question} \n" + "Please keep the answer human readable. Thank you!"
        response = ollama.chat(model='llama3', messages=[{ 'role': 'user', 'content': f"{llm_input}"}])
        final_response = response['message']['content'] + "\n" + f"\n Please Note: I am {self.master_name}'s AI assistant bot powered by Meta Llama3." 
        return final_response
    
    def initialization(self):
        
        bot_log_in_dict = {}
        bot_log_in_dict["CLIENT_ID"] =  input("Enter Client ID: ")
        bot_log_in_dict["CLIENT_SECRET"] =  input("Enter Client Secret: ")
        bot_log_in_dict["USERNAME"] =   input("Enter Bot's Username: ")
        bot_log_in_dict["PASSWORD"] =  input("Enter Bot's Password: ")
        bot_log_in_dict["USERAGENT"] = input("Enter the Bot's UserAgent: ")
        master_user_name =  input("Enter the Username of the person that the bot wants to serve as its master: ")
        cache_db = "bot_memory.db"  #input("Enter the name of the sqlite database where you want to store a memory of the bot's replies: ")

        return bot_log_in_dict, master_user_name, cache_db
