from scrapy import cmdline

cmdline.execute("scrapy crawl news -a limit=50 -a minParagraph=10".split())