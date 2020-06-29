// pages/passage/passage.js
mixins: [require('../../mixin/themeChanged')]
const api = require('../../utils/api.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.request({
      url: api.getPassages,
      data: {
        locationid: wx.getStorageSync('locationid'),
        openid: wx.getStorageSync('openid')
      },
      success: (res) => {
        that.setData({
            dataarray: res.data
        })
        console.log(res.data)
      }
    })
  },
  createPassage: function(e) {
    console.log('跳转创建文章页');
    wx.navigateTo({
        url: "/pages/passage/newPassage"
      });
  },
  goDetail: function(e) {
    console.log(e)
    wx.request({
      url: api.voteUp,
      data: {
        passageid: e.currentTarget.dataset.id,
        openid: wx.getStorageSync('openid')
      },
      success: (res) => {
        console.log(res)
        this.setData({

        })
      }
    })
  }
})