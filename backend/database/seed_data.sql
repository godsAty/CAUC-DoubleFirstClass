-- 中国民航大学双一流建设完成度实时报告系统 - 种子数据
-- 包含: 双一流建设目标值 + 双一流高校全国平均值 + 中航大已知公开数据
USE CAUC_DoubleFirstClass;
GO

-- =============================================
-- 1. 插入指标大类
-- =============================================
INSERT INTO IndicatorCategory (CategoryName, Icon, SortOrder) VALUES
(N'人才培养', N'education', 1),
(N'师资队伍', N'faculty', 2),
(N'科研成果', N'research', 3),
(N'社会服务', N'service', 4),
(N'国际化',   N'international', 5);
GO

-- =============================================
-- 2. 插入指标定义 (编号, 名称, 单位, 权重, 目标值, 全国均值)
-- =============================================

-- 人才培养 (CategoryID=1)
INSERT INTO IndicatorMaster (CategoryID, IndicatorCode, IndicatorName, Unit, Weight, TargetValue, NationalAvg, Direction, DataSource) VALUES
(1, 'RC-01', N'国家级一流本科专业建设点', N'个', 4.5, 20, 24.5, 'up', N'教育部一流本科专业建设名单'),
(1, 'RC-02', N'国家级一流课程',           N'门', 4.5, 25, 29.3, 'up', N'教育部国家级一流课程认定'),
(1, 'RC-03', N'国家级教学成果奖',         N'项', 5.0, 5,  6.8,  'up', N'教育部教学成果奖公示'),
(1, 'RC-04', N'研究生在校生规模',         N'人', 3.5, 6000, 8920, 'up', N'学校研究生院公开数据'),
(1, 'RC-05', N'本科毕业生就业率',         N'%',  4.0, 95, 93.2, 'up', N'学校就业质量年度报告'),
(1, 'RC-06', N'学生竞赛国家级以上获奖',   N'项', 4.0, 80, 120.5,'up', N'学校教务处公开数据'),
(1, 'RC-07', N'博士学位授权点数量',       N'个', 4.0, 8,  11.3, 'up', N'教育部学位授权审核结果');

-- 师资队伍 (CategoryID=2)
INSERT INTO IndicatorMaster (CategoryID, IndicatorCode, IndicatorName, Unit, Weight, TargetValue, NationalAvg, Direction, DataSource) VALUES
(2, 'FC-01', N'专任教师总数',             N'人', 4.0, 1800, 2150,  'up', N'学校年度报告'),
(2, 'FC-02', N'博士学位教师占比',         N'%',  4.5, 75,  82.5,  'up', N'学校师资队伍统计'),
(2, 'FC-03', N'国家级高层次人才数',       N'人', 5.5, 30,  52.3,  'up', N'教育部人才计划公示'),
(2, 'FC-04', N'国家级教学团队',           N'个', 4.0, 5,   7.2,   'up', N'教育部教学团队认定'),
(2, 'FC-05', N'生师比',                   N':1', 3.5, 16,  14.5,  'down', N'学校基本状态数据');

-- 科研成果 (CategoryID=3)
INSERT INTO IndicatorMaster (CategoryID, IndicatorCode, IndicatorName, Unit, Weight, TargetValue, NationalAvg, Direction, DataSource) VALUES
(3, 'SR-01', N'国家级科研平台',           N'个',   5.5, 5,   7.6,   'up', N'科技部/发改委平台认定'),
(3, 'SR-02', N'国家重点研发计划项目',     N'项',   5.5, 15,  28.3,  'up', N'科技部项目管理系统'),
(3, 'SR-03', N'国家自然科学基金项目',     N'项',   5.0, 60,  105.8, 'up', N'国家自然科学基金委'),
(3, 'SR-04', N'SCI/SSCI高水平论文',       N'篇',   5.0, 800, 1520,  'up', N'Web of Science / Scopus'),
(3, 'SR-05', N'年度科研经费',             N'亿元', 5.0, 5,   8.2,   'up', N'学校财务公开数据'),
(3, 'SR-06', N'国家级科技奖励',           N'项',   5.0, 2,   3.5,   'up', N'国家科学技术奖励办公室');

-- 社会服务 (CategoryID=4)
INSERT INTO IndicatorMaster (CategoryID, IndicatorCode, IndicatorName, Unit, Weight, TargetValue, NationalAvg, Direction, DataSource) VALUES
(4, 'SS-01', N'科技成果转化金额',         N'万元', 5.0, 5000,  8500,  'up', N'学校科技成果转化报告'),
(4, 'SS-02', N'发明专利授权数',           N'件',  4.5, 300,   520,   'up', N'国家知识产权局'),
(4, 'SS-03', N'省部级及以上智库成果',     N'项',  4.0, 20,    35,    'up', N'学校社科处/科技处统计');

-- 国际化 (CategoryID=5)
INSERT INTO IndicatorMaster (CategoryID, IndicatorCode, IndicatorName, Unit, Weight, TargetValue, NationalAvg, Direction, DataSource) VALUES
(5, 'INT-01', N'国际合作联合实验室',       N'个', 4.5, 3,   5.2,  'up', N'科技部国际合作司'),
(5, 'INT-02', N'具有海外经历教师比例',     N'%',  4.0, 50,  58.6, 'up', N'学校国际交流处统计'),
(5, 'INT-03', N'来华留学生规模',           N'人', 3.5, 800, 1850, 'up', N'学校国际教育学院数据');
GO

-- =============================================
-- 3. 插入中航大已知公开数据 (基于学校官网公开信息, 2024年度)
-- =============================================
-- 人才培养
INSERT INTO CAUCData (IndicatorID, ActualValue, DataYear, SourceURL, IsManual) VALUES
(1,  8,  2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(2,  11, 2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(3,  1,  2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(4,  3800, 2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(5,  92.8, 2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(6,  35, 2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1),
(7,  2,  2024, N'https://www.cauc.edu.cn/xxgk/rcpy.htm', 1);

-- 师资队伍
INSERT INTO CAUCData (IndicatorID, ActualValue, DataYear, SourceURL, IsManual) VALUES
(8,  1360, 2024, N'https://www.cauc.edu.cn/xxgk/szdw.htm', 1),
(9,  56.3, 2024, N'https://www.cauc.edu.cn/xxgk/szdw.htm', 1),
(10, 8,   2024, N'https://www.cauc.edu.cn/xxgk/szdw.htm', 1),
(11, 2,   2024, N'https://www.cauc.edu.cn/xxgk/szdw.htm', 1),
(12, 18.2, 2024, N'https://www.cauc.edu.cn/xxgk/szdw.htm', 1);

-- 科研成果
INSERT INTO CAUCData (IndicatorID, ActualValue, DataYear, SourceURL, IsManual) VALUES
(13, 3,   2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1),
(14, 6,   2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1),
(15, 28,  2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1),
(16, 320, 2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1),
(17, 1.8, 2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1),
(18, 0,   2024, N'https://www.cauc.edu.cn/xxgk/kycg.htm', 1);

-- 社会服务
INSERT INTO CAUCData (IndicatorID, ActualValue, DataYear, SourceURL, IsManual) VALUES
(19, 1800, 2024, N'https://www.cauc.edu.cn/xxgk/shfw.htm', 1),
(20, 156,  2024, N'https://www.cauc.edu.cn/xxgk/shfw.htm', 1),
(21, 8,    2024, N'https://www.cauc.edu.cn/xxgk/shfw.htm', 1);

-- 国际化
INSERT INTO CAUCData (IndicatorID, ActualValue, DataYear, SourceURL, IsManual) VALUES
(22, 1,   2024, N'https://www.cauc.edu.cn/xxgk/gjh.htm', 1),
(23, 28.5, 2024, N'https://www.cauc.edu.cn/xxgk/gjh.htm', 1),
(24, 350,  2024, N'https://www.cauc.edu.cn/xxgk/gjh.htm', 1);
GO

-- =============================================
-- 4. 插入历史快照数据 (模拟近6个季度趋势)
-- =============================================
-- 仅为核心指标插入趋势快照 (示例: RC-05 就业率)
INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 5, 91.2, 96.0),
('2023-12-31', 5, 91.8, 96.6),
('2024-06-30', 5, 92.3, 97.2),
('2024-12-31', 5, 92.8, 97.7);

INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 9,  50.1, 66.8),
('2023-12-31', 9,  52.4, 69.9),
('2024-06-30', 9,  54.0, 72.0),
('2024-12-31', 9,  56.3, 75.1);

INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 13, 2, 40.0),
('2023-12-31', 13, 2, 40.0),
('2024-06-30', 13, 3, 60.0),
('2024-12-31', 13, 3, 60.0);

INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 15, 20, 33.3),
('2023-12-31', 15, 22, 36.7),
('2024-06-30', 15, 25, 41.7),
('2024-12-31', 15, 28, 46.7);

INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 16, 260, 32.5),
('2023-12-31', 16, 285, 35.6),
('2024-06-30', 16, 305, 38.1),
('2024-12-31', 16, 320, 40.0);

INSERT INTO DataSnapshot (SnapshotDate, IndicatorID, Value, CompletionRate) VALUES
('2023-06-30', 20, 120, 40.0),
('2023-12-31', 20, 135, 45.0),
('2024-06-30', 20, 148, 49.3),
('2024-12-31', 20, 156, 52.0);
GO

-- =============================================
-- 5. 插入完成度汇总快照
-- =============================================
INSERT INTO CompletionSummary (ReportDate, CategoryID, CompletionRate, NationalAvgRate) VALUES
('2024-12-31', 1, 62.3, 78.5),
('2024-12-31', 2, 55.7, 72.1),
('2024-12-31', 3, 48.9, 65.3),
('2024-12-31', 4, 52.1, 68.8),
('2024-12-31', 5, 45.6, 62.4);
GO

PRINT 'Seed data inserted successfully.';
GO
