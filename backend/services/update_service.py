# ============================================================
# 数据更新服务 - 定时从爬虫结果更新数据库 + 生成历史快照
# ============================================================
from datetime import date, datetime
from decimal import Decimal
from database.models import db, IndicatorMaster, CAUCData, DataSnapshot, CompletionSummary


def generate_snapshot():
    """为所有指标生成当前快照（用于趋势图），每月自动执行"""
    today = date.today()
    # 检查今天是否已有快照
    existing = DataSnapshot.query.filter_by(SnapshotDate=today).first()
    if existing:
        return {'status': 'skip', 'msg': f'{today} 快照已存在'}

    indicators = IndicatorMaster.query.all()
    count = 0

    for ind in indicators:
        cauc = CAUCData.query.filter_by(IndicatorID=ind.IndicatorID)\
            .order_by(CAUCData.ScrapeTime.desc()).first()
        if not cauc:
            continue

        actual = float(cauc.ActualValue)
        target = float(ind.TargetValue) if ind.TargetValue and float(ind.TargetValue) > 0 else 1

        if ind.Direction == 'down':
            rate = min(round(target / actual * 100, 2), 100) if actual > 0 else 0
        else:
            rate = min(round(actual / target * 100, 2), 100) if target > 0 else 0

        snap = DataSnapshot(
            SnapshotDate=today,
            IndicatorID=ind.IndicatorID,
            Value=actual,
            CompletionRate=rate,
        )
        db.session.add(snap)
        count += 1

    db.session.commit()
    return {'status': 'ok', 'snapshots': count, 'date': str(today)}


def generate_completion_summary():
    """重新计算各维度完成度并保存"""
    today = date.today()
    categories = db.session.query(IndicatorMaster.CategoryID).distinct().all()

    for (cat_id,) in categories:
        indicators = IndicatorMaster.query.filter_by(CategoryID=cat_id).all()
        total_weighted = Decimal('0')
        total_weight = Decimal('0')
        total_nat_weighted = Decimal('0')

        for ind in indicators:
            cauc = CAUCData.query.filter_by(IndicatorID=ind.IndicatorID)\
                .order_by(CAUCData.ScrapeTime.desc()).first()
            if not cauc:
                continue

            actual = float(cauc.ActualValue)
            target = float(ind.TargetValue) if ind.TargetValue and float(ind.TargetValue) > 0 else 1
            national = float(ind.NationalAvg) if ind.NationalAvg and float(ind.NationalAvg) > 0 else 0
            weight = float(ind.Weight) if ind.Weight else 0

            if ind.Direction == 'down':
                rate = min(target / actual * 100, 100) if actual > 0 else 0
                nat_rate = min(national / actual * 100, 100) if actual > 0 else 0
            else:
                rate = min(actual / target * 100, 100) if target > 0 else 0
                nat_rate = min(national / target * 100, 100) if target > 0 else 0

            total_weighted += Decimal(str(rate * weight))
            total_weight += Decimal(str(weight))
            total_nat_weighted += Decimal(str(nat_rate * weight))

        cat_rate = float(total_weighted / total_weight) if total_weight > 0 else 0
        nat_rate = float(total_nat_weighted / total_weight) if total_weight > 0 else 0

        summary = CompletionSummary(
            ReportDate=today,
            CategoryID=cat_id,
            CompletionRate=round(cat_rate, 2),
            NationalAvgRate=round(nat_rate, 2),
        )
        db.session.add(summary)

    db.session.commit()
    return {'status': 'ok', 'categories': len(categories), 'date': str(today)}


def full_update_cycle():
    """执行完整的数据更新周期：快照 + 汇总"""
    result = {'snapshot': None, 'summary': None}

    try:
        result['snapshot'] = generate_snapshot()
    except Exception as e:
        result['snapshot'] = {'status': 'error', 'msg': str(e)}

    try:
        result['summary'] = generate_completion_summary()
    except Exception as e:
        result['summary'] = {'status': 'error', 'msg': str(e)}

    return result
