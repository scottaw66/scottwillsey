---
title: "Pseudo-Automating the Listened to Podcasts List on My /now Page"
description: Using Python to retrieve and parse my Overcast listening history.
date: "2024-08-03T05:00:00-08:00"
keywords: ["automation", "blog", "programming", "python"]
slug: "podcast-history"
---
As you know, I have a [/now](/now) page that I update on occasion to let anyone who cares know what kinds of things I’m watching, reading, and eating at some random point in my life. So far, it’s been a very manual update process because I haven’t had time to start automating any of it until now.

I’ve taken inspiration from [Robb Knight](https://rknight.me)’s video [Using Eleventy to Gobble Up Everything I Do Online](https://www.youtube.com/watch?v=e_87IF7KGgo), particularly for the Overcast part of the automation process. I watched enough of the video to see Robb mention the extended version of the Overcast OPML file you can download from your Overcast account that includes episode history and decided to write a script that would automate downloading and parsing it for me.

Enter **overcast-history**, my python script for checking to see when I last downloaded the OPML file, getting a new copy if needed, and parsing it if a new copy was downloaded (or if I passed it the -f flag to force it to parse the local OPML file anyway).

You might be thinking “hold on here, Robb also wrote a Python script, don’t act like you’re inventing the wheel!”, and that’s a fair point. I actually thought he was manually downloading his OPML file until I finished the video today (after writing my own Python script). Now I realize he’s at a high level of automation on this task.

Another key difference between Robb’s approach and mine so far, besides the fact that our Python scripts are completely different[^1], is that I believe he creates a JSON file with it and consumes that as part of his site build process to completely automatically update his listen history.

In contrast to Robb, I’m not very automated with my [/now](/now) page yet. This python script is part of a collection of tools for quickly automating certain aspects of updating my site, which I build locally and ftp to my server. I haven’t decided yet how much I want to automate the build process again.

Therefore, with the understanding that this is ONLY an example of how to grab and parse information off the internet, and with the understanding that my Python coding skills are shaky at best, here’s my approach to getting recently listened to podcast episodes from my Overcast history into a Markdown list.

## overcast-history

You’ll see immediately that I’m a terrible Python programmer and that I have no idea what Python best practices are yet. I have 6 files to do this one simple task:

- constants.py (purpose of which should be self-evident)
- session.py (used to keep the overcast login active across modules)
- main.py (entry point script that gets run directly to make it all happen)
- oc_login.py (logs in to my Overcast account)
- oc_history.py (handles downloading the extended OPML file from my Overcast account)
- oc_opml_parse.py (parses the OPML file and gives me the recent list of podcast episodes I want)

```python title="constants.py"
ACCOUNT_URL = 'https://overcast.fm/account'
ACCOUNT_PATH = '/account'
LOGIN_URL = 'https://overcast.fm/login?then=account'
EMAIL = 'xxxxxxxxxx@gmail.com'
PASSWORD = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
LOGIN_PATH = '/login'
OPML_AGE_LIMIT_DAYS = 2
OPML_LINK = 'https://overcast.fm/account/export_opml/extended'
SUCCESS = 200
TOO_MANY_REQUESTS = 429
OPML_FILE_PATH = 'overcast_history.opml'
NUMBER_OF_EPISODES = 10
```

Right away I’ve made you cry. Yes, I have my Overcast account password in my constants file. THIS WILL BE REMEDIED SOON! I plan to use [keyring](https://pypi.org/project/keyring/) to fix this issue. Maybe. Probably.

```python title="session.py"
import requests

session = requests.Session()
```

This one creates a [requests](https://github.com/psf/requests) session object which can then be imported into any other modules that need to use requests to grab stuff. That’s it. There’s probably a way better way to do this that I should know about.

```python title="main.py"
#!/Users/scott/Scripts/python/venv/bin/python
import argparse
import os
from datetime import datetime, timedelta
import constants as const
from oc_history import load_oc_history
from oc_opml_parse import oc_opml_parse

p = argparse.ArgumentParser()
p.add_argument('-f', '--force', action='store_true', help='Force local OPML file parsing')

args = p.parse_args()

def file_is_old(file_path):
    if not os.path.exists(file_path):
        return True
    
    file_mod_date = os.path.getmtime(file_path)
    display_date = datetime.fromtimestamp(file_mod_date)
    print(f'OPML file created on {display_date.strftime("%Y-%m-%d")}')
    file_datetime = datetime.fromtimestamp(file_mod_date)
    print(f'file_datetime = {file_datetime}')
    stale_date = datetime.now() - timedelta(days=const.OPML_AGE_LIMIT_DAYS)
    print(f'stale_date = {stale_date}')
    
    return file_datetime < stale_date

def main():
    history_was_loaded = False
    if file_is_old(const.OPML_FILE_PATH):
        print(f'OPML file is older than {const.OPML_AGE_LIMIT_DAYS} days or doesn\'t exist. Downloading new data...')
        history_was_loaded = load_oc_history()
    else:
        print(f'OPML file is less than {const.OPML_AGE_LIMIT_DAYS} days old. Skipping download.')
    
    if history_was_loaded or args.force:
        print('Parsing OPML file...')
        if oc_opml_parse():
            print('Done!')
        else:
            print('You have to update your podcast list manually, dude.')
    else:
        print('No new Overcast history generated.')
        
    

if __name__ == "__main__":
    main()
```

I run main.py as the script entry point and it gets all the work going. It checks to see if the date of my copy of the OPML file is older than the value in the OPML_AGE_LIMIT_DAYS constant and redownloads it if so, using the load_oc_history() function from oc_history.py.

If a new OPML file was downloaded OR I ran main.py with the -f flag, then it parses the OPML file by running the oc_opml_parse() function in oc_opml_parse.py.

```python title="oc_login.py"
import os
import constants as const

from session import session

def oc_login():
    if oc_test_login():
        return True
    else:
        return False

def oc_enter_login():
    print('Attempting login')
    r = session.post(const.LOGIN_URL, data={'email': const.EMAIL, 'password': const.PASSWORD})
    print(f"Response {r.status_code}")
    if r.status_code == const.SUCCESS:
        print("Successfully logged in")
        return True
    else:
        print("Failed login attempt")
        return False
        
def oc_test_login():
    print('Testing login status')
    r = session.get(const.ACCOUNT_URL)
    
    if const.ACCOUNT_PATH in r.url:
        print('Already logged in')
        return True
    elif const.LOGIN_PATH in r.url:
        print('Login required')
        if oc_enter_login():
            return True
    else:
        print(f"I have no idea what happened\n{r.url}")
        
    return False
```

Right now this doesn’t make sense, but if I actually store auth tokens somewhere later, maybe it will. Right now it always checks to see if I’m logged in or not by checking to see if I stayed on the /account page or got bounced back to the /login page. If I got bounced back, it logs me in.

The reason it doesn’t make sense is I don’t persist any login tokens across script runs, so if I need to download an OPML file, it’s always going to need to log into my Overcast account. I may just keep that workflow and simplify this script to not even check instead, and just admit it’s going login to the account every time.

```python title="oc_history.py"
import os
import constants as const
from session import session
from oc_login import oc_login

def load_oc_history():
    if not oc_login():
        print("Couldn't log in to Overcast.fm account!")
        return False

    print("Loading history...")
    r = session.get(const.OPML_LINK)
    print(f"Response {r.status_code}")

    match r.status_code:
        case const.SUCCESS:
            print('OPML file downloaded')
            file_path = 'overcast_history.opml'
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(r.text)
                print(f'OPML file saved to {os.path.abspath(file_path)}')
                return True
            except IOError as e:
                print(f'Error saving OPML file: {e}')
        case const.TOO_MANY_REQUESTS:
            print(r.headers)
            print(f'Too many requests - Retry-After = {r.headers.get('Retry-After')}')
        case _:
            print(f'Unexpected status code: {r.status_code}')

    return False
```

This is pretty simple. I download the OPML file and it either downloads ok or it doesn’t. It’s funny that I have the file name hardcoded here but I use constants for everything else. I’ll have to fix that.

```python title="oc_opml_parse.py"
import pyperclip
import xml.etree.ElementTree as ET
import constants as const
from datetime import datetime, timezone, timedelta

def find_podcast_name(root, episode_id):
    for podcast in root.findall(".//outline[@type='rss']"):
        for ep in podcast.findall("outline[@type='podcast-episode']"):
            if ep.get('overcastId') == episode_id:
                return podcast.get('text')
    return "Unknown"

def oc_opml_parse():
    with open(const.OPML_FILE_PATH, 'r') as f:
        content = f.read()
    try:
        with open(const.OPML_FILE_PATH, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {const.OPML_FILE_PATH}")
        return None
    
    root = ET.fromstring(content)

    # Find all podcast episode entries
    episodes = root.findall(".//outline[@type='podcast-episode']")

    current_date = datetime.now(timezone.utc)
    
    # Filter episodes with played="1"
    # played_episodes = [ep for ep in episodes if ep.get('played') == '1']
    played_episodes = [
        ep for ep in episodes 
        if ep.get('played') == '1' and 
        (current_date - datetime.strptime(ep.get('userUpdatedDate'), "%Y-%m-%dT%H:%M:%S%z")).days <= (const.OPML_AGE_LIMIT_DAYS + 1)
    ]

    # Sort episodes by userUpdatedDate, most recent first
    played_episodes.sort(key=lambda ep: datetime.strptime(ep.get('userUpdatedDate'), "%Y-%m-%dT%H:%M:%S%z"), reverse=True)

    # Get the most recent episodes
    top_episodes = played_episodes[:const.NUMBER_OF_EPISODES]

    # Print the results
    episodes_list = ""
    for ep in top_episodes:
        episodes_list += f"- [{find_podcast_name(root, ep.get('overcastId'))} – {ep.get('title')}]({ep.get('overcastUrl')})\n"
        
        # print(f"Title: {ep.get('title')}")
        # print(f"Updated Date: {ep.get('userUpdatedDate')}")
        # print(f"URL: {ep.get('url')}")
        # print(f"Overcast URL: {ep.get('overcastUrl')}")
        # podcast_name = find_podcast_name(root, ep.get('overcastId'))
        # print(f"Podcast: {podcast_name}")
        # print("---")
    
    print(episodes_list)
    pyperclip.copy(episodes_list)
    
    return True
```

This is the longest one and probably the one where my meager Pythoning probably should embarrass me the most. This parses the OPML file as XML and grabs information about any podcast episodes newer than a certain date (hint: the value of OPML_AGE_LIMIT_DAYS plus 1 day) and then sorts them by the userUpdatedDate value from that episode’s data. After that, it’s just creating a Markdown list of the episodes that match the date and listened to criteria, and copying that list to the clipboard using pyperclip.

I have a Raycast Script Command I can run this from, but obviously in the future it would be better to integrate it more into the site build process itself.

I assume you’re a Python genius compared to me, so [please let me know](https://social.lol/@scottwillsey) if you have any improvement suggestions beyond the ones I’ve already mentioned.

[^1]: I haven’t looked at his yet, but I assume they are different since I assume he’s a much better Python programmer than I am!
