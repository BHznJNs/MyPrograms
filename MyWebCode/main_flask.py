from romkan import to_roma
from janome.tokenizer import Tokenizer
from flask import Flask, render_template, request

# janome
t = Tokenizer()
# 处理日文字符
def dealwith(jp):
    result_analysed = ''
    result_roma = ''
    result_furi = ''
    for token in t.tokenize(jp):
        string = str(token)
        origin = string.split('\t')[0]
        roma = to_roma(string.split(',')[-1])
        furi = '{}[{}]'.format(origin, roma)
        result_analysed += string + '\n'
        result_roma += roma + ' '
        result_furi += furi
    return result_furi, result_analysed, result_roma

# Flask
application = Flask(__name__)

# 网站首页
@application.route('/')
def index():
    return render_template("index.html")
@application.route('/mobile')
def index_mobile():
    return render_template("index_mobile.html")

# 日文转罗马音
@application.route('/tools/jp2roma', methods=['GET', 'POST'])
def jp2roma():
    if request.method == 'GET':
        return render_template("jp2roma.html")
    elif request.method == 'POST':
        jp = request.form.get('jp')
        results = dealwith(jp)
        furigana = results[0]
        analysed = results[1]
        romaji = results [2]
        return render_template('jp2roma.html',
                jp=jp, romaji=romaji, analysed=analysed, furigana=furigana
                )

@application.route('/tools/cmdownload')
def cmdownload():
    return render_template('cmdownload.html')

#————————————————————————————————————————————————
# 网站图标
@application.route('/favicon.ico')
def favicon():
    return application.send_static_file('favicon.ico')

#——————————————————————————————————————————————————————
if __name__ == '__main__':
    application.run(debug=True)
