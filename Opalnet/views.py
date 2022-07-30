from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import urllib.request
import requests
from bs4 import BeautifulSoup

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.common.by import By
import csv
from django.http import HttpResponse

from .models import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

# from .serialzers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import math
import time

# Create your views here.


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="opalnet.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'link', 'crawled'])

    users = OpalnetCategories.objects.all().values_list(
        'id', 'link', 'crawled')
    for user in users:
        writer.writerow(user)

    return response


def Opalnet_entry(request):
    all_categories = OpalnetCategories.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(category_url)

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # look for load more button
        flag = True
        while flag == True:
            mybtn = driver.find_element(By.XPATH,
                "//*[@class='btn-load-more']")
            
            driver.execute_script("arguments[0].click();", mybtn)
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, "//*[@class='btn-load-more']")))
                print('element_found')
            except:
                flag = False
                break

        print('we are done')

        

        over_all_ol = soup.find(
            'ol', class_='filterproducts products list items product-items')

        product_cards = driver.find_elements(By.XPATH,
                                             "//*[starts-with(@class, 'item product product-item')]")

        for each_dri in product_cards:

            anchor_tag = each_dri.find_element(By.TAG_NAME,
                'a').get_attribute("href")
            # anchor_tag = anchor_tag.getAttribute("href")
            try:
                OpalnetProductLinks.objects.create(
                    link=anchor_tag,
                    crawled=False,
                )
                print('saved successfully')
            except:
                print('error')
                pass
        each_category.crawled = True
        each_category.save()
    return HttpResponse('good')


def Opalnetproduct(request):
    uncrawled_products = OpalnetProductLinks.objects.filter(
            crawled=False)
    for each_product in uncrawled_products:
        item_url =  each_product.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(item_url)
        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # get relevant fields.

        try:
            header_one = soup.find(
                'div', class_='product-info-main')
        except:
            header_one = ''

         # title
        try:
            product_name = header_one.find(
                'h1', class_="page-title").text
        except:
            product_name = ''

        # sku
        try:
            sku = header_one.find(
                'div', class_="product attribute sku").text.split()[1]
        except:
            sku = ''

        # stock available
         # stock

        in_stock = soup.find('div', class_='stock available')
        in_stock = in_stock.find_all('span')[1].text

        # sale price
        try:
            product_price = soup.find(
                'span', class_='price-wrapper').text
            product_price = product_price[4:]
        except:
            product_price = ''

        
        # regular price
        try:
            old_span = soup.find('span', class_='old-price')
            regular_price = old_span.find('span', class_='price').text

        except:
            regular_price = ''

        
        OpalnetFinalProducts.objects.create(
            product_name=product_name,
            product_price=product_price,
            regular_price=regular_price,
            sku=sku,
            stock_status=in_stock,
            product_link=item_url
        )
        print('saved moving to next product')
        each_product.crawled = True
        each_product.save()  

        break
































    # category_url = 'https://www.opalnet.co.ke/'
    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1920,1200")

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.get(category_url)

    # soup = driver.page_source.encode('utf-8').strip()
    # soup = BeautifulSoup(soup, 'lxml')

    # # level0 nav-1 first level-top parent ui-menu-item
    # nav_ul = soup.findAll(
    #     'li', class_='ui-menu-item level0 fullwidth parent')
    
    # category_links = []
    # for each_li in nav_ul:
    #     each_li_a = each_li.find('a', href=True)
    #     anchor_tag = each_li_a['href']
    #     category_links.append(anchor_tag)


    # print(category_links)
    # for each_a in category_links:
    #     try:
    #         OpalnetCategories.objects.create(
    #             link=each_a,
    #             crawled=False
    #         )
    #         print('saving')
    #     except:
    #         print('passing')
    # #         pass
        
    # return HttpResponse('cool')

