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
      const ringColor = this.getRingColor(data.overallRate);
      this.setData({
        overallRate: data.overallRate,
        updateTime: data.updateTime,
        categories: data.categories,
        ringColor: ringColor,
        loading: false,
        error: false,
      });
      this.drawRing(data.overallRate, ringColor);
    } catch (err) {
      console.error('API请求失败，请确认后端已启动:', err);
      this.setData({ loading: false, error: true });
    }
  },

  drawRing(rate, color) {
    const ctx = wx.createCanvasContext('overallRing');
    const cx = 85, cy = 85, r = 68, lineW = 14;

    // 底色圆环
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.setStrokeStyle('#e8ecf0');
    ctx.setLineWidth(lineW);
    ctx.setLineCap('round');
    ctx.stroke();

    // 进度弧
    const endAngle = -Math.PI / 2 + (Math.PI * 2 * rate) / 100;
    ctx.beginPath();
    ctx.arc(cx, cy, r, -Math.PI / 2, endAngle);
    ctx.setStrokeStyle(color);
    ctx.setLineWidth(lineW);
    ctx.setLineCap('round');
    ctx.stroke();

    ctx.draw();
  },

  getRingColor(rate) {
    if (rate >= 90) return '#2ecc71';
    if (rate >= 70) return '#3498db';
    if (rate >= 50) return '#f39c12';
    return '#e74c3c';
  },

  goToCategory(e) {
    const id = parseInt(e.currentTarget.dataset.id);
    app.globalData.selectedCategoryId = id;
    wx.switchTab({ url: '/pages/category/category' });
  },

  goToComparison() {
    wx.switchTab({ url: '/pages/comparison/comparison' });
  },
});
