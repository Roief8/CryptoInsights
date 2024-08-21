import requests
from typing import Dict, List
from config import API_KEY, BASE_URL, CRYPTO_LIMIT

def get_api_headers() -> Dict[str, str]:
    """Return the headers for API calls."""
    return {'X-CMC_PRO_API_KEY': API_KEY}

def make_api_request(endpoint: str, params: Dict[str, str]) -> Dict:
    """Make an API request and handle potential errors."""
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.get(url, headers=get_api_headers(), params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")

def get_available_cryptos() -> List[Dict]:
    """Fetch the top cryptocurrencies by rank."""
    params = {'sort': "cmc_rank", 'limit': str(CRYPTO_LIMIT)}
    data = make_api_request('cryptocurrency/map', params)
    return data['data']

def get_crypto_data(symbols: List[str]) -> Dict:
    """Fetch detailed data for specified cryptocurrencies."""
    params = {'id': ','.join(symbols)}
    data = make_api_request('cryptocurrency/quotes/latest', params)
    return data['data']