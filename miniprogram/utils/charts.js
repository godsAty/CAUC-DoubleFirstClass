// ECharts 图表初始化工具 (配合 echarts-for-weixin 组件使用)
// 需要在项目根目录引入 echarts-for-weixin 包

const app = getApp();

// 默认图表配色
const chartColors = ['#2d6cdf', '#3c9c3f', '#f5a623', '#d4443c', '#7b4e9e'];

// 通用的雷达图配置
const getRadarOption = (data) => {
  if (!data || !data.dimensions) return {};

  return {
    legend: {
      data: ['本校达成度', '全国均值达成度', '双一流目标'],
      bottom: 10,
      textStyle: { fontSize: 11 }
    },
    radar: {
      center: ['50%', '45%'],
      radius: '58%',
      indicator: data.dimensions.map(name => ({ name, max: 100 })),
      axisName: { fontSize: 10 }
    },
    series: [{
      type: 'radar',
      data: [
        {
          value: data.cauc || [],
          name: '本校达成度',
          lineStyle: { color: '#2d6cdf', width: 2 },
          areaStyle: { color: 'rgba(45, 108, 223, 0.2)' },
          itemStyle: { color: '#2d6cdf' }
        },
        {
          value: data.nationalAvg || [],
          name: '全国均值达成度',
          lineStyle: { color: '#f5a623', width: 2 },
          areaStyle: { color: 'rgba(245, 166, 35, 0.15)' },
          itemStyle: { color: '#f5a623' }
        },
        {
          value: data.target || [],
          name: '双一流目标',
          lineStyle: { color: '#3c9c3f', width: 2, type: 'dashed' },
          areaStyle: { color: 'rgba(60, 156, 63, 0.05)' },
          itemStyle: { color: '#3c9c3f' }
        }
      ]
    }]
  };
};

// 对比柱状图配置 (用于详情页)
const getBarOption = (data) => {
  if (!data || !data.indicators) return {};

  return {
    legend: {
      data: ['本校达成率', '全国均值达成率', '目标线'],
      bottom: 10,
      textStyle: { fontSize: 11 }
    },
    grid: {
      left: 15,
      right: 20,
      bottom: 40,
      top: 10,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.indicators || [],
      axisLabel: {
        rotate: 30,
        fontSize: 9,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      max: 100,
      name: '达成度(%)',
      axisLabel: { fontSize: 9 }
    },
    series: [
      {
        name: '本校达成率',
        type: 'bar',
        data: data.cauc || [],
        itemStyle: { color: '#2d6cdf', borderRadius: [4, 4, 0, 0] }
      },
      {
        name: '全国均值达成率',
        type: 'bar',
        data: data.nationalAvg || [],
        itemStyle: { color: '#f5a623', borderRadius: [4, 4, 0, 0] }
      },
      {
        name: '目标线',
        type: 'line',
        data: data.target || [],
        lineStyle: { color: '#3c9c3f', type: 'dashed', width: 2 },
        symbol: 'none'
      }
    ]
  };
};

module.exports = {
  chartColors,
  getRadarOption,
  getBarOption,
};
