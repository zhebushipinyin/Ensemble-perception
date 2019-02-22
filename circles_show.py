#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import random
import numpy as np
import pandas as pd

# 初始数据
tial_times = 30
inde = [i for i in range(10)]
(w, h) = (1280, 768)
dots = pd.read_csv("dots.csv")
stims = [0]*3*int(len(dots)/10)
for i in range(int(len(dots)/10)):
    stims[3*i] = [dots[10*i:10*(i+1)], 0]
    stims[3*i][0].index = inde
    stims[3*i+1] = [dots[10*i:10*(i+1)], 1]
    stims[3*i+1][0].index = inde
    stims[3*i+2] = [dots[10*i:10*(i+1)], 2]
    stims[3*i+2][0].index = inde
# 刺激样本
sample = []  # sample List
trial = random.shuffle(sample*tial_times)
# 窗口
win = visual.Window(size=(w, h), units='pix', fullscr=True)
fix = visual.ImageStim(win, image="fix.png", size=64)
pic = visual.ImageStim(win, size=64)
adjust_circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
circle = visual.Circle(win, radius=64, lineColor='white', fillColor='white')
block = visual.ShapeStim(win, lineColor='black', fillColor='black', closeShape=True)
# 实验
for i in range(len(stims)):
    adjust_circle.radius = 64
    pic.image = 'hp.png'
    # 注视点
    fix.draw()
    win.flip()
    core.wait(0.3)
    # 遮挡范围
    b_x1 = 300*stims[i][1]
    b_x2 = b_x1+300
    # 刺激
    for j in range(9):
        x, y, r = stims[i][0]['x'][j], stims[i][0]['y'][j], stims[i][0]['r'][j]
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
    win.flip()
    event.clearEvents()
    while True:
        key = event.waitKeys(keyList=['up', 'down', 'space', 'escape'])
        print(key)
        if 'up' in key:
            adjust_circle.radius += 1
        elif 'down' in key:
            adjust_circle.radius -= 1
        elif 'space' in key:
            event.clearEvents()
            break
        elif 'escape' in key:
            win.close()
            core.quit()
        adjust_circle.draw()
        win.flip()
        event.clearEvents()

win.close()
core.quit()
