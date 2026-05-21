// 首页 - 综合概览（数据来自后端 Flask API → SQL Server）
const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    overallRate: 0,
    updateTime: '---',
    categories: [],
    loading: true,
    error: false,
    ringColor: '#2d6cdf',
  },

  onLoad() {
    this.fetchData();
  },

  onShow() {
    // Tab切换回来时刷新最新数据
    if (!this.data.loading) this.fetchData();
  },

  onPullDownRefresh() {
    this.fetchData().finally(() => wx.stopPullDownRefresh());
  },

  async fetchData() {
    this.setData({ loading: true, error: false });
    try {
      const data = await api.getOverview();
      this.setData({
        overallRate: data.overallRate,
        updateTime: data.updateTime,
        categories: data.categories,
        ringColor: this.getRingColor(data.overallRate),
        loading: false,
        error: false,
      });
    } catch (err) {
      console.error('API请求失败，请确认后端已启动:', err);
      this.setData({ loading: false, error: true });
    }
  },

  getRingColor(rate) {
    if (rate >= 70) return '#2ecc71';
    if (rate >= 50) return '#3498db';
    if (rate >= 30) return '#f39c12';
    return '#e74c3c';
  },

  goToCategory(e) {
    const id = e.currentTarget.dataset.id;
    app.globalData.selectedCategoryId = id;
    wx.switchTab({ url: '/pages/category/category' });
  },

  goToComparison() {
    wx.switchTab({ url: '/pages/comparison/comparison' });
  },
});
