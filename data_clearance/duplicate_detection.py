#!/usr/bin/env python3
"""
Duplicate Detection and Removal Script
======================================
This script detects and removes duplicate records from the biomedical dataset.

Detection strategies:
1. Exact duplicates (all columns match)
2. Duplicates based on key columns (excluding potentially variable data)
3. Duplicates with a unique identifier (if available)
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuration
INPUT_FILE = 'data_clearance/output_cleaned.csv'
OUTPUT_FILE = 'data_clearance/output_no_duplicates.csv'
REPORT_FILE = 'data_clearance/duplicate_detection_report.txt'

def load_data(file_path):
    """Load the CSV file"""
    print(f"Loading data from: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records with {len(df.columns)} columns")
    return df

def detect_exact_duplicates(df):
    """
    Detect exact duplicates where all columns match
    """
    print("\n" + "="*80)
    print("1. EXACT DUPLICATE DETECTION (All columns match)")
    print("="*80)
    
    # Find duplicates
    duplicate_mask = df.duplicated(keep=False)
    num_duplicates = duplicate_mask.sum()
    
    print(f"Total records: {len(df)}")
    print(f"Duplicate records (including originals): {num_duplicates}")
    
    if num_duplicates > 0:
        # Show duplicate records
        duplicates = df[duplicate_mask].sort_values(by=list(df.columns))
        print(f"\nFound {len(duplicates)} duplicate rows:")
        print(duplicates)
        
        # Count unique duplicate groups
        duplicate_groups = df[duplicate_mask].groupby(list(df.columns)).size()
        print(f"\nNumber of unique duplicate groups: {len(duplicate_groups)}")
        print("\nDuplicate group sizes:")
        print(duplicate_groups)
        
        return duplicates, duplicate_mask
    else:
        print("No exact duplicates found!")
        return pd.DataFrame(), duplicate_mask

def detect_key_column_duplicates(df, key_columns):
    """
    Detect duplicates based on specific key columns
    
    Args:
        df: DataFrame
        key_columns: List of column names to use as unique identifier
    """
    print("\n" + "="*80)
    print(f"2. KEY COLUMN DUPLICATE DETECTION")
    print(f"Key columns: {key_columns}")
    print("="*80)
    
    # Find duplicates based on key columns
    duplicate_mask = df.duplicated(subset=key_columns, keep=False)
    num_duplicates = duplicate_mask.sum()
    
    print(f"Total records: {len(df)}")
    print(f"Duplicate records based on key columns: {num_duplicates}")
    
    if num_duplicates > 0:
        duplicates = df[duplicate_mask].sort_values(by=key_columns)
        print(f"\nFound {len(duplicates)} rows with duplicate key values:")
        print(duplicates)
        
        # Show which groups have duplicates
        duplicate_groups = df[duplicate_mask].groupby(key_columns).size()
        print(f"\nNumber of duplicate key groups: {len(duplicate_groups)}")
        print("\nDuplicate key combinations:")
        print(duplicate_groups[duplicate_groups > 1])
        
        return duplicates, duplicate_mask
    else:
        print(f"No duplicates found based on key columns!")
        return pd.DataFrame(), duplicate_mask

def detect_similar_records(df, threshold=0.9):
    """
    Detect potentially duplicate records that are very similar but not exact matches
    Uses similarity based on matching values across columns
    """
    print("\n" + "="*80)
    print("3. SIMILAR RECORD DETECTION (Fuzzy matching)")
    print("="*80)
    
    # This is a simplified approach - for full fuzzy matching you'd use libraries like fuzzywuzzy
    # Here we'll look for records that match on most columns
    
    potential_duplicates = []
    
    # Convert to string for comparison
    df_str = df.astype(str)
    
    for i in range(len(df)):
        if i % 20 == 0:
            print(f"Checking record {i}/{len(df)}...", end='\r')
        
        # Compare with subsequent rows
        for j in range(i+1, len(df)):
            # Count matching columns
            matches = (df_str.iloc[i] == df_str.iloc[j]).sum()
            similarity = matches / len(df.columns)
            
            if similarity >= threshold and similarity < 1.0:
                potential_duplicates.append({
                    'row1': i,
                    'row2': j,
                    'similarity': similarity,
                    'matching_columns': matches
                })
    
    print(f"\nFound {len(potential_duplicates)} potential similar record pairs (similarity >= {threshold})")
    
    if potential_duplicates:
        similar_df = pd.DataFrame(potential_duplicates)
        print("\nSimilar record pairs:")
        print(similar_df)
        return similar_df
    else:
        print("No similar records found!")
        return pd.DataFrame()

def remove_duplicates(df, strategy='first'):
    """
    Remove duplicates from DataFrame
    
    Args:
        df: DataFrame
        strategy: 'first' (keep first occurrence), 'last' (keep last), or None (remove all)
    """
    print("\n" + "="*80)
    print("4. DUPLICATE REMOVAL")
    print("="*80)
    
    original_count = len(df)
    
    # Remove exact duplicates
    df_clean = df.drop_duplicates(keep=strategy)
    
    removed_count = original_count - len(df_clean)
    
    print(f"Original records: {original_count}")
    print(f"Duplicate records removed: {removed_count}")
    print(f"Remaining records: {len(df_clean)}")
    print(f"Strategy used: Keep '{strategy}' occurrence")
    
    return df_clean, removed_count

def analyze_duplicate_patterns(df):
    """
    Analyze patterns in duplicates to understand why they exist
    """
    print("\n" + "="*80)
    print("5. DUPLICATE PATTERN ANALYSIS")
    print("="*80)
    
    # Check for duplicates in each column individually
    print("\nDuplicate values per column:")
    for col in df.columns:
        duplicates = df[col].duplicated(keep=False).sum()
        unique_values = df[col].nunique()
        total_values = len(df[col].dropna())
        
        if total_values > 0:
            duplicate_pct = (duplicates / len(df)) * 100
            print(f"  {col}: {duplicates} duplicates ({duplicate_pct:.1f}%) | {unique_values} unique values")

def generate_report(df_original, df_clean, duplicates_info, output_file):
    """
    Generate a comprehensive duplicate detection report
    """
    print("\n" + "="*80)
    print("6. GENERATING REPORT")
    print("="*80)
    
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("DUPLICATE DETECTION AND REMOVAL REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Original records: {len(df_original)}\n")
        f.write(f"Records after deduplication: {len(df_clean)}\n")
        f.write(f"Duplicates removed: {len(df_original) - len(df_clean)}\n")
        f.write(f"Duplicate percentage: {((len(df_original) - len(df_clean)) / len(df_original) * 100):.2f}%\n\n")
        
        if len(duplicates_info) > 0:
            f.write("DUPLICATE RECORDS FOUND\n")
            f.write("-" * 40 + "\n")
            f.write(duplicates_info.to_string())
            f.write("\n\n")
        
        f.write("COLUMN STATISTICS\n")
        f.write("-" * 40 + "\n")
        for col in df_original.columns:
            duplicates = df_original[col].duplicated(keep=False).sum()
            unique = df_original[col].nunique()
            f.write(f"{col}:\n")
            f.write(f"  - Unique values: {unique}\n")
            f.write(f"  - Duplicate values: {duplicates}\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"Report saved to: {output_file}")

def main():
    """Main execution function"""
    print("="*80)
    print("DUPLICATE DETECTION AND REMOVAL TOOL")
    print("="*80)
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Report file: {REPORT_FILE}\n")
    
    # Load data
    df = load_data(INPUT_FILE)
    
    # Display data overview
    print("\nData Overview:")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # 1. Detect exact duplicates
    exact_duplicates, exact_dup_mask = detect_exact_duplicates(df)
    
    # 2. Detect key column duplicates
    # For biomedical data, we might consider all demographic columns as key
    key_columns = ['Howoldareyou', 'MaritalStatus', 'Areyoumaleorfemale', 
                   'Whatisyourhighestlevelofeducation', 'Yourbodyweight', 'Yourheight']
    # Only use columns that exist
    key_columns = [col for col in key_columns if col in df.columns]
    
    key_duplicates, key_dup_mask = detect_key_column_duplicates(df, key_columns)
    
    # 3. Analyze duplicate patterns
    analyze_duplicate_patterns(df)
    
    # 4. Remove duplicates
    df_clean, removed_count = remove_duplicates(df, strategy='first')
    
    # 5. Generate report
    generate_report(df, df_clean, exact_duplicates, REPORT_FILE)
    
    # 6. Save cleaned data
    print("\n" + "="*80)
    print("7. SAVING CLEANED DATA")
    print("="*80)
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaned data saved to: {OUTPUT_FILE}")
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"✓ Original records: {len(df)}")
    print(f"✓ Cleaned records: {len(df_clean)}")
    print(f"✓ Duplicates removed: {removed_count}")
    print(f"✓ Data quality improved by: {(removed_count/len(df)*100):.2f}%")
    print(f"\nOutput files created:")
    print(f"  - {OUTPUT_FILE}")
    print(f"  - {REPORT_FILE}")
    print("="*80)

if __name__ == "__main__":
    main()
