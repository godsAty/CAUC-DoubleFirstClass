# API - 对比数据 (雷达图 + 柱状图)
from database.models import db, IndicatorCategory, IndicatorMaster, CAUCData, CompletionSummary


def get_comparison():
    """获取五大维度三方对比数据 + 综合完成度"""
    categories = IndicatorCategory.query.order_by(IndicatorCategory.SortOrder).all()

    radar_data = {
        'dimensions': [],
        'cauc': [],
        'nationalAvg': [],
        'target': [],
    }

    bar_data = {
        'indicators': [],
        'cauc': [],
        'target': [],
        'nationalAvg': [],
    }

    # 加权综合（与 dashboard 一致）
    total_weighted_rate = 0
    total_weighted_nat = 0
    total_weight = 0

    for cat in categories:
        radar_data['dimensions'].append(cat.CategoryName)

        indicators = IndicatorMaster.query.filter_by(CategoryID=cat.CategoryID).all()
        cat_rate_sum = 0
        cat_nat_sum = 0
        cat_weight_sum = 0

        for ind in indicators:
            cauc = CAUCData.query.filter_by(IndicatorID=ind.IndicatorID)\
                .order_by(CAUCData.ScrapeTime.desc()).first()

            actual = float(cauc.ActualValue) if cauc else 0
            target = float(ind.TargetValue) if ind.TargetValue else 1
            national = float(ind.NationalAvg) if ind.NationalAvg else 0
            weight = float(ind.Weight) if ind.Weight else 0

            if ind.Direction == 'down':
                rate = min(target / actual * 100, 100) if actual > 0 else 0
                nat_rate = min(national / actual * 100, 100) if actual > 0 else 0
            else:
                rate = min(actual / target * 100, 100) if target > 0 else 0
                nat_rate = min(national / target * 100, 100) if target > 0 else 0

            cat_rate_sum += rate * weight
            cat_nat_sum += nat_rate * weight
            cat_weight_sum += weight

            bar_data['indicators'].append(ind.IndicatorName)
            bar_data['cauc'].append(round(rate, 2))
            bar_data['target'].append(100)
            bar_data['nationalAvg'].append(round(nat_rate, 2))

        avg_rate = round(cat_rate_sum / cat_weight_sum, 2) if cat_weight_sum > 0 else 0
        avg_nat = round(cat_nat_sum / cat_weight_sum, 2) if cat_weight_sum > 0 else 0

        radar_data['cauc'].append(avg_rate)
        radar_data['nationalAvg'].append(avg_nat)
        radar_data['target'].append(100)

        total_weighted_rate += cat_rate_sum
        total_weighted_nat += cat_nat_sum
        total_weight += cat_weight_sum

    overall_cauc = round(total_weighted_rate / total_weight, 1) if total_weight > 0 else 0
    overall_nat = round(total_weighted_nat / total_weight, 1) if total_weight > 0 else 0

    return {
        'radar': radar_data,
        'bar': bar_data,
        'overallCauc': overall_cauc,
        'overallNational': overall_nat,
    }
