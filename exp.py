#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
import random
import time
import tkinter
import pandas as pd

# 初始数据
tial_times = 30
inde = [i for i in range(11)]
inde1 = [i for i in range(10)]
# 建立存储字典result
result = {'name': 'null', 'sex': 'null', 'age': 0, 'average_x': [], 'cover': [], 'estimate': [],
          'block': [], 'id': []}
# gui
myDlg = gui.Dlg(title="实验")
myDlg.addText('被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['男', '女'])
myDlg.addField('年龄:', 21)
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
window = tkinter.Tk()
(w, h) = (1280, 720)
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
if not myDlg.OK:
    core.quit()
result['name'] = ok_data[0]
result['sex'] = ok_data[1]
result['age'] = ok_data[2]

# 读取刺激数据
dots = pd.read_csv("increase_dots.csv")
tr_dots = pd.read_csv("train.csv")
# 抽样总数
sample_size = int(len(dots)/11)
# 实验材料 [刺激, 遮挡位置0-2]
# 正式实验刺激
stims = [0]*3*sample_size
for i in range(sample_size):
    stims[3*i] = [dots[11*i:11*(i+1)], 0]
    stims[3*i][0].index = inde
    stims[3*i+1] = [dots[11*i:11*(i+1)], 1]
    stims[3*i+1][0].index = inde
    stims[3*i+2] = [dots[11*i:11*(i+1)], 2]
    stims[3*i+2][0].index = inde
# 练习刺激
tr_stims = [0]*6
tr_stims[0] = [dots[0:10], 0]
tr_stims[0][0].index = inde1
tr_stims[1] = [dots[0:10], 1]
tr_stims[1][0].index = inde1
tr_stims[2] = [dots[10:20], 1]
tr_stims[2][0].index = inde1
tr_stims[3] = [dots[10:20], 2]
tr_stims[3][0].index = inde1
tr_stims[4] = [dots[20:30], 2]
tr_stims[4][0].index = inde1
tr_stims[5] = [dots[20:30], 0]
tr_stims[5][0].index = inde1
# 随机刺激样本
random.shuffle(stims)
random.shuffle(tr_stims)
# 窗口
win = visual.Window(size=(w, h), units='pix', fullscr=True)
# 图片
fix = visual.ImageStim(win, image="fix.png", size=64)
pic = visual.ImageStim(win, size=64)
adjust_circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
block = visual.ShapeStim(win, lineColor='black', fillColor='black', closeShape=True)
# 文本
text_1 = visual.TextStim(win, text='按“↑”键或“↓”键调节圆半径大小', height=32, pos=(0, -200))
lianxi = visual.TextStim(win, text='按“空格”键开始练习', height=64)
zhengshi = visual.TextStim(win, text='按“空格”键开始正式实验', height=64)
# 练习
lianxi.draw()
win.flip()
event.waitKeys(keyList=['space'])
flag = 0
for i in range(len(tr_stims)):
    adjust_circle.radius = 64
    # 注视点
    fix.draw()
    win.flip()
    core.wait(0.3)
    # 遮挡范围
    b_x1 = 300*tr_stims[i][1]
    b_x2 = b_x1+300
    # 刺激
    for j in range(9):
        x, y, r= tr_stims[i][0]['x'][j], tr_stims[i][0]['y'][j], tr_stims[i][0]['r'][j]
        circle.pos = (x-450, y)
        circle.radius = r
        if (x<b_x1)or(x>b_x2):
            circle.draw()
    # 遮挡
    block.vertices = ((b_x1-450, -h/2), (b_x1-450, h/2), (b_x2-450, h/2), (b_x2-450, -h/2))
    block.draw()
    win.flip()
    core.wait(2)
    # 空屏
    win.flip()
    core.wait(0.5)
    # 调节
    state = 'adjust'
    adjust_circle.draw()
    text_1.draw()
    win.flip()
    event.clearEvents()
    while True:
        key = event.waitKeys(keyList=['up', 'down', 'space', 'escape'])
        # print(key)
        if 'up' in key:
            adjust_circle.radius += 1
        elif 'down' in key:
            adjust_circle.radius -= 1
        elif 'space' in key:
            event.clearEvents()
            break
        elif 'escape' in key:
            flag = 1
        if flag == 1:
            event.clearEvents()
            break
        adjust_circle.draw()
        text_1.draw()
        win.flip()
        event.clearEvents()
# 实验
zhengshi.draw()
win.flip()
event.waitKeys(keyList=['space'])
for i in range(len(stims)):
    adjust_circle.radius = 64
    # 注视点
    fix.draw()
    win.flip()
    core.wait(0.3)
    # 遮挡范围
    b_x1 = 300*stims[i][1]
    b_x2 = b_x1+300
    result['cover'].append(stims[i][1])
    result['average_x'].append(stims[i][0]['r'][10])
    # 刺激
    for j in range(10):
        x, y, r, num= stims[i][0]['x'][j], stims[i][0]['y'][j], stims[i][0]['r'][j], stims[i][0]['num'][j]
        circle.pos = (x-450, y)
        circle.radius = r
        if (x<b_x1)or(x>b_x2):
            circle.draw()
    # 遮挡
    block.vertices = ((b_x1-450, -h/2), (b_x1-450, h/2), (b_x2-450, h/2), (b_x2-450, -h/2))
    block.draw()
    win.flip()
    core.wait(2)
    # 空屏
    win.flip()
    core.wait(0.5)
    # 调节
    state = 'adjust'
    adjust_circle.draw()
    text_1.draw()
    win.flip()
    event.clearEvents()
    while True:
        key = event.waitKeys(keyList=['up', 'down', 'space', 'escape'])
        # print(key)
        if 'up' in key:
            adjust_circle.radius += 1
        elif 'down' in key:
            adjust_circle.radius -= 1
        elif 'space' in key:
            result['estimate'].append(adjust_circle.radius)
            event.clearEvents()
            break
        elif 'escape' in key:
            win.close()
            core.quit()
        adjust_circle.draw()
        text_1.draw()
        win.flip()
        event.clearEvents()

# 将实验结果写入文件
with open("exp_data\\%s.csv" % (result['name']+time.strftime("%H-%M-%S")), 'a') as exp_data:
    exp_data.write(
        'num' + ',' + 'name' + ',' + 'age' + ',' + 'sex' + ',' + 'average_r' + ',' + 'cover' + ','+'estimate_size'+'\n')
    for i in range(len(result['average_x'])):
        exp_data.write(str(i + 1) + ',' + result['name'] + ',' + str(result['age']) + ',' + result['sex'] + ',' +
                       str(round(result['average_x'][i], 2)) + ',' +
                       str(result['cover'][i]) + ',' + str(result['estimate'][i]) + '\n')

visual.TextStim(win, text="实验结束！", height=64).draw()
win.flip()
core.wait(2)
win.close()
core.quit()