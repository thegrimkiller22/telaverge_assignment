import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access the variables using os.environ.get()
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
print("Connected to MongoDB")

db = client['ecommerce_db']
products_collection = db['products']
interactions_collection = db['interactions']

def preprocess_text(text):
    return text.lower()

def fetch_all_products():
    return list(products_collection.find())

def build_tfidf_matrix_for_categories(products):
    product_categories = [preprocess_text(product['main_category']) for product in products]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_categories)
    return vectorizer, tfidf_matrix

all_products = fetch_all_products()
vectorizer, tfidf_matrix = build_tfidf_matrix_for_categories(all_products)

def recommend_products(user_id, num_recommendations=10):
    # Fetch interactions for the target user
    target_user_interaction = interactions_collection.find_one({'user_id': user_id})
    print(target_user_interaction)
    if not target_user_interaction:
        return []  # Return empty list if user interactions not found
    
    target_products = target_user_interaction['products']
    
    # Fetch categories of interacted products
    interacted_product_categories = []
    for pid in target_products:
        product = products_collection.find_one({'_id': ObjectId(pid)})
        if product:
            interacted_product_categories.append(preprocess_text(product['main_category']))
    
    # Create a user vector for categories
    if not interacted_product_categories:
        return []  # Return empty list if no categories found for interacted products

    user_vector = vectorizer.transform(interacted_product_categories)
    
    # Calculate cosine similarity between user vector and all product categories
    similarities = cosine_similarity(user_vector, tfidf_matrix)
    
    # Sum similarities across user interactions to get a single score per product
    total_similarities = np.sum(similarities, axis=0)
    
    # Create a list of product indices and similarity scores
    product_scores = list(enumerate(total_similarities))
    
    # Sort products by similarity score in descending order
    product_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top recommended product indices, excluding already interacted products
    recommended_indices = [idx for idx, score in product_scores if str(all_products[idx]['_id']) not in target_products]
    
    # Fetch and return top recommended products
    recommended_products = [all_products[idx] for idx in recommended_indices[:num_recommendations]]
    
    return recommended_products

# Example usage:
user_id = "some_user_id"  # Replace with the actual user_id
recommended_products = recommend_products(user_id)
for product in recommended_products:
    print(f"Product Name: {product['name']}, Category: {product['main_category']}")
