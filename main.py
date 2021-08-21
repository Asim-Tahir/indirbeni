#!/usr/bin/python3
#-*- encoding:utf-8 -*-
from __future__ import unicode_literals
import os
import re
import sys
import time
import praw
import json
import random
import secrets
import requests
import youtube_dl
from praw.models import Message
from praw.models import Comment
from shutil import make_archive
from requests.exceptions import ConnectionError
from prawcore.exceptions import ServerError

class indirbeni:
  def __init__(self):
    self.ind        = 2749
    self.CHUNK_SIZE = 10000000
    self.path       = "<just write this part before indirbeni/>" # Absolute path to indirbeni, but remove indirbeni from the path string 
    self.NSFW       = {True:"### NSFW", False:""}
    self.f_index    = int(os.popen('cat %sindirbeni/index' %(self.path)).read())
    self.ydl_opts   = {'outtmpl': self.path + 'indirbeni/downloaded/video.%(ext)s'}
    self.subs       = ['KGBTR','ArsivUnutmaz','INDIRBENI','u_indirbeni','u_oldventura','Turkey','TurkeyJerky','BLKGM'] # Subreddit names
    self.help       = "```u/indirbeni``` :-: beni etiketlediğiniz içeriği indirip atıyorum\n\n```u/indirbeni help``` :-: kullanılabilir komutların listesini atıyorum\n\n```u/indirbeni random``` :-: rastgele bir içeriğin indirme linkini atıyorum\n\n```u/indirbeni wiki``` :-: rastgele bir wikipedia sayfasının linkini atıyorum\n\n```u/indirbeni porn``` :-: rastgele bir pornhub videosunun linkini atıyorum"
    self.links_id   = "<submission_id>" # Submission where you post links
    self.updates_id = "<submission_id>" # Submission where you post updates

    self.load_replies()
    self.check_internet()
    self.connect_to_reddit()

  def connect_to_reddit(self):
    self.reddit = praw.Reddit(
      client_id     = "<client_id>",
      client_secret = "<client_secret>",
      user_agent    = 'User-Agent: linux:com.<username>.runner:v1.0 (by /u/<username>)',
      username      = "<username>",
      password      = "<password>",
    )

  def check_internet(self):
    print ("Starting bot...")
    t = 0
    while True:
      try:
        print (requests.get("https://ipv4.icanhazip.com").content.decode())
      except ConnectionError:
        if t == 10000:
          os.system("reboot")
        print ("Connection Error: %s"%(t))
        t += 1
        continue
      break

  def load_replies(self):
    with open('%sindirbeni/replies.json' %(self.path),) as f:
      self.replies = json.load(f)['text']

  def format_url(self, url, title, nsfw):
    url = "## " + url + "\n\n%s\n\n%s" %(title, nsfw)
    return url

  def format_text(self, author, shortlink):
    text = "Buyur u/%s, işte resim bağlantın yukarıda \^\^\n\nBu da gönderinin kendisi: [LINK](%s)\n\n### -> [DONATE](https://ko-fi.com/indirbeni)" %(author, shortlink)
    return text

  def format_comment(self, url):
    cmt = "# [INDIR](%s)\n\n-\n\n##### -> [BAĞIŞ](https://ko-fi.com/indirbeni)" %(url)
    return cmt

  def random_porn(self):
    try:
      page = requests.get("https://www.pornhub.com/video/random").url
    except:
      page = "https://www.pornhub.com/view_video.php?viewkey=ph60f74690300a0"
    return "## [SURPRISE PORN](%s)" %(page)

  def random_wiki(self):
    try:
      page = requests.get("https://tr.wikipedia.org/wiki/%C3%96zel:Rastgele").url
    except:
      page = "https://tr.wikipedia.org/wiki/Mast%C3%BCrbasyon"
    return "## [SURPRISE WIKI](%s)" %(page)

  def random_link(self):
    try:
      with open("%sindirbeni/links.txt" %(self.path),"r") as s:
        s = s.read().splitlines()
        if len(s) >= 1:
          text = s[secrets.randbelow(len(s))]
    except FileNotFoundError:
      text = "https://www.youtube.com/watch?v=bSpqLqC7U6g"
    return "## [SURPRISE FILE](%s)" %(text)

  def read_in_chunks(self, file_object):
    while True:
      data = file_object.read(self.CHUNK_SIZE)
      if not data:
        break
      yield data

  def upload(self, path, file_name, file_type):
    f_size = os.stat(path).st_size
    print("video size:", f_size)
    response = requests.post('https://up.ufile.io/v1/upload/create_session', data={'file_size': f_size})
    parsed = json.loads(response.content)
    fuid = parsed['fuid']
    print("fuid:", fuid)

    with open(path, 'rb') as f:
      index = 1
      for chunk in self.read_in_chunks(f):
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
    self.f_index += 1
    os.popen("echo %s > %sindirbeni/index" %(self.f_index, self.path))
    return url[17:]

  def do_image(self, item,url):
    os.system("rm -f %sindirbeni/downloaded/*" %(self.path))
    file_type = url.rsplit(".")[-1]
    r         = requests.get(url)
    with open("%sindirbeni/downloaded/image.%s" % (self.path, file_type), "wb") as f:
      f.write(r.content)
    if os.listdir("%sindirbeni/downloaded" %(self.path)):
      f_name = os.listdir("%sindirbeni/downloaded" %(self.path))[0]
      f_ext = f_name.rsplit(".")[1]
    h    = os.popen("md5sum %sindirbeni/downloaded/%s" %(self.path, f_name)).read().split()[0][0:8]
    name = "file_" + str(self.f_index) + "-" + str(h) + '.%s'%(f_ext)
    image_url = "https://uploadfiles.io/" + self.upload("%sindirbeni/downloaded/image.%s" % (self.path, file_type), name, file_type)
    comment = self.reddit.submission(id=self.links_id).reply(self.format_url(image_url, item.submission.title, self.NSFW[item.submission.over_18]))
    posted_link = comment.reply(self.format_text(item.author.name, item.submission.shortlink))
    item.reply(self.format_comment(image_url))

  def do_gallery(self, item,url):
    os.system("rm -f %sindirbeni/gallery/*" %(self.path))
    os.system("rm -f %sindirbeni/images.zip" %(self.path))
    ind = 0
    for i in item.submission.media_metadata.items():
        url = i[1]['p'][0]['u'].split("?")[0].replace("preview", "i")
        file_type = url.rsplit(".")[-1]
        r = requests.get(url)
        with open("%sindirbeni/gallery/image_%s.%s" %(self.path, ind,file_type), "wb") as f:
          f.write(r.content)
        ind += 1
    f = make_archive('images_%s'%(self.f_index), 'zip', root_dir='%sindirbeni/gallery' %(self.path))
    gallery_url = "https://uploadfiles.io/" + self.upload(f, 'images_%s.zip'%(self.f_index), 'zip')
    comment = self.reddit.submission(id=self.links_id).reply(self.format_url(gallery_url, item.submission.title, self.NSFW[item.submission.over_18]))
    posted_link = comment.reply(self.format_text(item.author.name, item.submission.shortlink))
    item.reply(self.format_comment(gallery_url))

  def do_text(self, item):
    content = item.submission.selftext
    obj     = re.findall(r'https://reddit.com/link/.*/video/(.*)/player', content)
    if len(obj) > 0:
      video_url = "https://v.redd.it/" + str(obj[0])
      self.do_video((item, video_url))
      return
    try:
      comment = self.reddit.submission(id=self.links_id).reply(content)
      posted_link = comment.reply(self.format_text(item.author.name, item.submission.shortlink))
      item.reply(self.format_comment(comment.permalink))
    except praw.APIException:
      comment = self.reddit.submission(id=self.links_id).reply("Üzgünüm u%s, istediğin şeyi atamıyorum :(" %(item.author.name))

  def do_video(self, item):
    if type(item) == tuple:
      item, url = item
    else:
      url  = item.submission.url
    os.system("rm -f %sindirbeni/downloaded/*" %(self.path))
    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
      ydl.download([url])
    if os.listdir("%sindirbeni/downloaded" %(self.path)):
      f_name = os.listdir("%sindirbeni/downloaded" %(self.path))[0]
      f_ext = f_name.rsplit(".")[1]
    h    = os.popen("md5sum %sindirbeni/downloaded/%s" %(self.path, f_name)).read().split()[0][0:8]
    name = "file_" + str(self.f_index) + "-" + str(h) + '.%s'%(f_ext)
    video_url = "https://uploadfiles.io/" + self.upload('%sindirbeni/downloaded/video.%s' %(self.path, f_ext), name, f_ext)
    comment = self.reddit.submission(id=self.links_id).reply(self.format_url(video_url, item.submission.title, self.NSFW[item.submission.over_18]))
    posted_link = comment.reply(self.format_text(item.author.name, item.submission.shortlink))
    item.reply(self.format_comment(video_url))

  def handleit(self, item):
    if "u/indirbeni random" in item.body:
      item.reply(self.random_link())
    elif "u/indirbeni wiki" in item.body:
      item.reply(self.random_wiki())
    elif "u/indirbeni porn" in item.body:
      item.reply(self.random_porn())
    elif "u/indirbeni help" in item.body:
      item.reply(self.help)
    elif "u/indirbeni test" in item.body:
      item.reply(self.test)
    elif item.submission.is_self:
      self.do_text(item)
    else:
      url = item.submission.url.split("?")[0].replace("preview", "i")
      if url.startswith("https://v.redd.it") or url.startswith("https://gfycat.com"):
        self.do_video(item)
      elif url.startswith("https://i.redd.it"):
        self.do_image(item,url)
      elif url.startswith("https://www.reddit.com/gallery"):
        self.do_gallery(item,url)
      else:
        item.reply("Ya şimdi nasıl söylesem, bu postun neresini indireyim ben amcık?")
    Comment.mark_read(item)

if __name__== "__main__":
  x = indirbeni()
  while True:
    try:
      for item in x.reddit.inbox.unread(limit=None):
        print ("\nfrom:",item.author)
        print ("in:",item.context)
        print ("type:",item.type)
        print ("message:",item.body)

        if item.type == "username_mention":
          if item.submission.subreddit.display_name in x.subs:
            try:
              x.handleit(item)
            except Exception as e:
              if "No media found" in str(e):
                item.reply("Ya ben yamuluyorum ya da bu post'ta dikkate alınacak bir şey yok amk")
              else:
                print ("Error_message:",e)
          Message.mark_read(item)
        elif item.type == "post_reply":
          if item.submission.subreddit.display_name in ['u_indirbeni','KGBTR','INDIRBENI'] :
            if item.author != "AutoModerator":
              try:
                if item.body == "u/indirbeni random":
                  item.reply(x.random_link())
                else:
                  item.reply(x.replies[secrets.randbelow(len(x.replies))])
              except:
                pass
            Message.mark_read(item)
          else:
            if item.author != "AutoModerator":
              item.reply("Anam yabancılarla konuşma dedi, ne diyon lan sen öyle?")
          Message.mark_read(item)
        elif item.type == "comment_reply":
          if item.submission.subreddit.display_name in ['u_indirbeni','KGBTR','INDIRBENI']:
            if item.author != "AutoModerator":
              try:
                if item.body == "u/indirbeni random":
                  item.reply(x.random_link())
                else:
                  item.reply(x.replies[secrets.randbelow(len(x.replies))])
              except:
                pass
          Message.mark_read(item)
        else:
          print(item.type)
          Message.mark_read(item)
      x.ind += 1
      if x.ind == 2750:
        x.reddit.submission(x.updates_id).reply("Update: %s  Fully functional." %(time.strftime("%D %H:%M")))
        print("Fully functional.")
        x.ind = 0
    except Exception as e:
      print("Got Error\n###")
      print(str(e))
      print("###")
