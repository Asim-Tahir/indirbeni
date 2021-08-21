#!/usr/bin/python3
#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import time
import praw
import random
from praw.models import Message
from praw.models import Comment
from praw.models import MoreComments
from requests.exceptions import ConnectionError
from prawcore.exceptions import ServerError

links = []

reddit = praw.Reddit(
  client_id     = "<client_id>",
  client_secret = "<client_secret>",
  user_agent    = 'User-Agent: linux:com.<username>.runner:v1.0 (by /u/<username>)',
  username      = "<username>",
  password      = "<password>",
)

try:
  submission = reddit.submission(id="<submission_id>") # Where you post your links
  submission.comment_sort = 'new'
  for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
      continue
    for i in top_level_comment.body.split():
      if "https://uploadfiles.io" in i:
        links.append(i)

  print("\n".join(links))
except:
  print("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
