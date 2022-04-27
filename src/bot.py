#!/usr/bin/env python

import time

from praw import Reddit
from praw.exceptions import PRAWException
from praw.models import Submission
from telebot.apihelper import ApiTelegramException
from telebot.types import InputMediaPhoto

from utils import get_file_type


class Post:
    def __init__(self, post: Submission):
        self.post = post
        self.url = post.url
        self.caption = f"{post.title} r/{post.subreddit} {post.url}"

        if "/gallery/" not in post.url:
            self.type = get_file_type(self.url)
        else:
            self.type = "gallery"

    def send(self, telegram, chat_id):
        print(f"[Sending]: {self.caption}")

        if "/gallery/" in self.post.url:
            gallery = []
            for media in self.post.media_metadata.items():
                url = media[1]["p"][0]["u"]
                url = url.split("?")[0].replace("preview", "i")

                gallery.append(InputMediaPhoto(media=url))

            telegram.send_media_group(chat_id, media=gallery)
            telegram.send_message(chat_id, text=self.caption)
        elif self.type == "image":
            telegram.send_photo(
                chat_id,
                photo=self.url,
                caption=self.caption,
            )

        elif self.type == "video":
            telegram.send_video(
                chat_id,
                data=self.url,
                caption=self.caption,
                video=self.url,
            )
        else:
            telegram.send_message(chat_id, text=self.caption)


class Bot:
    def __init__(self, config, reddit: Reddit, telegram):
        self.config = config
        self.reddit = reddit
        self.telegram = telegram

    def _fetch(self):
        subreddit_list = "+".join(self.config.get("memebot", "subreddit").split(","))
        posts = self.reddit.subreddit(subreddit_list).hot()

        return posts

    def start(self):
        posts = self._fetch()

        for post in posts:
            post = Post(post=post)
            try:
                post.send(
                    telegram=self.telegram,
                    chat_id=self.config.get("telebot", "chat_id"),
                )

            except PRAWException as e:
                print(f"[Failed-Reddit]: {e}")
                continue

            except ApiTelegramException as e:
                print(f"[Failed-Telegram]: {e}")
                continue

            time.sleep(int(self.config.get("memebot", "breaktime")) * 60)
