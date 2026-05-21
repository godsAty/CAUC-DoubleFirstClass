// API 请求封装
const app = getApp();

const request = (url, method = 'GET', data = null) => {
  const base = app.globalData.apiBase;

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${base}${url}`,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success(res) {
        if (res.statusCode === 200 && res.data.code === 200) {
          resolve(res.data.data);
        } else {
          reject(res.data.msg || '请求失败');
        }
      },
      fail(err) {
        console.error('API请求失败:', err);
        reject(err.errMsg || '网络错误');
      }
    });
  });
};

// 综合概览
const getOverview = () => request('/api/overview');

// 分类详情
const getCategory = (categoryId) => request(`/api/category/${categoryId}`);

// 单项指标详情
const getIndicator = (indicatorId) => request(`/api/indicator/${indicatorId}`);

// 三方对比
const getComparison = () => request('/api/comparison');

// 历史趋势
const getTrend = (indicatorId) => request(`/api/trend/${indicatorId}`);

module.exports = {
  getOverview,
  getCategory,
  getIndicator,
  getComparison,
  getTrend,
};
