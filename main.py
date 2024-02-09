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

from config import id, secret, username, password, use_approved_submitters, approved_subreddits


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("modfax.log"),
        logging.StreamHandler()
    ]
)

logging.info("Starting ModFax")
if use_approved_submitters:
    logging.info("Using approved submitters")
else:
    logging.info("Using moderators")

try:
    reddit = praw.Reddit(
        client_id = id,
        client_secret = secret,
        user_agent = "linux:modfax:v0.2-dev",
        username = username,
        password = password)
except praw.exceptions.RedditAPIException as e:
    logging.critical(f"Error in login: {e}")
    sys.exit()

logging.info(f"Logged in as {reddit.user.me()}")

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
    
    logging.info(f"Received message from {item.author} with subject {item.subject}")

    # Mark it as read
    item.mark_read()

    subreddit_name = check_for_sub(item.subject)
    try:
        subreddit = reddit.subreddit(subreddit_name)
    except:
        logging.warning("Couldn't get subbreddit")
        continue
    
    if subreddit_name not in approved_subreddits:
        logging.warning("Subreddit not in approved subreddits")
        continue
    
    # Check for reddit messages
    if item.author == None:
        logging.warning("Received Reddit Message")
        continue
    
    # Check if we're a moderator of the subreddit
    if not subreddit.user_is_moderator:
        logging.warning("Self is not a moderator of the sub")
        continue
    
    # Check if the author of the message is a moderator
    if not item.author in subreddit.moderator():
        logging.warning("Message is not from moderator of the sub")
        continue
    
    # Send the message to each moderator of the subreddit
    if use_approved_submitters:
        moderators = subreddit.contributor()
    else:
        moderators = subreddit.moderator()
        
    for mod in moderators:
        # Skip the bot
        if mod == username:
            continue
        
        subject = f"📠Mod Fax📠 from /u/{item.author} to Mods of /r/{subreddit_name}"
        body = f"{item.body}\n --- \n This service is provided by [ModFax📠](https://github.com/AnnsAnns/ModFax)."\
            "\n\nSee [**How To Use 📖**](https://github.com/AnnsAnns/ModFax?tab=readme-ov-file#how-to-use)"\
            "\n\n*You received this message because the author, the bot and you were all moderators of the subreddit.* "
        try:
            mod.message(from_subreddit=subreddit, subject=subject, message=body)
        except praw.exceptions.RedditAPIException as e:
            logging.error(f"Error in sending message to {mod}: {e}")
            continue
        
        # Sleep for 10 seconds to avoid rate limiting
        # Because reddit decided to be like Twitter
        time.sleep(10)
            
        logging.info(f"Sent message to {mod}")