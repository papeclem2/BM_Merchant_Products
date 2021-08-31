from db.access import connect, disconnect, insertProduct
import requests, keyring
from models.Category import Category
from models.Product import Product
from requests.auth import HTTPBasicAuth

def getProductsByCategory(jsonContent, categoryId=-1, numPage=-1):
    """get products from json ('results' attribut)

    Args:
        jsonContent ([json]): result from ws
        categoryId (int, optional): [category id of BM marketplace, exemple 2 for 'Smartphone']. Defaults to -1.
        numPage (int, optional): [num of the current page (endpoint)]. Defaults to -1.

    Returns:
        [list]: [products list filtered by category id]
    """

    productList = []
    if jsonContent['results'] != None and len(jsonContent['results']):
        
        for jsonProduct in jsonContent['results']:
            if len(jsonProduct['title']) and jsonProduct['title'] != 'NULL' and jsonProduct['marketplace_category_id'] == categoryId:
                category = Category(categoryId, jsonProduct['category_name'])
                productList.append(Product(jsonProduct, category, numPage))

    return productList

if __name__ == '__main__':

    #start page BM endpoint
    startPage = 0
    postfix = "" if startPage == 0 else "?page=" + str(startPage)

    url = "https://www.backmarket.fr/ws/products" + postfix

    #keyring.set_password("bm", "secretlogin", "***")
    #keyring.set_password("bm", "secretpwd", "***")
    bmLogin = keyring.get_password("bm", "secretlogin")
    bmPwd = keyring.get_password("bm", "secretpwd")

    print("-"*20)

    response = requests.get(url, auth=HTTPBasicAuth(bmLogin, bmPwd))
    jsonResponse = response.json()

    pagesLimit = 10
    categoryFilter = 2

    if jsonResponse['next']:

        conn = connect()
        #delete cond "startPage < pagesLimit and" to call all ws pages 
        while(startPage < pagesLimit and jsonResponse['next'] is not None):
            
            # get products list in json ('results' attribut)
            products = getProductsByCategory(jsonResponse, categoryFilter, startPage)
            
            #insert product in db and print info
            for p in products:
                print(p)
                insertProduct(conn, p)
            
            if jsonResponse['next']:
                
                #load the next page
                jsonResponse = requests.get(jsonResponse['next'], auth=HTTPBasicAuth(bmLogin, bmPwd)).json()
            
            startPage += 1
        
        #exit db connection
        disconnect(conn)

    print("-"*20)
