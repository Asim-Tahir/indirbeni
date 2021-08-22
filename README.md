# u/indirbeni
Source code for u/indirbeni reddit bot

## This is how I did it
I used a linux system btw.  
Therefore, some things are specifically written for linux (such as paths).  
This script uses the symbol ```~``` in paths to reference to user's home directory.  
You can change the paths according to your system differences.  

### I. Preparation
#### Quick Installation:
```
$ git clone https://github.com/oldventura/indirbeni.git
$ cd indirbeni
$ pip -r requirements.txt
```
#### More Stuff to Do:
1) Create a new reddit account
2) Create a reddit app in that account [here](https://old.reddit.com/prefs/apps/)
3) Take a note of the ```client id``` and ```client_secret``` of your newly created app
4) Create a subreddit only for this bot's use
5) Create a post on the subreddit or somewhere else for updates
6) Create a post on the subreddit for your links
7) Take a note of the submission id of your "links post":  
For instance, consider the following url: https://www.reddit.com/r/INDIRBENI/comments/ogk6aj/uindirbeni_links_megathread/  
The ```submission id``` in this case is the part where it says ```ogk6aj```
8) Take a note of the submission id of your "updates post"

### II. Configuration
1) Open the downloaded repository and locate ```main.py```
    #### Things to change in the script ```main.py```:
    1) Line 24: write down your path field: \<just write this part before indirbeni/>
    2) Line 30: write down your ```links post id``` in field: \<submission_id>
    3) Line 31: write down your ```updates post id``` in field: \<submission_id>
    4) Line 39: write down your client id in field: \<client_id>
    5) Line 40: write down your client secret in field: \<client_secret>
    6) Line 41: write down your username in fields: \<username>
    7) Line 42: write down your username in field: \<username>
    8) Line 43: write down your password in field: \<password>
2) If you want your system to run your bot script on startup, you can make it possible with crontab:  
    Run in terminal: ```crontab -e```  
    Modify the following line and add it to the last line in crontab:  
    ```@reboot /usr/bin/python3 ~/reddit_bot/main.py >> ~/log.txt  2>&1```
3) If you want to add replies, open up the ```replies.json``` file and add your string inside the array according to the json indentation (4 spaces).
    
That's it, have a nice time with your bot!  

### III. Upcoming Features
- [x] Better filenames with file index and hash
- [x] Random link requests

##### Freedom for lord!
