// 指标卡片组件
const app = getApp();

Component({
  properties: {
    // 指标数据
    indicator: { type: Object, value: {} },
    // 是否显示完整对比
    showDetail: { type: Boolean, value: false },
    // 卡片索引
    index: { type: Number, value: 0 },
  },

  computed: {},

  methods: {
    onTapCard() {
      if (this.properties.indicator && this.properties.indicator.id) {
        wx.navigateTo({
          url: `/pages/detail/detail?id=${this.properties.indicator.id}`
        });
      }
    },

    getRateClass(rate) {
      if (rate >= 90) return 'tag-green';
      if (rate >= 70) return 'tag-blue';
      if (rate >= 50) return 'tag-orange';
      return 'tag-red';
    },

    getProgressColor(rate) {
      if (rate >= 90) return '#2ecc71';
      if (rate >= 70) return '#3498db';
      if (rate >= 50) return '#f39c12';
      return '#e74c3c';
    }
  }
});
