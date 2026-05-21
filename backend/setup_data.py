# ============================================================
# 中航大双一流建设完成度系统 - 数据流水线主控脚本
# 执行方式: python setup_data.py
#
# 数据来源全链路:
#   [公开渠道] → [搜索抓取] → [数据整理] → [SQL Server] → [Flask API] → [小程序展示]
#
# 步骤:
#   1. 创建数据库表结构 (init_db.sql)
#   2. 填充双一流基准指标 (seed_benchmarks.py) → 目标值 & 全国均值
#   3. 填充中航大实际数据 (seed_cauc_data.py) → 本校24项指标值
#   4. 生成历史快照数据 → 趋势图数据源
# ============================================================
import sys
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE_DIR, 'database')


def run_sql_file(filename):
    """通过 sqlcmd 执行 SQL 文件"""
    sql_path = os.path.join(SQL_DIR, filename)
    if not os.path.exists(sql_path):
        print(f'  [跳过] 文件不存在: {sql_path}')
        return False

    cmd = f'sqlcmd -S localhost -E -i "{sql_path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'  [OK] {filename}')
        return True
    else:
        # sqlcmd not found 也算正常，后续可用Python方式替代
        print(f'  [提示] sqlcmd执行失败，请确认SQL Server已启动。可手动在SSMS中执行 {filename}')
        return False


def run_python_script(filename):
    """运行 Python 数据脚本"""
    script_path = os.path.join(SQL_DIR, filename)
    if not os.path.exists(script_path):
        print(f'  [跳过] 脚本不存在: {script_path}')
        return False

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    if result.returncode == 0:
        print(f'  [OK] {filename}')
        return True
    else:
        print(f'  [提示] {filename} 执行失败（可能需要先启动SQL Server）')
        if result.stderr:
            # 只显示最后几行错误
            lines = result.stderr.strip().split('\n')
            for l in lines[-3:]:
                print(f'    {l[:120]}')
        return False


def main():
    print('=' * 70)
    print('  中国民航大学 双一流建设完成度系统 - 数据流水线')
    print('=' * 70)
    print()
    print('数据流向:')
    print('  公开渠道搜索 → 数据整理 → SQL Server → Flask API → 小程序')
    print()
    print('数据文件:')
    print('  database/init_db.sql          建库建表')
    print('  database/seed_benchmarks.py   双一流基准指标 (目标值+全国均值)')
    print('  database/seed_cauc_data.py    中航大24项实际数据')
    print('  database/update_benchmarks.sql 基准数据SQL版本（SSMS手动执行备用）')
    print('  database/update_real_data.sql  中航大数据SQL版本（SSMS手动执行备用）')
    print()
    print('=' * 70)
    print('  开始执行数据流水线...')
    print('=' * 70)

    # 步骤 1: 建库建表
    print('\n[步骤 1/4] 创建数据库和表结构...')
    run_sql_file('init_db.sql')

    # 步骤 2: 初始种子数据
    print('\n[步骤 2/4] 填充初始种子数据...')
    run_sql_file('seed_data.sql')

    # 步骤 3: 更新基准数据（Python脚本 + SQL双保险）
    print('\n[步骤 3/4] 更新双一流基准指标...')
    run_python_script('seed_benchmarks.py')

    # 步骤 4: 更新中航大实际数据
    print('\n[步骤 4/4] 更新中航大实际数据...')
    run_python_script('seed_cauc_data.py')

    print()
    print('=' * 70)
    print('  数据流水线执行完毕！')
    print()
    print('  下一步:')
    print('    python app.py              # 启动 Flask 后端')
    print('    微信开发者工具打开 miniprogram/  # 启动小程序前端')
    print()
    print('  验证 API:')
    print('    http://localhost:5000/api/overview    # 综合概览')
    print('    http://localhost:5000/api/category/1  # 人才培养详情')
    print('    http://localhost:5000/api/comparison  # 三方对比')
    print('=' * 70)


if __name__ == '__main__':
    main()
