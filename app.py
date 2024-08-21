from flask import Flask, render_template, jsonify, request
from utils import get_sorted_crypto_data
from data_process import create_table, plot_ranked_treemap, generate_crypto_pdf
from mail_service import check_email_subscription, create_sns_subscription  
import os

app = Flask(__name__)
top_by_rank, top_gainers, top_losers = get_sorted_crypto_data()

# Ensure the static directory exists
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(static_dir, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/treemap')
def treemap():
    plot_ranked_treemap(top_by_rank[:20]).savefig('static/treemap.png', bbox_inches='tight', pad_inches=0.1)
    return render_template('treemap.html')

@app.route('/info-tables')
def info_tables():
    create_table(top_by_rank[:30]).savefig('static/top_ranked_table.png', bbox_inches='tight', pad_inches=0.1)
    create_table(top_gainers[:30]).savefig('static/top_gainers_table.png', bbox_inches='tight', pad_inches=0.1)
    create_table(top_losers[:30]).savefig('static/top_losers_table.png', bbox_inches='tight', pad_inches=0.1)
    return render_template('info-tables.html')

@app.route('/crypto-report')
def crypto_report():
    try:
        top_by_rank, top_gainers, top_losers = get_sorted_crypto_data()
        crypto_tables = [(top_by_rank, 'Top Ranked Cryptocurrencies'), (top_gainers, 'Top Gainers Of The Day'), (top_losers, 'Top Losers Of The Day')]
        s3_url = generate_crypto_pdf(crypto_tables)
        return render_template('crypto-report.html', pdf_url=s3_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if check_email_subscription(email):
        return jsonify({"success": False, "message": "Already subscribed"})

    subscription_arn = create_sns_subscription(email)
    if subscription_arn:
        return jsonify({"success": True, "message": "Subscription successful"})
    else:
        return jsonify({"success": False, "message": "Failed to subscribe"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)