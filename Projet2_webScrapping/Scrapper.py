import csv
import requests
from bs4 import BeautifulSoup


scrap_dict = {}
infos_livre = []
entetes = []

def get_html_code(url):
    contenu = requests.get(url)
    global page
    page = BeautifulSoup(contenu.text, "html.parser")
    return page
    
def title_n_category():
    category = page.find("ul", {"class":"breadcrumb"}).find_next().find_next().find_next().find_next().find_next()
    title = category.find_next().find_next().text
    category = category.text
    infos_livre.append(title)
    infos_livre.append(category)
    #print(f'titre et catégorie: {title}, {category}')
    if 'Title' not in scrap_dict:
        scrap_dict['Title'] = []
        scrap_dict['Category'] = []
    scrap_dict['Title'].append(title)
    scrap_dict['Category'].append(category)
    return scrap_dict
    #entetes.append("Title")    
    #entetes.append("Category")
    
def get_description():
    product_description = page.find("div", {"id" : "product_description"}).find_next()
    product_description_entete = product_description.text
    if product_description_entete not in scrap_dict:
        scrap_dict[product_description_entete] = []
    #entetes.append(product_description.text)
    product_description = product_description.find_next().text
    scrap_dict[product_description_entete].append(product_description)
    return scrap_dict
    #infos_livre.append(product_description)    
    
def get_table_infos():
    table = (page.find("table", {"class":"table table-striped"}).find_all("tr"))
    for i, row in enumerate(table):
        #print(f"itération numéro: {i}, entete: {row.find('th').text}  -  info: {row.find('td').text}")
        if row.find('th').text not in scrap_dict:
            scrap_dict[row.find('th').text] = []
        scrap_dict[row.find('th').text].append(row.find('td').text)
    print(scrap_dict)
    return scrap_dict
        #entetes.append(row.find('th').text)
        #infos_livre.append(row.find('td').text)

def image_urls(url):
    img_url = page.find('div', {"class": "item active"}).find_next()["src"]
    img_url = f"https://books.toscrape.com{img_url[5:]}"
    #print(img_url)
    if "image url" not in scrap_dict:
        scrap_dict["image url"] = [] 
    scrap_dict["image url"].append(img_url)
    
def write_to_csv(entetes, infos_livre):
    fichier_existe = False

    try:
        with open('output.csv', 'r') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)
            if first_row and not all(cell == '' for cell in first_row):
                fichier_existe = True
    except FileNotFoundError:
        pass

    with open('output.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if not fichier_existe:
            writer.writerow(entetes)

            writer.writerow(infos_livre)


def book_scrapper(url):
    get_html_code(url)
    title_n_category()
    print(scrap_dict)
    get_description()
    get_table_infos()
    image_urls(url)
    print(scrap_dict)
    print (len(scrap_dict))
    #print (entetes, infos_livre)
    #write_to_csv(entetes, infos_livre)
    
    

    

book_scrapper("https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")