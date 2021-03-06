#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
import random
import time
import tkinter
import pandas as pd
import numpy as np

# 初始数据
tial_times = 30

# 建立存储字典result m1不表征m2就近表征m3表征总体
result = {'name': 'null', 'sex': 'null', 'age': 0, 'average_r': [], 'cover': [], 'estimate': [], 'group': [],
          'block': [], 'id': [], 'm_1': [], 'm_2': [], 'm_3': [], 'adjust_size': []}
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
for i in range(4):
    ad[i] = [40, 50, 60, 70]*15
    random.shuffle(ad[i])
adjust_size = ad[0]+ad[1]+ad[2]+ad[3]

for i in range(sample_size):
    stims[i] = [dots[11*i:11*(i+1)], 0, 0]
    stims[i][0].index = inde
    stims[80+i] = [dots[11*i:11*(i+1)], 0, 0]
    stims[80+i][0].index = inde
    stims[160+i] = [dots[11*i:11*(i+1)], 0, 0]
    stims[160+i][0].index = inde
    stims[240+i] = [dots[11*i:11*(i+1)], 0, 0]
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
    random.shuffle(each)
random.shuffle(a)
stims = a[0]+a[1]+a[2]+a[3]
for i in range(len(stims)):
    stims[i][2] = adjust_size[i]

# 练习刺激
tr_stims = [0]*4*3
for i in range(4):
    tr_stims[3*i] = [tr_dots[11*i:11*(i+1)], 0]
    tr_stims[3*i][0].index = inde
    tr_stims[3*i+1] = [tr_dots[11*i:11*(i+1)], 1]
    tr_stims[3*i+1][0].index = inde
    tr_stims[3*i+2] = [tr_dots[11*i:11*(i+1)], 2]
    tr_stims[3*i+2][0].index = inde
stims_block = [stims[:60], stims[60:120], stims[120:180], stims[180:]]
# 随机刺激样本
random.shuffle(tr_stims)
# 窗口
win = visual.Window(size=(w, h), units='pix', fullscr=True, color=(-0.2, -0.2, -0.2))
myMouse = event.Mouse()
myMouse.setVisible(0)
# 图片
fix = visual.ImageStim(win, image="fix.png", size=64)
pic = visual.ImageStim(win, size=64)
p_block = visual.ImageStim(win, size=(300, h), image="p3.png")
adjust_circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
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
    p_block.pos = (b_x1-300, 0)
    p_block.draw()
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
flag = 0
for i in range(N):
    if i in [int(N/4), int(N/2), int(3*N/4)]:
        flag += 1
        area.draw()
        rest.draw()
        win.flip()
        key = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in key:
            break
    result['block'].append(flag)
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
    model_s1 = np.array([])  # 模型1 不表征
    model_s2 = np.array([])  # 模型2 就进取样
    model_s3 = np.array([])  # 模型3 表征总体
    aa = []
    for j in range(10):
        x, y, r = stims[i][0]['x'][j], stims[i][0]['y'][j], stims[i][0]['r'][j]
        circle.pos = (x-450, y)
        circle.radius = r
        if (x < b_x1) or (x > b_x2):
            circle.draw()
            model_s1 = np.append(model_s1, r)
            model_s2 = np.append(model_s2, r)
            model_s3 = np.append(model_s3, r)
        else:
            aa.append(j)
            if stims[i][0]['group'][10] == 'random':
                model_s2 = np.append(model_s2, 55)
                model_s3 = np.append(model_s3, 55)
            else:
                model_s2 = np.append(model_s2, r)
                if stims[i][0]['group'][10] == 'increase':
                    model_s3 = np.append(model_s3, 0.1*b_x1+25)
                else:
                    model_s3 = np.append(model_s3, 110-25-0.1*b_x1)
    #  模型二元素计算
    if stims[i][0]['group'][10] != 'random':
        if aa[0] == 0:
            for each in aa:
                model_s2[each] = model_s2[aa[-1]]
        elif aa[-1] == 9:
            for each in aa:
                model_s2[each] = model_s2[aa[0]]
        else:
            for each in aa:
                model_s2[each] = (model_s2[aa[-1]]+model_s2[aa[0]])/2
    result['m_1'].append(model_s1.mean())
    result['m_2'].append(model_s2.mean())
    result['m_3'].append(model_s3.mean())
    # 遮挡
    p_block.pos = (b_x1-300, 0)
    p_block.draw()
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
        + 'group' + ',' + 'model1' + ',' + 'model2' + ',' + 'model3' + ',' + 'block' + ',' + 'adjust_size' + '\n')
    for i in range(len(result['average_r'])):
        exp_data.write(str(result['id'][i]) + ',' + result['name'] + ',' + str(result['age']) + ',' + result['sex']
                       + ',' + str(round(result['average_r'][i], 2)) + ',' + str(result['cover'][i]) + ',' +
                       str(result['estimate'][i]) + ',' + result['group'][i] + ',' + str(result['m_1'][i]) + "," +
                       str(result['m_2'][i]) + ',' + str(result['m_3'][i]) + "," + str(result['block'][i])
                       + "," + str(adjust_size[i]) + '\n')

visual.TextStim(win, text="实验结束！", height=64).draw()
win.flip()
core.wait(2)
win.close()
core.quit()