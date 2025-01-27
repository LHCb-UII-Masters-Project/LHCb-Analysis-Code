import os
import pandas as pd

def combine_csv_files():
    # Define the range of filenames
    filenames = [f"LambdacCompIP{i}.csv" for i in range(8)]
    
    # Check if all files exist
    missing_files = [file for file in filenames if not os.path.exists(file)]
    if missing_files:
        print(f"Error: The following files are missing: {', '.join(missing_files)}")
        return

    # Combine the CSV files
    combined_data = pd.concat([pd.read_csv(file) for file in filenames], ignore_index=True)

    # Save the combined data to a new CSV file
    output_filename = "Combined_LambdacCompIP.csv"
    combined_data.to_csv(output_filename, index=False)
    print(f"Successfully combined CSV files into '{output_filename}'.")

if __name__ == "__main__":
    combine_csv_files()