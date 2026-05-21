# ============================================================
# 定时调度器 - 自动爬取 + 数据快照 + 完成度汇总
# ============================================================
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import config

scheduler = BackgroundScheduler()


def init_scheduler(app):
    """初始化全部定时任务"""

    # ---- 任务1：每日爬取中航大首页新闻 ----
    def daily_crawl():
        with app.app_context():
            print(f'[调度器 {datetime.now():%H:%M}] 爬取中航大新闻...')
            try:
                from crawler.cauc_spider import crawl_cauc_news
                news = crawl_cauc_news()
                print(f'[调度器] 获取 {len(news)} 条新闻')
            except Exception as e:
                print(f'[调度器] 爬取失败: {e}')

    scheduler.add_job(
        daily_crawl,
        'interval',
        hours=6,
        id='cauc_crawl',
        replace_existing=True,
    )

    # ---- 任务2：每月1日自动生成数据快照 ----
    def monthly_snapshot():
        with app.app_context():
            print(f'[调度器 {datetime.now():%H:%M}] 生成月度数据快照...')
            try:
                from services.update_service import full_update_cycle
                result = full_update_cycle()
                print(f'[调度器] 快照完成: {result["snapshot"]}')
                print(f'[调度器] 汇总完成: {result["summary"]}')
            except Exception as e:
                print(f'[调度器] 快照失败: {e}')

    scheduler.add_job(
        monthly_snapshot,
        'cron',
        day=1,
        hour=3,
        minute=17,
        id='monthly_snapshot',
        replace_existing=True,
    )

    # ---- 任务3：启动时立即执行一次快照（如果今天还没有） ----
    with app.app_context():
        try:
            from services.update_service import generate_snapshot, generate_completion_summary
            snap = generate_snapshot()
            if snap.get('status') == 'skip':
                print(f'[调度器] 今日快照已存在，跳过')
            else:
                print(f'[调度器] 初始快照: {snap}')
                generate_completion_summary()
        except Exception as e:
            print(f'[调度器] 初始快照跳过（数据库可能未就绪）: {e}')

    scheduler.start()
    print(f'[调度器] 已启动 | 新闻爬取:每6小时 | 月度快照:每月1日03:17')
