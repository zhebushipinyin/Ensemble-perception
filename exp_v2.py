#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
import random
import time
import tkinter
import pandas as pd

# 初始数据
tial_times = 30

# 建立存储字典result
result = {'name': 'null', 'sex': 'null', 'age': 0, 'average_r': [], 'cover': [], 'estimate': [], 'group': [],
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
# 分布 r = kx+c, x[0~90]*10, k=0.1, c=10, r=55
dots = pd.read_csv("all_dots.csv")
inde = [i for i in range(11)]
tr_dots = pd.read_csv("train.csv")
# 抽样总数
sample_size = int(len(dots)/11)
# 实验材料 [刺激, 遮挡位置0-2, 反映圆大小]
# 正式实验刺激 sample_size = 20+20+40
stims = [0]*4*sample_size
pos = ['L', 'O', 'R', 'M']*80
ad = [0]*4
for i in range(len(ad)):
    ad[i] = [40, 70]*40
    random.shuffle(ad[i])
adjust_size = ad[0]+ad[1]+ad[2]+ad[3]

for i in range(sample_size):
    stims[i] = [dots[11*i:11*(i+1)], 0, adjust_size[i]]
    stims[i][0].index = inde
    stims[80+i] = [dots[11*i:11*(i+1)], 0, adjust_size[i]]
    stims[80+i][0].index = inde
    stims[160+i] = [dots[11*i:11*(i+1)], 0, adjust_size[i]]
    stims[160+i][0].index = inde
    stims[240+i] = [dots[11*i:11*(i+1)], 0, adjust_size[i]]
    stims[240+i][0].index = inde
# 矩阵赋值，遮位置LORM
for i in range(sample_size):
    stims[i][1] = pos[i]
    stims[80+i][1] = pos[80+i-1]
    stims[160+i][1] = pos[80+i-2]
    stims[240+i][1] = pos[80+i-3]
stims = [x for x in stims if x[1] != 'O']
a = [stims[0:60], stims[60:120], stims[120:180], stims[180:]]
for each in a:
    random.shuffle(a)
random.shuffle(a)
stims = a[0]+a[1]+a[2]+a[3]

# 练习刺激
tr_stims = [0]*3*3
for i in range(3):
    tr_stims[3*i] = [tr_dots[11*i:11*(i+1)], 0]
    tr_stims[3*i][0].index = inde
    tr_stims[3*i+1] = [tr_dots[11*i:11*(i+1)], 1]
    tr_stims[3*i+1][0].index = inde
    tr_stims[3*i+2] = [tr_dots[11*i:11*(i+1)], 2]
    tr_stims[3*i+2][0].index = inde
stims_block = [stims[:60], stims[60:120], stims[120:180], stims[180:]]
# 随机刺激样本
random.shuffle(stims)
random.shuffle(tr_stims)
random.shuffle(adjust_size)
# 窗口
win = visual.Window(size=(w, h), units='pix', fullscr=True, color=(-0.2, -0.2, -0.2))
# 图片
fix = visual.ImageStim(win, image="fix.png", size=64)
pic = visual.ImageStim(win, size=64)
adjust_circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
block = visual.ShapeStim(win, lineColor='black', fillColor='black', closeShape=True)
area = visual.ShapeStim(win, lineColor=(0,0,0), fillColor=(0,0,0), closeShape=True)
area.vertices = ((-450, -h/2), (-450, h/2), (450, h/2), (450, -h/2))
# 文本
text_1 = visual.TextStim(win, text='按“↑”键或“↓”键调节圆半径大小', height=32, pos=(0, -200))
lianxi = visual.TextStim(win, text='按“空格”键开始练习', height=40)
zhengshi = visual.TextStim(win, text='按“空格”键开始正式实验', height=40)
rest = visual.TextStim(win, text='休息一下，按“空格”键继续', height=40)
# 练习
lianxi.draw()
win.flip()
event.waitKeys(keyList=['space'])
flag = 0
for i in range(len(tr_stims)):
    adjust_circle.radius = random.choice([40, 70])
    # 注视点
    area.draw()
    fix.draw()
    win.flip()
    core.wait(0.3)
    # 遮挡范围
    b_x1 = 300*tr_stims[i][1]
    b_x2 = b_x1+300
    # 刺激
    area.draw()
    for j in range(10):
        x, y, r= tr_stims[i][0]['x'][j], tr_stims[i][0]['y'][j], tr_stims[i][0]['r'][j]
        circle.pos = (x-450, y)
        circle.radius = r
        if (x<b_x1)or(x>b_x2):
            circle.draw()
    # 遮挡
    block.vertices = ((b_x1-450, -h/2), (b_x1-450, h/2), (b_x2-450, h/2), (b_x2-450, -h/2))
    block.draw()
    win.flip()
    # 呈现时长
    core.wait(1)
    # 空屏
    area.draw()
    win.flip()
    core.wait(0.5)
    # 调节
    state = 'adjust'
    area.draw()
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
        area.draw()
        adjust_circle.draw()
        text_1.draw()
        win.flip()
        event.clearEvents()

# 实验
area.draw()
zhengshi.draw()
win.flip()
event.waitKeys(keyList=['space'])
N = len(stims)
for i in range(N):
    if i in [int(N/4), int(N/2), int(3*N/4)]:
        area.draw()
        rest.draw()
        win.flip()
        key = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in key:
            break
    adjust_circle.radius = stims[i][2]
    # 注视点
    area.draw()
    fix.draw()
    win.flip()
    core.wait(0.5)
    # 遮挡范围
    if stims[i][1] == 'L':
        b_x1 = 0
    elif stims[i][1] == 'M':
        b_x1 = 300
    else:
        b_x1 = 600
    b_x2 = b_x1+300
    area.draw()
    result['cover'].append(stims[i][1])
    result['average_r'].append(stims[i][0]['r'][10])
    result['id'].append(stims[i][0]['num'][10])
    result['group'].append(stims[i][0]['group'][10])
    # 刺激
    for j in range(10):
        x, y, r = stims[i][0]['x'][j], stims[i][0]['y'][j], stims[i][0]['r'][j]
        circle.pos = (x-450, y)
        circle.radius = r
        if (x<b_x1)or(x>b_x2):
            circle.draw()
    # 遮挡
    block.vertices = ((b_x1-450, -h/2), (b_x1-450, h/2), (b_x2-450, h/2), (b_x2-450, -h/2))
    block.draw()
    win.flip()
    # 呈现时长
    core.wait(1)
    # 空屏
    area.draw()
    win.flip()
    core.wait(0.5)
    # 调节
    state = 'adjust'
    area.draw()
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
        area.draw()
        adjust_circle.draw()
        text_1.draw()
        win.flip()
        event.clearEvents()

# 将实验结果写入文件
with open("exp_data\\%s.csv" % (result['name']+time.strftime("%H-%M-%S")), 'a') as exp_data:
    exp_data.write(
        'num' + ',' + 'name' + ',' + 'age' + ',' + 'sex' + ',' + 'average_r' + ',' + 'cover' + ','+'estimate_size' + ','
        + 'group' +'\n')
    for i in range(len(result['average_r'])):
        exp_data.write(str(result['id'][i]) + ',' + result['name'] + ',' + str(result['age']) + ',' + result['sex']
                       + ',' + str(round(result['average_r'][i], 2)) + ',' +
                       str(result['cover'][i]) + ',' + str(result['estimate'][i]) + ',' + result['group'][i]+ '\n')

visual.TextStim(win, text="实验结束！", height=64).draw()
win.flip()
core.wait(2)
win.close()
core.quit()