import colorama

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
        self.postcontent = soup.find("div", {"data-e2e" : "browse-video-desc"}).text
        self.commentsCount = soup.find("p", {"class" : "tiktok-1gseipw-PCommentTitle e1a7v7ak1"}).text
        self.comments = soup.findAll("div", {"class" : "tiktok-16r0vzi-DivCommentItemContainer eo72wou0"})
        self.commentUser = [comment.find('a')['href'].replace('/','') for comment in self.comments]
        self.commentUserLink = [comment.find('a')['href'].replace('/','https://www.tiktok.com/') for comment in self.comments]
        self.commentUserName = [comment.find("span", {"data-e2e" : "comment-username-1"}).text for comment in self.comments]
        self.commentContent = [comment.find("p", {"data-e2e" : "comment-level-1"}).text for comment in self.comments]
        self.commentLikes = [comment.find("span", {"data-e2e" : "comment-like-count"}).text for comment in self.comments]


#   def myfunc(self):
#     print("Hello my name is " + self.name)
#
# p1 = Person("John", 36)
# p1.myfunc()
