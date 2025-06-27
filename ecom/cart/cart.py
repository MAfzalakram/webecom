from ecomstore.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart_session = self.session.get("usersessionkey")
        if 'usersessionkey' not in request.session:
            cart_session = self.session['usersessionkey'] = {}


        self.cart_session = cart_session

    def __len__(self):
        return len(self.cart_session)

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart_session:
            pass
        else:
            self.cart_session[product_id] = quantity

        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product.id)
        self.cart_session[product_id] = quantity 
        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart_session:
            del self.cart_session[product_id]
            self.session.modified = True
       

    def getProducts(self):
        productids = self.cart_session.keys()
        products = Product.objects.filter(id__in=productids)
        return products
    
    def getQuantity(self):
        return self.cart_session

    def getTotal(self):
        product_keys = self.cart_session.keys()
        products = Product.objects.filter(id__in=product_keys)
        total = 0

        for key, quantity in self.cart_session.items():
            key = int(key)
            for product in products:
                if key == product.id:
                    price = product.sale_price if product.is_sale else product.price
                    total += price * quantity
        return total




