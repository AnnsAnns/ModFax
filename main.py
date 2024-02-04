###
# Copyright 2021-2024 AnnsAnn, git@annsann.eu
#
# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with theLicence.
#
# You may obtain a copy of the Licence at: https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and limitations under the Licence.
###

import praw
import logging
import sys
import re

from config import id, secret, username, password


try:
    reddit = praw.Reddit(
        client_id = id,
        client_secret = secret,
        user_agent = "linux:modfax:v0.1-dev",
        username = username,
        password = password)
except praw.exceptions.RedditAPIException as e:
    logging.critical(f"Error in login: {e}")
    sys.exit()

def check_for_sub(title: str):
    for x in title.split():          
        if (match := re.match(r"^[r]\/|^\/[r]\/", x)):
            title = x.replace(match.group(0), "").strip()
            logging.info(f"Found subreddit name of: {title}")
            
            return title
    if len(title.split()) == 1:
        logging.info(f"Found subreddit name of: {title}")
        return title
    
for item in reddit.inbox.stream():
    # Check if the item is a private message
    if item.was_comment:
        continue
    
    print(f"Received message from {item.author} with subject {item.subject}")

    # Mark it as read
    item.mark_read()

    subreddit_name = check_for_sub(item.subject)
    try:
        subreddit = reddit.subreddit(subreddit_name)
    except:
        print("Couldn't get subbreddit")
        continue
    
    # Check for reddit messages
    if item.author == None:
        print("Received Reddit Message")
        continue
    
    # Check if we're a moderator of the subreddit
    if not subreddit.user_is_moderator:
        print("Self is not a moderator of the sub")
        continue
    
    # Check if the author of the message is a moderator
    if not item.author in subreddit.moderator():
        print("Message is not from moderator of the sub")
        continue
    
    # Send the message to each moderator of the subreddit
    for mod in subreddit.moderator():
        subject = f"📠Mod Fax📠 from /u/{item.author} to Mods of /r/{subreddit_name}"
        mod.message(subject, item.body)
        print(f"Sent message to {mod}")