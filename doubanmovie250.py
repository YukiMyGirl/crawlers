import requests
from bs4 import BeautifulSoup
import sys

headers = {
    "User-Agent": "Mozilla / 5.0(Macintosh;Intel Mac OS X 10_15_2) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 79.0.3945.117 Safari / 537.36",
}
class downloader:
    def __init__(self):
        self.server = "https://movie.douban.com/top250?start="
        self.urls = []

    def get_movies_urls(self):
        print("开始获取列表...")
        for count in range(0, 250, 25):
            url = self.server + str(count)
            html = requests.get(url, headers=headers).text
            bs = BeautifulSoup(html, "html.parser")
            ol = bs.ol
            items = ol.find_all('div', class_="item")
            for each in items:
                pic = each.find('div', class_="pic").find("a")
                self.urls.append(pic['href'])
        print("获取列表成功")
    def download_detail(self):
        print("开始下载电影详情...")
        for i in range(250):
            html = requests.get(self.urls[i],headers=headers).text
            bf = BeautifulSoup(html, "html.parser")
            name = bf.find('span', property='v:itemreviewed')
            info = bf.find('div', id="info")
            score = bf.find("strong", property="v:average")
            summary = bf.find('span', property='v:summary')

            with open("豆瓣电影top250","a+") as f:
                f.write(name.string+info.get_text()+score.string+summary.get_text().replace(" ", "")+"\n\n")
            sys.stdout.write('\r'+"下载进度：%.2f%%" % float((i + 1) / 250 * 100))
            sys.stdout.flush()
        print("下载完成")

if __name__ == "__main__":
    dl = downloader()
    dl.get_movies_urls()
    dl.download_detail()

