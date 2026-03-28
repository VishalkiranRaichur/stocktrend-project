# StockTrend: Stock Data Analysis and Visualization Tool

## Authors
Vishalkiran Raichur  
Ahmed sonmez

## Project Description
This project is a Python-based application that allows users to fetch stock market data from the internet and analyze trends over time. The program will let users input a stock ticker and select a date range to view price changes. It will calculate simple statistics such as average price, highest and lowest values, and percentage change. The application will also generate visual graphs to help users understand stock trends more clearly. Overall, the goal is to create an interactive and user-friendly tool for exploring stock market behavior.

## Project Outline / Plan
- Build a Python interface using Tkinter or Flask
- Fetch stock data from an online API
- Store data in CSV format
- Perform analysis using Python libraries
- Visualize data using graphs (matplotlib)

## Interface Plan
- Home screen with input box for stock ticker
- Dropdown for selecting date range
- Button to fetch data
- Second screen to display statistics and graphs

## Data Collection and Storage Plan (Author #1)
The program will use an online API such as yfinance to fetch stock data. The data will include daily stock prices like open, close, high, and low values. This data will be stored in CSV files locally. Organizing the data this way will make it easier to access and analyze later.

## Data Analysis and Visualization Plan (Author #2)
The program will analyze stock data by calculating average price, daily returns, and trends over time. It will also identify increases or decreases in stock performance. For visualization, matplotlib will be used to generate line graphs showing stock price changes and moving averages.
