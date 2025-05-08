# CAGR Calculation for Geopolitical Events

## Pseudocode Tasks

### STEP 1: Preprocess
- Convert "Date" column in price_data to datetime format.
- Sort price_data by Date (if not already sorted).
- Create a list or array of trading dates from price_data.

### STEP 2: For each event_date in event_dates:

1. Find entry date:
   - Locate the trading date that is event_date + 2 trading days.
   - If not enough trading days ahead, skip this event.

2. Get entry price:
   - Adj Close price on the entry date.

3. For each horizon in [1 year, 3 years, 5 years]:
   
   a. Calculate the exit date:
      - Find the trading date that is entry date + (years * 252 trading days).
        (Alternatively, find the calendar date + years and then choose the closest trading date.)
   
   b. If exit date is available:
      - Get exit price (Adj Close on exit date).
      
      - Calculate CAGR:
          CAGR = (exit_price / entry_price) ** (1 / years) - 1
      
      - Convert CAGR to %:
          CAGR_percent = CAGR * 100
   
   c. If exit date not available:
      - Record CAGR as "N/A".

### STEP 3: Store Results
- For each event, create a row:
    ["Event Date", "Entry Date", "Entry Price", "1Y CAGR %", "3Y CAGR %", "5Y CAGR %"]

### STEP 4: Output final results table.

## TODO List
- [x] Upload price data CSV to the data directory
- [x] Create project directory structure
- [x] Create events documentation
- [x] Create tasks documentation
- [x] Create script to preprocess the data
- [x] Implement CAGR calculation logic
- [x] Generate results table
- [x] Visualize results 