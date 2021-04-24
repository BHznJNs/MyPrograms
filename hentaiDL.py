from awesome_progress_bar import ProgressBar
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from re import findall
from os import access, F_OK, mkdir

GALLERY = "https://imhentai.xxx/gallery/{}/"

while True:
	galleryID = input("输入本子ID | Please input the Gallery ID : ")
	if galleryID.isdigit():
		VIEW = "https://imhentai.xxx/view/{}/1/".format(galleryID)
		break
	else:
		print("输入数字！ | Please input a number!")
		continue

r = get(GALLERY.format(galleryID), timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# 获取标题
title = soup.h1.string
# 获取页数
page = soup.find("li", class_="pages").string

print("标题 | Title: " + title)
print("页数 | " + page)

toContinue = input("继续吗？ | Wanna continue? (y / n) ")
if toContinue == "y":
	pass
else:
	exit(0)
# 获取图片数
pageNum = int(page.split(": ")[-1])
print("开始下载。 | Download began.")

r = get(VIEW, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

img = soup.find("img", id="gimg") # 获取图片元素
src = img["src"] # 获取图片URL
imgFormat = src.split(".")[-1] # 获取图片格式
imgUrls = src.replace("1." + imgFormat, "") + "{}." + imgFormat

# 定义函数：如果文件夹不存在，则创建
def mkdir_(dirName):
	if access(dirName, F_OK):
		pass
	else:
		mkdir(dirName)
# 创建文件夹
mkdir_("HentaiDL")
mkdir_("HentaiDL/" + title)
# 设置下载路径
DlPath = "HentaiDL/{}/{}.{}".format(title, "{}", imgFormat)
# 定义函数：下载图片
def imgDL(url, path):
	r = get(url, timeout=10)
	with open(path, "wb") as f:
		f.write(r.content)
# 初始化进度条
bar = ProgressBar(pageNum, prefix="Downloading", bar_length=60)
succeeded = 0
failed = 0
failedImg = []
try:
	for num in range(1, pageNum+1):
		try:
			imgDL(imgUrls.format(num), DlPath.format(num))
			
			sleep(1)
			succeeded += 1
			bar.iter(" {}.{} downloaded!".format(num, imgFormat))
		except: # 请求错误(超时)处理
			sleep(0.5)
			failed += 1
			failedImg.append(num)
			bar.iter(" {}.{} failed!".format(num, imgFormat))
except: # 迭代结束
	bar.stop()
	exit(0)

bar.wait()
# 本次下载内容总览
print("下载完成！ | Download Finished!")
print("本次下载 | You downloaded :")
print("成功 | Succeeded: " + str(succeeded))
print("失败 | Failed: " + str(failed))

toDlFailed = input("是否重新下载错误的图片？ | Wanna download imgs failed? (y /n)")
if toDlFailed == "y":
	pass
else:
	exit(0)

bar = ProgressBar(len(failedImg), prefix="Downloading", bar_length=60)
try:
	for fNum in failedImg:
		imgDL(imgUrls.format(fNum), DlPath.format(fNum))

		sleep(1)
		bar.iter(" {}.{} downloaded!".format(fNum, imgFormat))
except:
	bar.stop()
	exit(0)
