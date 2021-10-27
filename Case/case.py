from BusinessModule import RegisterOrLogin,PublicFunction
import sys, time, unittest, os
from Expand.HTMLTestRunner_PY3 import HTMLTestRunner



class YiTaiChangTestSmoke(unittest.TestCase):
    def setUp(self):
        pass

    def testRegisterAndOpenAnAccount(self):
        self.CaseName = sys._getframe().f_code.co_name
        PublicFunction.DataAPP(self)
        PublicFunction.OpenApp(self)
        RegisterOrLogin.PAPLogin(self)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    NowTime = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    test = unittest.TestSuite()
    strCaseName = PublicFunction.Judge(PublicFunction.GetPerEnvData()[1])
    for i in strCaseName:
        test.addTest(YiTaiChangTestSmoke(i))
    filename = os.path.join(os.getcwd(), "Report/result_" + NowTime + ".html")
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(fp, verbosity=2, title='APP安卓端自动化测试报告',
                            description="义泰昌消费端APP自动化测试报告：" + PublicFunction.GetPerEnvData()[0])
    runner.run(test)
    fp.close()
