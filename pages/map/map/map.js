// pages/demo06/map/map.js
const api = require('../../../utils/api.js')
mixins: [require('../../../mixin/themeChanged')]
Page({

  /**
   * 页面的初始数据
   */

   data: {
     latitude: '39.917940',
     longitude: '116.397140'
   },


  

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    let that = this
    wx.request({
      url: api.getAllMarkers,
      success: (res) => {
        this.setData({
          markers: res.data
        })
        console.log(res.data)
      }
    })
    wx.getLocation({
      altitude: true,
      success: (res)=> {
        console.log(res)
        that.setData({
          latitude: res.latitude,
          longitude: res.longitude
        })
        wx.setStorageSync('latitude', res.latitude)
        wx.setStorageSync('longitude', res.longitude)
      }
    })
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },
  onShow: function () {
    wx.request({
      url: api.getAllMarkers,
      success: (res) => {
        this.setData({
          markers: res.data
        })
        console.log(res.data)
      }
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },
  createPassage: function(event) {
    console.log('跳转创建文章页');
    wx.navigateTo({
        url: "/pages/passage/newPassage"
      });
  },

  createLocation: function() {
    console.log('跳转创建地点页');
    wx.navigateTo({
        url: "/pages/location/location"
      });
  },
  //显示对话框
  showModal: function(event) {
    //console.log(event.markerId);
    var i = event.markerId;
    var that = this;
    console.log('详情页')
    wx.setStorageSync('locationid', i)
    wx.request({ 
      url: api.getLocation,
      data: {
        locationid: i,
        openid: wx.getStorageSync('openid')
      },
      success: function(res) {
        console.log(res);
        that.setData({
          nowlocation: res.data
        });
      }
    });
 
    // 显示遮罩层
    var animation = wx.createAnimation({
      duration: 200,
      timingFunction: "linear",
      delay: 0
    })
    this.animation = animation
    animation.translateY(300).step()
    this.setData({
      animationData: animation.export(),
      showModalStatus: true
    })
    setTimeout(function() {
      animation.translateY(0).step()
      this.setData({
        animationData: animation.export()
      })
    }.bind(this), 200)
  },
  //隐藏对话框
  hideModal: function() {
    // 隐藏遮罩层
    var animation = wx.createAnimation({
      duration: 200,
      timingFunction: "linear",
      delay: 0
    })
    this.animation = animation
    animation.translateY(300).step()
    this.setData({
      animationData: animation.export(),
    })
    setTimeout(function() {
      animation.translateY(0).step()
      this.setData({
        animationData: animation.export(),
        showModalStatus: false
      })
    }.bind(this), 200)
  },

  opendetail: function(event) {
    console.log('跳转文章页');
    wx.navigateTo({
        url: "/pages/passage/passage"
      });
  },
  openLocation: function(event) {
    wx.request({
      url: api.getLocation,
      data: {
        locationid: wx.getStorageSync('locationid')
      },
      success: (res) => {
        wx.setStorageSync('latitude', res.data.latitude)
        wx.setStorageSync('longitude', res.data.longitude)
      }
    })
    wx.openLocation({
      latitude: parseFloat(wx.getStorageSync('latitude')),
      longitude: parseFloat(wx.getStorageSync('longitude')),
    })
  },
  checkin: function(event) {
    wx.getLocation({
      altitude: true,
      success: (res) => {
        wx.request({
          url: api.checkin,
          data: {
            locationid: wx.getStorageSync('locationid'),
            openid: wx.getStorageSync('openid'),
            location: {
              latitude: res.latitude,
              longitude: res.longitude
            }
          },
          success: (res) => {
            console.log(res)
            if(res.data.msg==true) wx.showModal({
              showCancel: false,
              title: "打卡成功",
              content: "快去写篇想法分享你的喜悦吧~~",
            })
            else wx.showModal({
              showCancel: false,
              title: "打卡失败",
              content: "不在此位置或者已经打过卡了哦~~",
            })
          }
        })
      }
    })
  }
})