from flask import Blueprint, render_template , redirect , url_for , request , flash
from .models import *
from . import db
from werkzeug.exceptions import BadRequest
import random
from flask_bcrypt import generate_password_hash , check_password_hash
from flask_login import current_user , login_user , logout_user

main = Blueprint('main', __name__)


# TYPES_OF_GROCERY = {"vegetable" : Vegetable , "fruit": Fruit}
ALL_PRODUCT = [item for item in Product.query.all()]
top_six_product = random.sample(population=ALL_PRODUCT ,k=6)
random.shuffle(ALL_PRODUCT)



buylist = []



@main.route("/user")
def hello():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return f"user = {current_user} , {current_user.cart_items} buylsit = {buylist} "
    else:
        return f"user = {current_user} , buylsit = {buylist} "


def userId():
    if not current_user.is_authenticated:  
        return 0                                # id = 0  for (when not logegd in)
    else:
        return current_user.id

def addBuylistToCart():
    if buylist:
        itemExistInCart = False
        for product in buylist:
            productToAdd = Product.query.get(id)

            if product.product_id == productToAdd.id:                         # item already exists in buylist
                product.quantity += 1
                product.total_price += product.price
                itemExistInCart = True
                db.session.commit()       
                break
            if not itemExistInCart:
                db.session.add(product)
                db.session.commit()       

def calculate_total_price():
    total_price= 0
    if not current_user.is_authenticated:           # user is not logged in
        if buylist is None :
            return 0
        else:
            for product in buylist:
                total_price += product.total_price 
            return total_price
    
    else:                                           # user is logged in
        if current_user.cart_items is None :
            return 0
        else:
            for product in current_user.cart_items:
                total_price += product.total_price 
            return total_price

# Search bar
def search(product):
    # item = request.form.get('product')
    # print(item)
    searched_items = []

    for item in Product.query.all():
        name = item.name.lower()
        print(name.__eq__(product.lower()))
        if  name.__eq__(product.lower()):
            searched_items.append(item)
        if name.__contains__(product.lower()):
            searched_items.append(item)
    return searched_items

@main.route("/signup" , methods=['POST' , 'GET'])
def signup():
    # if current_user.is_authenticated():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password  = generate_password_hash(password= password)

        
        user = User.query.filter_by(email = email).first()
        if user:
            flash(message= 'Account already exist')
            return redirect(url_for('main.login'))
        else:
            new_user = User(username = username , email = email , password = hashed_password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            # if user added some item to cart it added to therir cart when they login
            addBuylistToCart()
            flash(f'Logged in Successfully {current_user.username}')
            return redirect(url_for('main.index'))

@main.route("/login", methods=['POST' , 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        print(email ,password)
        try:
            user = User.query.filter_by(email = email).first()
            print(user)
            if user == None:
                flash('Please create account first')
                return redirect(url_for('main.signup'))
            if user != None and check_password_hash(pw_hash = user.password , password=password):
                login_user(user = user)
                # if user added some item to cart it added to therir cart when they login
                addBuylistToCart()

                flash(f'Logged in Successfully {current_user.username}')
                return redirect(url_for('main.index'))
            else:
                flash('Either email or password is wrong try again!')
                return redirect(url_for('main.login'))
        except:
            flash('Please create account first')
            return redirect(url_for('main.signup'))
        


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# def item_exist_in_buylist():
#     productToAdd = TYPES_OF_GROCERY[type].query.get(id)
#     for index , product in enumerate(buylist):
#         print(product['product'].name , productToAdd)
#         if product.__getitem__('product') == productToAdd:
#             buylist[index]['quantity'] += 1
#             buylist[index]['total_price'] += productToAdd.price
#             return redirect(url_for('index'))

@main.errorhandler(BadRequest)
@main.route("/search/<page>/<product>" , methods=['GET'])
def main_search(product , page):

    searched_items = search(product=product)

    if page =="shop":
        return render_template("shop.html" ,all_product = searched_items  )
    if page == 'groceries':
        return render_template("search_result.html" ,searched_items = searched_items , )
    else:
        return 'bad request!', 400


@main.errorhandler(BadRequest)
@main.route('/inc/<itemindex>' ,  methods=['POST' , 'GET'])
def inc_quantity_price(itemindex):
    # itemindex = index-1
    if request.method == 'POST':
        itemindex = int(itemindex)
        if current_user.is_authenticated:
            current_user.cart_items[itemindex].quantity += 1
            current_user.cart_items[itemindex].total_price += current_user.cart_items[itemindex].price

            db.session.commit()
            print(f'{current_user.cart_items[itemindex]}  is inc')
            return redirect(url_for('main.cart'))
        else:
            buylist[itemindex].quantity += 1
            buylist[itemindex].total_price += buylist[itemindex].price

            return redirect(url_for('main.cart'))
    else:
        return 'bad request!', 400



@main.errorhandler(BadRequest)
@main.route('/dec/<itemindex>', methods=['POST' , 'GET'])
def dec_quantity_price(itemindex):
    # itemindex = index -1 
    if request.method == 'POST':
        itemindex = int(itemindex)
        if current_user.is_authenticated:
            if current_user.cart_items[itemindex] > 1:
                current_user.cart_items[itemindex].quantity -= 1
                current_user.cart_items[itemindex].total_price -= current_user.cart_items[itemindex].price

                db.session.commit()
                print(f'{current_user.cart_items[itemindex]}  is dec')
            else:   # removing the cart item
                cart_item = UserCart.query.get_or_404(int(current_user.cart_items[itemindex].id))
                db.session.delete(cart_item)

                db.session.commit()
            return redirect(url_for('main.cart'))
        else:
            if buylist[itemindex] > 1:
                buylist[itemindex].quantity -= 1
                buylist[itemindex].total_price -= buylist[itemindex].price

            else:   # removing the cart item
                buylist.pop(itemindex)
            return redirect(url_for('main.cart'))
    else:
        return 'bad request!', 400






@main.route("/")      # if url address start with this '/' print  'Hello, World'
def index():
    return render_template("index.html",
                            all_product = ALL_PRODUCT ,top_six_product = top_six_product )


@main.route("/404")      # if url address start with this '/' print  'Hello, World'
def error():
    return render_template("404.html")

@main.route("/addtocart/<id>")      # if url address start with this '/' print  'Hello, World'
def addtocart(id):
    productToAdd = Product.query.get(id)
    user_id = userId()
    # using func  user_id() for getting current_user.id 
    cart_item = UserCart(name = productToAdd.name , image = productToAdd.image, price = productToAdd.price, 
                         description = productToAdd.description , type = productToAdd.type , rating = productToAdd.rating, 
                         quantity = 1 , total_price = productToAdd.price , user_id = user_id , product_id = productToAdd.id)
    if current_user.is_authenticated:
        itemExistInCart = False
        for product in current_user.cart_items:
            if product.product_id == productToAdd.id:                         # item already exists in buylist
                product.quantity += 1
                product.total_price += product.price
                itemExistInCart = True
                db.session.commit()
                break
        if not itemExistInCart:
            db.session.add(cart_item)
            db.session.commit()
    else:
        itemExistInCart = False
        for product in buylist:
            if product.product_id == productToAdd.id:                         # item already exists in buylist
                product.quantity += 1
                product.total_price += product.price
                itemExistInCart = True
                break
        if not itemExistInCart:
            buylist.append(cart_item)
    return redirect(url_for('main.index'))


@main.route("/cart" )      # if url address start with this '/' print  'Hello, World'
def cart():
    # if request.method == "POST":
    if current_user.is_authenticated:                       # USer is logegd in
        product_to_buy = current_user.cart_items
    else:                                                   # USer is not logegd in
        product_to_buy = buylist
    return render_template("cart.html" ,product_to_buy = product_to_buy , total_price= calculate_total_price())

@main.route("/checkout")      # if url address start with this '/' print  'Hello, World'
def checkout():
    return render_template("checkout.html")



@main.route("/contact")      # if url address start with this '/' print  'Hello, World'
def contact():
    return render_template("contact.html")


@main.route("/shop-detail")      # if url address start with this '/' print  'Hello, World'
def shop_detail():
    return render_template("shop-detail.html")

@main.route("/shop")      # if url address start with this '/' print  'Hello, World'
def shop():

    return render_template("shop.html" , all_product = ALL_PRODUCT)

@main.route("/testimonial")      # if url address start with this '/' print  'Hello, World'
def testimonial():
    return render_template("testimonial.html")


# @main.route("/search")      # if url address start with this '/' print  'Hello, World'
# def search():
#     for product in buylist:
#         print(product)
#         # print(product['product'].name)

#     return 'sat saheb'
