// 对标对比页 - 雷达图 + 柱状对比（数据来自后端 API）
const api = require('../../utils/api');

Page({
  data: {
    radarData: null,
    barData: null,
    loading: true,
    error: false,
    overallCauc: 0,
    overallNational: 0,
  },

  onLoad() {
    this.fetchData();
  },

  onShow() {
    if (!this.data.loading && !this.data.radarData) this.fetchData();
  },

  onPullDownRefresh() {
    this.fetchData().finally(() => wx.stopPullDownRefresh());
  },

  async fetchData() {
    this.setData({ loading: true, error: false });
    try {
      const data = await api.getComparison();
      const caucAvg = data.radar.cauc.reduce((a, b) => a + b, 0) / data.radar.cauc.length;
      const natAvg = data.radar.nationalAvg.reduce((a, b) => a + b, 0) / data.radar.nationalAvg.length;

      this.setData({
        radarData: data.radar,
        barData: data.bar,
        overallCauc: caucAvg.toFixed(2),
        overallNational: natAvg.toFixed(2),
        loading: false,
      });

      setTimeout(() => this.drawRadarChart(), 500);
    } catch (err) {
      console.error('API请求失败:', err);
      this.setData({ loading: false, error: true });
    }
  },

  drawRadarChart() {
    const data = this.data.radarData;
    if (!data) return;

    const ctx = wx.createCanvasContext('radarCanvas');
    const w = 340, h = 340;
    const cx = w / 2, cy = h / 2 - 10;
    const maxR = 120;
    const dims = data.dimensions;
    const n = dims.length;

    for (let level = 1; level <= 5; level++) {
      const r = (maxR / 5) * level;
      ctx.beginPath();
      for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 / n) * i - Math.PI / 2;
        const x = cx + r * Math.cos(angle), y = cy + r * Math.sin(angle);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.setStrokeStyle('#e8ecf0');
      ctx.setLineWidth(1);
      ctx.stroke();
    }

    for (let i = 0; i < n; i++) {
      const angle = (Math.PI * 2 / n) * i - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + maxR * Math.cos(angle), cy + maxR * Math.sin(angle));
      ctx.setStrokeStyle('#e8ecf0');
      ctx.setLineWidth(1);
      ctx.stroke();

      const lx = cx + (maxR + 30) * Math.cos(angle);
      const ly = cy + (maxR + 30) * Math.sin(angle);
      ctx.setFillStyle('#333');
      ctx.setFontSize(12);
      ctx.setTextAlign('center');
      ctx.setTextBaseline('middle');
      ctx.fillText(dims[i], lx, ly);
    }

    const drawPolygon = (values, color, fillColor, lw, dashed) => {
      ctx.beginPath();
      for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 / n) * i - Math.PI / 2;
        const r = (maxR * values[i]) / 100;
        const x = cx + r * Math.cos(angle), y = cy + r * Math.sin(angle);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.setLineDash(dashed ? [6, 4] : []);
      ctx.setStrokeStyle(color);
      ctx.setLineWidth(lw);
      ctx.setFillStyle(fillColor);
      ctx.fill();
      ctx.stroke();
      ctx.setLineDash([]);

      for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 / n) * i - Math.PI / 2;
        const r = (maxR * values[i]) / 100;
        ctx.beginPath();
        ctx.arc(cx + r * Math.cos(angle), cy + r * Math.sin(angle), 3, 0, Math.PI * 2);
        ctx.setFillStyle(color);
        ctx.fill();
      }
    };

    drawPolygon(data.nationalAvg, '#f5a623', 'rgba(245,166,35,0.1)', 2, false);
    drawPolygon(data.target, '#3c9c3f', 'rgba(60,156,63,0.05)', 1.5, true);
    drawPolygon(data.cauc, '#2d6cdf', 'rgba(45,108,223,0.15)', 2.5, false);

    ctx.draw();
  },
});
