from app import db, login_manager
from flask_login import UserMixin, current_user



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    user_img = db.Column(db.String, nullable=False, default="default.jpg")
    password = db.Column(db.String, nullable=False, unique=True)
    user_description= db.Column(db.String)
    user_address = db.Column(db.String)
    user_state = db.Column(db.String)
    user_country = db.Column(db.String)
    user_gender = db.Column(db.String)
    product = db.relationship('Products', backref='seller', lazy=True)
    cart = db.relationship('Cart', backref='carts', lazy=True)
    wishlist = db.relationship('Wishlist', backref='wishlists', lazy=True)
    notification = db.relationship('Notification', backref='notifs', lazy=True)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.username}')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wishlist = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_description = db.Column(db.String, nullable=False)
    product_img1 = db.Column(db.String, nullable=False)
    product_img2 = db.Column(db.String)
    product_img3 = db.Column(db.String)
    product_img4 = db.Column(db.String)
    product_img5 = db.Column(db.String)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.product_name}', '{self.product_description}', '{self.category}', '{self.product_img1}')"




def update_orders(data):
    orders_entries = []
    for orders in data["all_orders"]:
        new_entry = Products(
                            product_name=orders['title'],
                            product_description = orders['description'],
                            price= orders['price'],
                            product_img1=orders['image'],
                            category= orders['category'],
                            user_id= 1 
                               
                                )
        
        orders_entries.append(new_entry)
    db.session.add_all(orders_entries)
    db.session.commit()


def add_to_cart(id):
    new_cart = Cart(cart=id, user_id=current_user.id)
    db.session.add(new_cart)
    db.session.commit()

def add_to_wishlist(id):
    new_wishlist = Wishlist(wishlist=id, user_id=current_user.id)
    db.session.add(new_wishlist)
    db.session.commit()

