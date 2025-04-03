from . import db
from sqlalchemy.orm import  relationship
from sqlalchemy import ForeignKey 
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# from flask_bcrypt import generate_password_hash , check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150))
    
    cart_items = relationship("UserCart", back_populates="user")

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# user = User(username = 'ankit' ,email = 'iak@gmail.com' , password= generate_password_hash('12345'))

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    product_ = relationship("UserCart", back_populates="product")

    def __repr__(self) -> str:
        return (f"product(id={self.id}, name='{self.name}', "
                f"image='{self.image}', price={self.price}, "
                f"description='{self.description}', type='{self.type}', "
                f"rating={self.rating})") 


class UserCart(db.Model):
    __tablename__ = 'user_cart'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="cart_items")

    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="product_")
    

    def __repr__(self) -> str:
        return (f"UserCart(id={self.id}, name='{self.name}', "
                f"image='{self.image}', price={self.price}, "
                f"description='{self.description}', type='{self.type}', "
                f"rating={self.rating}, quantity={self.quantity}, "
                f"total_price={self.total_price}, user_id={self.user_id})")



