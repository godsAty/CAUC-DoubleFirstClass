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

  _initialized: false,

  onLoad(options) {
    const app = getApp();
    const selectedId = options.id || app.globalData.selectedCategoryId;
    if (selectedId) {
      this.setData({ activeTab: parseInt(selectedId) });
      app.globalData.selectedCategoryId = null;
    }
    this._initialized = true;
    this.loadIndicators();
  },

  onShow() {
    // 首次进入：onShow 可能先于 onLoad 触发，跳过
    if (!this._initialized) return;

    // 从首页 switchTab 过来时，onLoad 不会重复触发，需在 onShow 中读取
    const app = getApp();
    const selectedId = app.globalData.selectedCategoryId;
    if (selectedId) {
      app.globalData.selectedCategoryId = null;
      this.setData({ activeTab: parseInt(selectedId), loading: true, error: false });
    }
    this.loadIndicators();
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

      // 加权平均（与首页 dashboard 一致）
      let weightedRateSum = 0;
      let weightedNatSum = 0;
      let weightSum = 0;
      data.forEach(item => {
        const w = item.weight || 0;
        weightedRateSum += item.completionRate * w;
        weightedNatSum += item.nationalRate * w;
        weightSum += w;
      });
      const avgRate = weightSum > 0 ? parseFloat((weightedRateSum / weightSum).toFixed(1)) : 0;
      const avgNat = weightSum > 0 ? parseFloat((weightedNatSum / weightSum).toFixed(1)) : 0;

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
