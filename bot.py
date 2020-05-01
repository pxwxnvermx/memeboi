#!/usr/bin/python

import praw
import random as rnd
import telebot
import datetime,threading
import configparser

config = configparser.ConfigParser()
config.read("telegrambot.ini")
token = config['telegram']['token']
chatId = config['telegram']['chat_id']

print("Bot Started")

subr = "+".join(["memes","dankmemes","softwaregore"])
print(subr)

memes = []

reddit = praw.Reddit('memeboi')

memebot = telebot.TeleBot(token=token)

def getMemes():
	subreddit = reddit.subreddit(subr)
	submission = subreddit.random()
	print(subreddit.display_name)
	return(submission.title,submission.url)


def sendMemes():
	print("Meme Coming",datetime.datetime.now())
	meme = getMemes()
	memebot.send_photo(
		chat_id=chatId,
		photo=meme[1],
		caption=meme[0]
	)		
	threading.Timer(10,sendMemes).start()

sendMemes()