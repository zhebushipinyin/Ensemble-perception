#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import random

# 初始数据
tial_times = 30
(w, h) = (1024, 768)
# 刺激样本
sample = []  # sample List
trial = random.shuffle(sample*tial_times)
# 窗口
win = visual.Window(size=(w, h), fullscr= False, units='pix')
fix = visual.ImageStim(win, image="fix.png", size=64)
pic = visual.ImageStim(win, size=64)
adjust_circle = visual.Circle(win, radius=64, lineColor='red')
# 实验
for i in range(2):
    pic.image = 'hp.png'
    # 注视点
    fix.draw()
    win.flip()
    core.wait(0.3)
    # 刺激
    pic.draw()
    win.flip()
    core.wait(0.5)
    # 空屏
    win.flip()
    core.wait(0.5)
    # 调节
    state = 'adjust'
    adjust_circle.draw()
    win.flip()
    event.clearEvents()
    while True:
        key = event.waitKeys(keyList=['up', 'down', 'space'])
        print(key)
        if 'up' in key:
            adjust_circle.radius += 1
        elif 'down' in key:
            adjust_circle.radius -= 1
        elif 'space' in key:
            event.clearEvents()
            break
        adjust_circle.draw()
        win.flip()
        event.clearEvents()

win.close()
core.quit()

