# -*- coding: utf-8 -*-
# @Author Michael Pavlov

import requests
import time
import urllib3
import random
from bs4 import BeautifulSoup
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

class GitHubCrawler():

    def __init__(self, username, password):
        self.logger = logging.getLogger("HomeService")
        self.logger.setLevel(logging.INFO)
        fh = RotatingFileHandler("home_service.log", mode='a', encoding='utf-8', backupCount=5,
                                 maxBytes=16 * 1024 * 1024)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.base_url_ = 'https://github.com/topics/python?o=desc&s=updated'
        self.headers = {
            'User-Agent': '''Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64'''}

        self.id_list = []

        self.base_dir = "D:\\git_github\\"
        self.git_path = "\"C:\\Program Files\\Git\\cmd\\git.exe\""

        self.github_username = username
        self.github_password = password

    def remove_dubble_spaces(self, line):
        try_again = True
        while try_again:
            line = line.replace("  ", " ")
            if line.find("  ") == -1:
                try_again = False
        return line

    def run(self):
        while True:

            try:
                url_ = self.base_url_
                session = requests.Session()
                # session.proxies = proxy
                r = session.get(url_, headers=self.headers, verify=False, timeout=5)
                if r.status_code == 200:
                    dt_now = datetime.datetime.now()
                    soup = BeautifulSoup(r.content, "lxml")
                    items_list = soup.find_all('article', {'class' : True})
                    print(time.ctime(),"Found repos: ",len(items_list))
                    for item in items_list:
                        title = item.find('h1').get_text().replace("\n","")
                        title = self.remove_dubble_spaces(title)
                        main_title = title[:title.find("/")].strip()
                        repo_title = title[title.find("/")+1:].strip()
                        id = title
                        # print(title)
                        href = "https://" + self.github_username + ":" + self.github_password + "@github.com/" + title.replace(" ","")
                        if id not in self.id_list:
                            print("new id: ", id, "; href", href)
                            print(main_title, repo_title)
                            self.id_list.append(id)
                            try:
                                if os.path.isdir(self.base_dir + main_title + "/" + repo_title):
                                    # есть репа, делаем git pull
                                    os.chdir(self.base_dir + main_title + "/" + repo_title)
                                    os.system(self.git_path + " " + "pull ")
                                    print("repo " + main_title + "/" + repo_title + " updated!")
                                elif os.path.isdir(self.base_dir + main_title):
                                    # есть юзер, но нет репы
                                    # делаем git clone
                                    os.chdir(self.base_dir + main_title)
                                    os.system(self.git_path + " " + "clone " + href)
                                    print("repo " + main_title + "/" + repo_title + " created!")
                                else:
                                    # нет юзера, создаем юзера и репу
                                    os.mkdir(self.base_dir + main_title)
                                    os.chdir(self.base_dir + main_title)
                                    os.system(self.git_path + " " + "clone " + href)
                                    print("repo " + main_title + "/" + repo_title + " created!")
                            except Exception as err:
                                print(err)
                            sleep_time = random.randint(10, 30)
                            print("sleep for", sleep_time, "seconds")
                            time.sleep(sleep_time)

                    if r.text.lower().find("captcha") > 0:
                        print("CAPTCHA")
                else:
                    print("pfff", datetime.datetime.now(), r.status_code)
            except Exception as e:
                print(e)
            sleep_time = random.randint(30,60)
            print("sleep for", sleep_time, "seconds")
            time.sleep(sleep_time)


if __name__ == '__main__':
    service = GitHubCrawler("user", "password")
    service.run()

