from dotenv import load_dotenv
load_dotenv()

import os

API_DETAILS = {
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
    'EXCHANGE_ID': os.getenv('EXCHANGE_ID')
}

OPTIONS = {
    'SYMBOL': os.getenv('SYMBOL'),
    'STARTING_PRICE': os.getenv('STARTING_PRICE'),
    'PERCENTAGE': os.getenv('PERCENTAGE')
}
