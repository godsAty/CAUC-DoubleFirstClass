// 单项指标详情页（数据来自后端 API）
const api = require('../../utils/api');

Page({
  data: {
    indicator: null,
    trend: [],
    loading: true,
    error: false,
    indicatorId: 0,
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ indicatorId: parseInt(options.id) });
      this.fetchDetail();
    }
  },

  async fetchDetail() {
    this.setData({ loading: true, error: false });
    try {
      const data = await api.getIndicator(this.data.indicatorId);
      this.setData({
        indicator: data,
        trend: data.trend || [],
        loading: false,
      });

      if (data.completionRate !== undefined) {
        setTimeout(() => this.drawCompletionRing(), 400);
      }
      if (data.trend && data.trend.length > 0) {
        setTimeout(() => this.drawTrendLine(), 500);
      }
    } catch (err) {
      console.error('API请求失败:', err);
      this.setData({ loading: false, error: true });
    }
  },

  drawCompletionRing() {
    const rate = this.data.indicator.completionRate;
    const ctx = wx.createCanvasContext('completionRing');
    const cx = 55, cy = 55, r = 45, lineW = 10;

    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.setStrokeStyle('#e8ecf0');
    ctx.setLineWidth(lineW);
    ctx.setLineCap('round');
    ctx.stroke();

    const endAngle = -Math.PI / 2 + (Math.PI * 2 * rate) / 100;
    ctx.beginPath();
    ctx.arc(cx, cy, r, -Math.PI / 2, endAngle);
    const color = rate >= 90 ? '#2ecc71' : rate >= 70 ? '#3498db' : rate >= 50 ? '#f39c12' : '#e74c3c';
    ctx.setStrokeStyle(color);
    ctx.setLineWidth(lineW);
    ctx.setLineCap('round');
    ctx.stroke();

    ctx.draw();
  },

  drawTrendLine() {
    const trend = this.data.trend;
    if (trend.length < 2) return;

    const ctx = wx.createCanvasContext('trendCanvas');
    const w = 320, h = 200;
    const padL = 45, padR = 20, padT = 20, padB = 35;
    const plotW = w - padL - padR, plotH = h - padT - padB;

    const values = trend.map(t => t.value);
    const minV = Math.min(...values) * 0.95;
    const maxV = Math.max(...values) * 1.05;
    const range = maxV - minV || 1;
    const toX = (i) => padL + (plotW / (trend.length - 1)) * i;
    const toY = (v) => padT + plotH - ((v - minV) / range) * plotH;

    ctx.setStrokeStyle('#f0f0f0');
    ctx.setLineWidth(1);
    for (let i = 0; i <= 3; i++) {
      const y = padT + (plotH / 3) * i;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();
    }

    ctx.beginPath();
    trend.forEach((t, i) => {
      const x = toX(i), y = toY(t.value);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.setStrokeStyle('#2d6cdf');
    ctx.setLineWidth(2.5);
    ctx.setLineJoin('round');
    ctx.stroke();

    trend.forEach((t, i) => {
      const x = toX(i), y = toY(t.value);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.setFillStyle('#2d6cdf');
      ctx.fill();
      ctx.setFillStyle('#666');
      ctx.setFontSize(10);
      ctx.setTextAlign('center');
      ctx.fillText(t.value, x, y - 12);
      ctx.setFillStyle('#999');
      ctx.setFontSize(9);
      ctx.fillText(t.date, x, h - 4);
    });

    ctx.draw();
  },
});
