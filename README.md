# 中国民航大学双一流建设完成度实时报告系统

对照教育部"双一流"建设检测指标体系，动态抓取学校公开数据，从**人才培养、师资队伍、科研成果、社会服务、国际化**五大维度呈现达成度。采用**行业特色型高校分层对标**策略，将本校数据与 B 层常模（同类高校基准值）进行科学对比。

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2+-000?logo=flask)](https://flask.palletsprojects.com/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-2016+-CC2927?logo=microsoftsqlserver)](https://www.microsoft.com/sql-server)
[![微信小程序](https://img.shields.io/badge/微信小程序-2.32+-07C160?logo=wechat)](https://developers.weixin.qq.com/miniprogram/)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

---

## 推荐环境

| 组件 | 要求 | 注意事项 |
|:---|:---|:---|
| Python | 3.9.7+ | 安装时勾选「Add Python to PATH」 |
| SQL Server | 2016+（含 Express） | 安装后确保服务已启动 |
| SSMS | 图形化执行 SQL 脚本 | 与 SQL Server 配套安装 |
| 微信开发者工具 | 最新稳定版 | 安装后登录微信账号 |

---

## 功能特性

- **24 项双一流检测指标**：依据教育部《"双一流"建设成效评价办法（试行）》（教研〔2020〕13 号）设计，覆盖人才培养（7项）、师资队伍（5项）、科研成果（6项）、社会服务（3项）、国际化（3项）。指标编号规则见第六节
- **分层对标体系**：将 147 所双一流高校分为 A/B/C 三层，中航大对标行业特色型高校（B 层），以南京航空航天大学、南京理工大学、河海大学、中国矿业大学、江南大学五所为参照
- **三方数据对比**：中航大实际值 ↔ 双一流建设目标值 ↔ 同类高校常模值（B 层），逐项呈现达成度
- **五维雷达图**：Canvas 手绘五大维度达成度雷达图，本校/全国均值/目标值三线叠加
- **环形进度条**：Canvas 动画绘制综合完成度环形图，四色阶梯（绿/蓝/橙/红）直观评定等级
- **历史趋势折线图**：每项指标可追溯最近季度变化趋势，支持月度快照自动累积
- **定时数据更新**：APScheduler 定时爬取中航大官网 + 每月自动生成数据快照
- **真实数据溯源**：24 项指标数据来自 24 个公开渠道，每条标注来源 URL 和可信度等级
- **数据流水线**：`setup_data.py` 一键完成数据库初始化→种子数据→基准数据→实际数据全流程

---

## 从零开始运行

> 无需配置环境变量，数据库连接直接在 `config.py` 中设置。

### 第一步：安装依赖

```powershell
cd "D:\Desktop\新建文件夹 (2)\backend"
pip install -r requirements.txt
```

### 第二步：初始化数据库

数据库名 `CAUC_DoubleFirstClass`。选一种方式执行：

**SSMS（推荐）** — 依次打开并执行这 4 个文件（每个按 F5）：

1. `backend\database\init_db.sql` → 建库建表
2. `backend\database\seed_data.sql` → 种子数据
3. `backend\database\update_benchmarks.sql` → 目标值 + 全国均值
4. `backend\database\update_real_data.sql` → 中航大实际值

**sqlcmd** — 逐条执行：

```powershell
sqlcmd -S localhost -E -i "backend\database\init_db.sql"
sqlcmd -S localhost -E -i "backend\database\seed_data.sql"
sqlcmd -S localhost -E -i "backend\database\update_benchmarks.sql"
sqlcmd -S localhost -E -i "backend\database\update_real_data.sql"
```

**Python 流水线**（等同于上面两步）：

```powershell
python setup_data.py
```

### 第三步：检查配置

打开 `backend\config.py`。默认使用 Windows 集成认证连接本地 SQL Server，一般无需修改。如果你的 SQL Server 是 Express 版（实例名 `SQLEXPRESS`），把 `DB_SERVER` 改为 `localhost\SQLEXPRESS` 即可。

### 第四步：启动后端

```powershell
cd "D:\Desktop\新建文件夹 (2)\backend"
python app.py
```

看到 `[OK] SQL Server 连接成功` 且出现 `http://127.0.0.1:5000` 即成功。保持窗口运行，不要关闭。

### 第五步：打开小程序

1. 微信开发者工具 → 导入项目 → 目录选 `miniprogram\` → AppID 用测试号
2. 点击编译。看到环形进度条和维度卡片即成功
3. 如果显示"数据加载失败"：确认 `miniprogram\app.js` 中 `apiBase` 为 `http://localhost:5000`，且第四步的 Flask 正在运行

---

## 项目目录结构

```
├── README.md / README.docx             项目文档
├── 设计文档.docx                        系统设计文档（字段级）
├── 数据来源说明报告.docx                 数据溯源专项报告
├── 中期报告.docx                        中期检查报告
├── 校徽.jfif                           校徽原文件
│
├── backend/                             Python Flask 后端
│   ├── app.py                           Flask 主入口（路由 + 调度器）
│   ├── config.py                        数据库连接 + 爬虫配置
│   ├── requirements.txt                 pip 依赖清单
│   ├── setup_data.py                    ★ 数据流水线主控（一键初始化）
│   │
│   ├── database/                        数据库层
│   │   ├── models.py                    SQLAlchemy ORM 模型（5 张表）
│   │   ├── init_db.sql                  建库建表脚本
│   │   ├── seed_data.sql                初始种子数据
│   │   ├── update_real_data.sql         中航大实际数据（可溯源）
│   │   ├── update_benchmarks.sql        双一流基准数据（B 层常模）
│   │   ├── seed_benchmarks.py           基准数据 Python 脚本（可单独执行）
│   │   └── seed_cauc_data.py            实际数据 Python 脚本（可单独执行）
│   │
│   ├── api/                             API 接口层
│   │   ├── dashboard.py                 GET /api/overview
│   │   ├── indicators.py                GET /api/category/<id>
│   │   └── comparison.py                GET /api/comparison
│   │
│   ├── services/                        业务服务层
│   │   └── update_service.py            数据快照生成 + 完成度汇总
│   │
│   └── crawler/                         爬虫与调度
│       ├── cauc_spider.py               中航大官网爬虫
│       └── scheduler.py                 APScheduler 定时调度器
│
└── miniprogram/                         微信小程序前端
    ├── app.js/json/wxss                 应用入口（航空蓝主题）
    ├── project.config.json              开发者工具配置
    ├── pages/                           4 个页面
    │   ├── index/                       首页 · 综合概览
    │   ├── category/                    分类指标详情
    │   ├── comparison/                  对标对比分析
    │   └── detail/                      单项指标详情
    ├── components/                      3 个组件
    │   ├── progress-ring/               环形进度条（Canvas 动画）
    │   ├── indicator-card/              指标卡片（三值对比 + 双层进度条）
    │   └── comparison-bar/              对比柱状条（双柱 + 目标虚线）
    ├── utils/                           工具函数
    │   ├── api.js                       API 请求封装 + 错误处理
    │   └── charts.js                    图表配置生成器
    └── assets/
        └── emblem.png                   中国民航大学校徽（200×200 圆角）
```

---

## 指标编号规则

24 项指标采用"维度英文缩写 + 序号"的统一编码，贯穿数据库、API、前端和数据脚本：

| 前缀 | 对应维度 | 编号范围 | 项数 |
|:---|:---|:---|:---:|
| RC | 人才培养（Personnel Cultivation） | RC-01 ~ RC-07 | 7 |
| FC | 师资队伍（Faculty Construction） | FC-01 ~ FC-05 | 5 |
| SR | 科研成果（Scientific Research） | SR-01 ~ SR-06 | 6 |
| SS | 社会服务（Social Services） | SS-01 ~ SS-03 | 3 |
| INT | 国际化（Internationalization） | INT-01 ~ INT-03 | 3 |

---

## 数据库设计

| 表名 | 说明 | 核心字段 |
|:---|:---|:---|
| IndicatorCategory | 指标大类（5 条） | CategoryID, CategoryName, SortOrder |
| IndicatorMaster | 指标定义主表（24 条） | IndicatorCode, TargetValue, NationalAvg, Weight, Direction |
| CAUCData | 中航大实际数据 | ActualValue, DataYear, SourceURL, IsManual |
| DataSnapshot | 历史快照（趋势图数据源） | SnapshotDate, Value, CompletionRate |
| CompletionSummary | 完成度汇总 | ReportDate, CategoryID, CompletionRate |

---

## API 接口

| 方法 | 路径 | 说明 |
|:---|:---|:---|
| `GET` | `/api/overview` | 综合概览：总完成度 + 五大维度 |
| `GET` | `/api/category/<id>` | 分类指标详情（id: 1–5） |
| `GET` | `/api/indicator/<id>` | 单项指标详情 + 历史趋势（id: 1–24） |
| `GET` | `/api/comparison` | 雷达图 + 柱状图三方对比数据 |
| `GET` | `/api/trend/<id>` | 某指标历史趋势 |
| `POST` | `/api/manual-update` | 手动更新指标实际值 |
| `POST` | `/api/snapshot` | 触发月度数据快照 |

---

## 数据来源

| 数据层 | 主要来源 | 覆盖学校数 |
|:---|:---|:---:|
| 中航大实际值 | 学校官网、招生简章、百度百科、新闻网、科技处、就业报告 | 1 所 |
| 双一流目标值 | 教育部教研〔2020〕13 号 + 5 所核心参照校公开数据 | 5 所 |
| 全国均值（全量覆盖 9 项） | 双万计划全量、学位授权公示、麦可思统计、NSFC 年报、Nature Index/ESI Top200 | 147–200 所 |
| 全国均值（大面积覆盖 3 项） | 一流课程认定名单、各校教学质量报告、青塔人才统计 | 30–100 所 |
| 全国均值（参照校覆盖 12 项） | 五所核心参照校（南航/南理工/河海/矿大/江大）公开数据 | 5–10 所 |

---

## 对标策略

147 所双一流高校分三层，中航大对标 **B 层（行业特色型高校）**：

| 层级 | 类型 | 代表学校 | 对标? |
|:---|:---|:---|:---:|
| A 层 | 综合类研究型 985 | 清华、北大、浙大、上交 | 否 |
| **B 层** | **行业特色型高校** | **南航、南理工、河海、矿大、江大** | **是** |
| C 层 | 区域服务型/新晋双一流 | 各省新晋双一流 | 参考下限 |

---

## 常见问题

**Q: pip install 时 pyodbc 安装失败？**

A: 未安装 ODBC Driver 17 for SQL Server。回到"基础准备"表格，下载安装 ODBC Driver 17：https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server

**Q: python app.py 时显示 `[WARN] SQL Server 连接失败`？**

A: 按顺序排查：① SQL Server 服务是否"正在运行"（Windows 服务中查看）；② `config.py` 中 `DB_SERVER` 是否正确（Express 版通常是 `localhost\SQLEXPRESS`）；③ 是否需要用户名密码（取消备用配置段注释）。

**Q: 小程序首页显示"数据加载失败"？**

A: ① 确认 Flask 正在运行（PowerShell 能看到 5000 端口）；② 确认 `miniprogram\app.js` 中 `apiBase` 为 `http://localhost:5000`；③ 检查 Windows 防火墙是否阻止了 5000 端口。

**Q: 如何更新某项指标的数据？**

A: `POST /api/manual-update`，JSON 参数 `{"indicator_id": 1, "value": 9, "year": 2025}`。或在 SSMS 中修改 `CAUCData` 表后重启 Flask。

**Q: 如何调整目标值或全国均值？**

A: 修改 `database/seed_benchmarks.py` 中对应字典值 → 执行 `python database/seed_benchmarks.py`。

**Q: 数据库需要完全重置？**

A: SSMS 中删除 `CAUC_DoubleFirstClass` 数据库 → 重新 `python setup_data.py`。

---

## 许可证

本项目采用 MIT License 开源。

---

> **"明德至善、弘毅兴邦"** — 中国民航大学校训
