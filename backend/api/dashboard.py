# API - 综合看板数据
from decimal import Decimal
from database.models import IndicatorCategory, IndicatorMaster, CAUCData


def get_overview():
    categories = IndicatorCategory.query.order_by(IndicatorCategory.SortOrder).all()
    category_data = []
    total_weighted_rate = Decimal('0')
    total_weight = Decimal('0')

    for cat in categories:
        indicators = IndicatorMaster.query.filter_by(CategoryID=cat.CategoryID).all()
        cat_completion_sum = Decimal('0')
        cat_weight_sum = Decimal('0')
        cat_national_sum = Decimal('0')
        indicator_list = []

        for ind in indicators:
            cauc = CAUCData.query.filter_by(IndicatorID=ind.IndicatorID)\
                .order_by(CAUCData.ScrapeTime.desc()).first()

            actual = float(cauc.ActualValue) if cauc else 0
            target = float(ind.TargetValue) if ind.TargetValue else 1
            national = float(ind.NationalAvg) if ind.NationalAvg else 0
            weight = float(ind.Weight) if ind.Weight else 0

            if ind.Direction == 'down':
                rate = (target / actual * 100) if actual > 0 else 0
                national_rate = (national / actual * 100) if actual > 0 else 0
            else:
                rate = (actual / target * 100) if target > 0 else 0
                national_rate = (national / target * 100) if target > 0 else 0

            rate = min(rate, 100)
            national_rate = min(national_rate, 100)

            cat_completion_sum += Decimal(str(rate * weight))
            cat_weight_sum += Decimal(str(weight))
            cat_national_sum += Decimal(str(national_rate * weight))

            indicator_list.append({
                'code': ind.IndicatorCode,
                'name': ind.IndicatorName,
                'actual': actual,
                'target': target,
                'nationalAvg': national,
                'unit': ind.Unit,
                'rate': round(rate, 1),
                'nationalRate': round(national_rate, 1),
            })

        cat_rate = float(cat_completion_sum / cat_weight_sum) if cat_weight_sum > 0 else 0
        cat_nat_rate = float(cat_national_sum / cat_weight_sum) if cat_weight_sum > 0 else 0

        category_data.append({
            'id': cat.CategoryID,
            'name': cat.CategoryName,
            'icon': cat.Icon,
            'rate': round(cat_rate, 1),
            'nationalRate': round(cat_nat_rate, 1),
            'indicators': indicator_list,
        })

        total_weighted_rate += cat_completion_sum
        total_weight += cat_weight_sum

    overall_rate = round(float(total_weighted_rate / total_weight), 1) if total_weight > 0 else 0

    latest = CAUCData.query.order_by(CAUCData.ScrapeTime.desc()).first()
    update_time = latest.ScrapeTime.strftime('%Y-%m-%d %H:%M') if latest else '暂无数据'

    return {
        'overallRate': overall_rate,
        'updateTime': update_time,
        'categories': category_data,
    }
