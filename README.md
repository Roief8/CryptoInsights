# CryptoInsights

## Overview

CryptoInsights is a web application that provides data-driven cryptocurrency analysis through detailed info tables, treemap visualizations, and daily reports. This project uses Python and Flask for the backend, along with AWS SNS and S3 for managing and delivering daily reports.

## Features

- **Cryptocurrency Info Tables**: View top-ranked cryptocurrencies, gainers, and losers with detailed metrics like market cap, price, and 24-hour changes.
- **Treemap Visualization**: Visualize market capitalization and performance of cryptocurrencies with an interactive treemap.
- **Daily Report**: Subscribe to receive daily insights and trends in the cryptocurrency market. The report is generated automatically and delivered via email using AWS SNS and stored in AWS S3.

## Screenshots

Home page - 

![cryptoinsights-homepage](https://github.com/user-attachments/assets/6f4d24ff-bdec-4f9a-8ede-1b6888b38ceb)

Home page dark mode - 

![homepage-dm](https://github.com/user-attachments/assets/810b30bd-34c0-4ee2-8fb2-f957898b7193)

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: AWS S3
- **Notification Service**: AWS SNS
- **Deployment**: Docker, EC2

## Usage

- Navigate to the "Treemap" tab to explore the market capitalization of various cryptocurrencies.
- Visit the "Info Tables" tab to view detailed information on top gainers, losers, and ranked cryptocurrencies.
- Use the "Crypto Report" tab to subscribe to daily reports. The report will be generated and emailed to you, and it will also be available for download directly from the app.

