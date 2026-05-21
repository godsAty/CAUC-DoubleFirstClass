# 中国民航大学双一流建设完成度实时报告系统 - 配置文件

# SQL Server 连接配置
DB_SERVER = 'localhost'
DB_NAME = 'CAUC_DoubleFirstClass'
DB_DRIVER = 'ODBC Driver 17 for SQL Server'

# 构建连接字符串 (Windows 集成认证)
def get_db_uri():
    return (
        f'mssql+pyodbc://@{DB_SERVER}/{DB_NAME}'
        f'?driver={DB_DRIVER.replace(" ", "+")}'
        f'&Trusted_Connection=yes'
        f'&TrustServerCertificate=yes'
    )

# 备用: SQL Server 用户名密码认证
DB_USERNAME = 'sa'
DB_PASSWORD = '123456'
def get_db_uri():
     return (
         f'mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
         f'?driver={DB_DRIVER.replace(" ", "+")}'
         f'&TrustServerCertificate=yes'
     )

# Flask 配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# 爬虫配置
CRAWL_INTERVAL_MINUTES = 360  # 默认6小时爬一次
REQUEST_TIMEOUT = 15
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 中航大官网爬取目标
CAUC_BASE_URL = 'https://www.cauc.edu.cn'
CAUC_URLS = {
    'school_intro': '/xxgk/xxjj.htm',
    'news': '/xwzx.htm',
    'info_disclosure': '/xxgk.htm',
}
