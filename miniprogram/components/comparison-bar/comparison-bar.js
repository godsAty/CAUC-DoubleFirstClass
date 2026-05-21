// 对比柱状条组件
Component({
  properties: {
    // 指标名称
    label: { type: String, value: '' },
    // 本校值
    caucValue: { type: Number, value: 0 },
    // 全国均值
    nationalValue: { type: Number, value: 0 },
    // 目标值
    targetValue: { type: Number, value: 100 },
    // 单位
    unit: { type: String, value: '%' },
    // 最大值(用于比例计算)
    maxValue: { type: Number, value: 100 },
  },

  data: {
    caucWidth: 0,
    nationalWidth: 0,
  },

  observers: {
    'caucValue, nationalValue, targetValue, maxValue'(cauc, nat, tar, max) {
      const m = max || 120;
      this.setData({
        caucWidth: Math.min((cauc / m) * 100, 100),
        nationalWidth: Math.min((nat / m) * 100, 100),
      });
    }
  },

  methods: {}
});
