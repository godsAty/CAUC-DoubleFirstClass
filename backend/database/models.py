# 中国民航大学双一流建设完成度实时报告系统 - 数据模型
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class IndicatorCategory(db.Model):
    __tablename__ = 'IndicatorCategory'

    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(50), nullable=False)
    Icon = db.Column(db.String(20))
    SortOrder = db.Column(db.Integer, nullable=False, default=0)

    indicators = db.relationship('IndicatorMaster', backref='category', lazy=True)


class IndicatorMaster(db.Model):
    __tablename__ = 'IndicatorMaster'

    IndicatorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryID = db.Column(db.Integer, db.ForeignKey('IndicatorCategory.CategoryID'), nullable=False)
    IndicatorCode = db.Column(db.String(10), unique=True, nullable=False)
    IndicatorName = db.Column(db.String(100), nullable=False)
    Unit = db.Column(db.String(20))
    Weight = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    TargetValue = db.Column(db.Numeric(18, 2))
    NationalAvg = db.Column(db.Numeric(18, 2))
    Direction = db.Column(db.String(5), nullable=False, default='up')
    DataSource = db.Column(db.String(200))

    cauc_data = db.relationship('CAUCData', backref='indicator', lazy=True)
    snapshots = db.relationship('DataSnapshot', backref='indicator', lazy=True)


class CAUCData(db.Model):
    __tablename__ = 'CAUCData'

    DataID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IndicatorID = db.Column(db.Integer, db.ForeignKey('IndicatorMaster.IndicatorID'), nullable=False)
    ActualValue = db.Column(db.Numeric(18, 2), nullable=False)
    DataYear = db.Column(db.Integer, nullable=False)
    ScrapeTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    SourceURL = db.Column(db.String(300))
    IsManual = db.Column(db.Boolean, nullable=False, default=False)


class DataSnapshot(db.Model):
    __tablename__ = 'DataSnapshot'

    SnapshotID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SnapshotDate = db.Column(db.Date, nullable=False)
    IndicatorID = db.Column(db.Integer, db.ForeignKey('IndicatorMaster.IndicatorID'), nullable=False)
    Value = db.Column(db.Numeric(18, 2), nullable=False)
    CompletionRate = db.Column(db.Numeric(5, 2), nullable=False)


class CompletionSummary(db.Model):
    __tablename__ = 'CompletionSummary'

    SummaryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ReportDate = db.Column(db.Date, nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('IndicatorCategory.CategoryID'), nullable=False)
    CompletionRate = db.Column(db.Numeric(5, 2), nullable=False)
    NationalAvgRate = db.Column(db.Numeric(5, 2), nullable=False)

    category = db.relationship('IndicatorCategory')
