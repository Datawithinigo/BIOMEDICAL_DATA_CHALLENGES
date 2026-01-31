#!/usr/bin/env python3
"""
Biomedical Data Transformation Script
Complete pipeline: SAV → CSV → Cleaned → Final output

Steps:
1. Convert SPSS (.sav) file to CSV
2. Transform and clean the data
3. Generate final output file

Author: Data Processing Pipeline
Date: 2026-01-29
"""

import pandas as pd
import numpy as np
import random
import os
import sys


def load_sav_file(input_path, output_path):
    """
    Load SPSS (.sav) file and convert to CSV
    
    Args:
        input_path: Path to the .sav file
        output_path: Path where the CSV will be saved
    
    Returns:
        DataFrame with the loaded data
    """
    print(f"Loading SPSS file from: {input_path}")
    
    try:
        # Read SPSS file
        df = pd.read_spss(input_path, convert_categoricals=True)
        print(f"  - Loaded {len(df)} records from SPSS file")
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"  - Saved to CSV: {output_path}")
        
        return df
    except Exception as e:
        print(f"  - Error loading SPSS file: {e}")
        raise


def load_data(input_path):
    """Load the input CSV file"""
    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"  - Loaded {len(df)} records")
    return df


def standardize_height_to_cm(df):
    """
    Standardize all heights to centimeters
    - Values >= 50: Already in centimeters -> no conversion
    - Values >= 3: Feet with decimal inches (e.g., 5.8 = 5 feet 8 inches) -> convert to cm
    - Values < 3: Meters -> convert to cm
    
    Conversion factors:
    - 1 foot = 30.48 cm
    - 1 inch = 2.54 cm
    - 1 meter = 100 cm
    """
    print("\nStandardizing heights to centimeters...")
    
    # Convert height column to numeric, handling any string values
    df['Yourheight'] = pd.to_numeric(df['Yourheight'], errors='coerce')
    
    def convert_height(height):
        if pd.isna(height):
            return np.nan
        elif height >= 50:  # Already in centimeters
            return height
        elif height >= 3:   # Feet with decimal inches (e.g., 5.8 = 5 feet 8 inches)
            feet = int(height)  # Extract whole feet
            inches = round((height - feet) * 10)  # Extract inches from decimal
            # Convert to centimeters: (feet * 30.48) + (inches * 2.54)
            return (feet * 30.48) + (inches * 2.54)
        else:  # Already in meters
            return height * 100  # Convert meters to centimeters
    
    df['Yourheight'] = df['Yourheight'].apply(convert_height)
    print(f"  - Height range: {df['Yourheight'].min():.2f}cm - {df['Yourheight'].max():.2f}cm")
    return df


def remove_duplicates(df):
    """Remove duplicate records"""
    print("\nRemoving duplicates...")
    initial_count = len(df)
    df = df.drop_duplicates(keep='first')
    removed = initial_count - len(df)
    print(f"  - Removed {removed} duplicate records")
    print(f"  - Remaining records: {len(df)}")
    return df


def capitalize_categorical_values(df):
    """Capitalize first letter of categorical values and standardize marital status"""
    print("\nCapitalizing categorical values...")
    
    # Capitalize marital status
    df['MaritalStatus'] = df['MaritalStatus'].str.capitalize()
    
    # Replace "Divorced/separated" with "Divorced"
    df['MaritalStatus'] = df['MaritalStatus'].str.replace('Divorced/separated', 'Divorced', regex=False)
    
    # Capitalize gender
    df['Areyoumaleorfemale'] = df['Areyoumaleorfemale'].str.capitalize()
    
    print("  - Marital status and gender values capitalized")
    print("  - 'Divorced/separated' standardized to 'Divorced'")
    return df


def calculate_bmi(df):
    """
    Calculate BMI (Body Mass Index)
    BMI = weight (kg) / (height (m))^2
    Since height is in cm, we convert to meters: height_m = height_cm / 100
    """
    print("\nCalculating BMI...")
    
    # Ensure numeric columns are properly typed
    df['Howoldareyou'] = pd.to_numeric(df['Howoldareyou'], errors='coerce')
    df['Yourbodyweight'] = pd.to_numeric(df['Yourbodyweight'], errors='coerce')
    
    # Convert height from cm to meters for BMI calculation
    height_in_meters = df['Yourheight'] / 100
    df['BMI'] = df['Yourbodyweight'] / (height_in_meters ** 2)
    print(f"  - BMI calculated for all records")
    print(f"  - BMI range: {df['BMI'].min():.2f} - {df['BMI'].max():.2f}")
    return df


def categorize_weight_status(bmi):
    """
    Categorize weight status based on BMI
    - BMI < 18.5: Underweight
    - BMI 18.5-24.9: Normal weight
    - BMI 25-29.9: Overweight
    - BMI >= 30: Obese
    """
    if pd.isna(bmi):
        return 'Unknown'
    elif bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'


def add_weight_status(df):
    """Add weight status column based on BMI"""
    print("\nCategorizing weight status...")
    df['weigthStatus'] = df['BMI'].apply(categorize_weight_status)
    
    # Print distribution
    print("  - Weight status distribution:")
    for status, count in df['weigthStatus'].value_counts().items():
        print(f"    * {status}: {count} ({count/len(df)*100:.1f}%)")
    
    return df


def filter_valid_records(df):
    """Filter out records with missing critical values"""
    print("\nFiltering valid records...")
    initial_count = len(df)
    
    # Remove records with missing age, gender, weight, or height
    df = df.dropna(subset=['Howoldareyou', 'Areyoumaleorfemale', 
                           'Yourbodyweight', 'Yourheight'])
    
    # Remove records with invalid BMI (too low or too high)
    df = df[(df['BMI'] >= 10) & (df['BMI'] <= 60)]
    
    removed = initial_count - len(df)
    print(f"  - Removed {removed} records with missing or invalid values")
    print(f"  - Valid records: {len(df)}")
    return df


def add_id_columns(df):
    """Add @_id and @_index columns"""
    print("\nAdding ID columns...")
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Generate random IDs (8-digit numbers)
    random.seed(42)  # For reproducibility
    df['@_id'] = [random.randint(10000000, 99999999) for _ in range(len(df))]
    
    # Add index column (1-based)
    df['@_index'] = range(1, len(df) + 1)
    
    print(f"  - Generated unique IDs for {len(df)} records")
    return df


def sort_by_height_descending(df):
    """Sort records by height in descending order"""
    print("\nSorting by height (descending)...")
    df = df.sort_values('Yourheight', ascending=False)
    df = df.reset_index(drop=True)
    print("  - Records sorted by height")
    return df


def reorder_columns(df):
    """Reorder columns to match the output format"""
    print("\nReordering columns...")
    
    # Select and reorder columns (remove education column)
    column_order = [
        'Howoldareyou',
        'MaritalStatus',
        'Areyoumaleorfemale',
        'Yourbodyweight',
        'Yourheight',
        '@_id',
        '@_index',
        'BMI',
        'weigthStatus'
    ]
    
    df = df[column_order]
    print("  - Columns reordered")
    return df


def save_output(df, output_path):
    """Save the transformed data to CSV"""
    print(f"\nSaving output to: {output_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  - Created output directory: {output_dir}")
    
    df.to_csv(output_path, index=False)
    print(f"  - Saved {len(df)} records")
    print("  - Transformation completed successfully!")


def convert_csv_to_sav(csv_path, sav_output_path):
    """
    Convert CSV file to SPSS (.sav) format
    
    Args:
        csv_path: Path to the input CSV file
        sav_output_path: Path where the .sav file will be saved
    """
    print(f"\nConverting CSV to SPSS format...")
    print(f"  - Reading CSV from: {csv_path}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)
        print(f"  - Loaded {len(df)} records from CSV")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(sav_output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"  - Created output directory: {output_dir}")
        
        # Convert and save to SPSS format
        # Note: We need to use pyreadstat for better SAV writing support
        try:
            import pyreadstat
            
            # SPSS variable names cannot start with special characters
            # Rename columns that start with @ to valid SPSS names
            column_mapping = {
                '@_id': 'id',
                '@_index': 'index'
            }
            df = df.rename(columns=column_mapping)
            print(f"  - Renamed columns for SPSS compatibility: '@_id' -> 'id', '@_index' -> 'index'")
            
            # Prepare column labels (optional metadata)
            column_labels = {
                'Howoldareyou': 'How old are you',
                'MaritalStatus': 'Marital Status',
                'Areyoumaleorfemale': 'Are you male or female',
                'Yourbodyweight': 'Your body weight (kg)',
                'Yourheight': 'Your height (cm)',
                'id': 'Unique ID',
                'index': 'Record Index',
                'BMI': 'Body Mass Index',
                'weigthStatus': 'Weight Status Category'
            }
            
            # Write to SPSS format
            pyreadstat.write_sav(df, sav_output_path, column_labels=column_labels)
            print(f"  - Successfully saved to: {sav_output_path}")
            print(f"  - Converted {len(df)} records to SPSS format")
            
        except ImportError:
            print("  - Warning: pyreadstat not available, using pandas fallback")
            # Fallback: Use pandas (may have limitations)
            # Note: This requires statsmodels to be installed
            from pandas.io.stata import StataWriter
            # For SAV format, we'll try to use the to_stata as a workaround
            # However, direct SAV writing requires pyreadstat
            print("  - Error: Direct SAV conversion requires 'pyreadstat' package")
            print("  - Please install it with: pip install pyreadstat")
            raise ImportError("pyreadstat package is required for SAV conversion")
            
    except Exception as e:
        print(f"  - Error during CSV to SAV conversion: {e}")
        raise


def main(process_from_sav=False):
    """
    Main transformation pipeline
    
    Args:
        process_from_sav: If True, starts from .sav file. If False, starts from CSV.
    """
    print("="*80)
    print("BIOMEDICAL DATA TRANSFORMATION PIPELINE")
    print("="*80)
    
    # File paths
    sav_input_path = '/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/1_Source_data/Unclean data.sav'
    intermediate_csv_path = '/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/2_data_clearance/input_cleaned.csv'
    final_output_path = '/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/3_deliver/end_file.csv'
    
    # Step 1: Load data (from SAV or CSV)
    if process_from_sav:
        print("\n" + "="*80)
        print("STEP 1: CONVERTING SPSS FILE TO CSV")
        print("="*80)
        df = load_sav_file(sav_input_path, intermediate_csv_path)
    else:
        print("\n" + "="*80)
        print("STEP 1: LOADING CSV FILE")
        print("="*80)
        df = load_data(intermediate_csv_path)
    
    # Step 2: Data Transformation Pipeline
    print("\n" + "="*80)
    print("STEP 2: DATA TRANSFORMATION PIPELINE")
    print("="*80)
    
    df = standardize_height_to_cm(df)
    df = remove_duplicates(df)
    df = capitalize_categorical_values(df)
    df = calculate_bmi(df)
    df = add_weight_status(df)
    df = filter_valid_records(df)
    df = sort_by_height_descending(df)
    df = add_id_columns(df)
    df = reorder_columns(df)
    
    # Step 3: Save output
    print("\n" + "="*80)
    print("STEP 3: SAVING FINAL OUTPUT")
    print("="*80)
    save_output(df, final_output_path)
    
    # Step 4: Convert CSV to SAV format
    print("\n" + "="*80)
    print("STEP 4: CONVERTING CSV TO SPSS FORMAT")
    print("="*80)
    sav_output_path = '/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/4_convert_to_sav/end_file.sav'
    try:
        convert_csv_to_sav(final_output_path, sav_output_path)
    except Exception as e:
        print(f"Warning: Could not complete SAV conversion: {e}")
        print("Note: The CSV output is still available at:", final_output_path)
    
    # Final Summary
    print("\n" + "="*80)
    print("TRANSFORMATION SUMMARY")
    print("="*80)
    if process_from_sav:
        print(f"Source file: {sav_input_path}")
        print(f"Intermediate CSV: {intermediate_csv_path}")
    else:
        print(f"Input file:  {intermediate_csv_path}")
    print(f"CSV output:  {final_output_path}")
    print(f"SAV output:  {sav_output_path}")
    print(f"Final record count: {len(df)}")
    print(f"\nSample of transformed data:")
    print(df.head(10).to_string())
    print("="*80)


if __name__ == "__main__":
    # Check command-line arguments
    process_from_sav = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--sav', '-s', '--from-sav']:
            process_from_sav = True
            print("\nMode: Processing from SPSS (.sav) file")
        elif sys.argv[1] in ['--csv', '-c', '--from-csv']:
            process_from_sav = False
            print("\nMode: Processing from CSV file")
        elif sys.argv[1] in ['--help', '-h']:
            print("\nBiomedical Data Transformation Script")
            print("=" * 50)
            print("\nUsage:")
            print("  python3 2_transform_data.py [OPTIONS]")
            print("\nOptions:")
            print("  --sav, -s, --from-sav    Process from SPSS (.sav) file")
            print("  --csv, -c, --from-csv    Process from CSV file (default)")
            print("  --help, -h               Show this help message")
            print("\nExamples:")
            print("  python3 2_transform_data.py              # Process from CSV")
            print("  python3 2_transform_data.py --sav        # Process from SAV")
            print("  python3 2_transform_data.py --from-csv   # Process from CSV")
            sys.exit(0)
        else:
            print(f"\nUnknown option: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    else:
        print("\nMode: Processing from CSV file (default)")
    
    # Run the pipeline
    main(process_from_sav=process_from_sav)
