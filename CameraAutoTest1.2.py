# -*- coding:utf8 -*- #
"""
    @Time  : 2019/11/21/10:35
    @Author: Andy deng
"""
# -*- coding:utf8 -*- #
"""
    @Time  : 2020/7/15/18:14
    @Author: Andy deng
"""
import os,time
import re,threading
import uiautomator2 as u2
times = 50

#获取所有连接电脑的Devices ID
def getDevices():
    os.popen('adb devices')
    os.popen('adb wait-for-device')
    test = os.popen("adb devices").read().strip()
    Devices = re.split(r'\W+',test)
    devicesList  = [Devices[one] for one in range(4,len(Devices),2)]
    print(f'已获取{len(devicesList)}台设备>>>>>{devicesList}')
    return devicesList

def getWlanAddr(devicesList):

    wlanAddrList = []
    for one in range(0, len(devicesList)):
        addr = os.popen(f"adb -s {devicesList[one]} shell ifconfig wlan0 | findstr inet")
        addr = addr.read().strip()
        addrlist = addr.split('Bcast')
        for one in addrlist:
            two = one.strip().split(':')[1]
            wlanAddrList.append(two)
            break
    print(wlanAddrList)
    return wlanAddrList

def installAtxServer(devices):

    semaphone.acquire()
    os.popen('adb -s {devices} wait-for-device')
    time.sleep(3)
    test = os.popen(f"python -m uiautomator2 init -s {devices}")
    context = test.read()
    if "Successfully" in context:
        print(f'\n{devices} ATX server安装成功')
    else:
        print(f'\n{devices} ATX server安装失败，尝试重新安装')
        os.system(f'python -m uiautomator2 init --server $IP -s {devices}')
        os.system("adb wait-for-device")
        test = os.popen(f'python -m uiautomator2 init -s {devices}')
        context2 = test.read()
        if "Successfully" in context2:
            print(f'\n{devices} 安装成功')
        else:
            print(f'\n{devices} 请手动安装u2所需应用')
            input('\n安装成功后，按任意按键开始测试')

    os.system("adb wait-for-device")

    semaphone.release()

def writeResult(info):
    if os.path.exists(r'D:\autoCamera'):
        pass
    else:
        os.mkdir(r'D:\autoCamera')
    with open(fr'D:\autoCamera\Camera.txt','a+') as f:
        f.write(info)
        f.close()

def photoResoSetup(d,setup = 0,teardown = False):

    resolution = [d(description="Framestandard"), d(description="Framesquare"), d(description="Framefull"),
                  d(description="Frame16_9")] #4:3,1:1,FULL,16:9
    if d(description="PHOTO").exists:
        if d(description="SubSetOff").exists:
            d(description="SubSetOff").click()
            time.sleep(2)
        elif  d(description="SubSetOn").exists:
            d(description="SubSetOn").click()
            time.sleep(2)
        for one in range(setup):
            if resolution[one].exists:
                if d(resourceId="com.oneplus.camera:id/oppo_subsetting_bar").exists:
                    resolution[one].click()
                    time.sleep(1)
        if teardown == True:
            for one in range(len(resolution)):
                if resolution[one].exists:
                    #print(str(resolution[one]),setup,setup in str(resolution[one]))
                    if d(resourceId="com.oneplus.camera:id/oppo_subsetting_bar").exists:
                        resolution[one].click()
                        time.sleep(1)
            d.click(0.5, 0.5)
            time.sleep(1)
    time.sleep(2)

def photoShoot(d,caseNum,caseName,deviceID,flishTime=1,brust=False,switchResolution =False,switchZoom =False):
    for one in range(times):
        try:
            if brust == True:
                d.long_click(0.501, 0.84, 4)
                time.sleep(flishTime)
            elif switchResolution == True:
                photoResoSetup(d, 0, True)
                d(resourceId="com.oneplus.camera:id/shutter_button").click()
                time.sleep(flishTime)
            elif switchZoom == True:
                swithZoom(d, '2x')
                swithZoom(d, '1x')
                d(resourceId="com.oneplus.camera:id/shutter_button").click()
                time.sleep(flishTime)
            else:
                d(resourceId="com.oneplus.camera:id/shutter_button").click()
                time.sleep(flishTime)
                # print('case01 ',case01+'第'+ f'{one}次',f'测试 {(wlanAddr)} >>> Pass')
        except:
            time.sleep(2)
            if d(resourceId="com.oneplus.camera:id/shutter_button").exists:
                pass
            else:
                info = f"{caseNum} {caseName} 第 {one}次  测试 {(deviceID)} >>> Flase\r\n"
                print(info)
                writeResult(info)
                d.screenshot(rf"D:\autoCamera\{caseNum}第{one}次测试-{(deviceID)}.jpg")
                raise Exception('未在相机页面')

def changeCameraMode(d,caseNum,caseName,deviceID,flishTime=1,switchFace=False,menuMode='',toMenumode=''):
    for one in range(times):
        try:
                if menuMode:
                    setMenuMode(d,menuMode)
                    setMenuMode(d,toMenumode)
                    setMenuMode(d,menuMode)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(flishTime)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(flishTime)
                    if d(description="SetOff").exists or d(description="SetOn").exists:
                        pass
                    else:
                        d(resourceId="com.oneplus.camera:id/shutter_button").click()
                elif switchFace ==True:
                    d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
                    time.sleep(1)
                    d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
                    time.sleep(1)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(flishTime)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(1)
                else:
                    time.sleep(1)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(flishTime)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(1)
                    if d(description="SetOff").exists or d(description="SetOn").exists:
                        pass
                    else:
                        d(resourceId="com.oneplus.camera:id/shutter_button").click()
                # print('case01 ',case01+'第'+ f'{one}次',f'测试 {(wlanAddr)} >>> Pass')
        except:
            time.sleep(2)
            if d(resourceId="com.oneplus.camera:id/shutter_button").exists:
                pass
            else:
                info = f"{caseNum} {caseName} 第 {one}次  测试 {(deviceID)} >>> Flase\r\n"
                print(info)
                writeResult(info)
                d.screenshot(rf"D:\autoCamera\{caseNum}第{one}次测试-{(deviceID)}.jpg")
                raise Exception('未在相机页面')
def changeCameraMoreMode(d,caseNum,caseName,deviceID,flishTime=1,menuMode='',toMenumode='',toMoreMode=''):

    if menuMode:
        setMenuMode(d, menuMode)
        setMenuMode(d, toMenumode)
        setMoreMenuMode(d, toMoreMode)
    for one in range(times):
        try:
                if menuMode:
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(flishTime)
                    d(resourceId="com.oneplus.camera:id/shutter_button").click()
                    time.sleep(1)
                    if d(description="SetOff").exists or d(description="SetOn").exists:
                        pass
                    else:
                        d(resourceId="com.oneplus.camera:id/shutter_button").click()
        except:
            time.sleep(2)
            if d(resourceId="com.oneplus.camera:id/shutter_button").exists:
                pass
            else:
                info = f"{caseNum} {caseName} 第 {one}次  测试 {(deviceID)} >>> Flase\r\n"
                print(info)
                writeResult(info)
                d.screenshot(rf"D:\autoCamera\{caseNum}第{one}次测试-{(deviceID)}.jpg")
                raise Exception('未在相机页面')

def swithZoom(d,zoom='2x'):
    if zoom == '2x':
        if d(description="Zoom Seek Bar1x").exists:
            d.click(0.504, 0.656)
    if zoom == '1x':
        if d(description="Zoom Seek Bar2x").exists:
            d.click(0.504, 0.656)

def rearFrontSwitch(d,face = 'rear'):
    time.sleep(1)
    if face == 'front':
        if d(description="Dazzle ColorOff").exists or d(description="Dazzle ColorOn").exists :
            d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
            time.sleep(1)
        else:
            d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
            time.sleep(1)
    if face == 'rear':
            if d(resourceId="com.oneplus.camera:id/face_beauty_enter_button").exists:
                d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
                time.sleep(1)
            else:
                if d(resourceId="com.oneplus.camera:id/switch_camera_button").exists:
                    d(resourceId="com.oneplus.camera:id/switch_camera_button").click()
                    time.sleep(1)

def switchFlash(d,face= 'rear',flash = 'on'):
    #d(description="Fill Light ModeOff")
    time.sleep(1)
    rearFlashList = [d(description="Flash ModeOff"),d(description="Flash ModeOn"),d(description="Flash ModeAuto"),d(description="Flash ModeFill Light")]
    frontFlashList = [d(description="Fill Light ModeOff"),d(description="Fill Light ModeOn"),d(description="Fill Light ModeAuto")]
    if face == 'rear':
        if flash == 'on':
            for one in range(len(rearFlashList)):
                if rearFlashList[one].exists:
                    if d(description="Flash ModeOn").exists:
                        pass
                    else:
                        rearFlashList[one].click()
                        time.sleep(2)
                        d(text="On").click()
                        break
        elif flash == 'Fill Light':
            for one in range(len(rearFlashList)):
                if rearFlashList[one].exists:
                    if d(description="Flash ModeFill Light").exists:
                        pass
                    else:
                        rearFlashList[one].click()
                        time.sleep(2)
                        d(text="Fill Light").click()
                        break
        else:
            for one in range(len(rearFlashList)):
                if rearFlashList[one].exists:
                    if d(description="Flash ModeOff").exists:
                        pass
                    else:
                        rearFlashList[one].click()
                        time.sleep(2)
                        if d(text="Off").exists:
                            d(text="Off").click()
                        elif d(text="OFF").exists:
                            d(text="OFF").click()
                        break

    elif face == 'front':
        if flash == 'on':
            for one in range(len(frontFlashList)):
                #print(frontFlashList[one].exists)
                if frontFlashList[one].exists:
                    if d(description="Flash ModeOn").exists:
                        pass
                    else:
                        frontFlashList[one].click()
                        time.sleep(1)
                        d(text="On").click()
                        break
        else:
            for one in range(len(frontFlashList)):
                if frontFlashList[one].exists:
                    if d(description="Flash ModeOff").exists:
                        pass
                    else:
                        frontFlashList[one].click()
                        time.sleep(1)
                        d(text="Off").click()
                        break
def filter(d,filter = True):
    if  filter == True:
        if d(description="Filteroff").exists or d(description="portrait new styleoff").exists:
            if d(resourceId="com.oneplus.camera:id/effect_scrollbar").exists:
                d.swipe_ext("left", 0.5)
                time.sleep(1)
                d.click(0.457, 0.404)
            else:
                if d(description="Filteroff").exists:
                    d(description="Filteroff").click()
                if d(description="portrait new styleoff").exists:
                    d(description="portrait new styleoff").click()
                d.swipe_ext("left", 0.5)
                time.sleep(1)
                d.click(0.457, 0.404)
    else:
        if d(resourceId="com.oneplus.camera:id/effect_scrollbar").exists:
            d.swipe_ext("right", 0.5)
            time.sleep(1)
            d.click(0.457, 0.404)
        else:
            if d(description="Filteroff").exists:
                d(description="Filteroff").click()
            if d(description="portrait new styleon").exists:
                d(description="portrait new styleon").click()
            d.swipe_ext("right", 0.5)
            time.sleep(1)
            d.click(0.457, 0.404)

def  setMenuMode(d,menuMode):
    time.sleep(2)
    if menuMode == 'video':
        time.sleep(1)
        if d(description="PHOTO").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
        elif d(description="PORTRAIT").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
            d.swipe_ext("right", 0.6)
        elif d(description="MORE").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
            d.swipe_ext("right", 0.6)
            time.sleep(1)
        else:
            pass

    elif menuMode == 'photo':
        time.sleep(1)
        if d(description="SetOff").exists or d(description="SetOn").exists:
            d.swipe_ext("left", 0.6)
            time.sleep(1)
        elif d(description="PORTRAIT").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
        elif d(description="MORE").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
        else:
            pass

    elif menuMode == 'more':
        time.sleep(1)
        if d(description="PHOTO").exists:
            d.swipe_ext("left", 0.6)
            time.sleep(1)
            d.swipe_ext("left", 0.6)
        elif d(description="SetOff").exists or d(description="SetOn").exists:
            d.swipe_ext("left", 0.6)
            time.sleep(1)
            d.swipe_ext("left", 0.6)
            time.sleep(1)
            d.swipe_ext("left", 0.6)
        elif d(description="PORTRAIT").exists:
            d.swipe_ext("left", 0.6)
    elif menuMode == 'portrait':
        time.sleep(1)
        if d(description="PHOTO").exists:
            d.swipe_ext("left", 0.6)
            time.sleep(1)
        elif d(description="SetOff").exists or d(description="SetOn").exists:
            d.swipe_ext("left", 0.6)
            time.sleep(1)
            d.swipe_ext("left", 0.6)
            time.sleep(1)
        elif d(description="MORE").exists:
            d.swipe_ext("right", 0.6)
            time.sleep(1)
        elif d(description="PORTRAIT").exists:
             pass

def setMoreMenuMode(d,mode):

    if mode:  # MacroOn MacroOFF
        if 'MacroOn' in mode:  # TIME-LAPSE PRO
            if d.xpath('//*[@content-desc="Macro"]').exists:
                d.xpath('//*[@content-desc="Macro"]').click()
        elif 'TIME-LAPSEOn' in mode:
            if d.xpath('//*[@content-desc="TIME-LAPSE"]').exists:
                d.xpath('//*[@content-desc="TIME-LAPSE"]').click()
        elif 'PROOn' in mode:
            if d.xpath('//*[@content-desc="PRO"]').exists:
                d.xpath('//*[@content-desc="PRO"]').click()
        elif 'OFF' in mode:
            if d(resourceId="com.oneplus.camera:id/mode_close").exists:
                d(resourceId="com.oneplus.camera:id/mode_close").click()

def switchVideoResolution(d,resolution='1080'):

    #d(resourceId="android:id/title", text="VIDEO")
    if d(description="SetOff").exists:
        d(description="SetOff").click()
    elif d(description="SetOn").exists:
        d(description="SetOn").click()
    else:
        setMenuMode(d,'video')
        if d(description="SetOff").exists:
            d(description="SetOff").click()
        elif d(description="SetOn").exists:
            d(description="SetOn").click()
    for one in range(10):
        d.swipe_ext('up',0.6)
        time.sleep(1)
        if d(resourceId="android:id/title", text="Video Resolution").exists:
            d(resourceId="android:id/title", text="Video Resolution").click()
            break
    if '1080' in resolution:
        time.sleep(1)
        if d(resourceId="com.oneplus.camera:id/pref_title", text="1080P").exists:
            d(resourceId="com.oneplus.camera:id/pref_title", text="1080P").click()
            d.press("back")
            d.press("back")
    elif '720' in resolution:
        time.sleep(1)
        if d(resourceId="com.oneplus.camera:id/pref_title", text="720P").exists:
            d(resourceId="com.oneplus.camera:id/pref_title", text="720P").click()
            d.press("back")
            d.press("back")
def cameraCloseShutterSound(d):

    if d(description="SubSetOff").exists:
        d(description="SubSetOff").click()
        time.sleep(1)
        d(description="Set").click()
        time.sleep(1)
        d(resourceId="android:id/title", text="Shutter sound").click()
        time.sleep(1)
        d.press("back")
    elif d(description="SubSetOn").exists:
        d(description="SubSetOn").click()
        time.sleep(1)
        d(description="Set").click()
        time.sleep(1)
        d(resourceId="android:id/title", text="Shutter sound").click()
        time.sleep(1)
        d.press("back")

def start_test(device):

    semaphone.acquire()
    d = u2.connect(f'{device}')
    print(f'{device} 已连接对应设备')
    d.implicitly_wait(10.0)

    #确保相机亮屏
    while True:
        d.press('home')
        time.sleep(2)
        if d(resourceId="com.google.android.setupwizard:id/welcome_emergency_dial").exists or d.xpath('//*[@resource-id="com.oneplus.provision:id/oos_emergency_call_layout"]').exists:
            break
        elif d(text='Messages'):
            break
        else:
            d.press('power')
            d.swipe(0.5, 0.9, 0.5, 0.6, 0.2, 10)
            time.sleep(1)
    #启动相机
    if d(text="Camera").exists:
        d.app_start('com.oneplus.camera')
        time.sleep(1)
        if d(resourceId="com.android.permissioncontroller:id/permission_allow_button").exists:
            d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click()
            time.sleep(1)
    else:
        d.press("back")
        d.press("back")
        d.press("home")
        if d(text="Camera").exists:
            d.app_start('com.oneplus.camera')
            time.sleep(2)
            if d(resourceId="com.android.permissioncontroller:id/permission_allow_button").exists:
                d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click()
                time.sleep(1)

    cameraCloseShutterSound(d) #关闭相机声音

    while True:

        case00 = 'Rear shooting(4:3, default)'
        caseNum = "case00"
        print('case00 ', case00 + '开始测试')
        photoResoSetup(d, 0)
        photoShoot(d,caseNum,case00,device)
        photoResoSetup(d, 0, True)
        print('case00 ', case00 + ' 结束测试')

        case01 = 'Rear shooting(1:1, default)'
        caseNum = "case01"
        print('case01 ',case01+'开始测试')
        photoResoSetup(d,1)
        photoShoot(d, caseNum,case01, device)
        photoResoSetup(d,0,True)
        print('case01 ',case01+' 结束测试')

        case02 = 'Rear shooting(Full, default)'
        caseNum = "case02"
        print('case02 ', case02+ '开始测试')
        photoResoSetup(d, 2)
        photoShoot(d, caseNum,case02, device)
        photoResoSetup(d, 0, True)
        print('case02 ', case02 + ' 结束测试')

        case03 = 'Rear shooting(16:9, default)'
        caseNum = "case03"
        print('case03 ', case03 + '开始测试')
        photoResoSetup(d, 3)
        photoShoot(d, caseNum,case03, device)
        photoResoSetup(d, 0, True)
        print('case03 ', case03 + ' 结束测试')

        case04 = 'Rear shooting(4:3, flash)'
        caseNum = "case04"
        print('case04 ', case04 + '开始测试')
        switchFlash(d, 'rear', 'on')
        photoShoot(d,caseNum, case04, device,3)
        switchFlash(d, 'rear', 'off')
        print('case04 ', case04 + ' 结束测试')

        case05 = 'Rear shooting(1:1, flash)'
        caseNum = "case05"
        print('case05 ', case05  + '开始测试')
        switchFlash(d, 'rear', 'on')
        photoShoot(d, caseNum,case05, device, 3)
        switchFlash(d, 'rear', 'off')
        print('case05 ', case05 + ' 结束测试')

        case06 = 'Rear shooting(Full, flash)'
        caseNum = "case06"
        print('case06 ', case06 + '开始测试')
        switchFlash(d, 'rear', 'on')
        photoShoot(d,caseNum, case06, device, 3)
        switchFlash(d, 'rear', 'off')
        print('case06 ', case06 + ' 结束测试')

        case07 = 'Rear shooting(16:9, flash)'
        caseNum = "case07"
        print('case07 ', case07  + '开始测试')
        switchFlash(d, 'rear', 'on')
        photoShoot(d,caseNum, case07, device, 3)
        switchFlash(d, 'rear', 'off')
        print('case07 ', case07 + ' 结束测试')

        case08 = 'Rear shooting(4:3, HDR)'
        caseNum = "case08"
        print('case08 ', case08 + '开始测试')
        if d(description="HDR FunctionOff").exists:
            d(description="HDR FunctionOff").click()
            time.sleep(1)
            d(text="On").click()
        photoShoot(d,caseNum, case08, device, 1)
        if d(description="HDR FunctionOn").exists:
            d(description="HDR FunctionOn").click()
            d(text="Off").click()
        print('case08 ', case08 + ' 结束测试')

        case09 = 'Rear shooting(1:1, HDR)'
        caseNum = "case09"
        print('case09 ', case09 + '开始测试')
        if d(description="HDR FunctionOff").exists:
            d(description="HDR FunctionOff").click()
            time.sleep(1)
            d(text="On").click()
        photoResoSetup(d,1)
        photoShoot(d, caseNum, case09, device, 1)
        photoResoSetup(d, 0, True)
        if d(description="HDR FunctionOn").exists:
            d(description="HDR FunctionOn").click()
            d(text="Off").click()
        print('case09 ', case09 + ' 结束测试')

        case10 = 'Rear shooting(FULL, HDR)'
        caseNum = "case10"
        print('case10 ', case10 + '开始测试')
        if d(description="HDR FunctionOff").exists:
            d(description="HDR FunctionOff").click()
            time.sleep(1)
            d(text="On").click()
        photoResoSetup(d, 2)
        photoShoot(d, caseNum, case10, device, 1)
        photoResoSetup(d, 0, True)
        if d(description="HDR FunctionOn").exists:
            d(description="HDR FunctionOn").click()
            d(text="Off").click()
        print('case10 ', case10 + ' 结束测试')

        case11 = 'Rear shooting(16:9, HDR)'
        caseNum = "case11"
        print('case11 ', case11 + '开始测试')
        if d(description="HDR FunctionOff").exists:
            d(description="HDR FunctionOff").click()
            time.sleep(1)
            d(text="On").click()
        photoResoSetup(d, 3)
        photoShoot(d, caseNum, case11, device, 1)
        photoResoSetup(d, 0, True)
        if d(description="HDR FunctionOn").exists:
            d(description="HDR FunctionOn").click()
            d(text="Off").click()
        print('case11 ', case11 + ' 结束测试')

        case12 = 'Rear shooting(4:3, Dazzle Color)'
        caseNum = "case12"
        print('case12 ', case12 + '开始测试')
        if d(description="Dazzle ColorOff").exists:
            d(description="Dazzle ColorOff").click()
            time.sleep(1)
        photoShoot(d, caseNum,case12, device, 1)
        if d(description="Dazzle ColorOn").exists:
            d(description="Dazzle ColorOn").click()
        print('case12 ', case12 + ' 结束测试')

        case13 = 'Rear shooting(4:3, Dazzle Color)'
        caseNum = "case13"
        print('case13 ', case13 + '开始测试')
        if d(description="Dazzle ColorOff").exists:
            d(description="Dazzle ColorOff").click()
            time.sleep(1)
        photoShoot(d, caseNum,case13, device, 1)
        if d(description="Dazzle ColorOn").exists:
            d(description="Dazzle ColorOn").click()
        print('case13 ', case13 + ' 结束测试')

        case14 = 'Rear shooting(1:1, Dazzle Color)'
        caseNum = "case14"
        print('case14 ', case14+ '开始测试')
        if d(description="Dazzle ColorOff").exists:
            d(description="Dazzle ColorOff").click()
            time.sleep(1)
        photoResoSetup(d,1)
        photoShoot(d, caseNum,case14, device, 1)
        photoResoSetup(d,0,True)
        if d(description="Dazzle ColorOn").exists:
            d(description="Dazzle ColorOn").click()
        print('case14 ', case14 + ' 结束测试')

        case15 = 'Rear shooting(FULL, Dazzle Color)'
        caseNum = "case15"
        print('case15 ', case15  + '开始测试')
        if d(description="Dazzle ColorOff").exists:
            d(description="Dazzle ColorOff").click()
            time.sleep(1)
        photoResoSetup(d, 1)
        photoShoot(d, caseNum,case15, device, 1)
        photoResoSetup(d, 0, True)
        if d(description="Dazzle ColorOn").exists:
            d(description="Dazzle ColorOn").click()
        print('case15 ', case15 + ' 结束测试')

        case16 = 'Rear shooting(16:9, Dazzle Color)'
        caseNum = "case16"
        print('case16 ', case16 + '开始测试')
        if d(description="Dazzle ColorOff").exists:
            d(description="Dazzle ColorOff").click()
            time.sleep(1)
        photoResoSetup(d, 1)
        photoShoot(d, caseNum,case16, device, 1)
        photoResoSetup(d, 0, True)
        if d(description="Dazzle ColorOn").exists:
            d(description="Dazzle ColorOn").click()
        print('case16 ', case16 + ' 结束测试')

        case17 = 'Rear shooting(4:3, burst)'
        caseNum = "case17"
        print('case17 ', case17 + '开始测试')
        photoResoSetup(d, 0)
        photoShoot(d,caseNum,case17,device,1,True)
        #photoResoSetup(d, 0, True)
        print('case17 ', case17 + ' 结束测试')

        case18 = 'Rear shooting(1:1, burst)'
        caseNum = "case18"
        print('case18 ', case18  + '开始测试')
        photoResoSetup(d, 1)
        photoShoot(d, caseNum,case18, device, 1, True)
        photoResoSetup(d, 0, True)
        print('case18 ', case18 + ' 结束测试')

        case19 = 'Rear shooting(FULL, burst)'
        caseNum = "case19"
        print('case19 ', case19 + '开始测试')
        photoResoSetup(d, 2)
        photoShoot(d, caseNum,case19, device, 1, True)
        photoResoSetup(d, 0, True)
        print('case19 ', case19 + ' 结束测试')

        case20 = 'Rear shooting(16:9, burst)'
        caseNum = "case20"
        print('case20 ', case20 + '开始测试')
        photoResoSetup(d, 3)
        photoShoot(d, caseNum,case20, device, 1, True)
        photoResoSetup(d, 0, True)
        print('case20 ', case20 + ' 结束测试')

        case21 = 'Rear resolution cycle switching and shooting'
        caseNum = "case21"
        print('case21 ', case21 + '开始测试')
        # photoResoSetup(d, 0, True)
        photoShoot(d, caseNum,case21, device, 1, False,True)
        print('case21 ', case21 + ' 结束测试')

        case22 = 'Rear shooting(2x zoom)'
        caseNum = "case22"
        print('case22 ', case22 + '开始测试')
        photoResoSetup(d, 0)
        swithZoom(d,'2x')
        photoShoot(d,caseNum,case22,device)
        photoResoSetup(d, 0, True)
        swithZoom(d, '1x')
        print('case22 ', case22 + ' 结束测试')

        case23 = 'Front shooting(4:3)'
        caseNum = "case23"
        print('case23 ', case23 + '开始测试')
        rearFrontSwitch(d,'front')
        photoShoot(d,caseNum,case23,device)
        photoResoSetup(d, 0, True)
        rearFrontSwitch(d, 'rear')
        print('case23 ', case23 + ' 结束测试')

        case24 = 'Front shooting(4:3, beauty)'
        caseNum = "case24"
        print('case24 ', case24 + '开始测试')
        rearFrontSwitch(d, 'front')
        if d(resourceId="com.oneplus.camera:id/face_beauty_enter_button").exists:
            d(resourceId="com.oneplus.camera:id/face_beauty_enter_button").click()
            d.click(0.746, 0.652)
        time.sleep(1)
        photoShoot(d, caseNum, case24, device)
        photoResoSetup(d, 0, True)
        rearFrontSwitch(d, 'rear')
        print('case24 ', case24 + ' 结束测试')

        case25 = 'Front shooting(4:3, flash)'
        caseNum = "case25"
        print('case25 ', case25 + '开始测试')
        rearFrontSwitch(d, 'front')
        switchFlash(d,'front','on')
        photoShoot(d, caseNum, case25, device)
        switchFlash(d, 'front','off')
        rearFrontSwitch(d, 'rear')
        print('case25 ', case25 + ' 结束测试')

        case26 = 'Rear Photo 1x zoom and 2x cycle switch'
        caseNum = "case26"
        print('case26 ', case26 + '开始测试')
        photoShoot(d, caseNum, case26, device,switchZoom=True)
        print('case26 ', case26 + ' 结束测试')

        case27 = 'Rear shooting(filter)'
        caseNum = "case27"
        print('case27 ', case27 + '开始测试')
        filter(d)
        photoShoot(d, caseNum, case27, device)
        filter(d,False)
        print('case27 ', case27 + ' 结束测试')

        case28 = 'Rear shooting(filter,2x zoom)'
        caseNum = "case28"
        print('case28 ', case28 + '开始测试')
        filter(d)
        swithZoom(d,'2x')
        photoShoot(d, caseNum, case28, device)
        filter(d, False)
        swithZoom(d, '1x')
        print('case28 ', case28 + ' 结束测试')

        case29 = 'Filter and video switch'
        caseNum = "case29"
        print('case29 ', case29 + '开始测试')
        filter(d,True)
        changeCameraMode(d, caseNum, case29, device,menuMode='photo',toMenumode='video')
        setMenuMode(d,'photo')
        filter(d, False)
        print('case29 ', case29 + ' 结束测试')

        case30 = 'Rear and front photo mode cycle switching'
        caseNum = "case30"
        print('case30 ',case30 + ' 开始测试')
        #rearFrontSwitch(d, 'front')
        changeCameraMode(d, caseNum, case30, device,switchFace=True)
        rearFrontSwitch(d, 'rear')
        print('case30 ', case30 + ' 结束测试')

        case31 = 'Rear and front video mode cycle switching'
        caseNum = "case31"
        print('case31 ', case31 + ' 开始测试')
        setMenuMode(d, 'video')
        changeCameraMode(d, caseNum, case31, device, switchFace=True)
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'photo')
        print('case31 ', case31 + ' 结束测试')

        case32 = 'Rear and front time-lapse mode cycle switching'
        caseNum = "case32"
        print('case32 ', case32 + ' 开始测试')
        setMenuMode(d, 'more')
        if d.xpath('//*[@content-desc="TIME-LAPSE"]').exists:
            d.xpath('//*[@content-desc="TIME-LAPSE"]').click()
        changeCameraMode(d, caseNum, case32, device)
        rearFrontSwitch(d, 'rear')
        if d(resourceId="com.oneplus.camera:id/mode_close").exists:
            d(resourceId="com.oneplus.camera:id/mode_close").click()
        setMenuMode(d, 'photo')
        print('case32 ', case32 + ' 结束测试')

        case33 = 'Rear and front pano mode cycle switching'
        caseNum = "case33"
        print('case33 ', case33 + ' 开始测试')
        setMenuMode(d, 'more')
        if d.xpath('//*[@content-desc="PANO"]').exists:
            d.xpath('//*[@content-desc="PANO"]').click()
        changeCameraMode(d, caseNum, case33, device)
        rearFrontSwitch(d, 'rear')
        if d(resourceId="com.oneplus.camera:id/mode_close").exists:
            d(resourceId="com.oneplus.camera:id/mode_close").click()
        setMenuMode(d, 'photo')
        print('case33 ', case33 + ' 结束测试')

        case34 = 'Rear and front portrait mode cycle switching'
        caseNum = "case31"
        print('case34 ', case34 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'portrait')
        changeCameraMode(d, caseNum, case34, device)
        setMenuMode(d, 'photo')
        print('case34 ', case34 + ' 结束测试')

        case35 = 'Rear photo and video mode cycle switching'
        caseNum = "case35"
        print('case35 ', case35 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        changeCameraMode(d, caseNum, case35, device,menuMode='photo',toMenumode='video')
        setMenuMode(d,'photo')
        print('case35 ', case35 + ' 结束测试')

        case36 = 'Front photo and video mode cycle switching'
        caseNum = "case36"
        print('case36 ', case36 + ' 开始测试')
        rearFrontSwitch(d, 'front')
        changeCameraMode(d, caseNum, case36, device, menuMode='photo', toMenumode='video')
        setMenuMode(d, 'photo')
        rearFrontSwitch(d, 'rear')
        print('case36 ', case36 + ' 结束测试')

        case37 = 'front photo and portrait mode cycle switching'
        caseNum = "case37"
        print('case37 ', case37 + ' 开始测试')
        rearFrontSwitch(d, 'front')
        changeCameraMode(d, caseNum, case37, device, menuMode='photo', toMenumode='portrait')
        setMenuMode(d, 'photo')
        rearFrontSwitch(d, 'rear')
        print('case37 ', case37 + ' 结束测试')

        case38 = 'Rear photo and portrait mode cycle switching'
        caseNum = "case38"
        print('case38 ', case38 + ' 开始测试')
        changeCameraMode(d, caseNum, case38, device, menuMode='photo', toMenumode='portrait')
        setMenuMode(d, 'photo')
        print('case38 ', case38 + ' 结束测试')

        case39 = 'Rear portrait and video mode cycle switching'
        caseNum = "case39"
        print('case39 ', case39 + ' 开始测试')
        changeCameraMode(d, caseNum, case39, device, menuMode='portrait', toMenumode='video')
        setMenuMode(d, 'photo')
        print('case39 ', case39 + ' 结束测试')

        #MacroOn MacroOFF TIME-LAPSE PRO
        case40 = 'Rear photo and Macro mode cycle switching'
        caseNum = "case40"
        print('case40 ', case40 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        changeCameraMoreMode(d, caseNum, case40, device, menuMode='photo', toMenumode='more',toMoreMode='MacroOn')
        setMoreMenuMode(d,'MacroOFF')
        setMenuMode(d, 'photo')
        print('case40 ', case40 + ' 结束测试')

        case41 = 'Rear photo and TIME-LAPSE mode cycle switching'
        caseNum = "case41"
        print('case41 ', case41 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        changeCameraMoreMode(d, caseNum, case41, device,flishTime=5, menuMode='photo', toMenumode='more', toMoreMode='TIME-LAPSEOn')
        setMoreMenuMode(d, 'TIME-LAPSEOFF')
        setMenuMode(d, 'photo')
        print('case41 ', case41 + ' 结束测试')

        case42 = 'Rear photo and Panorama mode cycle switching'
        caseNum = "case42"
        print('case42 ', case42 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        changeCameraMoreMode(d, caseNum, case42, device, flishTime=1, menuMode='photo', toMenumode='more',toMoreMode='PROOn')
        setMoreMenuMode(d, 'PROOFF')
        setMenuMode(d, 'photo')
        print('case42 ', case42 + ' 结束测试')

        case43 = 'Rear 1080P video record(10s,1x)'
        caseNum = "case43"
        print('case43 ', case43 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d,'video')
        switchVideoResolution(d,'1080')
        changeCameraMode(d, caseNum, case43, device,10)
        setMenuMode(d, 'photo')
        print('case43 ', case43 + ' 结束测试')

        case43 = 'Rear 1080P video record(10s,2x)'
        caseNum = "case43"
        print('case43 ', case43 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'video')
        switchVideoResolution(d, '1080')
        swithZoom(d,'2x')
        changeCameraMode(d, caseNum, case43, device, 10)
        setMenuMode(d, 'photo')
        print('case43 ', case43 + ' 结束测试')

        case44 = 'Rear 1080P video mode record(10s,flash)'
        caseNum = "case44"
        print('case44 ', case44 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'video')
        switchVideoResolution(d, '1080')
        switchFlash(d,'rear','Fill Light')
        changeCameraMode(d, caseNum, case44, device, 10)
        switchFlash(d, 'rear', 'OFF')
        setMenuMode(d, 'photo')
        print('case43 ', case44 + ' 结束测试')

        case45 = 'Rear 720P video record(10s,1x)'
        caseNum = "case45"
        print('case45 ', case45 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d,'video')
        switchVideoResolution(d,'720')
        changeCameraMode(d, caseNum, case45, device,10)
        setMenuMode(d, 'photo')
        print('case45 ', case45 + ' 结束测试')

        case46 = 'Rear 720P video mode record(10s,flash)'
        caseNum = "case46"
        print('case46 ', case46 + ' 开始测试')
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'video')
        switchVideoResolution(d, '720')
        switchFlash(d,'rear','Fill Light')
        changeCameraMode(d, caseNum, case46, device, 10)
        switchFlash(d, 'rear', 'OFF')
        setMenuMode(d, 'photo')
        print('case46 ', case46 + ' 结束测试')

        case47 = 'Front 1080P video record(10s)'
        caseNum = "case47"
        print('case47 ', case47 + ' 开始测试')
        setMenuMode(d, 'video')
        rearFrontSwitch(d, 'front')
        switchVideoResolution(d,'1080')
        changeCameraMode(d, caseNum, case47, device,10)
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'photo')
        print('case47 ', case47 + ' 结束测试')

        case48 = 'Front 720 video record(10s)'
        caseNum = "case48"
        print('case48 ', case48 + ' 开始测试')
        setMenuMode(d, 'video')
        rearFrontSwitch(d, 'front')
        switchVideoResolution(d, '720')
        changeCameraMode(d, caseNum, case48, device, 10)
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'photo')
        print('case48 ', case48 + ' 结束测试')

        case49 = 'Portrait mode shooting'
        caseNum = "case49"
        setMenuMode(d,'portrait')#portrait
        print('case49 ', case49 + '开始测试')
        photoShoot(d,caseNum,case49,device)
        setMenuMode(d, 'photo')
        print('case49 ', case49 + ' 结束测试')

        case50 = 'Portrait mode shooting(filter)'
        caseNum = "case50"
        setMenuMode(d, 'portrait')  # portrait
        filter(d,True)
        print('case50 ', case50 + '开始测试')
        photoShoot(d, caseNum, case50, device)
        filter(d,False)
        setMenuMode(d, 'photo')
        print('case50 ', case50 + ' 结束测试')

        case51 = 'Front portrait mode shooting'
        caseNum = "case51"
        print('case51 ', case51 + ' 开始测试')
        setMenuMode(d, 'portrait')  # portrait
        rearFrontSwitch(d, 'front')
        photoShoot(d, caseNum, case51, device)
        rearFrontSwitch(d, 'rear')
        setMenuMode(d, 'photo')
        print('case51 ', case51 + ' 结束测试')

        case52 = 'Front portrait mode shooting(filter)'
        caseNum = "case52"
        print('case52 ', case52 + '开始测试')
        setMenuMode(d, 'portrait')  # portrait
        rearFrontSwitch(d, 'front')
        filter(d, True)
        photoShoot(d, caseNum, case52, device)
        rearFrontSwitch(d, 'rear')
        filter(d,False)
        setMenuMode(d, 'photo')
        print('case52 ', case52 + ' 结束测试')


        print('\nFail项及截图保存地址>>>>>',r'D:\autoCamera','\n')
        print('测试完成\n')
        break

    semaphone.release()

if __name__ == '__main__':

    devicesList = getDevices()
    #wlanAddrList = getWlanAddr(devicesList)
    num = len(devicesList)
    semaphone = threading.BoundedSemaphore(num)

    if devicesList == []:
        print('未识别到Adb devices，请打开USB调试')

    else:
        select = input('请输入>>>>>\n1.安装自动化工具 \n2.开始测试\n>>>>>')
        if select == "1":
            #安装ATX server
            print(len(devicesList))

            for one in range(0, len(devicesList)):
                t = threading.Thread(target=installAtxServer, args=(devicesList[one],))
                t.start()

        if select == "2":
            for one in range(0,len(devicesList)):
                t = threading.Thread(target=start_test, args=(devicesList[one],))
                t.start()
