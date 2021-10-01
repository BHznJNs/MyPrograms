from awesome_progress_bar import ProgressBar
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from re import findall
from os import access, F_OK, mkdir, listdir
from sys import argv

GALLERY = "https://imhentai.xxx/gallery/{}/"
VIEW = "https://imhentai.xxx/view/{}/{}/"

while True:
	galleryID = input("输入本子ID | Please input the Gallery ID : ")
	if galleryID.isdigit():
		VIEW = VIEW.format(galleryID, "{}")
		break
	else:
		print("输入数字！ | Please input a number!")
		continue

try:
	r = get(GALLERY.format(galleryID), timeout=10)
except:
	print("标题和页数获取失败，请检查你的网络！")
	exit(0)
soup = BeautifulSoup(r.text, "html.parser")

# 获取标题
title = soup.h1.string.replace("/", "|").replace("{", "\\").replace("}", "\\")
# 获取页数
page = soup.find("li", class_="pages").string

print(page)

print("标题 | Title: " + title)
print("页数 | " + page)

# 获取图片数
pageNum = int(page.split(": ")[-1])

print("开始下载。 | Download began.")

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
DlPath = "./HentaiDL/{}/{}".format(title, "{}")

# 函数：图片下载
def imgDL(url, path, timeout=10):
	if access(path, F_OK):
		pass
	else:
		sleep(0.4)
		r = get(url, timeout=timeout)
		with open(path, "wb") as f:
			f.write(r.content)

# 函数：获取图片URL
def getImgURL(id):
	r = get(VIEW.format(id), timeout=10)
	soup = BeautifulSoup(r.text, "html.parser")

	img = soup.find("img", id="gimg") # 获取图片元素
	src = img["data-src"] # 获取图片URL

	# imgDL(src, DlPath.format(src.split("/")[-1]))
	return src

failedImg = []

def Downloader(dlList):
	global failedImg

	succeeded = 0
	failed = []
	# 初始化进度条
	bar = ProgressBar(len(dlList), prefix="Downloading", 					bar_length=60)
	try:
		for num in dlList:
			try:
				imgUrl = getImgURL(num)
				imgName = imgUrl.split("/")[-1]
				imgDL(imgUrl, DlPath.format(imgName))

				sleep(2)
				succeeded += 1
			except: # 请求错误(超时)处理
				failed.append(num)
				failedImg.append(num)
				sleep(0.5)

			bar.iter()
	except: # 迭代结束
		bar.stop()
		exit(0)

	bar.wait()
	# 本次下载内容总览
	print("下载完成！ | Download Finished!")
	print("本次下载 | You downloaded :")
	print("成功 | Succeeded: " + str(succeeded))
	print("失败 | Failed: " + str(len(failed)))

	if len(failed) == 0:
		exit(0)
	else:
		toDlFailed = input("是否重新下载错误的图片？ | Wanna download imgs failed? (y / n) ")
		# if toDlFailed == "y":
		failedImg = failed
		return True
		# else:
			# exit(0)

if len(argv) == 2 and argv[1].isdigit():
	toContinue = Downloader(range(int(argv[1]), pageNum+1))
else:
	toContinue = Downloader(range(1, pageNum+1))

while toContinue:
	toContinue = Downloader(failedImg)
