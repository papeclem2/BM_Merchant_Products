class Product:

    def __init__(self, jsonObj, category, numPage):

        self.product_id = jsonObj['product_id']
        self.title = jsonObj['title'].capitalize()
        self.ean = jsonObj['ean']
        self.category_name = jsonObj['category_name']
        self.marketplace_category_id = jsonObj['marketplace_category_id']
        self.brand = jsonObj['brand']
        self.images = jsonObj['images']
        self.page = numPage
        self.category = category
        self.scoringDate = "CURRENT_TIMESTAMP"
        self.scoringLink = ""
        self.scoringSource = ""
        self.scoringImg = ""
        self.sku = ""

    def __str__(self):
        return f"[{self.category.category_name}] {str(self.title)} ({str(self.brand)}) : page= {self.page}, id= {self.product_id}"