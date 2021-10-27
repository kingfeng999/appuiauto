# -*- coding:utf-8 -*-
import json, os, time, xlrd
from appium import webdriver
import os, pymysql
import requests, datetime


# 打开app
def OpenApp(self):
    self.desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.1.0',
        'deviceName': GetPerEnvData()[0],
        'app': "D:\code\python\yitaichang\AppData\package\义泰昌_0.0.2_yyb_2018122710_debug.apk",
        'appActivity': 'cn.yitaichang.consumer.mvp.ui.activity.SplashActivity',
        'appPackage': 'cn.yitaichang.consumer',
        'noReset': 'true',
        'unicodeKeyboard': 'true',
        'resetKeyboard': 'true',
        'udid': GetPerEnvData()[3],
        'noSign': 'true',
        'recreateChromeDriverSessions': 'true',
    }
    self.driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub',
                                   desired_capabilities=self.desired_caps)
    self.driver.implicitly_wait(10)

    # for i in range(5):
    #     try:
    #         self.driver.find_element_by_id("android:id/button1").click()
    #     except:
    #         pass
    print("Run start!")

    print("Run Case:" + self.CaseName)

# 获取手机分别率，对 swipe 滑动做兼容性开发
def GetWindowSize(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


# 向上滑动
def SwipeUp(driver, time):
    Coordinate = GetWindowSize(driver)
    x1 = int(Coordinate[0] * 0.5)
    y1 = int(Coordinate[1] * 0.9)
    y2 = int(Coordinate[1] * 0.1)
    driver.swipe(x1, y1, x1, y2, time)


# 向下滑动
def SwipeDown(driver, time):
    Coordinate = GetWindowSize(driver)
    x1 = int(Coordinate[0] * 0.5)
    y1 = int(Coordinate[1] * 0.1)
    y2 = int(Coordinate[1] * 0.9)
    driver.swipe(x1, y1, x1, y2, time)


# 向左滑动
def SwipeLeft(driver, time):
    Coordinate = GetWindowSize(driver)
    x1 = int(Coordinate[0] * 0.9)
    y1 = int(Coordinate[1] * 0.5)
    x2 = int(Coordinate[0] * 0.1)
    driver.swipe(x1, y1, x2, y1, time)


# 向右滑动
def SwipeRight(driver, time):
    Coordinate = GetWindowSize(driver)
    x1 = int(Coordinate[0] * 0.1)
    y1 = int(Coordinate[1] * 0.5)
    x2 = int(Coordinate[0] * 0.9)
    driver.swipe(x1, y1, x2, y1, time)


# 选择开户行、选择开户行所在地类似的小范围向上滑动屏幕 xc,yc1,yc2分别为当前坐标与分别率的比率
def SmallRangeSwipeUp(driver, xc, yc1, yc2, time):
    Coordinate = GetWindowSize(driver)
    x1 = int(Coordinate[0] * xc)
    y1 = int(Coordinate[1] * yc1)
    y2 = int(Coordinate[1] * yc2)
    driver.swipe(x1, y1, x1, y2, time)


# 点击屏幕
def ClickScreen(driver, x, y, time):
    xs = driver.get_window_size()['width']
    ys = driver.get_window_size()['height']
    xc = (x * xs) / 720
    yc = (y * ys) / 1280
    driver.swipe(xc, yc, xc, yc, time)


# 错误页面截图
def ErrorImage(driver):
    NowDate = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    NowTime = time.strftime("%H_%M_%S", time.localtime(time.time()))
    # UrlFrode = "D:\\AppAutomation\\AppData\\Results\\Android\\ErrorImage\\"
    UrlFrode = os.path.join(os.getcwd(), "../AppData/Results/Android/ErrorImage/")
    FoldURL = UrlFrode + NowDate
    FileURL = UrlFrode + NowDate + "\\" + NowTime
    if not os.path.isdir(FoldURL) and not os.path.exists(FoldURL):
        os.mkdir(FoldURL)
    else:
        print("The fold is exist on list")
    ImageURL = FileURL + "Error_png.png"
    driver.get_screenshot_as_file(ImageURL)


# 比较两个字符串相等
def StrEqual(driver, Exp, Act):
    if Exp == Act:
        print("Passed: The expect value: " + str(Exp) + " and the actual value: " + str(Act) + " are equal")
        # print "pass"
    else:
        print("Failed: The expect value: " + str(Exp) + " and the actual value: " + str(Act) + " does not equal")
        ErrorImage(driver)
        # exit()
        # print "fail"
    return Exp, Act


# 验证sub字符包含在par字符串中
def StrInClude(driver, sub, par):
    if sub in par:
        print("Passed: The value " + str(sub) + " included in the " + str(par))
        # print "pass"
    else:
        # print "fail"
        print("Failed: The value " + str(sub) + " does not included in the " + str(par))
        ErrorImage(driver)
        # exit()
    return sub, par


# 判断对象是否存在当前页面
def ObjDisplay(driver, Objects):
    if Objects.is_displayed() == True:
        print("Passed: The page display object")
    else:
        print("Failed: The page does not displayed object")
        ErrorImage(driver)
        # exit()
    return Objects


# 判断数据表格中可执行的Case
def Judge(sheetName):
    data = xlrd.open_workbook(
        os.path.join(os.getcwd(), "../AppData/Information/yitaichang.xlsx"))
    table = data.sheet_by_name(sheetName)
    Valuesrow = table.nrows
    strCaseList = []
    # 获取 sheet 的每一行
    for i in range(1, Valuesrow):
        # 如果这一行的第一列为 Y
        if table.cell(i, 0).value == u"Y":
            # 获取这一行的 CaseName
            strCaseName = table.cell(i, 1).value
            # 添加到 strCaseList
            strCaseList.append(strCaseName)
    return strCaseList


# 预发布环境的数据
def GetPerEnvData():
    data = xlrd.open_workbook(
        os.path.join(os.path.join(os.getcwd(), "../AppData/Information"), "yitaichang.xlsx"))
    table = data.sheet_by_name('PerEnvData')
    valuesrow = table.nrows
    arrValue = []
    for i in range(0, valuesrow):
        arrValue.append(table.row_values(i))
    for i in range(1, len(arrValue)):
        if arrValue[i][0] == u"Y":
            strEnv = arrValue[i][1]
            strSelectTable = arrValue[i][2]
            udid = arrValue[i][3]
    caseTable = data.sheet_by_name(strSelectTable)
    return strEnv, strSelectTable, caseTable, udid


def DataAPP(self):
    table = GetPerEnvData()[2]
    # data = xlrd.open_workbook(
    #     os.path.join(os.path.join(os.getcwd(), "../AppData/Information"), "ZhongYeXiongRong.xlsx"))
    # table = data.sheet_by_name('AllAutoTest')

    valuesrow = table.nrows
    self.arrValue = []
    for i in range(0, valuesrow):
        self.arrValue.append(table.row_values(i))
    for y in range(1, len(self.arrValue)):
        if self.CaseName == self.arrValue[y][1]:
            self.RegisteredPhone = self.arrValue[y][2]
            self.LoginPhone = self.arrValue[y][3]
            self.LoginPwd = self.arrValue[y][4]
            self.PayPwd = self.arrValue[y][5]
            self.CardNum = self.arrValue[y][6]
            self.CardUserName = self.arrValue[y][7]
            self.CardUserNum = self.arrValue[y][8]
            self.BankName = self.arrValue[y][9]
            self.Province = self.arrValue[y][10]
            self.City = self.arrValue[y][11]
            self.TheTotalNumberOfBank = self.arrValue[y][12]
            self.InvitePeoplePhone = self.arrValue[y][13]

# 切换搜狗输入法
def SwitchingSougouIme(driver):
    driver.activate_ime_engine("com.baidu.input_huawei/.ImeService")


# 切换appium输入法
def SwitchingAppiumIme(driver):
    driver.activate_ime_engine("io.appium.android.ime/.UnicodeIME")


# 查询maislq数据库
def OperatingMysql(host, dbname, sql):
    db = pymysql.connect(host, "mysqluser", "mysqluser@zyxr.com", dbname, charset="utf8")
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    # data = cursor.fetchone()
    data = cursor.fetchall()
    db.close()
    return data


# 比较数据库查询值返回的字典与页面查询出的项目是否有交集
def CompareTwoArrays(dicOne, elements):
    for i in range(0, len(dicOne) - 1):
        for j in range(0, len(elements) - 1):
            if dicOne[i]["asset_name"] == elements[j].text:
                print("Product" + " 《 " + elements[j].text + " 》 " + "Can Invest!")
                return elements[j]
    else:
        print("No Debts Can Invest!")


# 给用户添加优惠券
def AddCouPon(host, userMobile):
    data_login = {
        'username': 'admin',
        'password': '4478294166928c73c71ba7dc875f2225560bc753',
    }
    res_login = requests.post('http://' + host + '/AdminWeb/login/login.json?ajax=1', data=data_login)
    # d = res_login.json()
    # print(res_login.json(), res_login.cookies.get_dict()["XSession"])

    coupon_id = OperatingMysql("192.168.9.135", "reward",
                               "select id,name from reward.t_coupon_type where type = 3 and product_limit = '|0|1|5|6|' and product_tag_limit = '|0|1|' and amount_limit = 0 and day_limit = 0 and asset_hold_day = 0 limit 1;")

    user_id = OperatingMysql("192.168.9.135", "user",
                             'select id from user.t_user where mobile = "' + str(userMobile) + '"')

    data_coupon = {
        'id': '',
        'batchNo': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'couponTypeId': coupon_id[0]["id"],
        'source': 'test',
        'description': 'test',
        'startTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'endTime': (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
        'status': 0,
        'userIds': user_id[0]["id"]
    }
    # print(data_coupon)
    headers = {
        'Cookie': 'XSession=' + res_login.cookies.get_dict()["XSession"] + ';'
                                                                           '_ga=GA1.1.1382495494.1531980302;'
                                                                           'NTKF_T2D_CLIENTID=guest424804D1-B03D-D745-1E76-B124487378F6;'
                                                                           '_gid=GA1.1.1994861645.1532309618;'
                                                                           'Hm_lvt_cb3e1b64778f8ade024e7884a8fa0475=1531980303,1531983586,1532309618;'
                                                                           'ZYXRSession=a03b1585cb1422e3d2a7f5fafa2986a80a4c3391;'
                                                                           'nTalk_CACHE_DATA={uid:kf_10267_ISME9754_guest424804D1-B03D-D7,tid:1532403853059929};'
                                                                           'Hm_lpvt_cb3e1b64778f8ade024e7884a8fa0475=1532412095'
    }
    # print(headers)
    res_coupon = requests.post('http://' + host + '/RewardAdminWeb/couponDispatch/addCouponDispatch.json?ajax=1',
                               data=data_coupon, headers=headers)
    if res_coupon.json()["code"] == 0:
        print('用户：' + str(userMobile) + '  ' + '增加一张优惠券，优惠券名称为' + '  ' + '《  ' + coupon_id[0]["name"] + '  》')
    else:
        print("添加优惠券失败！")
