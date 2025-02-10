import pandas as pd
import os

def convert(input_file):
    # Reading CSV downloaded from flightradar24
    df_flightcsv = pd.read_csv(input_file)
    
    # Split the Position into longitude and latitude
    df_flightcsv[['latitude', 'longitude']] = df_flightcsv['Position'].str.split(',', expand=True)
    df_flightcsv['latitude'] = df_flightcsv['latitude'].astype(float)
    df_flightcsv['longitude'] = df_flightcsv['longitude'].astype(float)
    
    # Convert altitude from feet to meters
    df_flightcsv['Altitude'] = df_flightcsv['Altitude'] * 0.3048
    
    # Create a DataFrame to match FootPrint app format
    df_converted = pd.DataFrame({
        'dataTime': df_flightcsv['Timestamp'],
        'locType': 1,  # Default
        'longitude': df_flightcsv['longitude'],
        'latitude': df_flightcsv['latitude'],
        'heading': df_flightcsv['Direction'],
        'accuracy': 10,  # Default
        'speed': df_flightcsv['Speed'],
        'distance': 0.0,  # Default
        'isBackForeground': 1,  # Default
        'stepType': 0,  # Default
        'altitude': df_flightcsv['Altitude']
    })
    
    return df_converted

def batch_convert(input_folder, output_file):
    all_data = []
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_file = os.path.join(input_folder, file_name)
            df_converted = convert(input_file)
            all_data.append(df_converted)
    
    # Merge all data into a single DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv(output_file, index=False)
        print(f"Finished Conversion: {output_file}")
    else:
        print("No CSV files found in the input folder.")

if __name__ == "__main__":
    input_folder = "flight"  # Folder containing flight CSVs
    output_file = "FootPrint/merged_data.csv"  # Combined output CSV file
    batch_convert(input_folder, output_file)
