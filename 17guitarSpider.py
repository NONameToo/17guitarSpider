# coding:utf-8

# 此爬虫采用单线程的方式,速度相对比较慢,可以改为多线程的方式提高速度,有空我改改代码

import urllib.request as u2
from lxml import etree
import os
import re


class Spider_guitar(object):
    def __init__(self):
        self.url = "http://www.17jita.com/tab/index.php?page="
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
        self.page = 1
         

    def spider(self):
        """负责调度"""
        start = int(input('请输入起始页:'))
        stop = int(input('请输入结束页:'))
        for p in range(start, stop+1):
            self.page = p
            self.loadpage()
            print('当前爬取到:%d页'%self.page)



    def loadpage(self):
        # 构造完整的url
        url = self.url + str(self.page)

        # 构造请求对象
        request = u2.Request(url, headers=self.headers)

        # 发送请求
        response = u2.urlopen(request)
        html = response.read().decode('gbk')
        #print(html)
        self.dealpage(html)

    def dealpage(self, html):
        """解析吉他谱的名字和详细url"""
        # 把HTML转换成html dom模型
        content = etree.HTML(html)
        
        # 解析吉他谱的详细地址
        link_list = content.xpath("//dt/a/@href")

        for link in link_list:
            number = re.search(r"\d+",link)
            try:
                number = number.group()
                print(number)
            except Exception as e:
                print(e)
                continue
         
            # 处理链接地址：
            url = "http://www.17jita.com/tab/whole_"+number+".html"
            print(url)

            #构造请求对象
            request = u2.Request(url, headers=self.headers)

            # 发送请求
            response = u2.urlopen(request)
            html2  = response.read().decode('gbk')

            #print(html2)
            
            """解析吉他谱的图片地址"""
            # 把HTML转换成html dom模型
            content = etree.HTML(html2)
            
            # 解析吉他谱图片地址
            pic_list = content.xpath('//td[@id="article_contents"]//img/@src')
            #print(pic_list)
            # 解析名字
            pic_name = content.xpath('//h1')
            #print(pic_name)
            # 获取当前工作路径
            now_path = os.getcwd()
            # 判断目录是否已经存在
            #print(now_path+"/"+each.text)
            if len(pic_name) == 0:

                try:
                    # 处理链接地址：
                    url = "http://www.17jita.com/tab/img/"+number+".html" 
                    #print(url)

                    #构造请求对象
                    request = u2.Request(url, headers=self.headers)

                    # 发送请求
                    response = u2.urlopen(request)
                    html2  = response.read().decode('gbk')

                    #print(html2)
                    
                    """解析吉他谱的图片地址"""
                    # 把HTML转换成html dom模型
                    content = etree.HTML(html2)
                    # 解析吉他谱图片地址
                    pic_list = content.xpath('//td[@id="article_contents"]//img/@src')
                    #print(pic_list)
                    # 解析名字
                    pic_name = content.xpath('//h1')
                    #print(pic_name)

                except Exception  as e :
                    print(e)
                    continue

            file_name = pic_name[0].text
            #print(file_name)
            file_name = file_name.replace('/','&')
            print(file_name)
            have = os.path.exists(now_path+"/"+file_name)
            if not have:
                os.mkdir(now_path+"/"+file_name)
            i = 1 
            for pic in pic_list:
                #print(pic)
                try:
                
                    pic_request = u2.Request(pic, headers=self.headers)
                    # 发送请求
                    response = u2.urlopen(pic_request)

                except Exception as e:
                    print(e)
                    continue
                #读取数据
                pic_content = response.read()
                #print(pic_content)

                # 把图片保存到本地
                name = now_path+"/"+file_name+"/"+file_name + str(i)
                #print(pic_name)
                #print(pic_content)
                #print(pic_name)
                #print(name)
                with open(name, 'wb') as f:
                    f.write(pic_content)
                i += 1

if __name__ == "__main__":
   spider_guitar = Spider_guitar()
   spider_guitar.spider()




        


