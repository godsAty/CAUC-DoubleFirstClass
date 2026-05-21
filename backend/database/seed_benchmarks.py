# ============================================================
# 双一流高校全国均值 & 目标值 基准数据脚本
# 数据来源：教育部统计公报、各校教学质量报告、NSFC/青塔/软科等
# 执行方式：python database\seed_benchmarks.py
# ============================================================
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BENCHMARKS = {
    # === 人才培养 ===
    # 对标基准：行业特色型高校B层常模（参照校：南航、南理工、河海、矿大、江大等）
    'RC-01': {
        'name': '国家级一流本科专业建设点',
        'target': 15,
        'nationalAvg': 22.0,
        'source': '教育部"双万计划"全量汇总(144所双一流共5300+个)/行业特色校中位数约22个',
    },
    'RC-02': {
        'name': '国家级一流课程',
        'target': 12,
        'nationalAvg': 25.0,
        'source': '前两批10866门认定/南航48门、南理工46门、矿大40门、江大33门/B层中位数约25门',
    },
    'RC-03': {
        'name': '国家级教学成果奖',
        'target': 4,
        'nationalAvg': 4.5,
        'source': '教育部2022年国家级教学成果奖1998项公示/B层校均3-4项',
    },
    'RC-04': {
        'name': '研究生在校生规模',
        'target': 6000,
        'nationalAvg': 7000,
        'source': '各校研究生院公开数据/行业特色校5000-8000人',
    },
    'RC-05': {
        'name': '本科毕业生就业率',
        'target': 95,
        'nationalAvg': 93.0,
        'source': '各校2023-2024学年本科教学质量报告(30+所已公布)',
    },
    'RC-06': {
        'name': '学生竞赛国家级以上获奖',
        'target': 100,
        'nationalAvg': 120,
        'source': '各校教务处年度竞赛统计',
    },
    'RC-07': {
        'name': '博士学位授权点数量',
        'target': 4,
        'nationalAvg': 7.0,
        'source': '教育部学位授权审核公示/南航17个、南理工20个、江大10个/B层中位数约7个',
    },

    # === 师资队伍 ===
    'FC-01': {
        'name': '专任教师总数',
        'target': 2000,
        'nationalAvg': 2000,
        'source': '各校2023-2024学年本科教学质量报告 / 行业特色高校常模',
    },
    'FC-02': {
        'name': '博士学位教师占比',
        'target': 75,
        'nationalAvg': 78.0,
        'source': '麦可思研究147所双一流全样本统计(精确值82.8%)/行业特色工程应用型高校常模约78%',
    },
    'FC-03': {
        'name': '国家级高层次人才数',
        'target': 15,
        'nationalAvg': 20.0,
        'source': '青塔2024学科人才统计/南航~25人、矿大~15人、江大~18人/B层中位数约20人',
    },
    'FC-04': {
        'name': '国家级教学团队',
        'target': 3,
        'nationalAvg': 5.0,
        'source': '教育部教学团队认定公示/机务维修团队(全国工人先锋号)+空管仿真团队',
    },
    'FC-05': {
        'name': '生师比',
        'target': 17,
        'nationalAvg': 17.1,
        'source': '教育部2024年全国教育事业发展统计公报（精确值：17.14:1）',
    },

    # === 科研成果 ===
    'SR-01': {
        'name': '国家级科研平台',
        'target': 5,
        'nationalAvg': 5.0,
        'source': '科技部/发改委平台认定公示 / 行业特色高校常模（中航大已达标）',
    },
    'SR-02': {
        'name': '国家重点研发计划项目',
        'target': 10,
        'nationalAvg': 12.0,
        'source': '科技部公示 / 行业特色高校常模（非基础研究型大学）',
    },
    'SR-03': {
        'name': '国家自然科学基金项目',
        'target': 40,
        'nationalAvg': 50.0,
        'source': 'NSFC 2024年度统计 / 行业特色理工高校常模（工程应用导向）',
    },
    'SR-04': {
        'name': 'SCI/SSCI高水平论文',
        'target': 500,
        'nationalAvg': 700.0,
        'source': 'WoS数据库 / 行业特色高校常模（工程应用导向，SCI非唯一评价维度）',
    },
    'SR-05': {
        'name': '年度科研经费',
        'target': 3.5,
        'nationalAvg': 3.5,
        'source': '各校2024年公开决算数据 / 行业特色高校常模（非百亿级预算高校）',
    },
    'SR-06': {
        'name': '国家级科技奖励',
        'target': 1,
        'nationalAvg': 1.0,
        'source': '国家科学技术奖励办公室 / 行业特色高校常模（牵头获奖难度极高）',
    },

    # === 社会服务 ===
    'SS-01': {
        'name': '科技成果转化金额',
        'target': 3000,
        'nationalAvg': 3500,
        'source': '各校科技成果转化年度报告/行业特色高校常模（学科领域窄）',
    },
    'SS-02': {
        'name': '发明专利授权数',
        'target': 200,
        'nationalAvg': 250,
        'source': '国家知识产权局年报/行业特色理工高校常模',
    },
    'SS-03': {
        'name': '省部级及以上智库成果',
        'target': 10,
        'nationalAvg': 15,
        'source': '各校社科处/科技处统计/5个民航局重点实验室+1个天津市智库/行业特色高校常模',
    },

    # === 国际化 ===
    'INT-01': {
        'name': '国际合作联合实验室',
        'target': 1,
        'nationalAvg': 2.0,
        'source': '科技部国际合作司认定名单/中航大可持续航空燃料平台(国内首个中欧合作)已达标',
    },
    'INT-02': {
        'name': '具有海外经历教师比例',
        'target': 40,
        'nationalAvg': 40.0,
        'source': '各校国际交流处年报/行业特色高校常模（航空类以国内工程背景为主）',
    },
    'INT-03': {
        'name': '来华留学生规模',
        'target': 400,
        'nationalAvg': 600,
        'source': '教育部来华留学统计/行业特色高校常模（非综合性大学，留学生吸引力有限）',
    },
}


def print_benchmarks():
    """打印所有基准数据"""
    print(f'\n{"="*80}')
    print('  双一流建设检测指标 - 基准数据总览')
    print(f'{"="*80}')
    print(f'{"编号":<8} {"指标名称":<24} {"目标值":>8} {"全国均值":>10}  数据来源')
    print('-'*80)

    for code, info in BENCHMARKS.items():
        print(f'{code:<8} {info["name"]:<24} {info["target"]:>8} {info["nationalAvg"]:>10}   {info["source"][:50]}')

    print('-'*80)
    print(f'共 {len(BENCHMARKS)} 项指标\n')


def update_database():
    """将基准数据写入 SQL Server"""
    from database.models import db, IndicatorMaster
    from app import create_app

    app = create_app()
    with app.app_context():
        updated = 0
        for code, info in BENCHMARKS.items():
            ind = IndicatorMaster.query.filter_by(IndicatorCode=code).first()
            if ind:
                ind.TargetValue = info['target']
                ind.NationalAvg = info['nationalAvg']
                ind.DataSource = info['source']
                updated += 1

        db.session.commit()
        print(f'数据库已更新: {updated}/{len(BENCHMARKS)} 项指标的基准数据')


if __name__ == '__main__':
    print_benchmarks()

    # 尝试更新数据库
    try:
        update_database()
    except Exception as e:
        print(f'\n[提示] 数据库未连接，基准数据已打印在上方。')
        print(f'  手动执行 SQL: sqlcmd -S localhost -E -i database\\update_benchmarks.sql')
        print(f'  或启动 Flask 后再运行此脚本: python database\\seed_benchmarks.py')
