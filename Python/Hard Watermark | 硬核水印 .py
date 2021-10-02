#!/usr/bin/env python3
# encoding=utf8
import json
import os.path
import sys
import pyperclip
import tkinter as tk
from tkinter import TclError
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from random import randint
'''
写入文件函数，参数为：| A function to write settings into the json file
            文字颜色  填充颜色   背景颜色    字体风格     默认文字      水印模式
'''
def write_(fontColor, fillColor, bgColor, fontStyle, defaultText, wmMode):
    with open('./Setting.json', mode='w') as f:  # 保存为 json 文件
        f.write(json.dumps({
            'fontColor': fontColor,
            'fillColor': fillColor,
            'bgColor': bgColor,
            'fontStyle': fontStyle,
            'defaultText': defaultText,
            'wmMode': wmMode
            }))
# 读取 json 设置文件中内容 | To read contents in the json file
def read_():
    global fontColor, fillColor, bgColor, fontStyle, defaultText, wmMode
    with open('Setting.json', mode='r') as f:
        content = f.read()  # 读取设置数据 | To read settings
#       把 json 数据转化为 Python 数据 | To transform the json datas into Python datas
        sets = json.loads(content)

        fontColor = sets['fontColor']
        fillColor = sets['fillColor']
        bgColor = sets['bgColor']
        fontStyle = sets['fontStyle']
        defaultText = sets['defaultText']
        wmMode = sets['wmMode']

# 判断设置文件是否存在，不存在则创建，参数为默认参数
# To judge whether the file exists,or make one and set argument to defaults
if os.path.isfile('setting.json'):
    pass
else:
    write_('white', 'black', 'black', 'normal', 'Bilibili_BHznJNs', 'Text')
# 创建主窗口 | To turn ip the main window
window = tk.Tk()
# 获取屏幕分辨率 | To get the DPI of the screen
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
# 设置主窗口出现位置 | To set where the main window turns up
place_x = int(screenwidth)-250
place_y = int(screenheight/2)-100
window.geometry('245x100+{}+{}'.format(place_x, place_y))
window.title('硬核水印')

changed_x, changed_y = 0, 0
class WaterMark:  # 水印窗口的类 | A class of the watermark

    def create_():  # 创建水印窗口 | Create the window for watermark
#       创建水印后原窗口自动最小化 | Make window to be minimized after thewatermark is created
        window.state('icon')
        global watermark, watermark_size
        global max_x, max_y
        global pos_x, pos_y

        read_()

        try:  # 确保不会出现多个水印窗口 | Prevent to make several watermark
            watermark.destroy()
        except:
            pass
#       若 ’Fullscreen‘ 在水印模式设置中，则开启全屏背景 | To open fullscreen background if 'Fullscreen' is in wmMode
        if 'Fullscreen' in wmMode:
            background = tk.Toplevel()
            background.config(bg=bgColor)
#           全屏显示 | To fullscreen display
            background.attributes('-fullscreen', True)
#           点击 Esc 键关闭全屏背景 | Press the Escape button to close the fullscreen background
            background.bind('<Escape>', lambda event: background.destroy())
#       创建移动水印窗口 | To make the moving watermark window
        watermark = tk.Toplevel()
#		将水印置于顶层 | Put the watermark to the top
        watermark.attributes('-topmost', 1)
#       隐藏窗口外部 | To hide the decoration of the watermark window
        watermark.overrideredirect(True)

        try:
#           将输入转为整数 | Make the input integers
            size = int(size_text.get('0.0', 'end'))
            if 'Text' in wmMode:  # 文本模式 | The Text mode
                wm_label = tk.Label(watermark, font=('normal', size),
                                    text=wm_text.get('0.0', 'end').rstrip(),
                                    bg=fillColor, fg=fontColor
                                    )
            elif 'Picture' in wmMode:  # 图像模式 | The Picture mode
#               获取图像路径 | To get the file path of image
                img_path = wm_text.get('0.0', 'end').rstrip()
                image = Image.open(img_path)
                img_size = image.size  # 获取输入图像的分辨率 | To get the DPI of image
#               根据尺寸缩放图像 | To resize the image by the inputed size
                image = image.resize((int(img_size[0]*size/100), int(img_size[1]*size/100)))

                img = ImageTk.PhotoImage(image)
                wm_label = tk.Label(watermark, image=img, bg=fillColor)
        except ValueError:  # 尺寸输入错误 | Size error
            wm_label = tk.Label(watermark, font=('normal', 14),
                                bg='black', fg='white',
                                text='尺寸设置错误\nPlease set a proper size',
                                )
        except TclError:  # 颜色设置错误 | Color error
            wm_label = tk.Label(watermark, font=('normal', 14),
                                bg='black', fg='white',
                                text='请设置正确的颜色\nPlease set a proper color'
                                )
        except FileNotFoundError:  # 文件路径错误 | File path error
            wm_label = tk.Label(watermark, font=('normal', 14),
                                bg='black', fg='white',
                                text='请输入正确的文件路径\nPlease input a proper file path'
                                )

        wm_label.pack()
#       刷新，获取控件位置信息 | Update to get the position of the watermark
        watermark.update()
#       长和宽 | Width and height
        watermark_size = watermark.winfo_geometry().split('+')[0]
        wm_width = watermark_size.split('x')[0]  # 宽 | Width
        wm_height = watermark_size.split('x')[1]  # 长 | height
#       获取水印横纵方向的最大坐标 | To get the max horizontal and ordinate position
        max_x, max_y = screenwidth-int(wm_width), screenheight-int(wm_height)
#       随机设定一个水印起始坐标 | To set starting position randomly
        pos_x, pos_y = randint(0, max_x), randint(0, max_y)
#       开始刷新水印位置 | Start refresh the position of the watermark
        watermark.after(0, WaterMark.wm_move)

        watermark.mainloop()

    def wm_move():  # 控制水印移动 | Control the watermark to move
        global pos_x, pos_y
#       根据传入参数改变水印位置 | To change the position of watermark by the inputed argument
        watermark.geometry('{}+{}+{}'.format(watermark_size, pos_x, pos_y))

        pos_x = WaterMark.pos_change(pos_x, max_x, 'x')
        pos_y = WaterMark.pos_change(pos_y, max_y, 'y')
#       循环刷新，约每秒60次 | To be cycling about 60 times per second
        watermark.after(int(50/3), WaterMark.wm_move)

    def control_(changed):  # 防止changed变量数值过大 | Prevent the 'changed' var to be to big
        changed = changed - 1 if changed > 2 else changed + 1
        return changed
#   控制水印移动坐标 | Control the position of the watermark
    def pos_change(pos, max_, var):
        global changed_x, changed_y
        if pos == max_ or pos < 0:
            if var == 'x':
                changed_x = WaterMark.control_(changed_x)
            else:
                changed_y = WaterMark.control_(changed_y)
        else:
            pass
        changed = changed_x if var == 'x' else changed_y
#       当水印移动到屏幕边界时回弹 | Move back when the watermark moves to the side of the screen
        if changed % 2 == 1:
            pos -= 1
        else:
            pos += 1
        return pos

    def pause_():  # 关闭水印 | Close the watermark
        global changed_x, changed_y, pos_x, pos_y
        changed_x, changed_y, pos_x, pos_y = 0, 0, 1, 1
        try:
            watermark.destroy()
        except:
            pass
read_()
# 提示文本 | Notice text
notice_text = '请将水印文本输入到下方' if 'Text' in wmMode else '请将图片路径输入到下方'
notice = tk.Label(text=notice_text, bg='white', font=('normal', 14))
notice.place(x=0, y=0, relwidth=0.88, relheight=0.3)
# 水印生成按钮 | Button to create watermark
tk.Button(window, text='生\n成', command=WaterMark.create_, font=('normal', 14)).place(
    relx=0.88, y=0, relwidth=30/245, relheight=0.5)
# 停止水印并重置参数 | Pause watermark and reset the arguments(changed pos_x pos_y)
tk.Button(window, text='暂\n停', command=WaterMark.pause_, font=('normal', 14)).place(
    relx=0.88, rely=0.5, relwidth=30/245, relheight=0.5)
# 水印文本或图片路径 | Text in watermark or file path of image
wm_text = tk.Text(window, font=('normal', 14))
wm_text.place(x=0, rely=0.3, relwidth=0.7, relheight=0.7)
# 水印尺寸 | Size of watermark
tk.Label(window, text='尺寸', bg='white', font=('normal', 14)).place(
    relx=0.7, rely=0.3, relwidth=0.18, relheight=0.3)
size_text = tk.Text(window, font=('normal', 14))
size_text.place(relx=0.7, rely=0.6, relwidth=0.18, relheight=0.4)

tk.Label(window, bg='black').place(  # 分割线 | Separator
        relx=0.7, rely=0.3, relwidth=0.18, relheight=0.02)

size_text.insert('insert', '20')  # 默认字号 | Default font size
wm_text.insert('insert', defaultText)  # 默认文本 | Default text
# 点击鼠标中键后显示水印 | Display the watermark when the Middle Mouse Button is pressed
window.bind('<Button-2>', lambda event: WaterMark.create_())

def delete_():  # 删除 wm_text 中文本 | To delete text in widget wm_text
    wm_text.delete('0.0', 'end')
def paste_():  # 粘贴剪贴板 | Paste text into the widget wm_text from clipboard
    text = pyperclip.paste()
    wm_text.insert('insert', text)
def replace_():  # 替换成剪贴板内容 | Get text from clipboard and replace text in widget wm_text
    delete_()
    text = pyperclip.paste()
    wm_text.insert('insert', text)

def setting_():  # 设置界面 | Setting GUI
    read_()
    win_set = tk.Tk()
    win_set.resizable(0, 0)
    win_set.title('设置')
    win_x, win_y = int(screenwidth/2)-100, int(screenheight/2)-200
    win_set.geometry('200x280+{}+{}'.format(win_x, win_y))
#   放置控件 | Put widgets
    tk.Label(win_set, text='文字颜色', font=('normal', 14), bg='white').place(
        x=0, y=0, relheight=0.12, relwidth=0.4)
    fc_text = tk.Text(win_set, font=('normal', 14))
    fc_text.place(relx=0.4, y=0, relwidth=0.6, relheight=0.12)
    fc_text.insert('insert', fontColor)
#   填充颜色设置 | Widget to set filled color
    tk.Label(win_set, text='填充颜色', font=('normal', 14), bg='white').place(
        relx=0.02, rely=0.14, relwidth=0.47, relheight=0.1)
    fill_text = tk.Text(win_set, font=('normal', 14))
    fill_text.place(relx=0.02, rely=0.24, relwidth=0.47, relheight=0.12)
    fill_text.insert('insert', fillColor)
#   背景颜色设置 | Widget to set background color
    tk.Label(win_set, text='背景颜色', font=('normal', 14), bg='white').place(
        relx=0.51, rely=0.14, relwidth=0.47, relheight=0.1)
    bgColor_text = tk.Text(win_set, font=('normal', 14))
    bgColor_text.place(relx=0.51, rely=0.24, relwidth=0.47, relheight=0.12)
    bgColor_text.insert('insert', bgColor)
#   字体选择控件 | Widget to set fontStyle
    tk.Label(win_set, text='字体', font=('normal', 14), bg='white').place(
        relx=0.02, rely=0.37, relheight=0.12)
    fs_text = tk.Text(win_set, font=('normal', 14))
    fs_text.place(relx=0.25, rely=0.37, relwidth=0.73, relheight=0.12)
    fs_text.insert('insert', fontStyle)
#   默认文字设置 | Widget to set default text
    tk.Label(win_set, text='默认\n文字', bg='white', font=('normal', 14)).place(
        relx=0.02, rely=0.48)
    de_text = tk.Text(win_set, font=('normal', 14))
    de_text.place(relx=0.25, rely=0.48, relwidth=0.73, relheight=0.18)
    de_text.insert('insert', defaultText)

    tk.Label(win_set, bg='black').place(  # 分割线 | Separator
        relx=0.02, rely=0.48, relwidth=0.21, relheight=0.005)
#   显示模式选择控件 | Widget to select display mode
    tk.Label(win_set, text='显示\n模式', font=('normal', 14), bg='white').place(
        relx=0.02, rely=0.65)
    wmMode_com = Combobox(win_set, font=('normal', 14))
    wmMode_com['value'] = ('文字|Text', '图像|Picture',
                            '文字全屏|Text Fullscreen', '图片全屏|Picture Fullscreen')
    wmMode_com.current(('Text', 'Picture', 'Text Fullscreen',
                        'Picture Fullscreen').index(wmMode))
    wmMode_com.place(relx=0.25, rely=0.68, relwidth=0.73, relheight=0.12)

    tk.Label(win_set, bg='black').place(  # 分割线 | Separator
        relx=0.02, rely=0.655, relwidth=0.21, relheight=0.005)
#   保存设置函数 | A function to save settings
    def save_():
        fontColor = fc_text.get('0.0', 'end').rstrip()
        fillColor = fill_text.get('0.0', 'end').rstrip()
        bgColor = bgColor_text.get('0.0', 'end').rstrip()
        fontStyle = fs_text.get('0.0', 'end').rstrip()
        defaultText = de_text.get('0.0', 'end').rstrip()
        wmMode = wmMode_com.get().split('|')[1]

#       重设 wm_text 中文本为默认文本 | Reset text in wm_text to default text
        notice_text = '请将水印文本输入到下方' if 'Text' in wmMode else '请将图片路径输入到下方'
        notice.config(text=notice_text)
#       设置保存时将主窗口中的文本改为已设定的默认文本 | Reset text in main window when settings save
        wm_text.delete('0.0', 'end')
        wm_text.insert('insert', defaultText)

        write_(fontColor, fillColor, bgColor, fontStyle, defaultText, wmMode)

        win_set.destroy()
#   保存按键 | Button to save settings
    b_save = tk.Button(win_set, text='保存', font=('normal', 16),
                       bg='darkgrey', command=save_)
    b_save.place(relx=0.05, rely=0.85, relwidth=0.4, relheight=0.12)
#   取消按键 | Button to cancel settings
    b_cancel = tk.Button(win_set, text='取消', font=('normal', 16),
                         bg='darkgrey', command=win_set.destroy)
    b_cancel.place(relx=0.55, rely=0.85, relwidth=0.4, relheight=0.12)
# 右键菜单设置 | Settings of the right menu
right_menu = tk.Menu(window, tearoff=0, relief='flat', bg='white', fg='darkgray',
                     activebackground='black', activeforeground='white'
                     )
right_menu.add_command(label='清空', command=delete_)
right_menu.add_command(label='粘贴', command=paste_)
right_menu.add_command(label='替换', command=replace_)
right_menu.add_command(label='设置', command=setting_)

# 右键点击打开右键菜单 | Press the right key to open the right menu
window.bind('<Button-3>', lambda event: right_menu.post(event.x_root, event.y_root))
# 在主窗口中左键点击关闭菜单 | Press the left key in the main window to close the right menu
window.bind('<Button-1>', lambda event: right_menu.unpost())
# 点击关闭按钮时终止整个程序 | Press the close key to over the process
window.protocol('WM_DELETE_WINDOW', sys.exit)

window.mainloop()
