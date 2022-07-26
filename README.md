# TikTok Scraper
Since TikTok API is in constant change and I'm having issues using some of the TikTok APIs and Python modules available in the market I've built this scraper to help me do some of the data acquistion from their platform.\

# General Script Instillation
1. Install requirements by runing the python command `pip3 install -r requirements.txt`
2. After requirements installation run `python3 tiktok_scraper.py`
3. If everything goes well a Chrome browser screen will open to TikTok's login page
4. You will have to manually login into TikTok, this script do not capture or store any login information from the user
5. After you login you will have to type your search keyword that will be searched on TikTok
6. Once you type the keywork and hit enter the script will scrape the front page search results of the search query, and will continue working on its own you can follow what the script is doing on the browser screen

## Install Chromedriver
For Mac users, the Chromedriver extension is executed within the script no additional installation is needed.
For Linux and Windows users, you will need to install the Chromedriver - Reference here: https://www.makeuseof.com/how-to-install-selenium-webdriver-on-any-computer-with-python/
> Additional reference for Windows users:
http://www.learningaboutelectronics.com/Articles/How-to-install-chromedriver-Python-windows.php

### Linux users
Make sure to update the Chromedriver path on code line:
```python
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
```

### Windows users
Make sure to update the Chromedriver path on code line
```python
driver = webdriver.Chrome(executable_path="<PATH TO CHROMEDRIVER>", options=options)
```

## Results
As a result the script will save a Json file with the following Swagger:
```json
{
    "7079374480363048198": {
        "postURL": "https://www.tiktok.com/@planetmatters/video/7079374480363048198",
        "postcontent": "Let's clean up the ocean! 💙😊 #plasticpollution  #climatechange  #oceancleanup  #sealover  #foryou  #fypシ ",
        "commentsCount": "46.8K comments",
        "comments": {
            "@planetmatters": {
                "Userlink": "https://www.tiktok.com/@planetmatters",
                "UserName": "Planet Matters 🌍 ",
                "UserFollowing": "1",
                "UserFollowers": "2.9M",
                "UserLikes": "29.3M",
                "ReplyContent": "Thanks for the video @treasurehawaii 🎥💙",
                "Replylikes": "3",
                "replies": 0
            }
}
```

# Next Iterations will probably be
- [ ] Optimize script
- [X] Add Pandas and overall CSV export support
- [ ] Introduce concurrent futures and parallel processing
