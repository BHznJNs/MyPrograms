import pykakasi
from janome.tokenizer import Tokenizer
import pyperclip

# pykakasi
kks = pykakasi.kakasi()
convert = kks.convert
# janome
t = Tokenizer()
# 处理日文字符
'''特殊符号'''
symbols = ('、', '。', '’', 
            '”', '｛', '｝',
            '「', '」', 'ー',
            '＝', '_', '+',
            '/', '*', '-',
            '(', ')')
# 日文处理函数
def dealwith(jp):
	# 按行划分
	jp_list = jp.split('\n')

	result_roma = '''<div class="content">
<p class="content warn">本文内容仅供参考，未经许可，请勿转载</p>
<ul class="content startblank endblank">\n'''

	for jl in jp_list:
		if jp_list.index(jl) % 2 != 1 and jl != "":
			result_roma += '<li class="content">\n' + jl + '<br/>\n'
			for token in t.tokenize(jl):
				string = str(token)
				origin = string.split('\t')[0]

				if string.split(',')[-1] != '*':
					roma = convert(string.split(',')[-1])[0]['hepburn']
				else:
					roma = convert(origin)[0]['hepburn']
				
				result_roma += roma + ' '
			result_roma += '<br/>'
		
		elif jl == "":
			result_roma += "<br/>"
		
		else:
			result_roma += jl + '</li>'
		
		# 行尾换行
		result_roma += '\n'
	return result_roma + '</ul></div>'

result = dealwith('''将这里替换为中日间行的歌词''')

print(result)
pyperclip.copy(result)

