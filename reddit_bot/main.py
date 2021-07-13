#!/usr/bin/python3
#-*- encoding:utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import time
import praw
import json
import random
import requests
import youtube_dl
from praw.models import Message
from praw.models import Comment
from shutil import make_archive
from requests.exceptions import ConnectionError
from prawcore.exceptions import ServerError

print ("Starting bot...")
t = 0
while True:
  try:
    print (requests.get("https://ipv4.icanhazip.com").content.decode())
  except ConnectionError:
    print ("Connection Error: %s"%(t))
    t += 1
    continue
  break

reddit = praw.Reddit(
  client_id     = "<CLIENT ID>",
  client_secret = "<CLIENT SECRET>",
  user_agent    = 'User-Agent: linux:com.<BOT NAME>.<EXTRA NAME>:v1.0 (by u/<ACCOUNT USERNAME>)',
  username      = "<ACCOUNT USERNAME>",
  password      = "<ACCOUNT PASSWORD>",
)

ydl_opts   = {'outtmpl': '~/reddit_bot/downloaded/video.%(ext)s'}
CHUNK_SIZE =  10000000
ind        = 2749

with open('~/reddit_bot/replies.json',) as f:
  replies = json.load(f)['text']

def read_in_chunks(file_object):
  while True:
    data = file_object.read(CHUNK_SIZE)
    if not data:
      break
    yield data

def upload(path, file_name, file_type):
  f_size = os.stat(path).st_size
  print("video size:", f_size)
  response = requests.post('https://up.ufile.io/v1/upload/create_session', data={'file_size': f_size})
  parsed = json.loads(response.content)
  fuid = parsed['fuid']
  print("fuid:", fuid)

  with open(path, 'rb') as f:
    index = 1
    for chunk in read_in_chunks(f):
      data = {
          'chunk_index': index,
          'fuid': fuid
      }
      files = {
          'file': chunk
      }
      response = requests.post(
          'https://up.ufile.io/v1/upload/chunk', data=data, files=files)
      print(response.content, index)
      index += 1
  print("\nUpload done.\nChunk count:", index)

  data = {
      'fuid': fuid,
      'file_name': file_name,
      'file_type': file_type,
      'total_chunks': index-1,
  }

  response = requests.post('https://up.ufile.io/v1/upload/finalise', data=data)
  parsed = json.loads(response.content)
  url = parsed['url']
  return url[17:]

def do_image(item,url):
  file_type = url.rsplit(".")[-1]
  name      = item.submission.title.replace(".", "_") + '.%s' %(file_type)
  r         = requests.get(url)

  if os.path.exists("~/reddit_bot/downloaded/image.%s" %(file_type)):
    os.remove("~/reddit_bot/downloaded/image.%s" %(file_type))
  with open("~/reddit_bot/downloaded/image.%s" % (file_type), "wb") as f:
    f.write(r.content)

  url = "## https://uploadfiles.io/" + upload("~/reddit_bot/downloaded/image.%s" % (file_type), name, file_type)
  text = """Buyur u/%s, işte resim bağlantın yukarıda \^\^

Bu da gönderinin kendisi: [LINK](%s)""" %(item.author.name, item.submission.shortlink)
  comment = reddit.submission(id='<LINKS>').reply(url)
  comment.reply(text)

def do_gallery(item,url):
  for i in os.listdir("~/reddit_bot/gallery"):
    os.remove("~/reddit_bot/gallery/"+i)
  if os.path.exists("~/reddit_bot/images.zip"):
    os.remove("~/reddit_bot/images.zip")
  ind    = 0
  for i in item.submission.media_metadata.items():
      url = i[1]['p'][0]['u'].split("?")[0].replace("preview", "i")
      file_type = url.rsplit(".")[-1]
      r = requests.get(url)
      with open("~/reddit_bot/gallery/image_%s.%s" %(ind,file_type), "wb") as f:
        f.write(r.content)
      ind += 1
  f = make_archive('images', 'zip', root_dir='~/reddit_bot/gallery')
  url = "## https://uploadfiles.io/" + upload(f, 'images.zip', 'zip')
  text = """Buyur u/%s, işte galeri arşivin yukarıda \^\^

Bu da gönderinin kendisi: [LINK](%s)""" % (item.author.name, item.submission.shortlink)
  comment = reddit.submission(id='<LINKS>').reply(url)
  comment.reply(text)

def do_text(item):
  content = item.submission.selftext
  try:
    comment = reddit.submission(id='<LINKS>').reply(content)
    text = """Buyur u/%s, işte yazı yukarıda \^\^

Bu da gönderinin kendisi: [LINK](%s)""" %(item.author.name, item.submission.shortlink)
    comment.reply(text)
  except praw.APIException:
    comment = reddit.submission(id='<LINKS>').reply("Üzgünüm u%s, istediğin şeyi atamıyorum :(" %(item.author.name))

def do_video(item):
  url  = item.submission.url
  name = item.submission.title.replace(".","_") + '.mp4'

  if os.path.exists("~/reddit_bot/downloaded/video.mp4"):
    os.remove("~/reddit_bot/downloaded/video.mp4")
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

  url  = "## https://uploadfiles.io/" + upload('~/reddit_bot/downloaded/video.mp4', name, 'mp4')
  text = """Buyur u/%s, işte video bağlantın yukarıda \^\^

Bu da gönderinin kendisi: [LINK](%s)""" %(item.author.name, item.submission.shortlink)
  comment = reddit.submission(id='<LINKS>').reply(url)
  comment.reply(text)

def handleit(item):
  if item.submission.is_self:
    do_text(item)
  else:
    url = item.submission.url.split("?")[0].replace("preview", "i")
    if url.startswith("https://v.redd.it") or url.startswith("https://gfycat.com"):
      do_video(item)
    elif url.startswith("https://i.redd.it"):
      do_image(item,url)
    elif url.startswith("https://www.reddit.com/gallery"):
      do_gallery(item,url)
    else:
      item.reply("Ya şimdi nasıl söylesem, bu postun neresini indireyim ben amcık?")
  Comment.mark_read(item)

## START
while True:
  try:
    for item in reddit.inbox.unread(limit=None):
      print ("\nfrom:",item.author)
      print ("in:",item.context)
      print ("type:",item.type)
      print ("message:",item.body)

      if item.type == "username_mention":
        try:
          handleit(item)
        except Exception as e:
          if "No media found" in str(e):
            item.reply("Ya ben yamuluyorum ya da bu post'ta dikkate alınacak bir şey yok amk")
          else:
            print ("Error_message:",e)
          Message.mark_read(item)
      elif item.type == "post_reply":
        if item.submission.subreddit.display_name == "u_<ACCOUNT USERNAME>" or item.submission.subreddit.display_name == "KGBTR" or item.submission.subreddit.display_name == "<OWN SUBREDDIT NAME>":
          if item.author != "AutoModerator":
            item.reply(replies[random.randint(0,len(replies)-1)])
          Message.mark_read(item)
        else:
          if item.author != "AutoModerator":
            item.reply("Anam yabancılarla konuşma dedi, ne diyon lan sen öyle?")
        Message.mark_read(item)
      elif item.type == "comment_reply":
        if item.submission.subreddit.display_name == "u_<ACCOUNT USERNAME>" or item.submission.subreddit.display_name == "KGBTR" or item.submission.subreddit.display_name == "<OWN SUBREDDIT NAME>":
          if item.author != "AutoModerator":
            item.reply(replies[random.randint(0,len(replies)-1)])
        Message.mark_read(item)
      else:
        print(item.type)
        Message.mark_read(item)
    ind += 1
    if ind == 2750:
      reddit.submission("<UPDATES>").reply("Update: %s  Fully functional." %(time.strftime("%D %H:%M")))
      print("Fully functional.")
      ind = 0
  except ServerError as e:
    print("Got ServerError\n###")
    print(str(e))
    print("###")
