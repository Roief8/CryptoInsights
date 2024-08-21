from api_client import get_available_cryptos, get_crypto_data
import matplotlib.pyplot as plt
from typing import Dict, List, Union
from mail_service import upload_to_s3
import io
import squarify
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib
from config import CRYPTO_LIMIT

matplotlib.use('Agg')

## --- Helper Functions --- ## 

def format_price(price: Union[int, float, str], decimals: int = 2) -> str:
    try:
        format_string = f"${float(price):,.{decimals}f}"
        return format_string
    except (ValueError, TypeError):
        return 'N/A'

def format_percentage(percentage: Union[int, float, str]) -> str:
    try:
        return f"+{float(percentage):.2f}%" if percentage > 0 else f"{float(percentage):.2f}%"
    except (ValueError, TypeError):
        return 'N/A'
    
def format_crypto_info(data: Dict) -> str:
    return f"{data['Name']} ({data['Symbol']}): {data['Price (USD)']} ({data['Percent Change (24h)']})"

def display_crypto_data(data_list: List[Dict], limit: int = 3) -> str:
    if not data_list:
        return "No data to display."
    
    formatted_data = [format_crypto_info(data) for data in data_list]
    return f"\n".join(formatted_data)



def organize_data(crypto_info: Dict) -> Dict:
    usd_data = crypto_info.get('quote', {}).get('USD', {})
    return {
        'Name': crypto_info.get('name', 'N/A'),
        'Symbol': crypto_info.get('symbol', 'N/A'),
        'Market Cap': format_price(usd_data.get('market_cap'), 0),
        'Market Cap Dominance': format_percentage(usd_data.get('market_cap_dominance')).strip('+-'),
        'Price (USD)': format_price(usd_data.get('price')),
        'Market Rank': crypto_info.get('cmc_rank', 'N/A'),
        'Percent Change (24h)': format_percentage(usd_data.get('percent_change_24h')),

    }

def prepare_data():
    # Get and clean Crypto data
        available_cryptos = get_available_cryptos()
        top_ids = [str(crypto['id']) for crypto in available_cryptos[:CRYPTO_LIMIT]]
        crypto_data = get_crypto_data(top_ids)
        organized_data = [organize_data(crypto_data[symbol]) for symbol in top_ids]

        return organized_data


## --- Visualize Data Functions --- ## 

def create_table(data_list: List[Dict], title = None):
    fig, ax = plt.subplots(figsize=(14, 5)) 
    # Prepare the data for the table
    table_data = []
    for crypto in data_list:
        row = [
            f"{crypto['Name']} ({crypto['Symbol']})",
            f"#{crypto['Market Rank']}",
            crypto['Market Cap'],
            crypto['Price (USD)'],
            crypto['Percent Change (24h)']
        ]
        table_data.append(row)
    
    # Create the table
    table = ax.table(
        cellText=table_data,
        colLabels=["Cryptocurrency", "Rank", "Market Cap", "Price (USD)", "24h Change"],
        cellLoc='center',
        loc='center'
    )

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)  # Adjust cell height

    cmap = LinearSegmentedColormap.from_list("", ["#ff9999", "white", "#99ff99"])

    # Header and row styles
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Header
            cell.set_text_props(fontsize=9, fontweight='bold', color='white')
            cell.set_facecolor('#2c3e50')  # Dark blue background for headers
            cell.set_height(0.05)  # Adjust header height
        else:  # Data rows
            if j == 0:  # Cryptocurrency column
                cell.set_text_props(fontweight='bold')
            elif j == 4:  # Percentage change column
                value = float(cell.get_text().get_text().strip('%'))
                color = cmap(np.interp(value, [-10, 0, 10], [0, 0.5, 1]))
                cell.set_facecolor(color)
                
        cell.set_edgecolor('#d5d8dc')  # Light gray cell borders

     # Add title 
    ax.set_title(title, fontsize=18, fontweight='bold')
    ax.title.set_position([0.5, .6])  # Manually adjust the title's vertical position

    # Remove axis
    ax.axis('off')
    return plt

def plot_ranked_treemap(data_list, title = None):
    name = [data['Name'] for data in data_list]
    symbol = [data['Symbol'] for data in data_list]
    percent_changes = [float(data['Percent Change (24h)'].strip(' %')) for data in data_list]
    prices = [str(data['Price (USD)']) for data in data_list]
    market_ranks = [int(data['Market Rank']) for data in data_list]
    market_caps = [float(data['Market Cap'].replace(',','').strip(' $')) for data in data_list]
    market_cap_dominance = [data['Market Cap Dominance'] for data in data_list]

    # Create custom colormaps
    green_cmap = LinearSegmentedColormap.from_list("custom_green", ['#D0F0C0','#98FB98','#01411C'])
    red_cmap = LinearSegmentedColormap.from_list("custom_red", ['#F08080','#CC0000','#C80815'])

    # Define color normalization
    max_change = max(abs(min(percent_changes)), abs(max(percent_changes)))
    norm = Normalize(vmin=-max_change, vmax=max_change)

    # Create color list
    colors = []
    for change in percent_changes:
        if change >= 0:
            colors.append(green_cmap(norm(change)))
        else:
            colors.append(red_cmap(norm(change)))

    # Sort by market cap and identify the smallest 8 coins and largest 6 coins
    sorted_indices = sorted(range(len(market_caps)), key=lambda i: market_caps[i])
    smallest_indices = sorted_indices[:8]
    biggest_indices = sorted_indices[-6:]

    # Create labels with conditional formatting
    labels = []
    for i in range(len(name)):
        arrow = "⇧" if percent_changes[i] > 0 else "⇩"
        if i in smallest_indices:
            labels.append(f"{symbol[i]}\n{prices[i]}\n{arrow} {percent_changes[i]:.2f}%")
        elif i in biggest_indices:
            labels.append(f"{name[i]}\n({symbol[i]})\n\n{prices[i]}\n{arrow} {percent_changes[i]:.2f}%\n\nDominance: {market_cap_dominance[i]}")
        else:
            labels.append(f"{name[i]}\n{symbol[i]}\n{prices[i]}\n{arrow} {percent_changes[i]:.2f}%")
    # Create the treemap without labels
    fig, ax = plt.subplots(figsize=(16, 10))
    squarify.plot(sizes=[cap / sum(market_caps) for cap in market_caps], 
                color=colors, alpha=0.8, ax=ax)

    # Manually add labels with different styles
    for i, rect in enumerate(ax.patches):
        x = rect.get_x() + rect.get_width() / 2
        y = rect.get_y() + rect.get_height() / 2
        
        if i < 2: 
            ax.text(x, y, labels[i], ha="center", va="center", fontsize=16, fontweight='normal')
        elif i < 5:
            ax.text(x, y, labels[i], ha="center", va="center", fontsize=10, fontweight='normal')
        else:  # Other coins: Standard font
            ax.text(x, y, labels[i], ha="center", va="center", fontsize=8, fontweight='normal')

    # Add black borders around each rectangle
    for rect in ax.patches:
        rect.set_linewidth(2)
        rect.set_edgecolor('black')

    # Add title
    plt.title(title, fontsize=18, fontweight='bold', color='black')

    # Add a color legend
    green_patch = patches.Patch(color='#98FB98', label='Positive Change')
    red_patch = patches.Patch(color='#F08080', label='Negative Change')
    plt.legend(handles=[green_patch, red_patch], loc='upper left', fontsize=12, frameon=False)

    # Remove axis
    plt.axis('off')
    # Adjust spacing
    plt.tight_layout()

    return plt


## --- Generate PDF --- ## 

def generate_simple_page(pdf, title, bottom_text=None):
    fig, ax = plt.subplots(figsize=(12, 16))  # Standard letter size

    # Add title at the top of the page (adjusting to center)
    if bottom_text:
        plt.text(0.5, 0.75, title, fontsize=28, ha='center', va='center', fontweight='bold')

        plt.text(0.5, 0.2, bottom_text, fontsize=16, ha='center', va='bottom', fontweight='bold')
    else:
        plt.text(0.5, 0.65, title, fontsize=28, ha='center', va='center', fontweight='bold')

    # Remove axes
    ax.axis('off')

    # Save the figure into the PDF
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

def generate_table_page(pdf, tables):
    for table, title in tables:
        create_table(table[:10], title)
        pdf.savefig()  # Save the current figure into the PDF
        plt.close()    # Close the figure to release memory

def generate_crypto_pdf(crypto_tables):
    # Create an in-memory buffer
    pdf_buffer = io.BytesIO()
    
    with PdfPages(pdf_buffer) as pdf:
        current_date = datetime.now().strftime('%A, %d/%m/%Y (%H:%M:%S)')

        generate_simple_page(pdf, f'Daily Crypto Report \n {current_date}' ,bottom_text='®Made by\n Roi Efraim and Raz Sherf')
        
        generate_table_page(pdf,crypto_tables)

        # Generate and save the tree map plot
        plot_ranked_treemap(crypto_tables[0][0][:20], "Crypto Market Tree Map") # Needs to be the "top ranked" table
        pdf.savefig() 
        plt.close()

        generate_simple_page(pdf, f'\n\n\n\n\nThanks for using our service!\n')

    # Ensure the buffer's pointer is at the beginning
    pdf_buffer.seek(0)

    # Upload the in-memory PDF to S3
    url = upload_to_s3(pdf_buffer, 'crypto_report')
    
    return url

def generate_sns_message(crypto_tables: List[tuple], report_url: str) -> str:
    date = datetime.now().strftime('%A, %d/%m/%Y')

    # Get the top-ranked cryptocurrencies and format them with indentation for better alignment
    top_ranked = display_crypto_data(crypto_tables[0][0][:3])
    top_ranked = "\n                               ".join(top_ranked.splitlines())  # Indent each line
    
    # Get the biggest gainer and biggest loser
    biggest_gainer = display_crypto_data(crypto_tables[1][0][:1])
    biggest_loser = display_crypto_data(crypto_tables[2][0][:1])

    # Generate the final message with the formatted strings
    message = f"""📊 Crypto Daily Report ({date})📊\n
🔝 Top Ranked: {top_ranked}

🚀 Biggest Gainer: {biggest_gainer}

📉 Biggest Loser: {biggest_loser}

🔗 Read Full report: {report_url}
    """
    
    return message
    