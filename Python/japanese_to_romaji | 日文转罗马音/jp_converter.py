from pykakasi import kakasi
from janome.tokenizer import Tokenizer

# pykakasi
kks = kakasi()
convert = kks.convert
# janome
t = Tokenizer()
# 处理日文字符
'''特殊符号'''
symbols = (
	'、', '。', '’', 
	'”', '｛', '｝',
	'「', '」', 'ー',
	'＝', '_', '+',
	'/', '*', '-',
	'(', ')'
)
# 日文处理函数
def dealwith(jp):
	for token in t.tokenize(jp):
		string = str(token)
		origin = string.split('\t')[0]

		if string.split(',')[-1] != '*':
			roma = convert(string.split(',')[-1])[0]['hepburn']
		else:
			roma = convert(origin)[0]['hepburn']
		
		result_roma = roma + ' '
	return result_roma

result = dealwith(input())

print(result)
