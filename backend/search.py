from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bson import ObjectId
import recommendation

# MongoDB connection
from dotenv import load_dotenv
import os

# Load variables from the .env file into the environment
load_dotenv()

# Access the variables using os.environ.get()
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['ecommerce_db']
products_collection = db['products']

# Fetch products
products = list(products_collection.find())

def preprocess_text(text):
    return text.lower()

def build_tfidf_matrix(products):
    # Concatenate relevant product attributes into a single text string for TF-IDF vectorization
    product_texts = [' '.join([preprocess_text(str(product[attr])) for attr in ['name', 'main_category', 'sub_category', 'description'] if attr in product]) for product in products]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_texts)
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = build_tfidf_matrix(products)

def search_products(query, user_id, num_results=5):
    query = preprocess_text(query)
    query_vec = vectorizer.transform([query])
    
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Fetch recommended products for the user
    recommended_products = recommendation.recommend_products(user_id, num_recommendations=len(products))
    recommended_set = set([str(product['_id']) for product in recommended_products])
    
    product_scores = []
    for idx, score in enumerate(similarities):
        product_id = str(products[idx]['_id'])
        if product_id in recommended_set:
            score += 1  # Boost score for recommended products
        product_scores.append((idx, score))
    
    product_scores.sort(key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in product_scores[:num_results]]
    return [products[idx] for idx in top_indices]

# Example usage:
