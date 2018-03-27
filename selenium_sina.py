from selenium import webdriver
import time
import requests
import gzip
from lxml import etree


class MySpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        self.file = open('sz_bx.txt', 'a+', encoding='utf-8')

    # 获取详细页内容
    def detail_content(self, url, title):
        try:
            response = requests.get(url, headers=self.headers, timeout=3)
        except Exception as e:
            print('详细页请求失败 原因：%s' % e)
            return

        try:
            content = gzip.decompress(response.content).decode('utf-8')
        except OSError:
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
            content = response.text
        html = etree.HTML(content)
        content = ''.join(
            html.xpath('//*[@id="artibody"]//p//text()|//div[@class="WB_text W_f14"]//text()|//*[@id="article"]//p//text()')).strip().replace('\n', '').replace('\t', '').replace('​​　　', '').replace('\r', '')
        keywords = html.xpath('//*[@id="keywords"]/a')
        temp_str = '关键字:'
        for i in keywords:
            temp_str = temp_str + i.xpath('./text()')[0] + ','

        if len(content) != 0 and len(temp_str[:-1]) > 4:
            self.file.write(title.strip() + '\t' + url.strip() + '\t' + content + '\t' + temp_str[:-1] + '\n')
        elif len(content) != 0 and len(keywords) <= 0:
            self.file.write(title.strip() + '\t' + url.strip() + '\t' + content + '\n')
        else:
            pass

    # 科技：抓首页看得到的如下 01 02等新闻以及热点板块下的新闻
    def science_urls(self, driver, number):
        title = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[1]/a/span').text
        url = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[1]/a').get_attribute('href')
        time.sleep(1)
        print(title, url)
        self.detail_content(url, title)

        driver.find_element_by_xpath('//*[@id="slider-dot"]/p[2]/span').click()
        title = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[2]/a/span').text
        url = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[2]/a').get_attribute('href')
        time.sleep(1)
        print(title, url)
        self.detail_content(url, title)

        driver.find_element_by_xpath('//*[@id="slider-dot"]/p[3]/span').click()
        title = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[3]/a/span').text
        url = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[3]/a').get_attribute('href')
        time.sleep(1)
        print(title, url)
        self.detail_content(url, title)

        # driver.find_element_by_xpath('//*[@id="slider-dot"]/p[4]/span').click()
        # title = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[4]/a/span').text
        # url = driver.find_element_by_xpath('//*[@id="tech-slider"]/div/div[1]/div[4]/a').get_attribute('href')
        # time.sleep(1)
        # print(title, url)
        # self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="tech_body"]/div[3]/div[2]/div[2]/ul/li/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        target2 = driver.find_element_by_xpath('//*[@id="tyfeed-card-tabs"]/li[1]')
        driver.execute_script("arguments[0].scrollIntoView();", target2)
        for i in range(number):
            time.sleep(1)
            num = 4 * (i + 1)
            try:
                target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[1]/div[%s]' % num)
                driver.execute_script("arguments[0].scrollIntoView();", target2)
            except Exception as e:
                print('等待5秒再次获取')
                time.sleep(10)
                try:
                    target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[1]/div[%s]' % num)
                    driver.execute_script("arguments[0].scrollIntoView();", target2)
                except Exception as e:
                    self.get_urls(driver, '//*[@id="j_cardlist"]/div[1]/div[contains(@class, "ty-card ty-card-type1 clearfix")]')
                    print('获取完成')
                    break

    # 新闻：http://news.sina.com.cn/
    def new_urls(self, driver):
        target = driver.find_element_by_xpath('//*[@id="wrap"]/div[6]/div[1]/div[2]/div/div/a')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        nodes = driver.find_elements_by_xpath('//*[@id="syncad_1"]/h1')
        for node in nodes:
            title = node.find_element_by_xpath('./a').text
            url = node.find_element_by_xpath('./a').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="syncad_1"]/p/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="ad_entry_b2"]/ul/li/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="blk_guandian_01"]/div/ul/li/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="blk_guandian_01"]/div/div[4]/div/div/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="blk_guandian_01"]/div/div[4]/div/div/div[2]')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('./a').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

    # 财经要闻
    def finance_urls(self, driver):
        nodes = driver.find_elements_by_xpath('//*[@id="blk_hdline_01"]/h3/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        nodes = driver.find_elements_by_xpath('//*[@id="blk_hdline_01"]/p/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

        target = driver.find_element_by_xpath('//*[@id="directAd_huaxia"]/div[2]/div[1]/div[1]/h2/a')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        nodes = driver.find_elements_by_xpath('//*[@id="fin_tabs0_c0"]/div[2]/ul/li/a')
        for node in nodes:
            title = node.find_element_by_xpath('.').text
            url = node.find_element_by_xpath('.').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

    # 获取详细页链接和标题
    def get_urls(self, driver, site):
        nodes = driver.find_elements_by_xpath(site)
        for node in nodes:
            title = node.find_element_by_xpath('./div[2]/h3/a').text
            url = node.find_element_by_xpath('./div[2]/h3/a').get_attribute('href')
            print(title, url)
            self.detail_content(url, title)

    # 控制向下翻页
    def detail_urls(self, number, driver, temp, temp1, site):
        time.sleep(10)
        if temp != 'none':
            try:
                driver.find_element_by_xpath(temp).click()
            except Exception as e:
                print(e)
                time.sleep(5)
                driver.find_element_by_xpath(temp).click()
        else:
            target = driver.find_element_by_xpath('//*[@id="ty-top-ent0"]/div[1]/h3/a')
            driver.execute_script("arguments[0].scrollIntoView();", target)

        for i in range(number):
            time.sleep(1)
            num = 4 * (i + 1)
            try:
                if temp1 == 'yes':
                    target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[1]/div[%s]' % num)
                    driver.execute_script("arguments[0].scrollIntoView();", target2)
                else:
                    target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[2]/div[%s]' % num)
                    driver.execute_script("arguments[0].scrollIntoView();", target2)
            except Exception as e:
                print(e, '等待5秒再次获取')
                time.sleep(5)
                try:
                    if temp1 == 'yes':
                        target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[1]/div[%s]' % num)
                        driver.execute_script("arguments[0].scrollIntoView();", target2)
                    else:
                        target2 = driver.find_element_by_xpath('//*[@id="j_cardlist"]/div[2]/div[%s]' % num)
                        driver.execute_script("arguments[0].scrollIntoView();", target2)
                except Exception as e:
                    self.get_urls(driver, site)
                    print('获取完成')
                    break

    # 科技：抓首页看得到的如下 01 02等新闻以及热点板块下的新闻
    def science_item(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        self.science_urls(driver, 1000)
        driver.close()

    # 新闻：http://news.sina.com.cn/
    def new_item(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        self.new_urls(driver)
        driver.close()

    # 财经要闻
    def finance_item(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        self.finance_urls(driver)
        driver.close()

    # 娱乐版块
    def recreation_item(self, url, num, site, kwd='none', control='none'):
        driver = webdriver.Chrome()
        driver.get(url)
        self.detail_urls(num, driver, temp=kwd, temp1=control, site=site)
        driver.close()

    def __del__(self):
        self.file.close()

    # 运行
    def run(self):
        # 娱乐版块(要闻)
        self.recreation_item('http://ent.sina.com.cn/', 1000, '//*[@id="j_cardlist"]/div[2]/div[contains(@class, "ty-card ty-card-type1 clearfix")]')
        # 娱乐版块(电影)
        self.recreation_item('http://ent.sina.com.cn/', 1000, '//*[@id="j_cardlist"]/div[2]/div[contains(@class, "ty-card ty-card-type1 clearfix")]', kwd='//*[@id="tyfeed-card-tabs"]/li[4]')
        # 娱乐版块(电视剧)
        self.recreation_item('http://ent.sina.com.cn/', 1000, '//*[@id="j_cardlist"]/div[2]/div[contains(@class, "ty-card ty-card-type1 clearfix")]', kwd='//*[@id="tyfeed-card-tabs"]/li[5]')
        # 娱乐版块(综艺)
        self.recreation_item('http://ent.sina.com.cn/', 1000, '//*[@id="j_cardlist"]/div[2]/div[contains(@class, "ty-card ty-card-type1 clearfix")]', kwd='//*[@id="tyfeed-card-tabs"]/li[6]')
        # 汽车要闻
        self.recreation_item('http://auto.sina.com.cn/', 1000, '//*[@id="j_cardlist"]/div[1]/div[contains(@class, "ty-card ty-card-type1 clearfix")]', kwd='//*[@id="tyfeed-card-tabs"]/li[1]', control='yes')
        # 新闻中心要闻
        self.new_item('http://news.sina.com.cn/')
        # 科技首页
        self.science_item('http://tech.sina.com.cn/')
        # 财经要闻
        self.finance_item('http://finance.sina.com.cn/')


if __name__ == '__main__':
    spider = MySpider()
    spider.run()