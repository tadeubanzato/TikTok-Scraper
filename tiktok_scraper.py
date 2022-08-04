#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv

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
from selenium.webdriver.support import expected_conditions as ec

"Load Webdriver Installer"
from webdriver_manager.chrome import ChromeDriverManager

"Load Python Standard Modules"
import os, time, random, json, platform

"Load BeautifulSoup Module"
from bs4 import BeautifulSoup

"Load Common Classes"
from modules.general_classes import *

import requests
import json
import pandas as pd

from colorama import Fore, Back, Style
from colorama import init
init()

osID = platform.system().lower()

def configure():
    load_dotenv()

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
    if 'darwin' in osID:
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    ## When on linux load LINUX DRIVER
    if 'linux' in osID:
        return webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
    ## When on linux load LINUX DRIVER
    if 'windows' in osID:
        return webdriver.Chrome(executable_path="D:\GEPHI\ARQUIVOSRLINUX\homeR\chromedriver.exe", options=options)

def main(driver,keyword):
    if '#' in keyword:
        # https://www.tiktok.com/tag/jairbolsonaro
        driver.get(f'https://www.tiktok.com/tag/{keyword.replace("#","")}')
        hashed = True
    else:
        ## Open page results with Keywork as query string
        driver.get(f'https://www.tiktok.com/search?q={keyword}')
        hashed = False

    delay = 3 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')
    except TimeoutException:
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')

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
    print(f'\nFound total of {Fore.RED}{len(urls)}{Style.RESET_ALL} videos on this keyword.\n{Fore.GREEN}Start scraping{Style.RESET_ALL}')

    dict = {}
    commentReplies = []
    for url in urls:
        print(f'\n{Fore.BLUE}Scraping video post ID:{Style.RESET_ALL} {url.split("/")[-1]}')

        # url = "https://www.tiktok.com/@bolsonaromessiasjair/video/7120216471208283397"
        driver.get(url)
        # time.sleep(.5)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')

        ## Load Class
        scraped = scrape(soup)

        for comment in scraped.comments:
            try:
                commentReplies.append(comment.find("p", {"data-e2e" : "view-more-1"}).text.replace('View more replies (','').replace(')',''))
            except:
                commentReplies.append(0)

        commDict = {}
        # df = pd.DataFrame({'Userlink':Link,'UserName':Name,'UserFollowing':following,'UserFollowers':followers,'UserLikes':likes,'ReplyContent':Content,'Replylikes':Likes,'replies':Replies})
        df_user = pd.DataFrame(columns=['Userlink','originalPost','UserName','UserFollowing','UserFollowers','UserLikes','ReplyContent','Replylikes','replies'])
        df_posts = pd.DataFrame(columns=['posturl','postcontent','commentcounts'])

        for (User,Link,Name,Content,Likes,Replies) in zip(scraped.commentUser,scraped.commentUserLink,scraped.commentUserName,scraped.commentContent,scraped.commentLikes,commentReplies):
            print(f'     Scraping user {Fore.BLUE}{User}{Style.RESET_ALL} public information')

            # driver.get('https://www.tiktok.com/@tatianemorais211')
            driver.get(Link)
            driver.implicitly_wait(.2) # seconds

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

            commDict[User] = {'Userlink':Link, 'UserName':Name, 'UserFollowing':following, 'UserFollowers':followers, 'UserLikes':likes, 'ReplyContent':Content, 'Replylikes':Likes, 'replies':Replies}
            df_user.loc[len(df_user.index)] = {'Userlink':Link, 'originalPost':url.split('/')[-1], 'UserName':Name, 'UserFollowing':following, 'UserFollowers':followers, 'UserLikes':likes, 'ReplyContent':Content, 'Replylikes':Likes, 'replies':Replies}

            save_csv(df_user,f'user_list_{keyword}.csv')

        ## BUILD CSV for USERS List
        # if os.path.exists(f'results/user_list_{keyword}.csv'):

        #
        # if os.path.exists(os.path.join('results', f'user_list_{keyword}.csv')):
        #     saved_df = pd.read_csv(os.path.join('results', f'user_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
        #     frames = [df, saved_df]
        #     df_final = pd.concat(frames)
        #     df_final.to_csv(os.path.join('results', f'user_list_{keyword}.csv'), encoding='utf-8-sig',index=False)
        # else:
        #     df_user.to_csv(os.path.join('results', f'user_list_{keyword}.csv'), encoding='utf-8-sig',index=False)


        dict[url.split('/')[-1]] = {'postURL':url,'postcontent':scraped.postcontent,'commentsCount':scraped.commentsCount,'comments':commDict}

        df_posts.loc[len(df_posts.index)] = {'posturl':url,'postcontent':scraped.postcontent,'commentcounts':scraped.commentsCount}
        save_csv(df_posts,f'posts_list_{keyword}.csv')


        ## BUILD CSV for POSTS List

        # # if os.path.exists(f'results/posts_list_{keyword}.csv'):
        # if os.path.exists(os.path.join('results', f'posts_list_{keyword}.csv')):
        #     dfdp = pd.read_csv(os.path.join('results', f'posts_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
        #     frames = [df_posts, dfdp]
        #     dfp = pd.concat(frames)
        #     dfp.to_csv(os.path.join('results', f'posts_list_{keyword}.csv'), encoding='utf-8-sig',index=False)
        # else:
        #     df_posts.to_csv(os.path.join('results', f'posts_list_{keyword}.csv'), encoding='utf-8-sig',index=False)

    # json_object = json.dumps(dict, ensure_ascii=False, indent = 4)
    posts_clean = pd.read_csv(os.path.join('results', f'posts_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
    posts_clean.to_csv(os.path.join('results', f'posts_list_{keyword}.csv'), encoding='utf-8-sig',index=False)

    users_clean = pd.read_csv(os.path.join('results', f'user_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
    users_clean.to_csv(os.path.join('results', f'user_list_{keyword}.csv'), encoding='utf-8-sig',index=False)

    return json.dumps(dict, ensure_ascii=False, indent = 4)


if __name__ == '__main__':

    configure()

    ## Clear screen and instructions on terminal window
    if 'windows' in platform.system().lower():
        os.system('cls')
    else:
        os.system('clear')

    keyword = input(f'{Fore.GREEN}Enter keyword or a hashtag to search and press enter:{Style.RESET_ALL} ')

    driver = load_driver()
    driver.maximize_window()

    print(f'{Fore.GREEN}Follow the bellow instruction{Style.RESET_ALL}\n')
    print('  1. Do not close this terminal window')
    print('  2. A browser screen will open with TikTok login')

    driver.get("https://www.tiktok.com")
    time.sleep(.2)

    login_btn = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@data-e2e='top-login-button']")))
    login_btn.click()
    user_login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Use phone / email / username')]")))
    user_login.click()
    username = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Log in with email or username')]")))
    username.click()
    user = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@name='username']")))
    user.send_keys(os.getenv('username'))
    password = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@type='password']")))
    password.send_keys(os.getenv('password'))
    login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@class='e1w6iovg0 tiktok-15aypwy-Button-StyledButton ehk74z00']")))
    login.click()

    print(f'  3. {Fore.RED}Start runing scraper setup - If asked, perform human authentication{Style.RESET_ALL}')

    time.sleep(.5)

    loged = 'False'
    while not loged:
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Login Successful')]")))
            loged = True
        except:
            loged = False
    # print('\nThe only next step will be to add your search criteria for us to start scraping')


    json_object = main(driver,keyword)

    ## Save Json File export
    # os.path.join('results', 'json', f'data_{keyword}.json')
    # jsonFile = open(f'results/json/data_{keyword}.json', 'w')
    jsonFile = os.path.join('results', 'json', f'data_{keyword}.json')

    jsonFile.write(json_object)
    jsonFile.close()
