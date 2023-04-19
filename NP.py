# 小說狂人專用

# 導入模組
import requests as rq
from bs4 import BeautifulSoup
import re
import os
import codecs

while True:
    url = input('輸入網址(第零章)')
    res = rq.get(url)
    sp = BeautifulSoup(res.text, 'html.parser')

    # 提取小說書名與作者資訊
    content_page = sp.select('div.position a')[2]['href']
    content_url = 'https:'+content_page
    content_res = rq.get(content_url)
    content_sp = BeautifulSoup(content_res.text, 'html.parser')
    title = content_sp.select('span.title')[0].text
    author = content_sp.select('span.author')[0].text
    print(title + author)

    user_input = input('確認抓取此小說：y/n')
    # 使用者確認為y，開始抓取小說
    if user_input == 'y':
        # txt檔案前置動作
        f = codecs.open(title + '.txt', 'w', encoding='utf-8')
        f.write('%' + title + '\n' + '%' + author + '\n')
        break
    # 使用者確認為n，重新輸入網址
    elif user_input == 'n':
        continue
    else:
        print('請重新輸入')

# chapter_num = int(input('輸入總章節數'))
round = 0
while True:
    # 提取小說內文
    # chapter = soup.select('div.name')[0].text
    articals = sp.select('div.content')[0].text
    # f.write(chapter + '\n' + articals + '\n\n')
    f.write(articals + '\n\n')

    next_page = sp.select('ul.nav.chapter-nav a.next-chapter')
    if not next_page:
        break
    # 下一頁
    next_page_link = sp.select(
        'ul.nav.chapter-nav a.next-chapter')[0]['href']
    next_page_url = 'https:' + next_page_link
    url = next_page_url
    round += 1
    print(f'第 {round} 章已儲存')

    # if round == chapter_num:
    #    break

    res = rq.get(url)
    sp = BeautifulSoup(res.text, 'html.parser')

f.close()

# 轉成epub
cmd = 'pandoc.exe %s -o %s' % (title + '.txt', title+'.epub')
os.system(cmd)

print('convert over')
