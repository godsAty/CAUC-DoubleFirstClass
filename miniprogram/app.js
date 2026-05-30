// 中国民航大学双一流建设完成度实时报告小程序
App({
  onLaunch() {
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    this.globalData.systemInfo = systemInfo;
    this.globalData.statusBarHeight = systemInfo.statusBarHeight;
    this.globalData.windowWidth = systemInfo.windowWidth;
    this.globalData.windowHeight = systemInfo.windowHeight;
    this.globalData.pixelRatio = systemInfo.pixelRatio;
  },

  globalData: {
    // API 服务器地址 - 开发环境使用本地，上线替换为服务器域名
    apiBase: 'http://10.124.139.141:5000',

    // 五大维度颜色方案
    categoryColors: {
      1: { main: '#2d6cdf', light: '#e8f0fe', name: '人才培养' },
      2: { main: '#d4443c', light: '#fde8e7', name: '师资队伍' },
      3: { main: '#3c9c3f', light: '#e8f5e9', name: '科研成果' },
      4: { main: '#f5a623', light: '#fef5e7', name: '社会服务' },
      5: { main: '#7b4e9e', light: '#f3eaf8', name: '国际化' },
    },

    // 达成度颜色阶梯
    rateColors(rate) {
      if (rate >= 90) return { main: '#2ecc71', text: '#1a7a3a' };
      if (rate >= 70) return { main: '#3498db', text: '#1a5276' };
      if (rate >= 50) return { main: '#f39c12', text: '#7d6608' };
      return { main: '#e74c3c', text: '#922b21' };
    }
  }
});
