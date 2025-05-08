import pandas as pd
import numpy as np
import os

def preprocess_price_data(file_path):
    """
    Preprocess the price data:
    - Convert 'Date' column to datetime format
    - Sort data by date (if not already sorted)
    - Create a list of trading dates
    
    Parameters:
    -----------
    file_path : str
        Path to the price data CSV file
        
    Returns:
    --------
    price_data : pandas.DataFrame
        Processed price data
    trading_dates : list
        List of trading dates
    """
    # Read the CSV file
    print(f"Loading price data from {file_path}")
    price_data = pd.read_csv(file_path)
    
    # Show initial data info
    print(f"Initial data shape: {price_data.shape}")
    print(f"Initial columns: {price_data.columns.tolist()}")
    
    # Convert 'Date' column to datetime format
    price_data['Date'] = pd.to_datetime(price_data['Date'])
    
    # Sort by date (if not already sorted)
    price_data.sort_values('Date', inplace=True)
    
    # Reset the index
    price_data.reset_index(drop=True, inplace=True)
    
    # Create a list of trading dates
    trading_dates = price_data['Date'].tolist()
    
    print(f"Processed data shape: {price_data.shape}")
    print(f"Date range: {trading_dates[0]} to {trading_dates[-1]}")
    print(f"Total trading days: {len(trading_dates)}")
    
    return price_data, trading_dates

if __name__ == "__main__":
    # Define the file path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    file_path = os.path.join(data_dir, 'Geopolitical Risk v S&P500 returns - s&p500 daily returns 1950-2020.csv')
    
    # Preprocess the data
    price_data, trading_dates = preprocess_price_data(file_path)
    
    # Display some rows as a sample
    print("\nSample of processed data:")
    print(price_data.head()) 