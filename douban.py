import requests
import random
from lxml import etree
import os
import sys

ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .\
            NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)', 
        ]

#临时函数 将获取的html文件保存到本地，避免重复请求
def saveHtml(isbn, html):

    filename = isbn + '.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


#通过douban.com/isbn/isbn号查询图书的详细信息地址
def getSubject(isbn):

    filename = isbn + '.html'
    url = "http://douban.com/isbn/{}".format(isbn)
    if os.path.exists(filename):
        file = open(filename, 'r', encoding='utf-8')
        html = file.read()
        file.close()
    else:
        html = requests.get(url=url, headers={'User-Agent': random.choice(ua_list)})
        html = html.content.decode('utf-8', 'ignore')
        saveHtml(isbn, html)

    parse_html = etree.HTML(html)

    #查询的数据有
    #书名、作者、出版社、副标题、译者、出版年、页数、定价、装帧、ISBN号、图书图片、评分、评论数、内容简介

    bookImg = parse_html.xpath('//*[@id="mainpic"]/a/img/@src')[0].strip()
    bookName = parse_html.xpath('//*[@id="wrapper"]/h1/span/text()')[0].strip()
    bookInfo = parse_html.xpath('//*[@id="info"]')
    bookAuthor = bookInfo[0].xpath('.//span[@class="pl" and text()=" 作者"]/following-sibling::a/text()')[0].strip()
    #译者
    bookTranslator = bookInfo[0].xpath('.//span[@class="pl" and text()=" 译者"]/following-sibling::a/text()')[0].strip()
    #出版社
    bookPublisher = bookInfo[0].xpath('.//span[@class="pl" and text()="出版社:"]/following-sibling::a/text()')[0].strip()
    #出版年份
    bookPublisherYear = bookInfo[0].xpath('.//span[@class="pl" and text()="出版年:"]/following-sibling::text()')[0].strip()
    #页数
    bookPage = bookInfo[0].xpath('.//span[@class="pl" and text()="页数:"]/following-sibling::text()')[0].strip()
    #定价
    bookPrice = bookInfo[0].xpath('.//span[@class="pl" and text()="定价:"]/following-sibling::text()')[0].strip()
    #装帧
    bookBind = bookInfo[0].xpath('.//span[@class="pl" and text()="装帧:"]/following-sibling::text()')[0].strip()
    bookISBN = bookInfo[0].xpath('.//span[@class="pl" and text()="ISBN:"]/following-sibling::text()')[0].strip()
    #评分
    bookScore =parse_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0].strip()
    #评分人数
    bookScorePepoleNum= parse_html.xpath('//div[@class="rating_sum"]/span/a/span/text()')[0].strip()
    #简介
    bookIntroduction = parse_html.xpath('//div[@class="intro"]/p/text()')
    print(bookImg, bookName, bookAuthor, bookPublisher, bookPublisherYear, bookTranslator, bookPage, bookPrice, bookBind, bookISBN, bookScore, bookScorePepoleNum, bookIntroduction)

if __name__ == '__main__':

    getSubject('9787536097261')
    # try:
    #     while True:
    #         isbn = input()
    #         getSubject(isbn)
    # except:
    #     pass
