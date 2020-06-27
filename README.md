# JLU-Wechat-Miniprogram-Backgraoud

# 待办事项：
1、 让用户添加地点，并选择合适大小的范围，计算出四个点的坐标，此后有用户打卡时，判断用户是否在该范围内，如果是，完成打卡行为。  
2、 文章数据表创建`passageTitle`字段，如有可能创建`abstract`（摘要）字段。  
3、 创建一个浮于地图上的圆形绿色按钮，＋，点击后调用`createLocation`函数。  
4、 点击地点后，将地图空间缩小到50%，然后弹出一个文章列表，该文章列表可滑动，右下角有两个按钮，分别是导航（调用`wx.openLocation`函数）和新建文章（调用`createPassage`函数），而文章列表
显示的左面为用户头像+用户名，右面为文章标题+摘要，如有可能，加一个显示完整文章的页面（有点赞按钮），如没可能，把摘要页的摘要直接改成完整文章。

# 跨设备书签同步
https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html
https://developers.weixin.qq.com/miniprogram/dev/api/network/request/wx.request.html
https://developers.weixin.qq.com/miniprogram/dev/api/location/wx.getLocation.html
https://blog.csdn.net/qq_43467898/article/details/83187698
https://blog.csdn.net/qq_42396168/article/details/87971576
https://www.cnblogs.com/yangmv/p/5327477.html
