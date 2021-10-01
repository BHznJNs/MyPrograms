import os
import re
import requests
from bs4 import BeautifulSoup

path = "./bingWallpaper"
pathExist = os.path.exists(path)
if not pathExist:
    os.mkdir(path)

url = "https://cn.bing.com/"

pageReq = requests.get(url)
soup = BeautifulSoup(pageReq.text, 'html.parser')

imgLinkElement = soup.find("link", id="preloadBg")

imgLinkSoup = BeautifulSoup(str(imgLinkElement), 'html.parser')
tag = imgLinkSoup.link # 指定 tag
imgLink = "https://cn.bing.com" + tag["href"] # 返回并合成链接
imgName = re.findall("(?<=\?id=).*?(?=\&)", imgLink) # 匹配图片名称

#——————————————————————————————

imgReq = requests.get(imgLink)
imgRes = imgReq.content
with open("./bingWallpaper/" + imgName[0], "wb") as f:
    f.write(imgRes)
