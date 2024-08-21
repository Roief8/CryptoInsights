from data_process import prepare_data, generate_crypto_pdf, generate_sns_message
from mail_service import send_sns_mail

def get_sorted_crypto_data():
    data_set = prepare_data()

    top_by_rank = sorted(data_set, key=lambda x: x['Market Rank'])
    top_gainers = sorted(data_set, key=lambda x: float(x['Percent Change (24h)'].rstrip('%')), reverse=True)
    top_losers = sorted(data_set, key=lambda x: float(x['Percent Change (24h)'].rstrip('%')))

    return top_by_rank, top_gainers, top_losers

def generate_and_send_report():
    top_by_rank, top_gainers, top_losers = get_sorted_crypto_data()
    crypto_tables = [(top_by_rank, 'Top Ranked Cryptocurrencies'), (top_gainers,  'Top Gainers Of The Day'), (top_losers, 'Top Losers Of The Day')]
    
    url = generate_crypto_pdf(crypto_tables)
    sns_message = generate_sns_message(crypto_tables, url)
    send_sns_mail(sns_message)