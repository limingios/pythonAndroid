#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/13 23:09
# @Author  : Aries
# @Site    : 
# @File    : examplePc.py
# @Software: PyCharm

import win32api
import win32con
import win32gui
from ctypes import *
import time
import random
from PIL import ImageGrab
from PIL import Image
import operator
import math

import win32gui
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import auto_bot
from common.keyapi import VK_CODE
from pykeyboard import PyKeyboard

hwnd_title = dict()


def Key_event(self, key):
    win32api.keybd_event(key, 0, 0, 0)  #
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t is not "":
        print(h, t)

def mouse_click(x, y):
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def main():
    titles = set()
    auto_bot.init()
    hwnd = win32gui.FindWindow(0,"大话西游手游",)
    print(hwnd)
    win32gui.MoveWindow(hwnd, 20, 20, 805, 756, True)
    win32gui.SetForegroundWindow(hwnd)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot.jpg")
    _xy = auto_bot.getTargetCoordinatePC("screenshot.jpg","1.jpg")
    print(_xy)
    mouse_click(int(_xy[0])*2,int(_xy[1])*2+30)

    time.sleep(1);

    # 下一步
    screen2 = QApplication.primaryScreen()
    img = screen2.grabWindow(hwnd).toImage()
    img.save("screenshot2.jpg")
    _xy = auto_bot.getTargetCoordinatePC("screenshot2.jpg","2.jpg")
    print(_xy)
    mouse_click(int(_xy[0]) * 2, int(_xy[1]) * 2 + 30)

    time.sleep(1);
    key_input("zhugeaming1314");
    win32api.keybd_event(VK_CODE['shift'], 0, 0, 0)
    win32api.keybd_event(VK_CODE['2'], 0, 0, 0)
    win32api.keybd_event(VK_CODE['2'], 0, win32con.KEYEVENTF_KEYUP, 0)  #
    win32api.keybd_event(VK_CODE['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5);
    key_input("126.com");
    win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
    time.sleep(0.5);
    key_input("123456");
    win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)

    time.sleep(10);
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot3.jpg")
    _xy = auto_bot.getTargetCoordinatePC("screenshot3.jpg", "3.jpg")
    print(_xy)
    print(int(_xy[0]) * 2+40)
    print(int(_xy[1]) * 2+40)
    mouse_click(int(_xy[0]) * 2+40, int(_xy[1]) * 2+40)

    time.sleep(2);
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot4.jpg")
    _xy = auto_bot.getTargetCoordinatePC("screenshot4.jpg", "4.jpg")
    print(_xy)
    print(int(_xy[0]) * 2 + 40)
    print(int(_xy[1]) * 2 + 40)
    mouse_click(int(_xy[0]) * 2 + 40, int(_xy[1]) * 2 + 40)


def key_input(input_words):
    for word in input_words:
        win32api.keybd_event(VK_CODE[word], 0, 0, 0)
        win32api.keybd_event(VK_CODE[word], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
