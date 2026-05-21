# API - 分类指标详情
from database.models import IndicatorMaster, CAUCData


def get_category_detail(category_id):
    """获取某分类下所有指标的详情"""
    indicators = IndicatorMaster.query.filter_by(CategoryID=category_id)\
        .order_by(IndicatorMaster.IndicatorCode).all()

    result = []
    for ind in indicators:
        cauc = CAUCData.query.filter_by(IndicatorID=ind.IndicatorID)\
            .order_by(CAUCData.ScrapeTime.desc()).first()

        actual = float(cauc.ActualValue) if cauc else 0
        target = float(ind.TargetValue) if ind.TargetValue else 1
        national = float(ind.NationalAvg) if ind.NationalAvg else 0

        if ind.Direction == 'down':
            completion_rate = round(min(target / actual * 100, 100), 2) if actual > 0 else 0
            national_rate = round(min(national / actual * 100, 100), 2) if actual > 0 else 0
        else:
            completion_rate = round(min(actual / target * 100, 100), 2) if target > 0 else 0
            national_rate = round(min(national / target * 100, 100), 2) if target > 0 else 0

        gap_to_target = target - actual if ind.Direction == 'up' else actual - target
        gap_to_national = national - actual if ind.Direction == 'up' else actual - national

        result.append({
            'id': ind.IndicatorID,
            'code': ind.IndicatorCode,
            'name': ind.IndicatorName,
            'unit': ind.Unit,
            'weight': float(ind.Weight),
            'actual': actual,
            'target': target,
            'nationalAvg': national,
            'completionRate': completion_rate,
            'nationalRate': national_rate,
            'gapToTarget': round(gap_to_target, 2),
            'gapToNational': round(gap_to_national, 2),
            'direction': ind.Direction,
            'dataSource': ind.DataSource,
        })

    return result
