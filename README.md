# Geopolitical Risk and S&P 500 Returns Analysis

This project analyzes the impact of major geopolitical events on S&P 500 returns by calculating the Compound Annual Growth Rate (CAGR) at different time horizons after each event.

## Project Structure

```
geo-risk-snp/
├── data/
│   ├── Geopolitical Risk v S&P500 returns - s&p500 daily returns 1950-2020.csv  # Raw price data
│   └── cagr_results.csv  # Calculated CAGR results
├── docs/
│   └── events.txt  # List of geopolitical events
├── results/
│   ├── cagr_by_event.png  # Bar chart visualization
│   ├── cagr_heatmap.png  # Heatmap visualization
│   └── cagr_time_series.png  # Time series visualization
├── src/
│   ├── preprocess.py  # Script to preprocess the price data
│   ├── cagr_calculator.py  # Script to calculate CAGR for each event
│   └── visualize_results.py  # Script to visualize the results
├── tasks.md  # Project tasks and pseudocode
└── README.md  # This file
```

## Methodology

For each geopolitical event:

1. The entry date is determined as 2 trading days after the event.
2. The entry price is the S&P 500 Adjusted Close price on the entry date.
3. CAGR is calculated for 1-year, 3-year, and 5-year horizons using the formula:
   ```
   CAGR = (exit_price / entry_price) ^ (1 / years) - 1
   ```

## Results

The analysis has calculated CAGR for the following geopolitical events:
- Korean War Begins (1950)
- Suez Canal Crisis (1956)
- Cuban Missile Crisis (1962)
- JFK Assassinated (1963)
- Arab Oil Embargo (1973)
- President Nixon Resigns (1974)
- Iranian Hostage Crisis (1979)
- U.S.S.R. Invades Afghanistan (1979)
- U.S. Invades Panama (1989)

The results are visualized in three different formats:
1. Bar chart comparing CAGR across events
2. Heatmap showing CAGR by event and time horizon
3. Time series showing how CAGR varies over time

## Running the Code

1. To preprocess the data:
   ```
   python src/preprocess.py
   ```

2. To calculate CAGR:
   ```
   python src/cagr_calculator.py
   ```

3. To generate visualizations:
   ```
   python src/visualize_results.py
   ```

## Dependencies

- pandas
- numpy
- matplotlib
- seaborn 