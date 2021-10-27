from BusinessModule import PublicFunction

#验证码登陆注册页面
def RegisterOrLogin(self):
    #手机号码输入框
    self.RegisterOrLoginPhoneNumInputBox = self.driver.find_element_by_id("cn.yitaichang.consumer:id/phone_number")
    #验证码输入框
    self.InputVerifyCodeInputBox = self.driver.find_element_by_id("cn.yitaichang.consumer:id/input_verify_code")
    #确定按钮
    self.ConfirmButton = self.driver.find_element_by_id("cn.yitaichang.consumer:id/btn_next")
    #账号密码登陆按钮
    self.PhoneNumberAndPassWordLoginButton = self.driver.find_element_by_id("cn.yitaichang.consumer:id/tv_pwd_login")

#账号密码登陆页面
def PhoneNumberAndPassWordLogin(self):
    #手机号码输入框
    self.PAPPhoneNumberInputBox = self.driver.find_element_by_id("cn.yitaichang.consumer:id/phone_number")
    #密码输入框
    self.PAPPasswordInputBox = self.driver.find_element_by_id("cn.yitaichang.consumer:id/phone_pwd")
    #确定按钮
    self.PAPConfirmButton = self.driver.find_element_by_id("cn.yitaichang.consumer:id/btn_next")