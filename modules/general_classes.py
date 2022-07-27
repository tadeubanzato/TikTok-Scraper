import colorama
from types import SimpleNamespace
import json

######### COLORAMA CLASS #########
class color:
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


## NEW COMMON CLASS FOR ELEMENT
class scrape:
    def __init__(self, soup):
        tiktok = json.load(open('modules/tiktok_elements.json'), object_hook=lambda d: SimpleNamespace(**d))

        # self.postcontent = soup.find(tiktok.postcontent.element, {"data-e2e" : "browse-video-desc"}).text
        self.postcontent = soup.find(tiktok.postcontent.element, {tiktok.postcontent.attribute : tiktok.postcontent.attval}).text

        self.commentsCount = soup.find(tiktok.commentsCount.element, {tiktok.commentsCount.attribute : tiktok.commentsCount.attval}).text
        # self.comments = soup.findAll("div", {"class" : "tiktok-16r0vzi-DivCommentItemContainer eo72wou0"})
        self.comments = soup.findAll(tiktok.comments.element, {tiktok.comments.attribute : tiktok.comments.attval})

        # self.commentUser = [comment.find('a')['href'].replace('/','') for comment in self.comments]
        self.commentUser = [comment.find(tiktok.commentUser.element)['href'].replace('/','') for comment in self.comments]

        # self.commentUserLink = [comment.find('a')['href'].replace('/','https://www.tiktok.com/') for comment in self.comments]
        self.commentUserLink = [comment.find(tiktok.commentUserLink.element)['href'].replace('/','https://www.tiktok.com/') for comment in self.comments]

        # self.commentUserName = [comment.find("span", {"data-e2e" : "comment-username-1"}).text for comment in self.comments]
        self.commentUserName = [comment.find(tiktok.commentUserName.element, {tiktok.commentUserName.attribute : tiktok.commentUserName.attval}).text for comment in self.comments]

        # self.commentContent = [comment.find("p", {"data-e2e" : "comment-level-1"}).text for comment in self.comments]
        self.commentContent = [comment.find(tiktok.commentContent.element, {tiktok.commentContent.attribute : tiktok.commentContent.attval}).text for comment in self.comments]

        self.commentLikes = [comment.find("span", {"data-e2e" : "comment-like-count"}).text for comment in self.comments]
        # self.commentLikes = [comment.find(tiktok.commentLikes.element, {tiktok.commentLikes.attribute : tiktok.commentLikes.attval}).text for comment in self.comments]
