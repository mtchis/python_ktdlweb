import os
import re
import scrapy
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

CATEGORIES = {}
CATEGORIES_COUNTER = {}
SELECT_CATEGORIES = {}

folder_Get = 'GET'

class News(scrapy.Spider):
    name = 'news'
    BASE_URL = None
    out_data_path = 'Out_Data'
    folder_path = None
    page_limit = None
    min_paragraph = 0
    saveEachFile = False
    start_urls = []
    category_selected = None
    saveEachFile = False

    # constructor
    def __init__(self, saveEachFile = True, minParagraph=0, limit=None,*args, **kwargs):
        super(News, self).__init__(*args, **kwargs)

        # Input URL
        url = self.input_url()
        if url == None: return
        self.parse_httpbin(url)

        # select category
        cat = self.get_categories()
        category = cat.replace('$','')
        cat_name = cat.split('$')[0]
        self.category_selected = cat_name

        self.min_paragraph = int(minParagraph)

        # check limit
        if limit != None:
            self.page_limit = int(limit)

        if (saveEachFile == True):
            # set config
            self.saveEachFile = True
            # check SAVE file
            if os.path.exists(self.out_data_path + '/' + self.folder_path + '/' + self.category_selected + '/' + (self.category_selected + '.txt')):
                os.remove(self.out_data_path + '/' + self.folder_path + '/' + self.category_selected + '/' + (self.category_selected + '.txt'))
            if os.path.exists(
                    self.out_data_path + '/' + self.folder_path + '/' + self.category_selected + '/' + (self.category_selected + '.json')):
                os.remove(self.out_data_path + '/' + self.folder_path + '/' + self.category_selected + '/' + (self.category_selected + '.json'))
            # make dir
            if not os.path.exists(self.out_data_path):
                os.mkdir(self.out_data_path)
            if not os.path.exists(self.out_data_path + '/' + self.folder_path):
                os.mkdir(self.out_data_path + '/' + self.folder_path)
            # make subdir
            if self.category_selected != None:
                path = self.out_data_path + '/' + self.folder_path + '/' + self.category_selected
                if self.category_selected in CATEGORIES and not os.path.exists(path):
                    os.mkdir(path)
            else:
                for CATEGORIE in CATEGORIES:
                    path = self.out_data_path + '/' + self.folder_path + '/' + CATEGORIE
                    if not os.path.exists(path):
                        os.makedirs(path)

        # make URL
        if category != None:
            self.start_urls = [self.BASE_URL + category]
        else:
            for CATEGORIE in CATEGORIES:
                self.start_urls.append(self.BASE_URL + CATEGORIE)

    # Input & check URL
    def input_url(self):
        regex_url = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        while True:
            URL = input('Nhập đường dẫn URL: ')
            if re.match(regex_url, URL) is not None:
                if requests.get(URL).status_code == 404:
                    print('=> Lỗi 404 - Not Found!!!')
                    continue
                elif requests.get(URL).status_code in (301, 302, 303, 307):
                    print('=> Lỗi 301, 302, 303, 307 - Redirects!!!')
                    continue

                # Get BASE_URL - DOMAIN_URL
                parsed_uri = urlparse(URL)
                baseURL = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                domain_baseURL = '{uri.netloc}'.format(uri=parsed_uri)
                self.BASE_URL = baseURL
                self.folder_path = domain_baseURL
                return URL
            else:
                print('=> URL vừa nhập không đúng!')
                k = input('Bạn có muốn Thoát? (y/n): ')[0]
                if k in ('y', 'Y'):
                    return None
                continue

    # Parse URL
    def parse_httpbin(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        req = requests.get(url, headers=headers)

        parsed_uri = urlparse(req.url)
        _url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        pattern_url = _url
        pattern = '\;|\:|\#|\(|\)|\?|^[/]\s*$|photo|video|media|youtube|rss'
        pattern_reject = 'event|dien-dan|blog-phong-vien'

        url_next_page = ['/trang-2.htm', '/trang-2.html', '-p2', '/p2', '/trang2.html']
        list_temp = []
        i = 0

        soup = BeautifulSoup(req.text, "html.parser")
        my_ul = soup.findAll('ul')
        for u in my_ul:
            my_a = u.findAll('a')
            for a in my_a:
                my_href = a.get('href')
                if re.search(pattern_url, my_href):
                    my_href = re.sub(pattern_url, '', my_href)
                if (len(my_href) < 30 and not re.search(pattern, my_href) and not re.search(pattern_reject, my_href)):
                    if my_href.count('/') == 1:
                        my_href = my_href.split('.')[0]
                        my_topic = re.sub('/', '', my_href)
                    elif my_href.count('/') > 1:
                        my_topic = my_href.split('/')[1]

                    if my_topic != '':
                        for u in url_next_page:
                            _getStt = requests.get(self.BASE_URL + my_topic + u).status_code
                            if _getStt != 404:
                                rq_url = requests.get(self.BASE_URL + my_topic + u).url
                                if rq_url != self.BASE_URL and my_topic not in CATEGORIES:
                                    list_temp.append(my_topic)
                                    list_temp = list(dict.fromkeys(list_temp))

                                    i = i + 1
                                    CATEGORIES[my_topic] = my_topic
                                    CATEGORIES_COUNTER[my_topic] = 0
                                    SELECT_CATEGORIES[i] = my_topic + '$' + u

                                    if not os.path.exists(folder_Get):
                                        os.mkdir(folder_Get)

                                    file_cat = open(folder_Get + '/' + "CATEGORIES.json", "w")
                                    json.dump(CATEGORIES, file_cat)
                                    file_cat.close()

                                    file_catC = open(folder_Get + '/' + "CATEGORIES_COUNTER.json", "w")
                                    json.dump(CATEGORIES_COUNTER, file_catC)
                                    file_catC.close()

                                    file_scat = open(folder_Get + '/' + "SELECT_CATEGORIES.json", "w")
                                    json.dump(SELECT_CATEGORIES, file_scat)
                                    file_scat.close()
                                    break
        print('==> Danh Sách TOPIC:', list_temp)

    # Start Requests
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_news)

    # Parse List News
    def parse_list_news(self, response):
        # Kiểm tra limit
        category = self.category_selected
        if (self.page_limit is not None) and (CATEGORIES_COUNTER[category] >= self.page_limit):
            return

        # Xử lý
        list_news = response.css('a::attr(href)').getall()
        pattern = '\;|\#|\(|\)|\?|\*'
        for news in list_news:
            if (len(news) > 30 and not re.search(pattern, news)):
                if (self.page_limit is not None) and (CATEGORIES_COUNTER[category] >= self.page_limit):
                    return

                abs_url = response.urljoin(news)
                yield scrapy.Request(abs_url, callback=self.parse_news)

        # Next Page - Đệ quy
        next_url = self.get_url_next_page(response.url)
        yield scrapy.Request(response.urljoin(next_url), callback=self.parse_list_news)

    # Parse & Extract News
    def parse_news(self, response):
        title = response.css('h1::text').extract_first()
        content = response.css('p::text').getall()
        category = self.category_selected

        if category not in CATEGORIES:
            return

        if (self.page_limit is not None) and (CATEGORIES_COUNTER[category] >= self.page_limit):
            return

        # Check minimum paragrah
        if len(content) < self.min_paragraph:
            return

        CATEGORIES_COUNTER[category] = CATEGORIES_COUNTER[category] + 1

        # Lọc kí tự đặc biệt
        title = re.sub("[\n\t\r]", '', str(title))
        title = re.sub('\s', ' ', title)
        title = title.strip()

        jsonData = {
            'category': category,
            'id' : CATEGORIES_COUNTER[category],
            'title': title,
            'link': response.url,
            'content': content,
        }

        with open(self.out_data_path + '/' + self.folder_path + '/' + category + '/' + (category + '.txt'), 'ab') as f:
            f.write(response.body)
        self.log('Saved file %s' % category + '.txt')

        with open(self.out_data_path + '/' + self.folder_path + '/' + category + '/' + (category + '.json'), "a", encoding='utf8') as fileOut:
            if CATEGORIES_COUNTER[category] == 1:
                fileOut.write('[\n')
                json.dump(jsonData, fileOut, ensure_ascii=False)
                fileOut.write(',\n')
            elif CATEGORIES_COUNTER[category] > 1 and CATEGORIES_COUNTER[category] < self.page_limit:
                json.dump(jsonData, fileOut, ensure_ascii=False)
                fileOut.write(',\n')
            elif CATEGORIES_COUNTER[category] == self.page_limit or scrapy.signals.spider_closed:
                json.dump(jsonData, fileOut, ensure_ascii=False)
                fileOut.write('\n]')

        yield jsonData

    # Select_categories
    def get_categories(self):
        print('--------------- TOPICS ---------------')
        for i in SELECT_CATEGORIES:
            a = SELECT_CATEGORIES.get(i).split('$')[0]
            print("%s - %s" % (i, a))
        x = input('(!) Vui lòng chọn chủ đề (1 - ' + str(i) + '): ')
        rs_category = SELECT_CATEGORIES[int(x)]
        category = SELECT_CATEGORIES[int(x)].split('$')[0]
        print('=> Chủ đề đã chọn:', category)
        return rs_category

    # Get Number Page in URL
    def get_number_page(self, url):
        items = re.findall('\d+', url)
        page = 1
        if len(items) == 1:
            page = items[0]
        return int(page)

    # Get URL next Page
    def get_url_next_page(self, url):
        num = self.get_number_page(url)
        num = num + 1
        _url = url.replace('2', str(num))
        return _url