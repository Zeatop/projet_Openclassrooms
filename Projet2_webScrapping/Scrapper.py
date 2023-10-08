import csv
import requests
from bs4 import BeautifulSoup
import os


# Initialisation fonctions



def get_html_code(url):
    contenu = requests.get(url)
    page = BeautifulSoup(contenu.text, "html.parser")
    return page
    
def title_n_category(page):
    category = page.find("ul", {"class":"breadcrumb"}).find_next().find_next().find_next().find_next().find_next()
    title = category.find_next().find_next().text
    category = category.text
    category = category[1:-1]
    title_cat_dict = {'Title':title,'Category': category}
    return title_cat_dict
    
def get_description(page):
    description_dict = {}
    try:
        product_description = page.find("div", {"id" : "product_description"}).find_next()
        product_description = product_description.find_next().text
    except AttributeError:
        print('pas de description')
        product_description = ('No description')
    description_dict['Description'] = product_description
    return description_dict
 
def get_table_infos(page):
    table_info_dict = {}
    table = (page.find("table", {"class":"table table-striped"}).find_all("tr"))
    for i, row in enumerate(table):
        table_info_dict[row.find('th').text] = ''
        table_info_dict[row.find('th').text] = (row.find('td').text)
    table_info_dict['Price (excl. tax)'] = table_info_dict['Price (excl. tax)'][1:]
    table_info_dict['Price (incl. tax)'] = table_info_dict['Price (incl. tax)'][1:]
    table_info_dict['Tax'] = table_info_dict['Tax'][1:]
    return table_info_dict

def image_urls(url, page):
    image_url_dict = {}
    img_url = page.find('div', {"class": "item active"}).find_next()["src"]
    img_url = f"https://books.toscrape.com{img_url[5:]}"
    image_url_dict["image url"] = img_url
    img_data = requests.get(img_url).content
    img_name = page.find('div', {"class": "item active"}).find_next()["alt"]
    img_name = img_name.replace('/', '_')
    wd_path = os.getcwd()
    folder_path = os.path.join(wd_path,"scrap_output")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(f'{folder_path}/{img_name}jpg', 'wb') as handler: 
        handler.write(img_data) 
    return image_url_dict

def book_scrapper(url):
    page = get_html_code(url)
    page
    title_cat_dict = title_n_category(page)
    description_dict = get_description(page)
    table_info_dict = get_table_infos(page)
    image_url_dict = image_urls(url, page)
    scrap_dict = title_cat_dict.copy()
    scrap_dict.update(description_dict)
    scrap_dict.update(table_info_dict)
    scrap_dict.update(image_url_dict)
    return scrap_dict

# create a list of all book's urls of a page
def get_book_url(url, book_list):
    page = get_html_code(url)
    page
    category = page.find_all("div", {"class":"image_container"})
    for i, links in enumerate(category):
            div = links.find("a")
            link= div.get("href")
            bookurl = f"https://books.toscrape.com/catalogue/{link[6:]}"
            book_list.append(bookurl)
    return book_list
      
# create a list of all pages' url in a category
def get_pages_url(url):
    category_url_list = []
    category_url_list.append(url)
    url = url[:-10]
    for i in list(range(2,101)):
        url_page = url + "page-" + str(i) + ".html"
        response = requests.get(url_page)
        status_code = response.status_code
        if status_code == 200:
            category_url_list.append(url_page)
        else:
            return category_url_list

def category_to_csv(book_data):
    category = book_data['Category']
    wd_path = os.getcwd()
    folder_path = os.path.join(wd_path,"scrap_output")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(f'{folder_path}/{category}.csv', mode='a', newline='') as fichier_csv:
        fieldnames = ['Title','Category', 'Description', 'UPC',
                      'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 
                      'Number of reviews', 'image url']
        writer = csv.DictWriter(fichier_csv, fieldnames)
        if fichier_csv.tell() == 0:
            writer.writeheader()
        writer.writerow(book_data)



# Récolte des données
def do_stuff():
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    pages_url_list = get_pages_url(url)
    book_list = []

    for urls in pages_url_list:
        get_book_url(urls, book_list)
    print(len(book_list))
    i = 0
    for urls in book_list:
        i = i+1
        print(f'{i} - url traitée: {urls}')
        book_data = book_scrapper(urls)
        category_to_csv(book_data) 

do_stuff()