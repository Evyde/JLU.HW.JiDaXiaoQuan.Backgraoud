//app.js
require('./libs/Mixins.js');

const themeListeners = [];
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              this.globalData.detail = res
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    theme: 'light', // dark
},
themeChanged(theme) {
    this.globalData.theme = theme;
    themeListeners.forEach((listener) => {
        listener(theme);
    });
},
watchThemeChange(listener) {
    if (themeListeners.indexOf(listener) < 0) {
        themeListeners.push(listener);
    }
},
unWatchThemeChange(listener) {
    const index = themeListeners.indexOf(listener);
    if (index > -1) {
        themeListeners.splice(index, 1);
    }
},
})