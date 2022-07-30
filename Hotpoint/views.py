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
from django.http import HttpResponse

# Create your views here.


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hotpoint.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'link', 'crawled'])

    users = HotpointCategories.objects.all().values_list(
        'id', 'link', 'crawled')
    for user in users:
        writer.writerow(user)

    return response


def Hotpoint_reset(request):
    all_categories = HotpointCategories.objects.all()
    for each_category in all_categories:
        each_category.crawled = False
        each_category.save()
    return HttpResponse("saved")


def Hotpointentry(request):
    all_categories = HotpointCategories.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = 'https://hotpoint.co.ke' + each_category.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(category_url)

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # get the number of pagination in this category

        page_number_of = soup.find(
            'div', class_="results-meta-count").text

        numbers = []
        for word in page_number_of.split():
            if word.isdigit():
                numbers.append(int(word))

        last_index_of_list = numbers[-1]
        number_of_pages = math.ceil(last_index_of_list/80)

        select_fr = Select(driver.find_element("name", "items_per_page"))
        select_fr.select_by_index(2)

        # After refresh get fresh soup

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # now we have everything.

        # first page
        product_cards = soup.findAll(
            'div', class_="product-item d-flex col-6 col-sm-4 col-xl-3")

        for inside_card in product_cards:
            anchor_tag = inside_card.find(
                'a', href=True)
            anchor_tag = anchor_tag['href']

            print(anchor_tag)
            try:
                HotpointProductLinks.objects.create(
                    link=anchor_tag,
                    crawled=False,
                )
            except:
                print('error')
                pass

        i = 2
        # other pages
        for page in range(1, number_of_pages):
            print('fetching page' + str(i))
            category_url = 'https://hotpoint.co.ke' + \
                each_category.link + \
                '?sort_by=popularity&items_per_page=80&page=' + str(i)
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1200")

            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(category_url)
            soup = driver.page_source.encode('utf-8').strip()
            final_soup = BeautifulSoup(soup, 'lxml')

            product_cards = final_soup.findAll(
                'div', class_="product-item d-flex col-6 col-sm-4 col-xl-3")

            for inside_card in product_cards:
                anchor_tag = inside_card.find(
                    'a', href=True)
                anchor_tag = anchor_tag['href']

                print(anchor_tag)
                try:
                    HotpointProductLinks.objects.create(
                        link=anchor_tag,
                        crawled=False,
                    )
                except:
                    print('error')
                    pass
            i += 1
        each_category.crawled = True
        each_category.save()
        # break
    return HttpResponse("saved")


def Hotpointproduct(request):
    uncrawled_products = HotpointProductLinks.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = 'https://hotpoint.co.ke' + each_product.link
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
                'div', class_='product-title')
        except:
            header_one = ''

        # title
        try:
            product_name = header_one.find(
                'h1').text
        except:
            product_name = ''

        # brand
        try:
            brand = header_one.find(
                'a').text
        except:
            brand = ''

        # price
        try:
            product_price = soup.find(
                'span', class_='stockrecord-price-current').text.strip()
            product_price = product_price[4:]
        except:
            product_price = ''

        # regular price
        try:
            regular_price = soup.find(
                'span', class_='stockrecord-price-old').text.strip()
            regular_price = regular_price[4:]
        except:
            regular_price = ''

        # upc
        try:
            gen_table = soup.find('table', class_='table table-sm')
            mytds = gen_table.findAll('td')
            try:
                upc = mytds[0].text
            except:
                upc = ''

            try:
                sku = mytds[1].text
            except:
                sku = ''

        except:
            upc = ''
            sku = ''

        # save to db.

        HotpointProducts.objects.create(
            product_name=product_name,
            product_price=product_price,
            regular_price=regular_price,
            brand=brand,
            upc=upc,
            sku=sku,
            product_link=item_url
        )
        each_product.crawled = True
        each_product.save()
        return HttpResponse("com")
        break
