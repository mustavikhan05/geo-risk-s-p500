import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_results(results_file):
    """
    Load the CAGR results from a CSV file.
    
    Parameters:
    -----------
    results_file : str
        Path to the results CSV file
        
    Returns:
    --------
    results_df : pandas.DataFrame
        DataFrame containing the CAGR results
    """
    print(f"Loading results from {results_file}")
    results_df = pd.read_csv(results_file)
    print(f"Loaded results for {len(results_df)} events")
    return results_df

def plot_cagr_by_event(results_df, output_dir):
    """
    Create a bar chart of CAGR values by event.
    
    Parameters:
    -----------
    results_df : pandas.DataFrame
        DataFrame containing the CAGR results
    output_dir : str
        Directory to save the plots
    """
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Extract CAGR columns and event names
    cagr_columns = [col for col in results_df.columns if 'CAGR' in col]
    events = results_df['Event']
    
    # Convert CAGR columns to numeric (handling non-numeric values)
    for col in cagr_columns:
        results_df[col] = pd.to_numeric(results_df[col], errors='coerce')
    
    # Set up bar positions
    x = np.arange(len(events))
    width = 0.25  # Width of the bars
    
    # Create bars for each time horizon
    plt.bar(x - width, results_df['1Y CAGR %'], width, label='1 Year')
    plt.bar(x, results_df['3Y CAGR %'], width, label='3 Years')
    plt.bar(x + width, results_df['5Y CAGR %'], width, label='5 Years')
    
    # Add labels and title
    plt.xlabel('Geopolitical Event')
    plt.ylabel('CAGR (%)')
    plt.title('Compound Annual Growth Rate (CAGR) After Geopolitical Events')
    plt.xticks(x, events, rotation=45, ha='right')
    plt.legend()
    
    # Add a horizontal line at y=0
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'cagr_by_event.png')
    plt.savefig(output_file, dpi=300)
    print(f"Saved plot to {output_file}")
    plt.close()

def plot_cagr_heatmap(results_df, output_dir):
    """
    Create a heatmap of CAGR values.
    
    Parameters:
    -----------
    results_df : pandas.DataFrame
        DataFrame containing the CAGR results
    output_dir : str
        Directory to save the plots
    """
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Extract CAGR columns and event names
    cagr_columns = [col for col in results_df.columns if 'CAGR' in col]
    
    # Create a pivot table for the heatmap
    heatmap_data = results_df[['Event'] + cagr_columns].set_index('Event')
    
    # Convert to numeric (handling non-numeric values)
    heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')
    
    # Create the heatmap
    sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', center=0, fmt='.1f', 
                linewidths=0.5, cbar_kws={'label': 'CAGR (%)'})
    
    # Add title
    plt.title('CAGR Heatmap by Geopolitical Event and Time Horizon')
    
    # Adjust layout and save
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'cagr_heatmap.png')
    plt.savefig(output_file, dpi=300)
    print(f"Saved heatmap to {output_file}")
    plt.close()

def plot_time_series(results_df, output_dir):
    """
    Create a time series plot of CAGR values.
    
    Parameters:
    -----------
    results_df : pandas.DataFrame
        DataFrame containing the CAGR results
    output_dir : str
        Directory to save the plots
    """
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Convert Event Date to datetime
    results_df['Event Date'] = pd.to_datetime(results_df['Event Date'])
    
    # Sort by event date
    results_df = results_df.sort_values('Event Date')
    
    # Extract CAGR columns
    cagr_columns = [col for col in results_df.columns if 'CAGR' in col]
    
    # Convert CAGR columns to numeric (handling non-numeric values)
    for col in cagr_columns:
        results_df[col] = pd.to_numeric(results_df[col], errors='coerce')
    
    # Plot each CAGR line
    for col in cagr_columns:
        plt.plot(results_df['Event Date'], results_df[col], marker='o', linewidth=2, label=col)
    
    # Add labels and title
    plt.xlabel('Event Date')
    plt.ylabel('CAGR (%)')
    plt.title('CAGR Over Time for Different Geopolitical Events')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Add annotations for each event
    for idx, row in results_df.iterrows():
        plt.annotate(row['Event'], 
                     (row['Event Date'], results_df.loc[idx, '1Y CAGR %']),
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center',
                     fontsize=8,
                     rotation=45)
    
    # Add a horizontal line at y=0
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'cagr_time_series.png')
    plt.savefig(output_file, dpi=300)
    print(f"Saved time series plot to {output_file}")
    plt.close()

def main():
    # Define the file paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Create output directory for plots
    output_dir = os.path.join(base_dir, 'results')
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the CAGR results
    results_file = os.path.join(data_dir, 'cagr_results.csv')
    results_df = load_results(results_file)
    
    # Generate plots
    plot_cagr_by_event(results_df, output_dir)
    plot_cagr_heatmap(results_df, output_dir)
    plot_time_series(results_df, output_dir)
    
    print("Visualization complete!")

if __name__ == "__main__":
    main() 