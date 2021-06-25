import requests, re
import pyperclip

url = 'https://cn.bing.com/dict/search?q={}'

while 1:
	word = input()
	if word != 'n':
		html = requests.get(url.format(word)).text
		
		result = re.findall(r"的释义，美(.+?)，", html)[0].replace('[', '').replace(']','')
		pyperclip.copy(result)
		print(result)
	else:
		break
