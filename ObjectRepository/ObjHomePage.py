def HomePage(self):
    #左上方地址按钮
    self.PositioningBut = self.driver.find_element_by_id("cn.yitaichang.consumer:id/position")
    #左上方地址信息
    self.PositioningInfo = self.driver.find_element_by_id("cn.yitaichang.consumer:id/tv_position")
    #底部“首页”页面元素
    self.HomeBtn = self.driver.find_element_by_xpath("//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout")
    #底部“购物车”页面元素
    self.ShoppingCartBtn = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]")
    #底部“订单”页面元素
    self.OrderBtn = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]")
    #底部“我的”页面元素
    self.MineBtn = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[4]")
