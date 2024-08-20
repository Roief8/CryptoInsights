# CryptoInsights

## Overview

CryptoInsights is a web application that provides data-driven cryptocurrency analysis through detailed info tables, treemap visualizations, and daily reports. This project uses Python and Flask for the backend, along with AWS SNS and S3 for managing and delivering daily reports.

## Features

- **Cryptocurrency Info Tables**: View top-ranked cryptocurrencies, gainers, and losers with detailed metrics like market cap, price, and 24-hour changes.
- **Treemap Visualization**: Visualize market capitalization and performance of cryptocurrencies with an interactive treemap.
- **Daily Report**: Subscribe to receive daily insights and trends in the cryptocurrency market. The report is generated automatically and delivered via email using AWS SNS and stored in AWS S3.

## Screenshots

Home page - report download option

![homepage](https://github.com/user-attachments/assets/ef3bfa30-1a8e-48bb-8675-5b0d16af5bff)

Info tables page - Top-ranked cryptocurrencies
![info-tables](https://github.com/user-attachments/assets/3b4837dc-3ba9-4185-8c0e-9fda236ae05a)

treemap of cryptocurrency market performance
![treemap](https://github.com/user-attachments/assets/b0a0a2af-7a56-48ed-9775-a397fd3cb6e0)

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: AWS S3
- **Notification Service**: AWS SNS
- **Deployment**: Docker, EC2

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/roief8/crypto-insights.git
    cd crypto-insights
    ```

2. Build the Docker image:
    ```bash
    docker build -t crypto_report .
    ```

3. Run the Docker container:
    ```bash
    docker run -d -p 5000:5000 crypto_report
    ```

4. Access the application in your browser at `http://127.0.0.1:5000`.

### Enviroment variables Configuration

AWS_ACCESS_KEY_ID: Your AWS access key

AWS_SECRET_ACCESS_KEY: Your AWS secret access key

S3_BUCKET_NAME: The name of your S3 bucket

SNS_TOPIC_ARN: The ARN of your SNS topic

## Usage

- Navigate to the "Treemap" tab to explore the market capitalization of various cryptocurrencies.
- Visit the "Info Tables" tab to view detailed information on top gainers, losers, and ranked cryptocurrencies.
- Use the "Crypto Report" tab to subscribe to daily reports. The report will be generated and emailed to you, and it will also be available for download directly from the app.

