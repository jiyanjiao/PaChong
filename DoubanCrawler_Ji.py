from selenium import webdriver
import time

import bs4
import csv

"""定义全局变量"""

name = ""
rate = 0
info_link = ""
cover_link = ""

movielist = []

"""
实现函数,构造对应类型和地区的url地址
参数:
    category:类型
    location:地区
"""


def getMovieURl(category,location):

    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags={},{},{}'.format(
            '电影',category,location
        )
    return url



"""
电影类:应包含成员(电影名称,电影评分,电影类型,电影地区,电影页面链接,电影海报图片链接(同时,应该实现电影类的构造函数))
"""

def Movie(name, rate, location, category, info_link, cover_link):
    global movielist
    sublist = []
    for i in (name,rate,category,location,info_link,cover_link):
        sublist.append(i)
    movielist.append(sublist)
    print('movielist====',movielist)


"""
获得豆瓣电影信息
通过url返回的html,获取每一步电影名称,评分,海报图和页面链接写入到一个list,再讲所有的电影的的单个list写入到总的list里
"""


def findmovie(category,location):

    global name, rate, info_link, cover_link
    ulists = []

    url = getMovieURl(category,location)
    html = getHtml(url)
    soup = bs4.BeautifulSoup(html,"lxml")

    list_all = soup.find('div',attrs={'class':'list-wp'})
    for a in list_all.children:
        if isinstance(a,bs4.element.Tag):
            tds = a('span')
            img = a('img')
            href = a.get('href')
            ulists.append([tds[1].text,tds[2].text,href,img[0]['src']])
    #print('ulists==',ulists)
    for i in range(len(ulists)):
        ulist = ulists[i]
        name = ulist[0]
        rate = ulist[1]
        info_link = ulist[2]
        cover_link = ulist[3]
        Movie(name, rate, location, category, info_link, cover_link)


"""
    构造电影信息数据表
    从网页上选取任意三个电影类型,然后获得每个地区的电影信息,获取的一个包含三个类型,所有地区
        评分超过9分的完整电影对象的列表,将列表输出到文件'movies.csv'格式(名称,评分,地区,类型,连接)
"""


"""
统计电影数据
统计选取的每个电影类别中,数量排名前三的地区有哪些,分别占此类别电影总数的百分比
结果输出到文件'output.txt'
"""



"""
获取电影页面的HTML
getMovieURL返回url后,根据这个url获取页面的HTML
直接使用requests,对于大多数页面来说没有问题,但有些列表需要多页显示,需要不断点击**加载更多**按钮来显示
    这个列表上的全部电影,所以使用了selenium编写
参数:
    url:添加的类型和地区后的url
    loadmore:是否点击加载更多按钮
    waittime:等待初始化加载后的时间
"""


def getHtml(url,loadmore=False,waittime=5):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                next_buttton = browser.find_element_by_class_name("more")
                next_buttton.click()
                time.sleep(waittime)
            except Exception as e:
                break
    html = browser.page_source
    browser.quit()
    return html


"""读取csv文件"""


def readfile():
    with open('movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        movielist = list(reader)
        #count(movielist)


"""写入csv文件"""


def writecsv(mlist):
    csvfile = open('movies.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    for item in mlist:
        writer.writerow(item)
    csvfile.close()


if __name__ == '__main__':
    # url = r'https:\\www.baidu.com'
    # getHtml(url)
    #url = getMovieURl('传记','美国')
    #print(url)
    #html = getHtml(url)
    #print(html)
    #findmovie('剧情','香港')
    #readfile()
    #writecsv(movielist)
    # 全部地区
    loclist = [
        "中国大陆",
        "美国",
        "香港",
        "台湾",
        "日本",
        "韩国",
        "英国",
        "法国",
        "德国",
        "意大利",
        "西班牙",
        "印度",
        "泰国",
        "俄罗斯",
        "伊朗",
        "加拿大",
        "澳大利亚",
        "爱尔兰",
        "瑞典",
        "巴西",
        "丹麦"]
    catlist = ["剧情", "喜剧", "动作"]
    for loc in loclist:
        for cat in catlist:
            findmovie(cat, loc)
            writecsv(movielist)




