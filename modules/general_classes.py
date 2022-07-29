from types import SimpleNamespace
import json
import os
import pandas as pd

def save_csv(df,file):
    if os.path.exists(os.path.join('results', file)):
        saved_df = pd.read_csv(os.path.join('results', file), on_bad_lines='skip').drop_duplicates() #Open file
        frames = [df, saved_df]
        df_final = pd.concat(frames)
        df_final.to_csv(os.path.join('results', file), encoding='utf-8-sig',index=False)
    else:
        df.to_csv(os.path.join('results', file), encoding='utf-8-sig',index=False)



## NEW COMMON CLASS FOR ELEMENT
class scrape:
    def __init__(self, soup):

        # os.path.join('modules', 'tiktok_elements.json')
        # tiktok = json.load(open(f'modules/tiktok_elements.json'), object_hook=lambda d: SimpleNamespace(**d))
        elements = os.path.join('modules', 'tiktok_elements.json')
        tiktok = json.load(open(elements), object_hook=lambda d: SimpleNamespace(**d))

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
