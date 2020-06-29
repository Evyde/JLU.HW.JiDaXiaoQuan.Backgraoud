//index.js
//获取应用实例
mixins: [require('../../mixin/themeChanged')]
const app = getApp()
const api = require('../../utils/api.js')

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })

    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        wx.request({
          url: api.setUserInfo,
          data: {
            rawData: e.detail.rawData,
            signature: e.detail.signature,
            openid: res.data
          },
          success: (res) => {
            console.log(res)
          }
        })
      }
    })
  },
  wlogin: function(e) {
    wx.checkSession({
      success: ()=>{

      },
      complete: () => {
        wx.login({
          complete: (res) => {
            console.log(res)
            wx.request({
              url: api.login,
              method: 'GET',
              data: {resCode: res.code},
              success: (res) => {
                console.log(res)
                if(res.data.errcode != 0)
                  this.wlogin(e)
                else wx.setStorage({
                  data: res.data.openid,
                  key: 'openid',
                })
              }
            })
          },
        })
        wx.getStorage({
          key: 'openid',
          success: (res) => {
            console.log(app.globalData.detail)
            wx.request({
              url: api.setUserInfo,
              data: {
                rawData: app.globalData.detail.rawData,
                signature: app.globalData.detail.signature,
                openid: res.data
              },
              success: (res) => {
                console.log(res)
              }
            })
          }
        })
      }
    })
  }



})