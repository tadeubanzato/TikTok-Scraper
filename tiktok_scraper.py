#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Load Selenium for pupeteering"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

"Load Webdriver Installer"
from webdriver_manager.chrome import ChromeDriverManager

"Load Python Standard Modules"
import os, time, random, json, platform

"Load BeautifulSoup Module"
from bs4 import BeautifulSoup

import requests
import json
import pandas as pd

def load_driver():
    ### Using Selenium as a puppeteer for amazon scraper
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")

    # ### Desable image load in chrome may improve performance
    # chrome_prefs = {}
    # options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    ## When on mac load MAC DRIVER
    if 'darwin' in platform.system().lower():
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    ## When on linux load LINUX DRIVER
    if 'linux' in platform.system().lower():
        return webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
    ## When on linux load LINUX DRIVER
    if 'windows' in platform.system().lower():
        return webdriver.Chrome(executable_path="<PATH TO CHROMEDRIVER>", options=options)

def main(driver,keyword):
    if '#' in keyword:
        # https://www.tiktok.com/tag/jairbolsonaro
        driver.get(f'https://www.tiktok.com/tag/{keyword.replace("#","")}')
        hashed = True
    else:
        ## Open page results with Keywork as query string
        driver.get(f'https://www.tiktok.com/search?q={keyword}')

    delay = 3 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Page is ready!")

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    if hashed:
        videoList = soup.find("div", {"data-e2e": "challenge-item-list"})
        allVids = videoList.findAll("div", {"class": "tiktok-x6y88p-DivItemContainerV2 e19c29qe7"})
    else:
        videoList = soup.find("div", {"mode": "search-video-list"})
        allVids = videoList.findAll("div", {"class": "tiktok-1soki6-DivItemContainerForSearch e19c29qe9"})

    # allVids = videoList.findAll("div", {"class": "tiktok-1soki6-DivItemContainerForSearch e19c29qe9"})
    urls = [vid.find("a")['href'] for vid in allVids]
    print(f'Found total of {len(urls)} videos on this keyword.\nStart scraping')

    dict = {}
    commentReplies = []
    for url in urls:
        print(f'Scraping post ID: {url.split("/")[-1]}')

        # url = "https://www.tiktok.com/@bolsonaromessiasjair/video/7120216471208283397"
        driver.get(url)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        postcontent = soup.find("div", {"data-e2e" : "browse-video-desc"}).text
        commentsCount = soup.find("p", {"class" : "tiktok-1gseipw-PCommentTitle e1a7v7ak1"}).text
        comments = soup.findAll("div", {"class" : "tiktok-16r0vzi-DivCommentItemContainer eo72wou0"})
        commentUser = [comment.find('a')['href'].replace('/','') for comment in comments]
        commentUserLink = [comment.find('a')['href'].replace('/','https://www.tiktok.com/') for comment in comments]
        commentUserName = [comment.find("span", {"data-e2e" : "comment-username-1"}).text for comment in comments]
        commentContent = [comment.find("p", {"data-e2e" : "comment-level-1"}).text for comment in comments]
        commentLikes = [comment.find("span", {"data-e2e" : "comment-like-count"}).text for comment in comments]
        # commentReplies = [comment.find("p", {"data-e2e" : "view-more-1"}).text.replace('View more replies (','').replace(')','') for comment in comments]
        for comment in comments:
            try:
                commentReplies.append(comment.find("p", {"data-e2e" : "view-more-1"}).text.replace('View more replies (','').replace(')',''))
            except:
                commentReplies.append(0)

        commDict = {}
        for (User,Link,Name,Content,Likes,Replies) in zip(commentUser,commentUserLink,commentUserName,commentContent,commentLikes,commentReplies):
            driver.get(Link)
            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, 'html.parser')
            try:
                following = soup.find("strong", {"title" : "Following"}).text
            except:
                following = 0
            try:
                likes = soup.find("strong", {"title" : "Likes"}).text
            except:
                likes = 0
            try:
                followers = soup.find("strong", {"title" : "Followers"}).text
            except:
                followers = 0

            commDict[User] = {'Userlink':Link,'UserName':Name,'UserFollowing':following,'UserFollowers':followers,'UserLikes':likes,'ReplyContent':Content,'Replylikes':Likes,'replies':Replies}

        dict[url.split('/')[-1]] = {'postURL':url,'postcontent':postcontent,'commentsCount':commentsCount,'comments':commDict}

    # json_object = json.dumps(dict, ensure_ascii=False, indent = 4)
    return json.dumps(dict, ensure_ascii=False, indent = 4)


if __name__ == '__main__':

    ## Clear screen and instructions on terminal window
    os.system('clear')
    print('Follow the bellow instruction\n')
    print('  1. Do not close this window')
    print('  2. A browser screen will open with TikTok login screen')
    print('  3. Finish your TikTok login on the new browser screen and come back to this terminal screen')
    time.sleep(3)

    driver = load_driver()
    driver.maximize_window()
    driver.get("https://www.tiktok.com")
    ## Selenium clicks on Login Button to open login lightbox
    driver.find_element(By.XPATH,".//*[@data-e2e='top-login-button']").click()

    print('\n\n  4. This screen is paused so you can finish your login, press any key to continue')

    os.system('clear')
    print('\nThe only next step will be to add your search criteria for us to start scraping')
    keyword = input("Enter keyword to search and press enter: ")

    json_object = main(driver,keyword)

    ## Save Json File export
    jsonFile = open(f'data_{keyword}.json', 'w')
    jsonFile.write(json_object)
    jsonFile.close()
