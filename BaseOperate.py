# -*-encoding:utf-8-*-
import subprocess
from config import *
import datetime
import shutil
import cv2
import numpy as np
import time
import sys

class BaseOperate:
    def __init__(self):
        self.screen = ""
        self.target = ""

    @staticmethod
    def tap(x0, y0):
        cmd_tap = 'adb shell input tap {x1} {y1}'.format(
            x1=x0,
            y1=y0
        )
        print(cmd_tap)
        subprocess.Popen(cmd_tap).wait()

    @staticmethod
    def screenshot():
        starttime = datetime.datetime.now()
        subprocess.Popen("adb shell screencap -p /sdcard/screen.png").wait()
        subprocess.Popen("adb pull /sdcard/screen.png").wait()
        subprocess.Popen("adb shell rm /sdcard/screen.png").wait()
        now_time = datetime.datetime.strftime(datetime.datetime.now(), "%H-%M-%S")
        #shutil.copyfile(screenshot_path + "screen.png", screenshot_path + now_time + ".png")
        endtime = datetime.datetime.now()
        print('{0} {1}'.format('截屏耗时', (endtime - starttime).seconds))

    @staticmethod
    def getTargetCoordinate(target_pic):
        img_rgb = cv2.imread(screenshot_path + "screen.png")
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("D:/work/jiji/blhx/assets/img/"+target_pic, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        allxy = []
        threshold = 0.7
        # print('图片{0}相似度{1}'.format(target_pic,res))
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            allxy.append(pt)
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        st_data = sorted(allxy, key=lambda x: x[0], reverse=False)
        print('st_data:%s' %st_data)
        if len(st_data) < 1:
            return -1
        print(st_data[0])
        return [st_data[0][0] + w/2, st_data[0][1] + h/2]
        # cv2.imshow("img", img_rgb)
        # cv2.waitKey(0)

    @staticmethod
    def selectEnemy():
        print('当前执行方法%s' %sys._getframe().f_code.co_name)
        searchTime = 0
        swipeTime = 0
        _xy = -1
        while _xy == -1:
            BaseOperate.screenshot()
            for enemy in enemy_pic:
                _xy = BaseOperate.getTargetCoordinate('common/{0}.png'.format(enemy))
                searchTime = searchTime + 1
                if _xy != -1:
                    break
            if _xy == -1:
                BaseOperate.swipe()
                swipeTime = swipeTime + 1
            if swipeTime > 2:
                BaseOperate.swipeBack()

        BaseOperate.tap(_xy[0], _xy[1])
        time.sleep(3)

    @staticmethod
    def selectEnemyCoordinate():
        print('当前执行方法%s' % sys._getframe().f_code.co_name)
        BaseOperate.screenshot()
        for enemy in enemy_pic:
            _xy = BaseOperate.getTargetCoordinate('common/{0}.png'.format(enemy))
            if _xy != -1:
                break
        return _xy

    @staticmethod
    def attack():
        print('当前执行方法%s' % sys._getframe().f_code.co_name)
        _xy = -1
        while _xy == -1:
            BaseOperate.screenshot()
            _xy = BaseOperate.getTargetCoordinate('common/sub_attack.png')
            if _xy == -1:
                _xy = BaseOperate.selectEnemyCoordinate()
                if _xy != -1:
                    BaseOperate.tap(_xy[0], _xy[1])
                    time.sleep(3)
                    _xy = -1
        BaseOperate.tap(_xy[0], _xy[1])
        time.sleep(40)

    @staticmethod
    def chooseAct(actUri):
        print('当前执行方法%s' %sys._getframe().f_code.co_name)
        BaseOperate.screenshot()
        _xy = BaseOperate.getTargetCoordinate('{0}.png'.format(actUri))
        if _xy != -1:
            BaseOperate.tap(_xy[0], _xy[1])
            time.sleep(1)
        return _xy


    @staticmethod
    def tapProcess(processImg):
        print('当前执行方法{0},图片{1}'.format(sys._getframe().f_code.co_name,processImg))
        _xy = -1
        while _xy == -1:
            BaseOperate.screenshot()
            _xy = BaseOperate.getTargetCoordinate('common/{0}.png'.format(processImg))
            if _xy == -1 and processImg == 'victor':
                # 防止出现掉落sr或新角色卡住
                BaseOperate.tap(960, 540)
            if _xy == -1 and processImg == 'wtconfirm':
                break
        if _xy != -1:
            BaseOperate.tap(_xy[0], _xy[1])
        # time.sleep(1)


    @staticmethod
    def changeRoleDouble():
        print('切换角色两次，获取当前角色视野')
        _xy = -1
        while _xy == -1:
            BaseOperate.screenshot()
            _xy = BaseOperate.getTargetCoordinate('common/changerole.png')
            if _xy != -1:
                BaseOperate.tap(_xy[0], _xy[1])
                time.sleep(2)
                BaseOperate.tap(_xy[0], _xy[1])
                time.sleep(1)

    @staticmethod
    def swipe():
        print('滑动屏幕')
        x1 = 960
        y1 = 540
        x2 = 1550
        y2 = 640
        timeLength = 1000
        cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {t}'.format(x1=x1, y1=y1, x2=x2, y2=y2, t=timeLength)
        subprocess.Popen(cmd).wait()

    @staticmethod
    def swipeBack():
        print('滑动屏幕')
        x1 = 960
        y1 = 540
        x2 = 520
        y2 = 330
        timeLength = 1000
        cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {t}'.format(x1=x1, y1=y1, x2=x2, y2=y2, t=timeLength)
        subprocess.Popen(cmd).wait()

    @staticmethod
    def closeWarningColor():
        print('关闭警告色')
        BaseOperate.tap(1850, 667)
        BaseOperate.tap(1709, 667)
        BaseOperate.tap(1612, 667)