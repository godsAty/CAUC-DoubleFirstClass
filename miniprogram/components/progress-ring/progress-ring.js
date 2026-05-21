// 环形进度条组件
Component({
  properties: {
    // 百分比 0-100
    percent: { type: Number, value: 0 },
    // 环形直径(rpx)
    size: { type: Number, value: 200 },
    // 环形宽度(rpx)
    strokeWidth: { type: Number, value: 16 },
    // 主色
    color: { type: String, value: '#2d6cdf' },
    // 底色
    bgColor: { type: String, value: '#e8ecf0' },
    // 是否显示文字
    showText: { type: Boolean, value: true },
    // 文字标题
    title: { type: String, value: '' },
    // 副标题
    subtitle: { type: String, value: '' },
  },

  data: {
    ringPercent: 0,
  },

  observers: {
    'percent'(val) {
      this.animatePercent(val);
    }
  },

  lifetimes: {
    attached() {
      // 延迟触发动画
      setTimeout(() => {
        this.animatePercent(this.properties.percent);
      }, 300);
    }
  },

  methods: {
    animatePercent(target) {
      let current = this.data.ringPercent;
      const step = Math.ceil((target - current) / 20);
      const timer = setInterval(() => {
        current += step;
        if ((step > 0 && current >= target) || (step < 0 && current <= target) || step === 0) {
          current = target;
          clearInterval(timer);
        }
        this.setData({ ringPercent: current });
      }, 30);
    }
  }
});
