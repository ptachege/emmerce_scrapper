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


def delete_products(request):
    Products.objects.all().delete()
    print('delete successfull.')
    return HttpResponse('deleted successfully')

def start_scrap(request):
    # Hotpointentry(request)
    # Hypermart_entry(request)
    # Mikaentry(request)
    # Opalnet_entry(request)
    # ============= Give the server a little break bana ================
    # time.sleep(20)
    # ============= break is over continue with the scrap ================
 

    Hotpointproduct(request)
    Hypermarttproduct(request)
    MikaProducts(request)
    Opalnetproduct(request)

    return HttpResponse(200)



def mine(request):
    print('==============================================================')


def reset_scrap(request):

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

    for each_product_link in HotpointProductLinks2.objects.all():
        each_product_link.crawled = False
        each_product_link.save()

    for each_product_link in HypermartProductLinks2.objects.all():
        each_product_link.crawled = False
        each_product_link.save()


    for each_product_link in MikaProductLinks2.objects.all():
        each_product_link.crawled = False
        each_product_link.save()

    for each_product_link in OpalnetProductLinks2.objects.all():
        each_product_link.crawled = False
        each_product_link.save()

    # now everything has been reset to default


def Hotpointentry(request):
    all_categories = HotpointCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = 'https://hotpoint.co.ke' + each_category.link
#         options = Options()
#         options.headless = True
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)
        
        
        

#         driver = webdriver.Chrome(ChromeDriverManager().install())
        

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
    return HttpResponse("saved")


def Hotpointproduct(request):
    uncrawled_products = HotpointProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = 'https://hotpoint.co.ke' + each_product.link
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)
       

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
        try:
            regular_price = out_wrapper.find(
                'span', class_='stockrecord-price-old').text.strip()
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

            # try:
            #     # sku = mytds[1].text
            #     gen_table.find()
                
            # except:
            #     sku = ''

        except:
            upc = ''
            sku = ''

        # stock status 

        try:
            stock_status = soup.find('div', class_='stockrecord-availability outofstock').text
        except:
            stock_status = 'In Stock'


        # save to db.
        # products = Products.objects.all()

        # # checking if a product with this sku exists. ==========> if it does we update the record
        # for product in products:
        #     if product.sku == sku:
        #         this_product = Products.objects.get(sku=sku)
        #         this_product.product_name=product_name
        #         this_product.sale_price=sale_price
        #         this_product.regular_price=regular_price
        #         this_product.brand=brand
        #         this_product.upc=upc
        #         this_product.stock_status=stock_status
        #         this_product.product_link=item_url
        #         this_product.save()

        #         print('product with this sku is getting updated.')
        #         break
        #     else:    
                # ============= if it doesn't we create a new entry. ===================
        Products.objects.create(
            product_name=product_name,
            sale_price = '',
            regular_price=regular_price,
            brand=brand,
            upc=upc,
            sku=upc,
            stock_status=stock_status,
            product_link=item_url
        )
        print('product saved as a new entry.')
                # break
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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
        
        driver.quit()
    return HttpResponse('good')


def Hypermarttproduct(request):
    uncrawled_products = HypermartProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
            regular_price = soup.find(
                'span', class_='price').text.strip()
            regular_price = regular_price[4:]
        except:
            regular_price = ''

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

        
        # save to db. 
        # ================ we first check if this sku exists =================

        # products = Products.objects.all()

        # checking if a product with this sku exists. ==========> if it does we update the record
        # for product in products:
        #     if product.sku == sku:
        #         this_product = Products.objects.get(sku=sku)
        #         this_product.product_name=product_name
        #         this_product.regular_price=regular_price
        #         this_product.stock_status=stock_status
        #         this_product.product_link=item_url
        #         this_product.save()

        #         print('product with this sku is getting updated.')
        #         break
        #     else:    
                # ============= if it doesn't we create a new entry. ===================
        Products.objects.create(
            product_name=product_name,
            sku=sku,
            regular_price=regular_price,
            product_link=item_url,
            stock_status=stock_status,
        )
        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
#         driver.stop_client()
#         driver.close()
#         driver.quit()
    return HttpResponse("com")


def Mikaentry(request):
    all_categories = MikaCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
                        MikaProductLinks2.objects.create(
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
#         driver.stop_client()
#         driver.close()
#         driver.quit()

    return HttpResponse("good")


def MikaProducts(request):
    uncrawled_products = MikaProductLinks2.objects.filter(crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
            # sale_price = price_wrapper.find(
            #     'ins')
            # sale_price = sale_price.find('bdi').text
            # sale_price = sale_price[4:]

            regular_price = price_wrapper.find(
                'del')
            regular_price = regular_price.find(
                'bdi').text
            regular_price = regular_price[4:]

        except:
            regular_price = 0
            regular_price = 0
            regular_price = 0
            # sale_price = ''
       

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

        # save to db.

        # products = Products.objects.all()

        # checking if a product with this sku exists. ==========> if it does we update the record
        # for product in products:
        #     if product.sku == sku:
        #         this_product = Products.objects.get(sku=sku)
        #         this_product.product_name = product_name
        #         this_product.sale_price = sale_price
        #         this_product.regular_price = regular_price
        #         this_product.stock_status = stock_status
        #         this_product.product_link = item_url
        #         this_product.save()

        #         print('product with this sku is getting updated.')
        #         break
        #     else:
                # ============= if it doesn't we create a new entry. ===================
        Products.objects.create(
            product_name=product_name,
            sale_price='',
            regular_price=regular_price,
            sku=sku,
            stock_status=stock_status,
            product_link=item_url
        )
        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
#         driver.stop_client()
#         driver.close()
#         driver.quit()
    return HttpResponse("com")


def Opalnet_entry(request):
    all_categories = OpalnetCategories2.objects.filter(crawled=False)
    for each_category in all_categories:
        category_url = each_category.link
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
#         driver.stop_client()
#         driver.close()
#         driver.quit()
    return HttpResponse('good')


def Opalnetproduct(request):
    uncrawled_products = OpalnetProductLinks2.objects.filter(
        crawled=False)
    for each_product in uncrawled_products:
        item_url = each_product.link
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
#         chrome_options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', options=chrome_options)

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
            old_span = soup.find('div', class_='old-price-save')
            regular_price = old_span.find('span', class_='price').text

            # sale_price = soup.find(
            #     'span', class_='price-wrapper').text
            # sale_price = sale_price[3:]
        except:
            regular_price = soup.find(
                'span', class_='price-wrapper').text
            regular_price = regular_price[3:]
            # sale_price = ''

        # <==================get an array of all products ===============>

        # products = Products.objects.all()

        # checking if a product with this sku exists. ==========> if it does we update the record
        # for product in products:
        #     if product.sku == sku:
        #         this_product = Products.objects.get(sku=sku)
        #         this_product.product_name = product_name
        #         this_product.sale_price = sale_price
        #         this_product.regular_price = regular_price
        #         this_product.stock_status = in_stock
        #         this_product.product_link = item_url
        #         this_product.save()

        #         print('product with this sku is getting updated.')
        #         break
        #     else:
                # ============= if it doesn't we create a new entry. ===================
        Products.objects.create(
            product_name=product_name,
            sale_price='',
            regular_price=regular_price,
            sku=sku,
            stock_status=in_stock,
            product_link=item_url
        )
        print('product saved as a new entry.')
        each_product.crawled = True
        each_product.save()
#         driver.stop_client()
#         driver.close()
#         driver.quit()
    return HttpResponse('saved')
