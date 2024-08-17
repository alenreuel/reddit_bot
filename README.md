# AI assistant reddit bot. 

## Contents of the Repo

1) reddit_bot.py: Contains the logic behind which the bot operates.
2) run_bot.py: Simple script to run the bot.
3) config.txt: Details to be entered.
4) sqlite database that acts as the bot's memory.(not shown in this repository)

## Project Overview

### Summary
This project demonstrates how one can use generative AI to power a social media bot. In this case, I developed a personal AI assistant bot which can be used to ask questions about a post on reddit. An example of it's application is shown here:

![show](https://github.com/user-attachments/assets/a4965fbb-3ce1-45e4-8ec2-5618249c60ef)

### Mechanics

The following tools have been used for the project:
1) Ollama: Platform to download and interact with LLMs locally. [Learn More](https://ollama.com/)
2) praw: Reddit API wrapper [Learn More](https://praw.readthedocs.io/en/stable/)

The program uses praw library(A reddit API wrapper) to serach through the comments made by a user where it has been tagged. If the bot's username is tagged then it will use the reddit submission as context and answers any questions using Llama 3 api via Ollama. The bot will then reply to the comment with it's AI generated answer.

#### How to use?

Step 1: Enter all details in config.txt. \
Step 2: Run run_bot.py \
Step 3: Comment on any reddit post to test it out! \

Thank you!

