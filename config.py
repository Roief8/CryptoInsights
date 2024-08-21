import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://pro-api.coinmarketcap.com/v1/"
CRYPTO_LIMIT = 39
DISPLAY_COUNT = 5
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ARN_SNS = os.getenv("ARN_SNS")
