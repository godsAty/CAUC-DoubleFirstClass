-- 中国民航大学双一流建设完成度实时报告系统 - 数据库初始化脚本
-- 适用: SQL Server 2016+

-- 创建数据库
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'CAUC_DoubleFirstClass')
BEGIN
    CREATE DATABASE CAUC_DoubleFirstClass;
END
GO

USE CAUC_DoubleFirstClass;
GO

-- =============================================
-- 1. 指标大类表
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'IndicatorCategory') AND type = 'U')
BEGIN
    CREATE TABLE IndicatorCategory (
        CategoryID   INT IDENTITY(1,1) PRIMARY KEY,
        CategoryName NVARCHAR(50)  NOT NULL,
        Icon         NVARCHAR(20)  NULL,
        SortOrder    INT           NOT NULL DEFAULT 0
    );
END
GO

-- =============================================
-- 2. 指标定义主表
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'IndicatorMaster') AND type = 'U')
BEGIN
    CREATE TABLE IndicatorMaster (
        IndicatorID    INT IDENTITY(1,1) PRIMARY KEY,
        CategoryID     INT            NOT NULL,
        IndicatorCode  VARCHAR(10)    NOT NULL UNIQUE,
        IndicatorName  NVARCHAR(100)  NOT NULL,
        Unit           NVARCHAR(20)   NULL,
        Weight         DECIMAL(5,2)   NOT NULL DEFAULT 0,
        TargetValue    DECIMAL(18,2)  NULL,
        NationalAvg    DECIMAL(18,2)  NULL,
        Direction      VARCHAR(5)     NOT NULL DEFAULT 'up',
        DataSource     NVARCHAR(200)  NULL,
        CONSTRAINT FK_Indicator_Category FOREIGN KEY (CategoryID) REFERENCES IndicatorCategory(CategoryID)
    );
END
GO

-- =============================================
-- 3. 中航大实际数据表
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'CAUCData') AND type = 'U')
BEGIN
    CREATE TABLE CAUCData (
        DataID       INT IDENTITY(1,1) PRIMARY KEY,
        IndicatorID  INT            NOT NULL,
        ActualValue  DECIMAL(18,2)  NOT NULL,
        DataYear     INT            NOT NULL,
        ScrapeTime   DATETIME       NOT NULL DEFAULT GETDATE(),
        SourceURL    NVARCHAR(300)  NULL,
        IsManual     BIT            NOT NULL DEFAULT 0,
        CONSTRAINT FK_CAUCData_Indicator FOREIGN KEY (IndicatorID) REFERENCES IndicatorMaster(IndicatorID)
    );
END
GO

-- =============================================
-- 4. 历史快照表（趋势图数据源）
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'DataSnapshot') AND type = 'U')
BEGIN
    CREATE TABLE DataSnapshot (
        SnapshotID     INT IDENTITY(1,1) PRIMARY KEY,
        SnapshotDate   DATE           NOT NULL,
        IndicatorID    INT            NOT NULL,
        Value          DECIMAL(18,2)  NOT NULL,
        CompletionRate DECIMAL(5,2)   NOT NULL,
        CONSTRAINT FK_Snapshot_Indicator FOREIGN KEY (IndicatorID) REFERENCES IndicatorMaster(IndicatorID)
    );
END
GO

-- =============================================
-- 5. 完成度汇总快照表
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'CompletionSummary') AND type = 'U')
BEGIN
    CREATE TABLE CompletionSummary (
        SummaryID       INT IDENTITY(1,1) PRIMARY KEY,
        ReportDate      DATE           NOT NULL,
        CategoryID      INT            NOT NULL,
        CompletionRate  DECIMAL(5,2)   NOT NULL,
        NationalAvgRate DECIMAL(5,2)   NOT NULL,
        CONSTRAINT FK_Summary_Category FOREIGN KEY (CategoryID) REFERENCES IndicatorCategory(CategoryID)
    );
END
GO

PRINT 'All tables created successfully.';
GO
