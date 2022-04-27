#_*_coding:utf8 _*_
from bs4 import BeautifulSoup        #网页解析，获取数据
import re         #正则表达式，进行文字匹配
import urllib.request,urllib.error   #制定url，获取网页数据
import xlwt       #进行excel操作



def main():
    baseurl="https://www.tianqi.com/province/guangdong"
    url="https://www.tianqi.com"
    areaname=getAreaName(baseurl)
    datalist = []
    num=0
    for i in areaname:
        data = getData(url+i)
        datalist.append(data)
        num+=1

    savepath = "广东省各县区天气.xls"
    # 3.保存数据
    saveData(datalist, savepath,num)








def askURL(url):
    head={     #模拟浏览器头部信息，向服务器发送消息
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 100.0.4896.127Safari / 537.36"
    }#用户代理，代表告诉豆瓣服务器我们是什么类型的机器，浏览器（本质上是告诉浏览器我们可以接收什么水平的文件内容）

    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        resonse=urllib.request.urlopen(request)
        html=resonse.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



findLink=re.compile(r'<span>(.*?)</span>',re.S)
def getAreaName(baseurl):   #获取广东省各县区的拼音
    html=askURL(baseurl)
    # print(html)
    # 2.解析数据
    soup = BeautifulSoup(html, "html.parser")
    CityArea=[]
    for item in soup.find_all('ul', class_="racitys"):
        item = str(item)
        # print(item)
        link=re.findall(findLink,item)
        for city in link:
            cityarea=re.compile(r'href="(.*?)"')
            area=re.findall(cityarea,city)
            for i in area:
                CityArea.append(i)
    return CityArea


findName=re.compile(r'<h1>(.*?)</h1>')
findTime=re.compile(r'<dd class="week">(.*)</dd>')
findTemperature=re.compile(r'<p class="now"><b>(.*)</b>')
findSpan=re.compile(r'<span><b>(.*)</b>')
findOther=re.compile(r'<dd class="shidu"><b>(.*)</b>')



def getData(url):
    # datalist = []
    html = askURL(url)  # 保存获取到的网页源码

    # 解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('dl', class_="weather_info"):
        data = []  #保存天气信息
        item = str(item)

        name=re.findall(findName,item)
        data.append(name)
        # print(name)

        time=re.findall(findTime,item)
        for i in time:
            i = re.sub('\s', ' ', str(i))
            data.append(i)
            # print(i)

        temperature=re.findall(findTemperature,item)
        data.append(temperature)
        # print(temperature)

        span=re.findall(findSpan,item)
        data.append(span)
        # print(span)

        other=re.findall(findOther,item)
        other=re.sub('</b><b>',' ',str(other))
        data.append(other)
        # print(other)
        print(data)
    return data


def saveData(datalist,savepath,num):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('广东省各县区天气', cell_overwrite_ok=True)  # 创建工作表
    col = ("区域", "日期", "温度", "天气情况", "其他")
    for i in range(0, 5):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, num):
        print("第%d条" % i)
        data = datalist[i]
        for j in range(0, 5):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)



if __name__=="__main__":
    main()
