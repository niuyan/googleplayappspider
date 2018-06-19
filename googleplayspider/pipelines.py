# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sqlite3
import logging

fileName = 'googleplay.json'
db = 'googleplay.db'

class GoogleplayspiderPipeline(object):
    def __init__(self):
        # json
        with open(fileName, 'w') as f:
            f.write('[\n')

    def open_spider(self, spider):
        # sqlite
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.con.text_factory = str
        self.cur.execute('DROP TABLE IF EXISTS googleplay')

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS" + " googleplay(Name VARCHAR(50), Icon VARCHAR(1000), Link VARCHAR(100), "+
            "Last_updated VARCHAR(50),Author VARCHAR(30),  Installs VARCHAR(50),"+
            "Version VARCHAR(30),  OS VARCHAR(50), Content_rating VARCHAR(30),"+
            "Genre VARCHAR(50), "+
            "Price VARCHAR(30), Review_rating VARCHAR(20), Review_number VARCHAR(30), "+
            "Description VARCHAR(50000), Developer VARCHAR(100), "+
            "Offeredby VARCHAR(50))"
        )



    def close_spider(self, spider):
        # sqlite
        self.con.commit()
        self.con.close()

        # json
        with open(fileName, 'r') as f:
            content = f.read()
        with open(fileName, 'w') as f:
            f.write(content[:-1] + "\n]")

    def process_item(self, item, spider):
        # sqlite
        if str(item['Link']).find('details?id') != - 1:
            col = ','.join(item.keys())
            placeholders = ','.join(len(item) * '?')
            print('insert new value:'+item['Link'])
            sql = 'INSERT INTO googleplay({}) values({})'
            logging.debug(sql.format(col, placeholders))
            logging.debug(list(item.values()))
            self.cur.execute(sql.format(col, placeholders), list(item.values()))

            # json
            line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ','
            with open(fileName, 'a') as f:
                f.write(line)
        return item
