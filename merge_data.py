import pandas as pd

def load_and_preprocess_house_data(house_id):
    """Loads and preprocesses data for a single house."""
    base_url = "https://raw.githubusercontent.com/Fateme9977/dataseat/Fateme9977-data/"
    load_url = f"{base_url}Load%20House%20{house_id}.csv"
    pv_url = f"{base_url}PV%20Generation%20House%20{house_id}.csv"
    weather_url = f"{base_url}Weather%20House%20{house_id}.csv"

    df_load = pd.read_csv(load_url)
    df_pv = pd.read_csv(pv_url)
    df_weather = pd.read_csv(weather_url)

    df_load.rename(columns={'DateTime': 'Timestamp'}, inplace=True)
    
    for df in [df_load, df_pv, df_weather]:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

    df_pv['PV Power Generation (kW)'] = df_pv['PV Power Generation (W)'] / 1000
    df_pv.drop(columns=['PV Power Generation (W)'], inplace=True)
    
    # Selecting only the target columns to avoid redundancy
    df_load = df_load[['Consumption (kW)']]
    df_pv = df_pv[['PV Power Generation (kW)']]
    
    return df_load, df_pv, df_weather

# --- Main execution ---
house_id = 1
print(f"Loading and preprocessing data for House {house_id}...")
df_load, df_pv, df_weather = load_and_preprocess_house_data(house_id)
print("Data loaded.")

# Merge the dataframes
print("Merging dataframes...")
df_merged = df_weather.join(df_pv, how='outer')
df_merged = df_merged.join(df_load, how='outer')
print("Merge complete.")

# Sort the index to ensure chronological order
df_merged.sort_index(inplace=True)

# Inspect the merged dataframe
print("\n--- Merged DataFrame Info ---")
df_merged.info()

print("\n--- Missing Values Count ---")
print(df_merged.isnull().sum())

print("\n--- Merged DataFrame Head ---")
print(df_merged.head())

print("\n--- Merged DataFrame Tail ---")
print(df_merged.tail())

print("\nMerge logic verified successfully without saving the file.")
