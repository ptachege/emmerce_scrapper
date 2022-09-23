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
from django.db.models import F
import random


def delete_products(request):
    Products.objects.all().delete()
    print('delete successfull.')
    return HttpResponse('deleted successfully')


def start_scrap(request):
    Hotpointentry(request)
    Hypermart_entry(request)
    Mikaentry(request)
    Opalnet_entry(request)
    # ============= Give the server a little break bana ================
    time.sleep(20)
    # ============= break is over continue with the scrap ================

    Hotpointproduct(request)
    Hypermarttproduct(request)
    MikaProducts(request)
    Opalnetproduct(request)

    return HttpResponse(200)


def mine(request):
    print('==============================================================')


def reset_scrap(request):
    HotpointProductLinks2.objects.all().delete()
    HypermartProductLinks2.objects.all().delete()
    MikaProductLinks2.objects.all().delete()
    OpalnetProductLinks2.objects.all().delete()

    # reset all parent categories.
    for each_category in HotpointCategories2.objects.all():
        each_category.crawled = False
        each_category.save()

    for each_category in HypermartCategories2.objects.all():
        each_category.crawled = False
        each_category.save()

    for each_category in MikaCategories2.objects.all():
        each_category.crawled = False
        each_category.save()

    for each_category in OpalnetCategories2.objects.all():
        each_category.crawled = False
        each_category.save()

    # now reset all product links

#     for each_product_link in HotpointProductLinks2.objects.all():
#         each_product_link.crawled = False
#         each_product_link.save()

    for each_product_link in HypermartProductLinks2.objects.all():
        each_product_link.crawled = False
        each_product_link.save()

#     for each_product_link in MikaProductLinks2.objects.all():
#         each_product_link.crawled = False
#         each_product_link.save()

#     for each_product_link in OpalnetProductLinks2.objects.all():
#         each_product_link.crawled = False
#         each_product_link.save()

    return HttpResponse('reset successful')

    # now everything has been reset to default


def Hotpointentry(request):
    all_categories = HotpointCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = 'https://hotpoint.co.ke' + each_category.link
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

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
                HotpointProductLinks2.objects.create(
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
            # options = Options()
            # options.headless = True
            # options.add_argument("--window-size=1920,1200")

            # driver = webdriver.Chrome(ChromeDriverManager().install())
            user_agent_list = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
                'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            ]
            user_agent = random.choice(user_agent_list)

            browser_options = webdriver.ChromeOptions()
            browser_options.add_argument("--no-sandbox")
            browser_options.add_argument("--headless")
            browser_options.add_argument("start-maximized")
            browser_options.add_argument("window-size=1900,1080")
            browser_options.add_argument("disable-gpu")
            browser_options.add_argument("--disable-software-rasterizer")
            browser_options.add_argument("--disable-dev-shm-usage")
            browser_options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=browser_options, service_args=[
                                      "--verbose", "--log-path=test.log"])

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
                    HotpointProductLinks2.objects.create(
                        link=anchor_tag,
                        crawled=False,
                    )
                except:
                    print('error')
                    pass
            i += 1
        each_category.crawled = True
        each_category.save()
        driver.stop_client()
        driver.close()
        driver.quit()

    return HttpResponse("saved")


def Hotpointproduct(request):
    uncrawled_products = HotpointProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = 'https://hotpoint.co.ke' + each_product.link
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])
        # options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")

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

        # regular price
        out_wrapper = soup.find('div', class_='product-actions')
        backup_wrapper = soup.find('div', class_='stockrecord-prices')
        try:
            try:
                regular_price = out_wrapper.find(
                    'span', class_='stockrecord-price-old').text.strip()
                regular_price = regular_price[4:]

            except:
                regular_price = backup_wrapper.find(
                    'span', class_='stockrecord-price-old').text.strip()
                regular_price = regular_price[4:]
        except:
            try:
                regular_price = backup_wrapper.find(
                    'span', class_='stockrecord-price-current').text.strip()
                regular_price = regular_price[4:]
            except:
                regular_price = out_wrapper.find(
                    'span', class_='stockrecord-price-current').text.strip()
                regular_price = regular_price[4:]
        # upc
        try:
            gen_table = soup.find('table', class_='table table-sm')
            mytds = gen_table.findAll('td')
            try:
                upc = mytds[0].text
            except:
                upc = ''

        except:
            upc = ''
            sku = ''

        # stock status

        try:
            # my_form = soup.find("form", {"id": "alert_form"})

            # ============= Am trying to get the out of stock div =======
            my_outofstock_div = out_wrapper.find(
                "div", class_="stockrecord-availability outofstock")
            print(my_outofstock_div.text)

            if my_outofstock_div is not None:
                stock_status = "Out Of Stock"
            else:
                stock_status = 'In Stock'
        except:
            stock_status = 'In Stock'

        # description

        try:
            description = soup.find('div', class_='product-features').text

        except:
            print('mised')   


        #  images
        image_list = []

        try:
            image_ul = soup.find(
                'ul', class_='catalogue-gallery-thumbnails-switcher-items')
            for image_li in image_ul:
                try:
                    temp = image_li.find(
                        'img')['src']

                    first_part = temp.split('.')[0]
                    second_part = temp.split('.')[1]

                    # now append the @2x
                    first_part = first_part + '@2x.'

                    final_url = 'https://hotpoint.co.ke' + first_part + second_part

                    print(final_url)
                    
                    image_list.append(final_url)
                except:
                    pass

        except:
            image_wrapper = soup.find('div', class_='catalogue-gallery-items')
            temp = image_wrapper.find(
                        'img')['src']
            image_list.append('https://hotpoint.co.ke' + temp)


        Products.objects.create(
            product_name=product_name,
            sale_price='',
            regular_price=regular_price,
            brand=brand,
            upc=upc,
            sku=upc,
            stock_status=stock_status,
            product_link=item_url,
            short_description = description,
            image_list=image_list,
        )

        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse("saved successfully")


def Hypermart_entry(request):
    all_categories = HypermartCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        #
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

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
                HypermartProductLinks2.objects.create(
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
                user_agent_list = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
                    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
                ]
                user_agent = random.choice(user_agent_list)

                browser_options = webdriver.ChromeOptions()
                browser_options.add_argument("--no-sandbox")
                browser_options.add_argument("--headless")
                browser_options.add_argument("start-maximized")
                browser_options.add_argument("window-size=1900,1080")
                browser_options.add_argument("disable-gpu")
                browser_options.add_argument("--disable-software-rasterizer")
                browser_options.add_argument("--disable-dev-shm-usage")
                browser_options.add_argument(f'user-agent={user_agent}')
                driver = webdriver.Chrome(options=browser_options, service_args=[
                    "--verbose", "--log-path=test.log"])

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
                        HypermartProductLinks2.objects.create(
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
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse('good')


def Hypermarttproduct(request):
    uncrawled_products = HypermartProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link
        # item_url = 'https://www.ramtons.com/washing-drying/ramtons-dishwasher-12-settings-mar-silver-rw-300'

        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])
        # options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")
        # driver = webdriver.Chrome(ChromeDriverManager().install())


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
            most_outer_wrapper = soup.find('span', class_='old-price')
            second_outer_wrapper = soup.find(
                'span', class_='price-label').find_next_sibling('span')

            try:
                regular_price = most_outer_wrapper.find(
                    'span', class_='price').text.strip()
                regular_price = regular_price[4:]
            except:
                regular_price = second_outer_wrapper.find(
                    'span', class_='price').text.strip()
                regular_price = regular_price[4:]

        except:
            product_main = soup.find('div', class_='product-info-main')
            f_outer_wrapper = product_main.find(
                'span', class_='price-container price-final_price tax weee')
            outer_wrapper = product_main.find('span', class_='price-wrapper')

            try:
                regular_price = f_outer_wrapper.find(
                    'span', class_='price').text.strip()
                regular_price = regular_price[4:]
            except:
                regular_price = outer_wrapper.find(
                    'span', class_='price').text.strip()
                regular_price = regular_price[4:]

        # sku
        try:
            sku = product_name.split()[-1]
        except:
            sku = ''

        # stock

        try:
            stock_status = soup.find('div', class_='stock unavailable').text
        except:
            stock_status = 'In Stock'


        # short description
        try:
            feature_wrapper = soup.find("div", {"id": "feature"})
            short_description = feature_wrapper.find('ul').text

        except:
            try:
                outer_wrapper_feature = soup.find('div', class_='product-info-features')
                short_description = outer_wrapper_feature.find('ul').text
            except:
                pass

            
        # long description
        try:
            long_description_wrapper = soup.find(
                "div", class_='product attribute description').text
        except:
            try:
                long_description_backup = soup.find(
                    "div", {"id": "description"}).text
            except:
                pass
        

        # images

        image_list = []

        try:
            image_divs = soup.find(
                'div', class_='fotorama-item fotorama fotorama1663814196635')
                
            print(image_divs)
            for image_li in image_divs:
                try:
                    temp = image_li.find(
                        'img')['src']
            #         first_part = temp.split('.')[0]
            #         second_part = temp.split('.')[1]

            #         # now append the @2x
            #         first_part = first_part + '@2x.'

            #         final_url = 'https://hotpoint.co.ke' + first_part + second_part

            #         print(final_url)
                    
            #         image_list.append(final_url)
                except:
                    pass

        except:
            print('single enety')            
            my_img = soup.find('img', class_='fotorama__img')
            print(my_img)
        #     image_wrapper = soup.find('div', class_='catalogue-gallery-items')
        #     temp = image_wrapper.find(
        #                 'img')['src']
        #     image_list.append('https://hotpoint.co.ke' + temp)

            


        Products.objects.create(
            product_name=product_name,
            sku=sku,
            brand = 'Ramtoms',
            regular_price=regular_price,
            product_link=item_url,
            stock_status=stock_status,
            short_description=short_description,
            long_description=long_description_wrapper,
        )
        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse("scrapped successfully")


def Mikaentry(request):
    all_categories = MikaCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        print(category_url)
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--remote-debugging-port=9222')
        # chrome_options.add_argument("--window-size=1920,1200")
        # driver = webdriver.Chrome(
        #     '/usr/bin/chromedriver', options=chrome_options)

        # options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")

        # driver = webdriver.Chrome(ChromeDriverManager().install())
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

        driver.get(category_url)

        soup = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(soup, 'lxml')

        # get the number of pagination in this category
        try:
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
                    MikaProductLinks2.objects.create(
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
                    # try:
                    #     closebtn = driver.find_elements(By.XPATH,
                    #                                     "//*[@class='next page-numbers']")[0]
                    #     driver.execute_script(
                    #         "arguments[0].click();", closebtn)
                    #     time.sleep(3)
                    # except:
                    #     print('failed button')
                    #     pass
                    category_urly = category_url.strip("?orderby=price-desc")
                    caty = category_urly+"page/" + \
                        str(page+1)+"/?orderby=price-desc"
                    driver.get(caty)

                    print('fetching page' + caty)

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
                            MikaProductLinks2.objects.create(
                                link=anchor_tag,
                                crawled=False,
                            )
                            print('saved successfully'+anchor_tag)

                        except:
                            print('error')
                            pass
                    i += 1

            each_category.crawled = True
            each_category.save()
        except:
            print("no products")
        driver.stop_client()
        driver.close()
        driver.quit()

    return HttpResponse("good")


def MikaProducts(request):
    uncrawled_products = MikaProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link

        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

        # options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")

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

         # sale price
        try:

            regular_price = price_wrapper.find(
                'bdi').text
            regular_price = regular_price[4:]

        except:
            regular_price = header_one.find(
                'span', class_='woocommerce-Price-amount amount')
            regular_price = regular_price.find(
                'bdi').text
            regular_price = regular_price[4:]

        # sku
        try:
            sku = header_one.find(
                'h3').text
        except:
            sku = ''

        # stock
        try:

            in_stock = soup.find('p', class_='stock in-stock').text

            if in_stock == 'In stock':
                stock_status = 'In Stock'
            else:
                stock_status = 'Out Of Stock'
        except:
            in_stock = 'In Stock'

        # short description

        my_description_div = soup.find('div', class_='description').text

        # image
        image_list = []

        try:
            img_hrefs = soup.findAll('a', class_='img-thumbnail')
            for image_li in img_hrefs:
                try:
                    temp = image_li['data-image']
                    image_list.append(temp)
                except:
                    pass

        except:
            print('failed')


        Products.objects.create(
            product_name=product_name,
            sale_price='',
            regular_price=regular_price,
            sku=sku,
            stock_status=stock_status,
            product_link=item_url,
            brand = 'Mika',
            short_description = my_description_div,
            image_list=image_list
        )

        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse("com")


def Opalnet_entry(request):
    all_categories = OpalnetCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

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
                OpalnetProductLinks2.objects.create(
                    link=anchor_tag,
                    crawled=False,
                )
                print('saved successfully')
            except:
                print('error')
                pass
        each_category.crawled = True
        each_category.save()
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse('good')


def Opalnetproduct(request):
    uncrawled_products = OpalnetProductLinks2.objects.filter(
        crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=browser_options, service_args=[
            "--verbose", "--log-path=test.log"])

        # options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")

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
        try:

            in_stock = soup.find('div', class_='stock available')
            in_stock = in_stock.find_all('span')[1].text
        except:
            in_stock = 'In Stock'
        # sale price
        try:
            old_span = soup.find('span', class_='old-price')
            regular_price = old_span.find('span', class_='price').text

        except:
            regular_price = soup.find(
                'span', class_='price-wrapper').text
            regular_price = regular_price[3:]
            # sale_price = ''


        # descriptions

        try:
            feature_list = soup.find('ul', class_='feature-list').text
            print(feature_list)
        except:
            pass

        
        # images


        Products.objects.create(
            product_name=product_name,
            sale_price='',
            regular_price=regular_price,
            sku=sku,
            stock_status=in_stock,
            product_link=item_url,
            brand= 'LG',
            short_description = feature_list,

        )
        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
        driver.stop_client()
        driver.close()
        driver.quit()
    return HttpResponse('saved')
