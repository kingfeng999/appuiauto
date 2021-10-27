from ObjectRepository import ObjHomePage,ObjMinePage,ObjRegisterOrLoginPage
from BusinessModule import PublicFunction
import unittest

def PAPLogin(self):
    ObjHomePage.HomePage(self)
    # PublicFunction.ObjDisplay(self.driver,self.PositioningBut)
    self.assertIsNotNone(self.PositioningBut,msg=str(self.PositioningBut.text) + "不存在")
    self.MineBtn.click()
    ObjMinePage.MinePage(self)
    # PublicFunction.ObjDisplay(self.driver,self.PersonalInfoPageInfo)
    self.assertIsNotNone(self.PersonalInfoPageInfo, msg=str(self.PersonalInfoPageInfo.text) + "不存在")
    self.PersonalInfoPageInfo.click()
    ObjRegisterOrLoginPage.RegisterOrLogin(self)
    # PublicFunction.ObjDisplay(self.driver,self.RegisterOrLoginPhoneNumInputBox)
    self.assertIsNotNone(self.RegisterOrLoginPhoneNumInputBox, msg=str(self.RegisterOrLoginPhoneNumInputBox.text) + "不存在")
    self.PhoneNumberAndPassWordLoginButton.click()
    ObjRegisterOrLoginPage.PhoneNumberAndPassWordLogin(self)
    # PublicFunction.ObjDisplay(self.driver,self.PAPPhoneNumberInputBox)
    self.assertIsNotNone(self.PAPPhoneNumberInputBox, msg=str(self.PAPPhoneNumberInputBox.text) + "不存在")
    self.PAPPhoneNumberInputBox.send_keys(self.LoginPhone)
    self.PAPPasswordInputBox.send_keys(self.LoginPwd)
    self.PAPConfirmButton.click()