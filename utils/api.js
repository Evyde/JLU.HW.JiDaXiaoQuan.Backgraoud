var appId = 'wx908d78c4818ee8d3';  //小程序的iD
var baseUrl = 'https://mp.evyde.xyz:2419';   //统一的域名，注意要用https
var api = {
 baseUrl: baseUrl,
  // appid
  appId: appId,
  // 注册接口
  login: baseUrl + '/jlu/wxLogin',
  // 用户基本信息
  setUserInfo: baseUrl + '/jlu/wxSetUserInfo', //如此类推
  // 验证数据安全
  ckSignature: baseUrl + '/jlu/wxCheckSignature',
  // 获取Makers
  getAllMarkers: baseUrl + '/jlu/getAllMarkers',
  // 创建新地点
  createLocation: baseUrl + '/jlu/createLocation',
  // 获取文章
  getPassages: baseUrl + '/jlu/getPassages',
  // 获得位置详情
  getLocation: baseUrl + '/jlu/getLocationByID',
  // 获取用户信息
  getUserInfo: baseUrl + '/jlu/wxGetUserInfo',
  // 打卡
  checkin: baseUrl + '/jlu/checkin',
  // 获取校内通知
  getAnnounce: baseUrl + '/jlu/getAllAnnounce',
  // 获取用户打卡过的地点
  getCheckedinLocations: baseUrl + '/jlu/getCheckedinLocations',
  // 创建新文章
  createPassage: baseUrl + '/jlu/createPassage',
  // 为文章点赞
  voteUp: baseUrl + '/jlu/voteUp',


  }

module.exports = api    //模块化