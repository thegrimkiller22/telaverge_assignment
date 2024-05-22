This project is an e-commerce recommendation system that provides product recommendations based on user interactions. It also includes a search functionality that integrates user preferences to boost the relevance of search results.

## Project Structure

- backend/: Backend folder containing Flask application.
- frontend/: Frontend folder containing React application.

## Features

- *User Interaction Recording*: Record user interactions with products.
- *Product Recommendation*: Recommend products to users based on their interaction history using cosine similarity and TF-IDF.
- *Search Functionality*: Search for products with relevance boosted by user preferences.

## Technologies Used

### Backend (backend)

- Flask
- Flask-CORS
- pymongo
- scikit-learn
- numpy

### Frontend (frontend)

- React
- Fetch API

## Prerequisites

- Python 3.x
- Node.js and npm
- MongoDB

## Installation


### Clone the Repository

1. Clone the repository:
    sh
    git clone https://link-to-project
    
    

### Backend Setup

1. Navigate to the backend directory:
    sh
    cd backend
    

2. Install the Python dependencies:
    sh
    pip install -r requirements.txt
    

### Frontend Setup

1. Navigate to the frontend directory:
    sh
    cd frontend
    

2. Install the npm dependencies:
    sh
    npm install
    

## Running the Project

### Concurrently

To run both the backend and frontend servers concurrently, use the npm start command in the root directory:

    sh
    npm start
