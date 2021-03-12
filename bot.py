#!/usr/bin/env python

import praw
import telebot
import time
import configparser
import os

config = configparser.ConfigParser()
config.read("telegrambot.ini")
token = config['telegram']['token']
chatId = config['telegram']['chat_id']

print("Bot Started")

subr = "+".join(["memes","dankmemes","softwaregore"])

memes = []

reddit = praw.Reddit('memeboi')

memebot = telebot.TeleBot(token=token)

def getMemes():
	subreddit = reddit.subreddit(subr)
	submission = subreddit.random()
	return(submission.title,submission.url)


def checkType(url):
	_, extension = os.path.splitext(url)
	if(extension == ".jpg" or extension == ".png" or extension == ".jpeg"):
		return True

def sendMemes():
	meme = getMemes()
	if(checkType(meme[1])):
		memebot.send_photo(
			chat_id=chatId,
			photo=meme[1],
			caption=meme[0]
		)	

while True:
	sendMemes()
	time.sleep(900)