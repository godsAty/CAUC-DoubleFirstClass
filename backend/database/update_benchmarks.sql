-- ============================================================
-- 双一流建设指标 - 基准数据更新（基于具体高校公开数据）
-- 对标策略：行业特色型高校（B层），以具名高校为参照
-- 数据来源：软科2024排名、高绩统计、Nature Index、ESI、NSFC年报等
-- ============================================================
USE CAUC_DoubleFirstClass;
GO

-- ===== 人才培养 (CategoryID=1) =====
-- 数据来源：教育部"双万计划"三批认定汇总（全国11,761个国家级一流专业）
-- 144所双一流共约5,300个，校均37个（TOP10均90+，中位数约22个）
-- 参照校：南航48门课/南理工46门/河海42门/江南大学33门
-- 中航大实际情况：47个本科专业（行业特色，专业总数远少于综合类大学的100+专业）

UPDATE IndicatorMaster SET TargetValue = 16, NationalAvg = 22.0 WHERE IndicatorCode = 'RC-01';  -- 一流专业
-- 参照：中航大8个，参照校南航约20个(47专业基础)，行业特色校均值约22个

UPDATE IndicatorMaster SET TargetValue = 18, NationalAvg = 40.0 WHERE IndicatorCode = 'RC-02';  -- 一流课程
-- 参照：清华223、南航48、南理工46、河海42、苏大42、矿大40、江大33。行业特色校中位数约40门

UPDATE IndicatorMaster SET TargetValue = 5,  NationalAvg = 5.5  WHERE IndicatorCode = 'RC-03';  -- 教学成果奖
-- 参照：2022年国家级教学成果奖共1998项，147校校均约5.5项（含参与）

UPDATE IndicatorMaster SET TargetValue = 6000, NationalAvg = 7000 WHERE IndicatorCode = 'RC-04';  -- 研究生规模
-- 参照：综合类大学10000+，行业特色校5000-8000

UPDATE IndicatorMaster SET TargetValue = 95,  NationalAvg = 93.0 WHERE IndicatorCode = 'RC-05';  -- 就业率
-- 参照：各校2023-2024学年本科教学质量报告（30+所已公布）
-- 浙大92.0%、南航95.4%、同济97.3%、华南理工97.5%、福州大学89.3%

UPDATE IndicatorMaster SET TargetValue = 100, NationalAvg = 120  WHERE IndicatorCode = 'RC-06';  -- 竞赛获奖
-- 参照：各校教务处年度竞赛统计

UPDATE IndicatorMaster SET TargetValue = 5,   NationalAvg = 8.0  WHERE IndicatorCode = 'RC-07';  -- 博士点
-- 参照：四川大学53个、上海科大1个。行业特色校：南航17个、南理工20个、江南大学10个
-- 中航大定位：安全+交通+航空宇航+管理+信息=5个核心学科覆盖
-- 行业特色校中位数约8个（非综合性大学）
GO

-- ===== 师资队伍 (CategoryID=2) =====
-- 数据来源：软科2024"师资规模与结构"模块、各校本科教学质量报告

UPDATE IndicatorMaster SET TargetValue = 2000, NationalAvg = 2100 WHERE IndicatorCode = 'FC-01';  -- 教师总数
-- 参照：吉林大学6300(双一流最多)、中国音乐学院<500(最少)
-- 行业特色校：南航2300、南理工2100、河海2200、矿大2100

UPDATE IndicatorMaster SET TargetValue = 75,   NationalAvg = 78.0 WHERE IndicatorCode = 'FC-02';  -- 博士占比
-- 来源：麦可思研究147所统计，双一流平均82.8%（全国本科平均47.6%）
-- 行业特色工程应用型校：南航68%、河海75%。目标75属合理水平

UPDATE IndicatorMaster SET TargetValue = 20,   NationalAvg = 25.0 WHERE IndicatorCode = 'FC-03';  -- 高层次人才
-- 来源：青塔2024学科人才统计
-- 软科"高端人才"模块：清华88.4分、北大92.4分（百分制）
-- 行业特色校：南航约30人、南理工约25人（两院院士+长江+杰青+万人+优青）

UPDATE IndicatorMaster SET TargetValue = 4,    NationalAvg = 5.0  WHERE IndicatorCode = 'FC-04';  -- 教学团队
-- 参照：教育部教学团队认定公示

UPDATE IndicatorMaster SET TargetValue = 17,   NationalAvg = 17.1 WHERE IndicatorCode = 'FC-05';  -- 生师比
-- 来源：教育部2024年统计公报——全国普通本科平均17.14:1
-- 双一流精英校<10:1，大规模型综合校16-18:1
GO

-- ===== 科研成果 (CategoryID=3) =====
-- 数据来源：Nature Index 2024、ESI 2024、NSFC 2024年报

UPDATE IndicatorMaster SET TargetValue = 5,   NationalAvg = 5.0  WHERE IndicatorCode = 'SR-01';  -- 科研平台
-- 中航大已有5个国家级平台，已达行业特色高校均值

UPDATE IndicatorMaster SET TargetValue = 10,  NationalAvg = 12.0 WHERE IndicatorCode = 'SR-02';  -- 重点研发
-- 科技部项目管理系统公示

UPDATE IndicatorMaster SET TargetValue = 50,  NationalAvg = 55.0 WHERE IndicatorCode = 'SR-03';  -- 国自然
-- 来源：NSFC 2024集中接收期全国约4.5万项/147校，均值约300项但中位数仅85项
-- 行业特色理工校：南航约120项、南理工约100项、河海约80项、矿大约60项
-- 中位数约55项（剔除极端值后的行业特色校水平）

UPDATE IndicatorMaster SET TargetValue = 500, NationalAvg = 700  WHERE IndicatorCode = 'SR-04';  -- SCI论文
-- 来源：Nature Index 2024（145种顶刊）、ESI 2024（十年累计）
-- 行业特色校：南航约1000篇/年、南理工约800篇/年、河海约700篇/年
-- 中位数约700篇（数据来自WoS数据库检索推算）

UPDATE IndicatorMaster SET TargetValue = 3.5, NationalAvg = 4.0  WHERE IndicatorCode = 'SR-05';  -- 科研经费(亿)
-- 来源：各校2024年公开决算
-- 头部校：清华80亿级、浙大/上交70亿级
-- 行业特色校：南航约8亿、南理工约5亿、河海约4亿。中位数约4亿

UPDATE IndicatorMaster SET TargetValue = 1,   NationalAvg = 1.0  WHERE IndicatorCode = 'SR-06';  -- 科技奖励
-- 来源：国家科学技术奖励办公室
-- 行业特色校牵头获国家奖极为困难，通常作为参与单位
GO

-- ===== 社会服务 (CategoryID=4) =====
UPDATE IndicatorMaster SET TargetValue = 3000, NationalAvg = 3500 WHERE IndicatorCode = 'SS-01';  -- 成果转化(万)
UPDATE IndicatorMaster SET TargetValue = 200,  NationalAvg = 250  WHERE IndicatorCode = 'SS-02';  -- 发明专利(件)
UPDATE IndicatorMaster SET TargetValue = 12,   NationalAvg = 15   WHERE IndicatorCode = 'SS-03';  -- 智库成果
GO

-- ===== 国际化 (CategoryID=5) =====
UPDATE IndicatorMaster SET TargetValue = 2,   NationalAvg = 2.0  WHERE IndicatorCode = 'INT-01';  -- 国际实验室
UPDATE IndicatorMaster SET TargetValue = 40,  NationalAvg = 40.0 WHERE IndicatorCode = 'INT-02';  -- 海外经历(%)
UPDATE IndicatorMaster SET TargetValue = 500, NationalAvg = 600  WHERE IndicatorCode = 'INT-03';  -- 留学生
GO

PRINT '==========================================';
PRINT '  基准数据更新完成（行业特色高校B层常模）';
PRINT '  参照校：南航、南理工、河海、矿大、江大等';
PRINT '  数据来源：软科2024、Nature Index 2024、';
PRINT '            ESI 2024、NSFC年报、各校质量报告';
PRINT '==========================================';
GO
