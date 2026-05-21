# 中航大官网爬虫 - 抓取学校公开数据
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import config


def fetch_page(url, timeout=None):
    """通用页面抓取"""
    timeout = timeout or config.REQUEST_TIMEOUT
    try:
        resp = requests.get(url, headers=config.REQUEST_HEADERS, timeout=timeout)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        if resp.status_code == 200:
            return resp.text
        return None
    except Exception as e:
        print(f'[爬虫] 请求失败: {url} - {e}')
        return None


def parse_news_list(html):
    """解析新闻列表，提取标题和链接"""
    soup = BeautifulSoup(html, 'lxml')
    news_items = []

    # 尝试多种常见选择器匹配新闻列表
    selectors = [
        '.news-list li a',
        '.list-news li a',
        '.article-list li a',
        '.xinwen-list li a',
        'a[href*="info"]',
    ]

    for selector in selectors:
        items = soup.select(selector)
        if items:
            for item in items[:20]:
                title = item.get_text(strip=True)
                href = item.get('href', '')
                if title and href:
                    if not href.startswith('http'):
                        href = config.CAUC_BASE_URL + href if href.startswith('/') else config.CAUC_BASE_URL + '/' + href
                    news_items.append({'title': title, 'url': href})
            break

    return news_items


def crawl_cauc_news():
    """爬取中航大首页新闻"""
    url = config.CAUC_BASE_URL + config.CAUC_URLS['news']
    html = fetch_page(url)
    if not html:
        return []

    news = parse_news_list(html)

    result = []
    for item in news[:10]:
        detail_html = fetch_page(item['url'])
        if detail_html:
            soup = BeautifulSoup(detail_html, 'lxml')
            content = soup.select_one('.article-content, .content, .v_news_content, .entry-content')
            text = content.get_text(strip=True)[:500] if content else ''
            result.append({
                'title': item['title'],
                'url': item['url'],
                'summary': text[:200],
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })

    return result


def crawl_school_intro():
    """抓取学校简介页面-提取关键数字"""
    url = config.CAUC_BASE_URL + config.CAUC_URLS['school_intro']
    html = fetch_page(url)
    if not html:
        return {}

    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text()

    # 提取关键数据(基于正则或者关键字)
    info = {
        'url': url,
        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'raw_text': text[:1000],
    }
    return info


if __name__ == '__main__':
    print('=== 测试爬虫 ===')
    news = crawl_cauc_news()
    print(f'获取到 {len(news)} 条新闻')
    for n in news[:3]:
        print(f'  - {n["title"]}')
