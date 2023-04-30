#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_message(bot_token, chat_id, msg):
    url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + chat_id + "&text=" + msg
    # send message
    requests.get(url)

def github_check():
    URL = "https://github.com/search?q=42ctf"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    repos = soup.find_all("li", class_="repo-list-item")
    path = "./known_github_repos.txt"
    leaks = []
    i = 0
    if not os.path.exists(path):
        os.mknod(path)
    with open("known_github_repos.txt", "r+") as f:
        for repo in repos:
            item = repo.find("a", class_="v-align-middle")
            is_new = False
            item_text = "https://github.com/" + item.text.strip()
            for line in f:
                if line.strip('\n') == item_text:
                    is_new = True
                    break
            if is_new == False:
                f.write(item_text + '\n')
                leaks.append(item_text)
        for leak in leaks:
            send_message(BOT_TOKEN, CHAT_ID, "New potential leak on Github\n" + leak)
            i = i + 1
    return i

def codeberg_check():
    URL = "https://codeberg.org/explore/repos?sort=recentupdate&language=&q=42ctf"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    repos = soup.find_all("div", class_="repo-title")
    path = "./known_codeberg_repos.txt"
    leaks = []
    i = 0
    if not os.path.exists(path):
        os.mknod(path)
    with open("known_codeberg_repos.txt", "r+") as f:
        for repo in repos:
            item = repo.find("a", class_="name")
            is_new = False
            item_text = "https://codeberg.org/" + item.text.strip().replace(" ","")
            for line in f:
                if line.strip('\n') == item_text:
                    is_new = True
                    break
            if is_new == False:
                f.write(item_text + '\n')
                leaks.append(item_text)
        for leak in leaks:
            send_message(BOT_TOKEN, CHAT_ID, "New potential leak on Codeberg\n" + leak)
            i = i + 1
    return i

if __name__ == "__main__":
    count = github_check()
    count += codeberg_check()
    if count > 0:
        print(f"{count} new potential(s) leak(s) found!")
