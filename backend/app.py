from flask import Flask, render_template, request, session, redirect, url_for, jsonify,send_from_directory
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from models import create_user, authenticate_user, get_user_by_email, get_products, log_user_interaction,delete_user_interaction
import pymongo
from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access the variables using os.environ.get()
MONGO_URI = os.environ.get("MONGO_URI")
# Connect to MongoDB using environment variables
import recommendation
import search
from bson.objectid import ObjectId 

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'mysecret'
bcrypt = Bcrypt(app)

client = MongoClient(MONGO_URI)
db = client['ecommerce_db']
users_collection = db['users']
products_collection = db['products']
PRODUCTS_PER_PAGE = 12
@app.route('/', methods=['GET'])
def get_data():
    
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = authenticate_user(email, password)
        if user:
            session['email'] = user['email']
            user["_id"]=str(user["_id"])
            return jsonify(user)
        return 'Invalid email/password combination'
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        result = create_user(name, email, password)
        if 'error' in result:
            return result['error']
        data = {"message": "succsesfully register"}
        return jsonify(data)
    
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/dashboard',methods=['POST'])
def dashboard():
    data = request.get_json()
    id = data.get('user_id')
    page = data.get('page')
    page_size = data.get('page_size')
    
    print(id)
    recommended_products = recommendation.recommend_products(id)
    print(recommended_products)
    
    # Fetch products from the database that match the recommended product names
   
    # Calculate start and end indexes
    start = (page - 1) * page_size
    end = start + page_size

    # Slice the products list to get the current page of products
    paginated_products = recommended_products[start:end]
    for product in paginated_products:
        product['_id'] = str(product['_id'])

    # Return the paginated products and total number of products
    return jsonify({
        "products": paginated_products,
        "total": len(recommended_products)
    }), 200
   
    

from bson import json_util  # Import json_util from bson

@app.route('/products', methods=['GET'])
def list_products():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('size', 5))
    products = list(products_collection.find())
    # Calculate start and end indexes
    start = (page - 1) * page_size
    end = start + page_size

    # Slice the products list to get the current page of products
    paginated_products = products[start:end]
    for product in paginated_products:
        product['_id'] = str(product['_id'])

    # Return the paginated products and total number of products
    return jsonify({
        "products": paginated_products,
        "total": len(products)
    }), 200

    

    
 

@app.route('/search', methods=['GET','POST'])
def search_route():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('size', 5))
    query = request.args.get('query')
    # Calculate start and end indexes
    start = (page - 1) * page_size
    end = start + page_size

    if query is None or not isinstance(query, str):
        return jsonify(error="Invalid search query"), 400

    data = request.get_json() if request.method == 'POST' else {}
    user_id = data.get('user_id')
   
    
    search_results = search.search_products(query, user_id)
    print(search_results)
    
    for product in search_results:
        product['_id'] = str(product['_id'])

    paginated_products = search_results[start:end]
    

    # Return the paginated products and total number of products
    return jsonify({
        "products": paginated_products,
        "total": len(search_results)
    }), 200
 

    
    

@app.route('/record_interaction', methods=['POST'])
def record_interaction():
    # Parse request data
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    log_user_interaction(user_id, product_id)
    return jsonify({'message': 'Interaction recorded successfully'}), 200

@app.route('/delete_interaction', methods=['DELETE'])
def delete_interaction():
    # Parse request data
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    if not user_id or not product_id:
        return jsonify({'message': 'User ID and Product ID are required'}), 400
    delete_user_interaction(user_id, product_id)
    return jsonify({'message': 'Interaction deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
