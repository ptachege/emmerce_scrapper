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
    response['Content-Disposition'] = 'attachment; filename="hotpoint.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'link', 'crawled'])

    users = HypermartCategories.objects.all().values_list(
        'id', 'link', 'crawled')
    for user in users:
        writer.writerow(user)

    return response

def Hypermart_entry(request):
    all_categories = HypermartCategories.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(category_url)

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        page_number_of = soup.find(
            'div', class_="product-amount")
        page_number_of = page_number_of.find(
            'span').text

        try:
            number_of_pages = math.ceil(int(page_number_of)/60)
        except:
            number_of_pages = 1


        # first page
        product_cards = soup.findAll(
            'li', class_='item product product-item')
        
        for inside_card in product_cards:
            anchor_tag = inside_card.find(
                'a', href=True)
            anchor_tag = anchor_tag['href']

            try:
                HypermartProductLinks.objects.create(
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
                print('fetching page' + str(i))
                category_url = each_category.link + \
                    '?p=' + str(i)
                options = Options()
                options.headless = True
                options.add_argument("--window-size=1920,1200")

                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.get(category_url)
                soup = driver.page_source.encode('utf-8').strip()
                final_soup = BeautifulSoup(soup, 'lxml')

                product_cards = final_soup.findAll(
                    'li', class_='item product product-item')

                for inside_card in product_cards:
                    anchor_tag = inside_card.find(
                        'a', href=True)
                    anchor_tag = anchor_tag['href']

                    try:
                        HypermartProductLinks.objects.create(
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
    return HttpResponse('good')



def Hypermarttproduct(request):
    uncrawled_products = HypermartProductLinks.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url =  each_product.link
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(item_url)
        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

         # title
        try:
            product_name = soup.find(
                'h1', class_="page-title").text
        except:
            product_name = ''

         # price
        try:
            product_price = soup.find(
                'span', class_='price').text.strip()
            product_price = product_price[4:]
        except:
            product_price = ''
        
        HypermartProducts.objects.create(
            product_name=product_name,
            product_price=product_price
        )
        
        each_product.crawled = True
        each_product.save()

        return HttpResponse("com")






