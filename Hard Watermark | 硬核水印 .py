import tkinter as tk
from random import randint 

window = tk.Tk()
screenwidth, screenheight = window.winfo_screenwidth(), window.winfo_screenheight()#获取当前屏幕分辨率
place_x = int(screenwidth)-245
place_y = int(screenheight/2)-100
window.geometry('245x100+{}+{}'.format(place_x, place_y))
window.title('硬核水印')
window.resizable(0, 0)

def create_() : #创建水印窗口 | Create the window for watermark
    window.state('icon') #创建水印后原窗口自动最小化 | Make window to be minimized after thewatermark is created
    global watermark
    global max_x, max_y
    global pos_x, pos_y

    try : #确保不会出现多个水印窗口 | Prevent to make several watermark
        watermark.destroy()
    except :
        pass
    
    watermark = tk.Tk()
    watermark.overrideredirect(True) #隐藏窗口外部 | To hide the decoration of the watermark window
    
    try : #检测输入是否为数字 | Check whether the inserted are number
        font_size = int(float(font_text.get('0.0', 'end'))) #将输入转为整数 | Make the input integers
        wm_label = tk.Label(watermark, text=wm_text.get('0.0', 'end').rstrip(),
             bg='black', fg='white', font=('微软雅黑-Tahoma-韩文版', font_size))
    except :
        wm_label = tk.Label(watermark, text='字号应为数字\nThe font size should be number',
             bg='black', fg='white', font=('微软雅黑-Tahoma-韩文版', 14))
    wm_label.pack()
    watermark.update() #刷新，获取空间位置信息 | Update to get the position of the watermark
    # 获取水印长宽 | Get the width and height of the watermark
    wm_size = wm_label.winfo_geometry()
    size_list = wm_size.split('x')
    wm_width = size_list[0]
    wm_height = size_list[1].split('+')[0]
    
    max_x, max_y = screenwidth-int(wm_width), screenheight-int(wm_height)

    pos_x, pos_y = randint(0, max_x), randint(0, max_y)

    watermark.after(0, wm_move) #开始刷新水印位置，每秒62.5次 | Start refresh the position of the watermark 62.5 times each second
    
    watermark.mainloop()

def wm_move() : #控制水印移动 | Control the watermark to move
    global pos_x, pos_y
    
    wm_size = watermark.winfo_geometry().split('+')[0]
    watermark.geometry('{}+{}+{}'.format(wm_size, pos_x, pos_y))

    pos_x = pos_change(pos_x, max_x, 'x')
    pos_y = pos_change(pos_y, max_y, 'y')
    
    watermark.after(int(50/3), wm_move)

def control_(x) : #防止changed变量数值过大 | Prevent the 'changed' var to be to big
    if x > 2 :
        x -= 1
    else :
        x += 1
    return x

changed_x, changed_y = 0, 0
def pos_change(pos, max_, var) : #控制水印移动坐标 | Control the position of the watermark
    global changed_x, changed_y
    if pos == max_ or pos < 0 :
        if var == 'x' :
            changed_x = control_(changed_x)
        else :
            changed_y = control_(changed_y)
    else :
        pass
    changed = changed_x if var == 'x' else changed_y
    if changed%2 == 1 : #当水印移动到屏幕边界时回弹 | Move back when the watermark moves to the side of the screen
        pos -= 1
    else :
        pos += 1
    return pos

def pause_(): #关闭水印 | Close the watermark
    global changed, pos_x, pos_y
    changed_x, changed_y, pos_x, pos_y = 0, 0, 1, 1
    try :
        watermark.destroy()
    except :
        pass

tk.Label(text='请将水印文本输入到下方', bg='white', font=('微软雅黑-Tahoma-韩文版', 14)).place(
    x=0, y=0)
tk.Button(window, text='生\n成', command=create_, font=('微软雅黑-Tahoma-韩文版', 14)).place(
    x=215, y=0, width=30, height=50)
tk.Button(window, text='暂\n停', command=pause_, font=('微软雅黑-Tahoma-韩文版', 14)).place(
    x=215, y=50, width=30, height=50)

wm_text = tk.Text(window, font=('微软雅黑-Tahoma-韩文版', 14))
wm_text.place(x=0, y=30, width=195, height=70)
font_text = tk.Text(window, font=('微软雅黑-Tahoma-韩文版', 14))
font_text.place(x=195, y=30, width=20, height=70)

font_text.insert('insert', '14') #默认字号 | Default font size
wm_text.insert('insert', 'BiliBili_BHznJNs') #默认文本 | Default text
# 点击鼠标中键后显示水印 | Display the watermark when the Middle Mouse Button is pressed
window.bind('<Button-2>', lambda event : create_())
# 右键点击删除text文本框中文本 | Press the right key to clear the Text
wm_text.bind('<Button-3>', lambda event:wm_text.delete('0.0', 'end'))
# 点击关闭按钮时终止整个程序 | Press the close key to over the process
window.protocol('WM_DELETE_WINDOW', exit) 

window.mainloop()
