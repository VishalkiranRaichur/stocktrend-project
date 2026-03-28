# StockTrend: Stock Data Analysis and Visualization Tool

## Authors
Vishalkiran Raichur  
Ahmed Sonmez

## Project Description
StockTrend is a Python-based application that allows users to fetch real-time and historical stock market data from the internet. Users can input a stock ticker symbol and select a date range through an interactive graphical interface. The program organizes the retrieved data into structured files stored locally, making it easy to access and reuse. It then performs statistical analysis to identify trends and patterns in stock performance. Finally, the application generates clear visualizations so users can quickly understand how a stock has behaved over time.

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

## Data Collection and Storage Plan (Ahmed)
The program will use an online API such as yfinance to fetch stock data. The data will include daily stock prices like open, close, high, and low values. This data will be stored in CSV files locally. Organizing the data this way will make it easier to access and analyze later.

## Data Analysis and Visualization Plan (Vishalkiran)
The program will analyze stock data by calculating average price, daily returns, and trends over time. It will also identify increases or decreases in stock performance. For visualization, matplotlib will be used to generate line graphs showing stock price changes and moving averages.
