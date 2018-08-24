# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 16:20
# @Author  : 陈子昂

import time

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import save_img, img_name_processor


# 图虫创意分有：共享图库（免费），优选图库，高端图库
# 共享图库就是不停下拉，最底下会有“都被你看光了”一行字。
# 优选图库和高端图库是分页

def tuchong(keyword: str, pages=20):
    """本函数用于爬优选图库和高端图库"""
    img_cnt = 0

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('D:/chromedriver', chrome_options=chrome_options)
    driver.maximize_window()
    for page in range(pages):
        urls = [f'https://stock.tuchong.com/search?term={keyword}&type=2&page={page}&platform=creativevip',
                f'https://stock.tuchong.com/search?term={keyword}&type=2&page={page}']
        for url in urls:
            print(url)
            driver.get(url)
            time.sleep(2)
            for px in range(0, 5000, 100):
                js = f"var q=document.documentElement.scrollTop={px}"
                driver.execute_script(js)
            time.sleep(2)
            items = driver.find_elements_by_class_name('row-item')

            for item in items:
                src = item.find_element_by_xpath('./img').get_attribute('src')
                if not src:
                    continue
                filename = img_name_processor(src)
                path = rf'D://人脸相关的图片//图虫//{keyword}'
                if not os.path.exists(path):
                    os.makedirs(path)
                file = os.path.join(path, filename)
                rt = save_img(file=file, src=src)
                img_cnt += 1
                if rt:
                    print(f'第{img_cnt}张[{keyword}]图片保存成功...')
                else:
                    print(f'第{img_cnt}张[{keyword}]图片保存失败...')
    driver.close()


def tuchongfree(keyword: str):
    """本函数用于爬共享图库"""
    img_cnt = 0
    # chrome_options = Options()
    driver=webdriver.Ie('D:/IEDriverServer.exe')
    # driver = webdriver.Chrome('D:/IEDriverServer.exe', chrome_options=chrome_options)
    driver.maximize_window()
    url = f'https://stock.tuchong.com/free/search/?term={keyword}'
    driver.get(url)
    driver.find_element_by_class_name('search-input').click()
    # for px in range(0, 5000, 100):
    #     js = f"var q=document.documentElement.scrollTop={px}"
    #     driver.execute_script(js)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    # time.sleep(2)
    # items = driver.find_elements_by_class_name('row-item')
    #
    # for item in items:
    #     src = item.find_element_by_xpath('./img').get_attribute('src')
    #     if not src:
    #         continue
    #     filename = img_name_processor(src)
    #     path = rf'D://人脸相关的图片//图虫//{keyword}'
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     file = os.path.join(path, filename)
    #     rt = save_img(file=file, src=src)
    #     img_cnt += 1
    #     if rt:
    #         print(f'第{img_cnt}张[{keyword}]图片保存成功...')
    #     else:
    #         print(f'第{img_cnt}张[{keyword}]图片保存失败...')
    # driver.close()


if __name__ == "__main__":
    # 女脸，女脸部，
    tuchong(keyword='美女',pages=50)
