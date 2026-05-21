# 中国民航大学双一流建设完成度实时报告系统 - Flask 主入口
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
from database.models import db, IndicatorMaster, CAUCData, DataSnapshot


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'TrustServerCertificate': 'yes'}
    }
    app.config['JSON_AS_ASCII'] = False

    CORS(app)
    db.init_app(app)

    with app.app_context():
        try:
            db.engine.connect()
            print('[OK] SQL Server 连接成功')
        except Exception as e:
            print(f'[WARN] SQL Server 连接失败(将使用模拟数据): {e}')

    # ===== API 路由 =====

    @app.route('/api/overview')
    def api_overview():
        """综合概览"""
        try:
            from api.dashboard import get_overview
            return jsonify({'code': 200, 'data': get_overview()})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/category/<int:category_id>')
    def api_category(category_id):
        """分类指标详情"""
        try:
            from api.indicators import get_category_detail
            return jsonify({'code': 200, 'data': get_category_detail(category_id)})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/indicator/<int:indicator_id>')
    def api_indicator(indicator_id):
        """单项指标详情 + 历史趋势"""
        try:
            ind = IndicatorMaster.query.get(indicator_id)
            if not ind:
                return jsonify({'code': 404, 'msg': '指标不存在'}), 404

            cauc = CAUCData.query.filter_by(IndicatorID=indicator_id)\
                .order_by(CAUCData.ScrapeTime.desc()).first()
            snapshots = DataSnapshot.query.filter_by(IndicatorID=indicator_id)\
                .order_by(DataSnapshot.SnapshotDate.asc()).all()

            actual = float(cauc.ActualValue) if cauc else 0
            target = float(ind.TargetValue) if ind.TargetValue else 1
            national = float(ind.NationalAvg) if ind.NationalAvg else 0

            if ind.Direction == 'down':
                completion_rate = round(min(target / actual * 100, 100), 2) if actual > 0 else 0
                national_rate = round(min(national / actual * 100, 100), 2) if actual > 0 else 0
            else:
                completion_rate = round(min(actual / target * 100, 100), 2) if target > 0 else 0
                national_rate = round(min(national / target * 100, 100), 2) if target > 0 else 0

            trend = [{
                'date': s.SnapshotDate.strftime('%Y-%m-%d'),
                'value': float(s.Value),
                'rate': float(s.CompletionRate),
            } for s in snapshots]

            return jsonify({'code': 200, 'data': {
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
                'direction': ind.Direction,
                'trend': trend,
            }})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/comparison')
    def api_comparison():
        """三方对比数据"""
        try:
            from api.comparison import get_comparison
            return jsonify({'code': 200, 'data': get_comparison()})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/trend/<int:indicator_id>')
    def api_trend(indicator_id):
        """某指标历史趋势"""
        try:
            snapshots = DataSnapshot.query.filter_by(IndicatorID=indicator_id)\
                .order_by(DataSnapshot.SnapshotDate.asc()).all()
            data = [{
                'date': s.SnapshotDate.strftime('%Y-%m-%d'),
                'value': float(s.Value),
                'rate': float(s.CompletionRate),
            } for s in snapshots]
            return jsonify({'code': 200, 'data': data})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/manual-update', methods=['POST'])
    def api_manual_update():
        """手动更新指标数据"""
        try:
            payload = request.get_json()
            indicator_id = payload.get('indicator_id')
            value = payload.get('value')
            year = payload.get('year', 2024)

            new_data = CAUCData(
                IndicatorID=indicator_id,
                ActualValue=value,
                DataYear=year,
                IsManual=True,
            )
            db.session.add(new_data)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '数据更新成功'})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    @app.route('/api/snapshot', methods=['POST'])
    def api_snapshot():
        """手动触发数据快照 + 完成度汇总（管理员操作）"""
        try:
            from services.update_service import full_update_cycle
            result = full_update_cycle()
            return jsonify({'code': 200, 'data': result})
        except Exception as e:
            return jsonify({'code': 500, 'msg': str(e)}), 500

    # ===== 首页路由 =====
    @app.route('/')
    def index():
        return jsonify({
            'name': '中国民航大学双一流建设完成度实时报告系统',
            'version': '1.0.0',
            'endpoints': [
                'GET /api/overview',
                'GET /api/category/<id>',
                'GET /api/indicator/<id>',
                'GET /api/comparison',
                'GET /api/trend/<indicator_id>',
                'POST /api/manual-update',
                'POST /api/snapshot  (触发快照)',
            ],
        })

    return app


if __name__ == '__main__':
    app = create_app()
    # 启动定时调度器（新闻爬取:每6小时 | 月度快照:每月1日）
    from crawler.scheduler import init_scheduler
    init_scheduler(app)
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
