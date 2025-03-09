import sqlite3
import os
import re
from datetime import datetime
from scrapy.exceptions import DropItem

from projectscrapy.spiders.noviny import NovinySpider
from projectscrapy.spiders.ukf import UkfSpider
from projectscrapy.spiders.blog_sme import BlogSmeSpider
from projectscrapy.spiders.blog_pravda import BlogPravdaSpider
from projectscrapy.spiders.vedanadosah import VedanadosahSpider
from projectscrapy.spiders.wikipediask import WikipediaskSpider


class SqlitePipeline:

    def __init__(self):
        main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(main_dir, 'data', 'demo.db')
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS novinysk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS ukfsk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS blogsmesk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS blogpravdask (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS vedanadosahsk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS wikipediask (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS generalspider (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                preprocessed_content TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        ''')

    def process_item(self, item, spider):
        try:
            if 'url' not in item or not item['url']:
                spider.logger.warning('Item doesnt have URL')
                return item

            if isinstance(spider, NovinySpider):
                table_name = 'novinysk'
            elif isinstance(spider, UkfSpider):
                table_name = 'ukfsk'
            elif isinstance(spider, BlogSmeSpider):
                table_name = 'blogsmesk'
            elif isinstance(spider, BlogPravdaSpider):
                table_name = 'blogpravdask'
            elif isinstance(spider, VedanadosahSpider):
                table_name = 'vedanadosahsk'
            elif isinstance(spider, WikipediaskSpider):
                table_name = 'wikipediask'
            else:
                table_name = 'generalspider'

            self.cur.execute(f'SELECT * FROM {table_name} WHERE url = ?', (item['url'],))
            result = self.cur.fetchone()

            if result:
                spider.logger.warning(f'Item exists already in {table_name}: {item['title']}')
            else:
                self.cur.execute(f'''
                    INSERT INTO {table_name} (title, content, preprocessed_content, url, scraped_at) VALUES (?, ?, ?, ?, ?)
                ''', (
                    item['title'],
                    item['content'],
                    item['preprocessed_content'],
                    item['url'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
                self.con.commit()
                spider.logger.info(f'Item saved to {table_name}: {item['title']}')

        except sqlite3.Error as e:
            spider.logger.error(f'SQLite error: {e}')
        return item


class CleanTextPipeline:

    def process_item(self, item, spider):
        if not item.get('title') or item['title'].strip() == '':
            item['title'] = 'Bez názvu'
        if not item.get('content') or item['content'].strip() == '':
            raise DropItem(f'No content inside {item['url']}.')
        item['title'] = re.sub(r'\s+', ' ', item['title']).strip()
        item['content'] = re.sub(r'[\u200b\uFEFF]', '', item['content'])
        item['content'] = re.sub(r'\s+', ' ', item['content']).strip()
        if isinstance(spider, NovinySpider):
            if 'content' in item:
                item['content'] = item['content'].replace(
                    'Vďaka financiám z reklamy prinášame kvalitné a objektívne informácie. '
                    'Povoľte si prosím zobrazovanie reklamy na našom webe. '
                    'Ďakujeme, že podporujete kvalitnú žurnalistiku. ', ''
                )
        if isinstance(spider, WikipediaskSpider):
            if 'content' in item:
                item['content'] = re.sub(r'\[\d+]', '', item['content'])
        return item


class PreprocessingPipeline:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        stopwords_path = os.path.join(base_dir, 'stopwords', 'slovak_stopwords.txt')

        with open(stopwords_path, 'r', encoding='utf-8') as file:
            self.slovak_stopwords = file.read().splitlines()

    def process_item(self, item, spider):
        original_content = item['content']
        item['preprocessed_content'] = self.preprocess_text(original_content)
        return item

    def preprocess_text(self, text):
        text = re.sub(r'http[s]?://\S+', ' ', text)
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text_tokens = text.split()
        text_tokens = [word for word in text_tokens if word not in self.slovak_stopwords]
        clean_content = ' '.join(text_tokens)
        return clean_content
