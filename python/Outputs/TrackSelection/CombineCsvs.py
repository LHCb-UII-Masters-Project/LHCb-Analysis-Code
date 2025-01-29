import os
import pandas as pd

from os import listdir
from os.path import isfile, join


def combine_csv_files():
    # Define the range of filenames
    directory = "/home/user294/Documents/selections/python/Outputs/TrackSelection"
    onlyfiles = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.csv')]
    # Check if all files exist
    #missing_files = [file for file in onlyfiles if not os.path.exists(file)]
   # if missing_files:
        #print(f"Error: The following files are missing: {', '.join(missing_files)}")
        #return

    # Combine the CSV files
    combined_data = pd.concat([pd.read_csv(file) for file in onlyfiles], ignore_index=True)

    # Save the combined data to a new CSV file
    output_filename = "Combined_LambdacCompIP.csv"
    combined_data.to_csv(join(directory, output_filename), index=False)
    #print(f"Successfully combined CSV files into '{output_filename}'.")

if __name__ == "__main__":
    combine_csv_files()