# 抓取网易云音乐播放量大于 500 万的歌单

from selenium import webdriver
import csv
from selenium.webdriver.chrome.options import Options

url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

csv_file = open('playlist.csv', 'w', encoding='gb18030')
writer = csv.writer(csv_file)
writer.writerow(['标题', '播放量', '链接'])


while url != 'javascript:void(0)':
    print(url)

    driver.get(url)

    driver.switch_to.frame('contentFrame')

    data = driver.find_element_by_id('m-pl-container').\
        find_elements_by_tag_name('li')

    for i in range(len(data)):
        nb = data[i].find_element_by_class_name('nb').text
        if '万' in nb and int(nb.split('万')[0]) > 500:
            msk = data[i].find_element_by_css_selector('a.msk')

            print([msk.get_attribute('title'), nb, msk.get_attribute('href')])
            writer.writerow([msk.get_attribute('title'),
                             nb, msk.get_attribute('href')])

    url = driver.find_element_by_css_selector('a.zbtn.znxt').\
        get_attribute('href')

print('complete work!!!')
csv_file.close()
