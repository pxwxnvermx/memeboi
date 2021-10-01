#!/usr/bin/env python

from re import match
import praw
from prawcore.exceptions import PrawcoreException
import telebot
import time
import configparser
import os
import subprocess

from telebot.apihelper import ApiTelegramException

config = configparser.ConfigParser()
config.read("./config.ini")
praw_config = config['praw']
telebot_config = config['telebot']
memebot_config = config['memebot']

subreddit_list = "+".join(memebot_config["subreddit"].split(","))
match = memebot_config["match"].split(",")

reddit = praw.Reddit(
		client_id=praw_config["client_id"],
    	client_secret=praw_config["client_secret"],
    	user_agent=praw_config["user_agent"],
	)

memebot = telebot.TeleBot(token=telebot_config["token"])

def getMemes():
	print("[Fetching]")
	subreddit = reddit.subreddit(subreddit_list)
	submission = subreddit.rising()
	return submission

def download_video(url):
	command=['youtube-dl', '-g', url]
	result=subprocess.run(
		command,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		universal_newlines=True
		).stdout.split()
	print("[DL URL]: ", result)
	return result

def sendMemes():
	memes = getMemes()
	for meme in memes:
		url = meme.url
		_, extension = os.path.splitext(url)

		print("[Sending]: ",meme.title, meme.subreddit, meme.url)
		try:
			if(extension == ".jpg" or extension == ".png" or extension == ".jpeg"):
				memebot.send_photo(
					chat_id=telebot_config["chat_id"],
					photo=meme.url,
					caption="{} r/{}".format(meme.title, meme.subreddit)
				)
			elif(extension == ".mp4" or extension == ".gif" or extension == ".gifv"):
				memebot.send_video(
					chat_id=telebot_config["chat_id"],
					data=download_video(meme.url)[0],
					caption="{} r/{}".format(meme.title, meme.subreddit)
				)
			elif(x in meme.url for x in match):
				memebot.send_video(
					chat_id=telebot_config["chat_id"],
					data=download_video(meme.url)[1],
					caption="{} r/{}".format(meme.title, meme.subreddit)
				)
			else:
				memebot.send_message(
					chat_id=telebot_config["chat_id"],
					text=meme.title + "\n" +meme.url
				)
				print(meme.subreddit)
		except PrawcoreException:
			print("[Failed]: Reddit")
		except ApiTelegramException:
			print("[Failed]: Telegram")
		except IndexError:
			print("[Failed]")

		print("[Sent]")
		time.sleep(120)

def main():
	print("Bot Started")

	while True:
		sendMemes()

if __name__ == "__main__":
	main()