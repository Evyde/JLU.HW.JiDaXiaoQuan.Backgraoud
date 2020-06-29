// pages/location/location.js
mixins: [require('../../mixin/themeChanged')]
const api = require('../../utils/api.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {
    latitude: wx.getStorageSync('latitude'),
    longitude: wx.getStorageSync('longitude'),
    locationid: wx.getStorageSync('locationid'),
    openid: wx.getStorageSync('openid'),
    loRange: "",
    laRange: "",
    name: ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData(data, {
    latitude: wx.getStorageSync('latitude'),
    longitude: wx.getStorageSync('longitude'),
    locationid: wx.getStorageSync('locationid'),
    openid: wx.getStorageSync('openid'),
    loRange: "",
    laRange: "",
    name: ""
  },)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },
  createLocation: function (e) {
    var that = this
    console.log(e)
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        console.log(that)
        wx.request({
          url: api.createLocation,
          data: {
            openid: res.data,
            latitude: that.data.latitude,
            longitude: that.data.longitude,
            name: e.detail.value.name,
            laRange: e.detail.value.laRange,
            loRange: e.detail.value.loRange
          },
          success: (es) => {
              if(es.data.msg == true)
                wx.showModal({
                  showCancel: false,
                  title: "提交结果",
                  content: "提交成功了哦~感谢您为社区做的贡献"
                })
              else wx.showModal({
                showCancel: false,
                title: "提交结果",
                content: "提交失败了哦~重新试一下吧"
              })
          }
        })
      }
    })
  },
  inputsla: function (e) {
    console.log(e)
    var v1 = e.detail.value;
    var v2 = parseFloat(v1).toFixed(6)
    if(v2 <= 0.0001 || v2 >= 0.03) {
      wx.showToast({
      title: '输入必须介于0.0001至0.03之间',
      icon: "none"
    })
    this.setData({
        laRange: ""
      })
    }
  },
  inputslo: function (e) {
    console.log(e)
    var v1 = e.detail.value;
    var v2 = parseFloat(v1).toFixed(6)
    if(v2 <= 0.0001 || v2 >= 0.03) {
      wx.showToast({
      title: '输入必须介于0.0001至0.03之间',
      icon: "none"
    })
      this.setData({
        loRange: ""
      })
    }
  },
  inputs: function(e) {
    if(e.detail.value == "") {
      wx.showToast({
        title: '输入不能为空',
        icon: "none"
      })
        this.setData({
          name: ""
        })
    }
  }
})