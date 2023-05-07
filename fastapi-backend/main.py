import requests
import pymongo
import logging
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the MongoDB connection parameters
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'emertondb'
MONGODB_COLLECTION = 'bitcoin_prices'

# Define the API endpoint
API_ENDPOINT = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# Initialize the FastAPI app
app = FastAPI()

# Define CORS origins and middleware
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to fetch and store bitcoin price
async def fetch_and_store_bitcoin_price():
    await get_bitcoin_price()


# Schedule the fetch_and_store_bitcoin_price function to run every day
scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_and_store_bitcoin_price, 'interval', days=1)
scheduler.start()


# Endpoint to get current Bitcoin price and store it in MongoDB
@app.get("/bitcoin-price")
async def get_bitcoin_price():
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()

        if 'bpi' not in data or 'USD' not in data['bpi']:
            raise KeyError('Invalid data structure')

        cleaned_data = {
            'time': pd.to_datetime(data['time']['updatedISO']),
            'USD': data['bpi']['USD']['rate_float'],
            'GBP': data['bpi']['GBP']['rate_float'],
            'EUR': data['bpi']['EUR']['rate_float']
        }

        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]
        result = collection.insert_one(cleaned_data)

        logging.info(f'Successfully stored data in MongoDB with document ID: {result.inserted_id}')

        return {'price': cleaned_data['USD']}

    except (requests.exceptions.RequestException, pymongo.errors.PyMongoError, KeyError) as e:
        logging.error(f'Error fetching or storing data: {e}')
        return {'error': 'An error occurred'}

# Endpoint to get all data from the database
@app.get("/bitcoin-data")
async def get_bitcoin_data():
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]
        data = list(collection.find())

        for d in data:
            d['_id'] = str(d['_id'])

        return {'data': data}

    except pymongo.errors.PyMongoError as e:
        logging.error(f'Error fetching data from MongoDB: {e}')
        return {'error': 'An error occurred'}

# Endpoint to get histroic Bitcoin prices and store them in MongoDB
@app.get("/bitcoin-historic")
async def get_bitcoin_historic():
    try:
        response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2013-09-01&end=2023-05-06')
        response.raise_for_status()
        data = response.json()["bpi"]

        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db['bitcoin_historic']

        for date, price in data.items():
            collection.insert_one({"time": date, "price": price})

        stored_data = [doc for doc in collection.find({}, {"_id": 0})]

        return {"data": stored_data}

    except:
        return {"message": "Error retrieving bitcoin historic data."}

# Endpoint to calculate Bitcoin KPIs
@app.get("/bitcoin-kpis")
async def get_bitcoin_kpis():
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db['bitcoin_historic']
        
        data = collection.find()
        
        df = pd.DataFrame(list(data))
        df = df[['time', 'price']]
        df[['year', 'month', 'day']] = df['time'].str.split('-', expand=True)
        df.drop(columns=['time'], inplace=True)
        df = df[['price', 'year', 'month', 'day']]

        min_price = str(round(df['price'].min(), 2))
        max_price = str(round(df['price'].max(), 2))
        avg_price = str(round(df['price'].mean(), 2))
        volatility = str(round(df['price'].std(), 2))

        filtered_df = df.loc[df['year'] == '2022']
        min_two = str(round(filtered_df['price'].min(), 2))
        max_two = str(round(filtered_df['price'].max(), 2))

        return {
            'avg_price': avg_price,
            'min_price': min_price,
            'max_price': max_price,
            'volatility': volatility,
            'min_two': min_two,
            'max_two': max_two
        }

    except pymongo.errors.PyMongoError as e:
        logging.error(f'Error fetching data from MongoDB: {e}')
        return {'error': 'An error occurred'}

# Endpoint to get historic Bitcoin data from MongoDB
@app.get("/get-historic")
async def get_historic(year: int = Query(...), month: int = Query(...)):
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db['bitcoin_historic']
        
        data = collection.find()
        
        df = pd.DataFrame(list(data))
        df = df[['time', 'price']]
        df[['year', 'month', 'day']] = df['time'].str.split('-', expand=True)
        df.drop(columns=['time'], inplace=True)
        df = df[['price', 'year', 'month', 'day']]

        filtered_df = df.loc[(df['year'] == str(year)) & (df['month'] == f"{month:02d}")]

        result = filtered_df.to_dict(orient='records')

        return result

    except pymongo.errors.PyMongoError as e:
        logging.error(f'Error fetching data from MongoDB: {e}')
        return {'error': 'An error occurred'}




# start backend:
# cd fastapi-backend && uvicorn main:app --reload