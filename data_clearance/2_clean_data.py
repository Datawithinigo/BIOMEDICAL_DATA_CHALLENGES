#!/usr/bin/env python3
"""
Data Cleaning Script
This script cleans the output.csv file by:
1. Converting all text values to lowercase
2. Stripping leading/trailing whitespace
3. Saving the cleaned data to a new file
"""

import pandas as pd
import os

def clean_data(input_file, output_file):
    """
    Clean the data by converting to lowercase and removing extra spaces.
    
    Parameters:
    -----------
    input_file : str
        Path to the input CSV file
    output_file : str
        Path to save the cleaned CSV file
    """
    # Read the CSV file
    print(f"Reading data from: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Original shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Select only the required columns
    required_columns = [
        'Howoldareyou',
        'MaritalStatus', 
        'Areyoumaleorfemale',
        'Whatisyourhighestlevelofeducation',
        'Yourbodyweight',
        'Yourheight'
    ]
    
    print(f"\nSelecting required columns: {required_columns}")
    df = df[required_columns]
    
    # Clean the data
    print("\nCleaning data...")
    
    # Process each column
    for col in df.columns:
        # For object (string) columns, convert to lowercase and strip whitespace
        if df[col].dtype == 'object':
            # Strip whitespace first
            df[col] = df[col].astype(str).str.strip()
            # Convert to lowercase
            df[col] = df[col].str.lower()
            # Replace 'nan' string back to actual NaN
            df[col] = df[col].replace('nan', pd.NA)
            
            print(f"  - Cleaned column: {col}")
    
    # Save the cleaned data
    print(f"\nSaving cleaned data to: {output_file}")
    df.to_csv(output_file, index=False)
    
    print(f"✓ Cleaning complete!")
    print(f"✓ Cleaned data saved to: {output_file}")
    print(f"✓ Total rows: {len(df)}")
    print(f"✓ Total columns: {len(df.columns)}")
    
    # Show sample of cleaned data
    print("\nSample of cleaned data (first 5 rows):")
    print(df.head())
    
    # Show unique values for key columns
    print("\nUnique values in key columns:")
    key_cols = ['areyoumaleorfemale', 'maritalstatus', 'whatisyourhighestlevelofeducation']
    for col in key_cols:
        if col in df.columns:
            unique_vals = df[col].dropna().unique()
            print(f"  - {col}: {sorted(unique_vals)}")
    
    return df

if __name__ == "__main__":
    # Define file paths
    input_file = "processed_data/output.csv"
    output_file = "data_clearance/output_cleaned.csv"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        exit(1)
    
    # Clean the data
    cleaned_df = clean_data(input_file, output_file)
    
    print("\n" + "="*60)
    print("Data cleaning completed successfully!")
    print("="*60)
