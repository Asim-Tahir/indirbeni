# u/indirbeni
Source code for u/indirbeni reddit bot

## This is how I did it
I used a linux system btw.  
Therefore, some things are specifically written for linux (such as paths)  
This script uses the symbol ```~``` in paths to reference to user's home directory.  
You can change the paths according to your system differences.  

### Preparation
1) Clone the repository into your home folder
2) change directory to the repository folder
3) ```pip -r requirements.txt```
4) Create a new reddit account
5) Create a reddit app in that account [here](https://old.reddit.com/prefs/apps/)
6) Take a note of the ```client id``` and ```client``` secret of your newly created app
7) Create a subreddit only for this bot's use
8) Create a post on the subreddit or somewhere else for updates
9) Create a post on the subreddit for your links
10) Take a note of the submission id of your links post:  
For instance, consider the following url: https://www.reddit.com/r/INDIRBENI/comments/ogk6aj/uindirbeni_links_megathread/  
The ```submission id``` in this case is the part where it says ```ogk6aj```
9) Take a note of the submission id of your updates post

### Configuration
1) Open the downloaded repository and locate ```main.py```
    #### Things to change in the script ```main.py```:
    1) Line 30: write down your ```client id``` in field: <CLIENT ID>
    2) Line 31: write down your ```client secret``` in field: <CLIENT SECRET>
    3) Line 33: write down your account username in field: <ACCOUNT USERNAME>
    4) Line 34: write down your account password in field: <ACCOUNT PASSWORD>
    5) Line 101: write down your submission id of your links post in field: <LINKS>
    6) Line 122: write down your submission id of your links post in field: <LINKS>
    7) Line 128: write down your submission id of your links post in field: <LINKS>
    8) Line 149: write down your submission id of your links post in field: <LINKS>
    9) Line 204: write down your submission id of your updates post in field: <UPDATES>
2) If you want your system to run your bot on startup, you can make it possible crontab:
   
