# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 11:02
# @Author  : 陈子昂
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
from utils import save_img,  img_name_processor


def pixabay(keyword):
    img_cnt = 0
    folder, key = keyword, keyword
    if not folder: sys.exit('程序退出：未输入分类名称！')
    if not key: sys.exit('程序退出：未输入关键字！')

    query_url = f'https://pixabay.com/zh/photos/?q={key}&image_type=photo'
    query_res = requests.get(query_url)
    query_soup = BeautifulSoup(query_res.text, 'lxml')
    pic_num = query_soup.h1.text  # str
    print(f'-----共{pic_num}-----')
    page_num = query_soup.select('.add_search_params')[0].text.strip().lstrip('/ ')
    print(f'-----共{page_num}页-----')
    if "抱歉，我们没找到相关信息。" in query_res.text:
        return "抱歉，我们没找到相关信息。"
    for page in tqdm(range(1, int(page_num) + 1)):
        url = f'https://pixabay.com/zh/photos/?q={key}&pagi={page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        items = soup.select('.credits .item')
        # print(items)
        for item in items:
            img_attrs = item.a.img.attrs
            if img_attrs['src'] == '/static/img/blank.gif':
                img_src = img_attrs['data-lazy']
            else:
                img_src = img_attrs['src']
            path = rf'D://人脸相关的图片//pixabay//{keyword}'
            if not os.path.exists(path):
                os.makedirs(path)
            filename = img_name_processor(img_src)
            file = os.path.join(path, filename)
            rt = save_img(file=file, src=img_src) # 是save_img的返回值，
            img_cnt += 1
            if img_cnt == pic_num:
                print(f"已搜集{img_cnt}张{key}图片，程序退出...")
                break
            if rt:
                print(f'第{img_cnt}张[{key}]图片保存成功...')
            else:
                print(f'第{img_cnt}张[{key}]图片保存失败...')


if __name__ == "__main__":
    # 女脸，女性 脸，美女，
    pixabay('美女')
