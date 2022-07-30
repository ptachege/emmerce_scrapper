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


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mika.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'link', 'crawled'])

    users = MikaCategories.objects.all().values_list(
        'id', 'link', 'crawled')
    for user in users:
        writer.writerow(user)

    return response


def Mika_reset(request):
    all_categories = MikaCategories.objects.all()
    for each_category in all_categories:
        each_category.crawled = False
        each_category.save()
    return HttpResponse("saved")


def Mikaentry(request):
    all_categories = MikaCategories.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(category_url)

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # get the number of pagination in this category

        page_number_of = soup.find(
            'div', class_="woocommerce-result-count hidden-xs").text

        numbers = []
        for word in page_number_of.split():
            if word.isdigit():
                numbers.append(int(word))

        try:
            last_index_of_list = numbers[-1]
            number_of_pages = math.ceil(last_index_of_list/16)

            print(number_of_pages)
        except:
            number_of_pages = 1

        # now we have everything.

        # first page
        first_ul = soup.find(
            'ul', class_="products products-list row grid")
        product_cards = first_ul.findAll(
            'li')

        for inside_card in product_cards:
            anchor_tag = inside_card.find(
                'a', href=True)
            anchor_tag = anchor_tag['href']

            try:
                MikaProductLinks.objects.create(
                    link=anchor_tag,
                    crawled=False,
                )
                print('saved successfully')
            except:
                print('error')
                pass
        # other pages

        if number_of_pages > 1:
            i = 2
            # go to next page
            # next page-numbers

            for page in range(1, number_of_pages):
                try:
                    closebtn = driver.find_elements(By.XPATH,
                                                    "//*[@class='next page-numbers']")[0]
                    driver.execute_script("arguments[0].click();", closebtn)
                    time.sleep(3)
                except:
                    print('failed button')
                    pass
                print('fetching page' + str(i))

                soup = driver.page_source.encode('utf-8').strip()
                soup = BeautifulSoup(soup, 'lxml')

                first_ul = soup.find(
                    'ul', class_="products products-list row grid")
                product_cards = first_ul.findAll(
                    'li')

                for inside_card in product_cards:
                    anchor_tag = inside_card.find(
                        'a', href=True)
                    anchor_tag = anchor_tag['href']

                    try:
                        MikaProductLinks.objects.create(
                            link=anchor_tag,
                            crawled=False,
                        )
                        print('saved successfully')
                    except:
                        print('error')
                        pass
                i += 1

        each_category.crawled = True
        each_category.save()

    return HttpResponse("good")


def MikaProducts(request):
    uncrawled_products = MikaProductLinks.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link

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
                'div', class_='bwp-single-image col-lg-6 col-md-12 col-12')
        except:
            header_one = ''

         # title
        try:
            product_name = header_one.find(
                'h1').text
        except:
            product_name = ''


        try:
            price_wrapper = header_one.find('h2')
        except:
            pass
        


    

        # regular price
        try:
            regular_price = price_wrapper.find(
                'del')
            regular_price = regular_price.find(
                'bdi').text
            regular_price = regular_price[4:]
        except:
            regular_price = ''

        # sale price
        try:
            product_price = price_wrapper.find(
                'ins')
            product_price = product_price.find('bdi').text
            product_price = product_price[4:]
        except:
            product_price = 'nothing'
        
        
        # sku
        try:
            sku = header_one.find(
                'h3').text
        except:
            sku = ''

        # stock

        in_stock = soup.find('p', class_='stock in-stock').text

        if in_stock == 'In stock':
            stock_status = 'In Stock'
        else:
            stock_status = 'Out Of Stock'
        

        # save to db.
        MikaFinalProducts.objects.create(
            product_name=product_name,
            product_price=product_price,
            regular_price=regular_price,
            sku=sku,
            stock_status=stock_status,
            product_link=item_url
        )
        each_product.crawled = True
        each_product.save()
        return HttpResponse("com")
        break


