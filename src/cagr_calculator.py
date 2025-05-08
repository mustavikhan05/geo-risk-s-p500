import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from preprocess import preprocess_price_data

def load_events(events_file):
    """
    Load the event dates from a file.
    
    Parameters:
    -----------
    events_file : str
        Path to the events file
        
    Returns:
    --------
    events_df : pandas.DataFrame
        DataFrame containing event names and dates
    """
    events_df = pd.read_csv(events_file)
    print(f"Loaded {len(events_df)} events")
    
    # Handle date ranges (some events span multiple days)
    events_df['Event Date'] = events_df['Time of Event'].apply(
        lambda x: x.split('–')[0] if '–' in x else x
    )
    
    # Clean spaces and convert to datetime
    events_df['Event Date'] = events_df['Event Date'].str.strip()
    events_df['Event Date'] = pd.to_datetime(events_df['Event Date'], errors='coerce')
    
    # Check for any parsing failures
    if events_df['Event Date'].isna().any():
        print("Warning: Some event dates could not be parsed properly.")
    
    return events_df

def find_closest_trading_date(target_date, trading_dates, direction='forward'):
    """
    Find the closest trading date to the target date.
    
    Parameters:
    -----------
    target_date : datetime
        The target date to find the closest trading date to
    trading_dates : list
        List of trading dates
    direction : str, optional
        Direction to search ('forward' or 'backward')
        
    Returns:
    --------
    closest_date : datetime
        The closest trading date
    """
    # Convert trading_dates to numpy array for faster comparison
    trading_dates_array = np.array(trading_dates)
    
    if direction == 'forward':
        # Find the first trading date that is >= target_date
        mask = trading_dates_array >= target_date
        if np.any(mask):
            return trading_dates_array[mask][0]
        else:
            return None
    else:  # 'backward'
        # Find the first trading date that is <= target_date
        mask = trading_dates_array <= target_date
        if np.any(mask):
            return trading_dates_array[mask][-1]
        else:
            return None

def find_trading_date_offset(base_date, trading_dates, offset):
    """
    Find a trading date that is 'offset' trading days away from the base date.
    
    Parameters:
    -----------
    base_date : datetime
        The base date
    trading_dates : list
        List of trading dates
    offset : int
        Number of trading days to offset (can be positive or negative)
        
    Returns:
    --------
    offset_date : datetime
        The date that is 'offset' trading days away from the base date
    """
    try:
        # Find the index of the base date in the trading dates list
        base_idx = trading_dates.index(base_date)
        
        # Calculate the target index
        target_idx = base_idx + offset
        
        # Check if the target index is valid
        if 0 <= target_idx < len(trading_dates):
            return trading_dates[target_idx]
        else:
            return None
    except ValueError:
        # Base date not found in trading dates
        closest_date = find_closest_trading_date(base_date, trading_dates)
        if closest_date is not None:
            return find_trading_date_offset(closest_date, trading_dates, offset)
        else:
            return None

def calculate_cagr(entry_price, exit_price, years):
    """
    Calculate the Compound Annual Growth Rate (CAGR).
    
    Parameters:
    -----------
    entry_price : float
        The price at entry
    exit_price : float
        The price at exit
    years : float
        The number of years between entry and exit
        
    Returns:
    --------
    cagr : float
        The CAGR as a percentage
    """
    if entry_price <= 0 or exit_price <= 0 or years <= 0:
        return None
    
    cagr = (exit_price / entry_price) ** (1 / years) - 1
    return cagr * 100  # Convert to percentage

def process_events(price_data, trading_dates, events_df):
    """
    Process each event and calculate CAGR for different time horizons.
    
    Parameters:
    -----------
    price_data : pandas.DataFrame
        Processed price data
    trading_dates : list
        List of trading dates
    events_df : pandas.DataFrame
        DataFrame containing event names and dates
        
    Returns:
    --------
    results_df : pandas.DataFrame
        DataFrame containing the results
    """
    results = []
    
    for idx, row in events_df.iterrows():
        event_name = row['Event name']
        event_date = row['Event Date']
        
        print(f"\nProcessing event: {event_name} ({event_date.strftime('%Y-%m-%d')})")
        
        # Find the closest trading date to the event date
        closest_event_date = find_closest_trading_date(event_date, trading_dates)
        if closest_event_date is None:
            print(f"  No trading date found close to event date")
            continue
            
        # Find entry date (event date + 2 trading days)
        entry_date = find_trading_date_offset(closest_event_date, trading_dates, 2)
        if entry_date is None:
            print(f"  Not enough trading days after the event")
            continue
            
        # Get entry price
        entry_price = price_data.loc[price_data['Date'] == entry_date, 'Adj Close'].values[0]
        print(f"  Entry date: {entry_date.strftime('%Y-%m-%d')}, Entry price: {entry_price:.2f}")
        
        # Initialize result row
        result_row = {
            'Event': event_name,
            'Event Date': event_date.strftime('%Y-%m-%d'),
            'Entry Date': entry_date.strftime('%Y-%m-%d'),
            'Entry Price': entry_price
        }
        
        # Calculate CAGR for different time horizons
        for years in [1, 3, 5]:
            # Find exit date (entry date + years * 252 trading days)
            exit_date = find_trading_date_offset(entry_date, trading_dates, years * 252)
            
            if exit_date is not None:
                # Get exit price
                exit_price = price_data.loc[price_data['Date'] == exit_date, 'Adj Close'].values[0]
                
                # Calculate CAGR
                cagr = calculate_cagr(entry_price, exit_price, years)
                
                print(f"  {years}Y Exit date: {exit_date.strftime('%Y-%m-%d')}, "
                      f"Exit price: {exit_price:.2f}, CAGR: {cagr:.2f}%")
                
                result_row[f'{years}Y CAGR %'] = cagr
            else:
                print(f"  {years}Y Exit date: Not available")
                result_row[f'{years}Y CAGR %'] = "N/A"
                
        results.append(result_row)
    
    results_df = pd.DataFrame(results)
    return results_df

def main():
    # Define the file paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    docs_dir = os.path.join(base_dir, 'docs')
    
    price_file = os.path.join(data_dir, 'Geopolitical Risk v S&P500 returns - s&p500 daily returns 1950-2020.csv')
    events_file = os.path.join(docs_dir, 'events.txt')
    
    # Preprocess the price data
    price_data, trading_dates = preprocess_price_data(price_file)
    
    # Load the events
    events_df = load_events(events_file)
    
    # Process the events and calculate CAGR
    results_df = process_events(price_data, trading_dates, events_df)
    
    # Display the results
    print("\nResults:")
    print(results_df)
    
    # Save the results to a CSV file
    results_file = os.path.join(data_dir, 'cagr_results.csv')
    results_df.to_csv(results_file, index=False)
    print(f"\nResults saved to {results_file}")

if __name__ == "__main__":
    main() 