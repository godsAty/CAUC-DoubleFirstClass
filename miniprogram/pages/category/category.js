// 分类指标详情页（数据来自后端 Flask API → SQL Server）
const api = require('../../utils/api');

Page({
  data: {
    tabs: [
      { id: 1, name: '人才培养' },
      { id: 2, name: '师资队伍' },
      { id: 3, name: '科研成果' },
      { id: 4, name: '社会服务' },
      { id: 5, name: '国际化' },
    ],
    activeTab: 1,
    indicators: [],
    categoryRate: 0,
    nationalRate: 0,
    loading: true,
    error: false,
  },

  onLoad(options) {
    const app = getApp();
    const selectedId = options.id || app.globalData.selectedCategoryId;
    if (selectedId) {
      this.setData({ activeTab: parseInt(selectedId) });
      app.globalData.selectedCategoryId = null;
    }
    this.loadIndicators();
  },

  onShow() {
    if (!this.data.loading) this.loadIndicators();
  },

  onPullDownRefresh() {
    this.loadIndicators().finally(() => wx.stopPullDownRefresh());
  },

  switchTab(e) {
    const id = e.currentTarget.dataset.id;
    this.setData({ activeTab: id, loading: true, error: false });
    this.loadIndicators();
  },

  async loadIndicators() {
    this.setData({ loading: true, error: false });
    try {
      const data = await api.getCategory(this.data.activeTab);
      const totalRate = data.reduce((sum, item) => sum + item.completionRate, 0);
      const totalNat = data.reduce((sum, item) => sum + item.nationalRate, 0);
      const avgRate = data.length > 0 ? parseFloat((totalRate / data.length).toFixed(2)) : 0;
      const avgNat = data.length > 0 ? parseFloat((totalNat / data.length).toFixed(2)) : 0;

      this.setData({
        indicators: data,
        categoryRate: avgRate,
        nationalRate: avgNat,
        loading: false,
        error: false,
      });
    } catch (err) {
      console.error('API请求失败:', err);
      this.setData({ loading: false, error: true });
    }
  },
});
