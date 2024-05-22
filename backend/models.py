from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import random
from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access the variables using os.environ.get()
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['ecommerce_db']
users_collection = db['users']
products_collection = db['products']
interactions_collection = db['interactions']

bcrypt = Bcrypt()

def create_user(name, email, password):
    if users_collection.find_one({"email": email}):
        return {'error': 'Email already exists'}
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        'name': name,
        'email': email,
        'password': hashed_password
    }
    users_collection.insert_one(user)
    return {'message': 'User registered successfully'}

def authenticate_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and bcrypt.check_password_hash(user['password'], password):
        return user
    return None

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

def add_product(name, description, price, category,image):
    product = {
        'name': name,
        'description': description,
        'price': price,
        'category': category,
        'image':image
    }
    products_collection.insert_one(product)
    return {'message': 'Product added successfully'}

# def add_sample_products():
#     if products_collection.count_documents({}) == 0:
#         categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Toys']
#         images=['https://plus.unsplash.com/premium_photo-1661769750859-64b5f1539aa8?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cHJvZHVjdCUyMGltYWdlfGVufDB8fDB8fHww','https://assets-global.website-files.com/619e8d2e8bd4838a9340a810/64c590c754d6bc13ebd90cbc_ai_product_photo_styles.webp','https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvZHVjdHxlbnwwfHwwfHx8MA%3D%3D','https://st4.depositphotos.com/21486874/26758/i/450/depositphotos_267580846-stock-photo-blank-white-cosmetic-skincare-makeup.jpg']
#         for i in range(100):
#             add_product(
#                 name=f"Product {i}",
#                 description=f"Description for product {i}",
#                 price=round(random.uniform(10, 1000), 2),
#                 category=random.choice(categories),
#                 image=random.choice(images)
#             )


def get_products():
    return list(products_collection.find())

def log_user_interaction(user_id, product_id):
    interactions_collection.update_one(
        {'user_id': user_id},
        {'$addToSet': {'products': product_id}},
        upsert=True
    )
def delete_user_interaction(user_id, product_id):
    interaction = interactions_collection.find_one({'user_id': user_id})
    if interaction and product_id in interaction['products']:
        interactions_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'products': product_id}}
        )
