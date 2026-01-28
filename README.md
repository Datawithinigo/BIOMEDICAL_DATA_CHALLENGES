# Biomedical Data Transformation Pipeline

A comprehensive Python-based data processing pipeline for biomedical health data, transforming raw SPSS (.sav) files or CSV files into clean, standardized datasets with calculated health metrics.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Workflow](#pipeline-workflow)
- [Data Transformations](#data-transformations)
- [File Structure](#file-structure)
- [Output Format](#output-format)
- [Examples](#examples)
- [Requirements](#requirements)

## 🎯 Overview

This project provides an end-to-end solution for processing biomedical survey data, including:
- Converting SPSS (.sav) files to CSV format
- Standardizing height measurements (supports meters, feet+inches, centimeters)
- Calculating Body Mass Index (BMI)
- Categorizing health status based on BMI
- Removing duplicates and invalid records
- Generating unique identifiers for each record

## ✨ Features

### Data Processing
- **Multi-format Input**: Supports both SPSS (.sav) and CSV input files
- **Intelligent Height Conversion**: Automatically detects and converts:
  - Meters → Centimeters
  - Feet with decimal inches (e.g., 5.8 = 5'8") → Centimeters
  - Centimeters (no conversion needed)
- **BMI Calculation**: Accurate BMI computation with health categorization
- **Data Quality**: Removes duplicates and filters invalid records
- **Marital Status Standardization**: "Divorced/separated" → "Divorced"

### Health Metrics
- **BMI Categories**:
  - Underweight: BMI < 18.5
  - Normal weight: 18.5 ≤ BMI < 25
  - Overweight: 25 ≤ BMI < 30
  - Obese: BMI ≥ 30

### Command-Line Interface
- Flexible processing modes (CSV or SAV)
- Built-in help documentation
- Progress tracking and detailed logging

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
cd /path/to/BIOMEDICAL_DATA_CHALLENGES
```

### Step 2: Install Required Packages

**For CSV processing only:**
```bash
pip install pandas numpy
```

**For SPSS (.sav) file processing:**
```bash
pip install pandas numpy pyreadstat
```

### Optional: Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

pip install pandas numpy pyreadstat
```

## 💻 Usage

### Basic Usage

**Process from CSV (default):**
```bash
python3 2_transform_data.py
```

**Process from SPSS file:**
```bash
python3 2_transform_data.py --sav
```

**Show help:**
```bash
python3 2_transform_data.py --help
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--sav`, `-s`, `--from-sav` | Process from SPSS (.sav) file |
| `--csv`, `-c`, `--from-csv` | Process from CSV file (default) |
| `--help`, `-h` | Show help message |

## 🔄 Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                             │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  SPSS File       │         │  CSV File        │         │
│  │  (.sav format)   │         │  (pre-cleaned)   │         │
│  └────────┬─────────┘         └────────┬─────────┘         │
│           │                            │                    │
│           └────────────┬───────────────┘                    │
│                        ▼                                    │
└────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 1: DATA LOADING                            │
│  • Load from SAV or CSV                                     │
│  • Convert SAV to CSV (if needed)                           │
│  • Save intermediate CSV                                    │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 2: DATA TRANSFORMATION PIPELINE                 │
│                                                              │
│  1. Height Standardization                                  │
│     • Convert all heights to centimeters                    │
│     • Handle meters, feet+inches, and cm                    │
│                                                              │
│  2. Duplicate Removal                                       │
│     • Identify and remove exact duplicates                  │
│                                                              │
│  3. Categorical Value Standardization                       │
│     • Capitalize marital status and gender                  │
│     • Standardize "Divorced/separated" to "Divorced"        │
│                                                              │
│  4. BMI Calculation                                         │
│     • Calculate: BMI = weight(kg) / height²(m)              │
│                                                              │
│  5. Weight Status Classification                            │
│     • Categorize based on BMI thresholds                    │
│                                                              │
│  6. Data Validation                                         │
│     • Remove records with missing critical values           │
│     • Filter invalid BMI values (<10 or >60)                │
│                                                              │
│  7. Sorting                                                 │
│     • Sort by height (descending)                           │
│                                                              │
│  8. ID Generation                                           │
│     • Generate unique @_id (8-digit random)                 │
│     • Add sequential @_index (1-based)                      │
│                                                              │
│  9. Column Reordering                                       │
│     • Arrange columns in final output format                │
│                                                              │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 3: SAVE FINAL OUTPUT                       │
│  • Create output directory (if needed)                      │
│  • Save cleaned data to CSV                                 │
│  • Display summary statistics                               │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT FILE                               │
│                                                              │
│              4_deliver/end_file.csv                          │
│  • 120 valid records (example)                              │
│  • 9 columns with calculated metrics                        │
│  • Sorted by height (descending)                            │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Data Transformations

### Height Conversion Logic

The pipeline intelligently detects and converts heights:

```python
# Detection Rules:
- Value >= 50    → Already in centimeters (no conversion)
- Value >= 3     → Feet with decimal inches
                   Example: 5.8 = 5 feet 8 inches
                   Conversion: (5 × 30.48) + (8 × 2.54) = 172.72 cm
- Value < 3      → Meters
                   Conversion: value × 100
```

### BMI Calculation

```
BMI = weight (kg) / [height (m)]²

Where:
- Weight is in kilograms
- Height is converted from cm to meters: height_m = height_cm / 100
```

### Weight Status Categories

| BMI Range | Category | Health Indication |
|-----------|----------|-------------------|
| < 18.5 | Underweight | Below healthy weight |
| 18.5 - 24.9 | Normal weight | Healthy weight range |
| 25.0 - 29.9 | Overweight | Above healthy weight |
| ≥ 30.0 | Obese | Significantly above healthy weight |

## 📁 File Structure

```
BIOMEDICAL_DATA_CHALLENGES/
│
├── 1_Source_data/
│   ├── Unclean data.sav           # Original SPSS data file
│   ├── Unclean data_comma.sav     # Alternative format
│   └── guide.md                   # Data dictionary
│
├── 2_data_clearance/
│   ├── input_cleaned.csv          # Intermediate CSV (after SAV conversion)
│   ├── output_no_duplicates.csv   # Deduplicated data
│   └── output_processed.csv       # Fully processed data
│
├── 3_processed_data/
│   ├── output.csv                 # Legacy processed files
│   ├── output.xlsx
│   └── inigo_arriazu_output_processed.xlsx
│
├── 4_deliver/
│   └── end_file.csv              # FINAL OUTPUT FILE ⭐
│
├── old_code/
│   └── process_data_executed.ipynb  # Legacy Jupyter notebooks
│
├── 1_procesing_sav_csv.py        # Legacy: SAV to CSV converter
├── 2_transform_data.py           # 🚀 MAIN SCRIPT
├── README.md                     # This file
└── README_transform.md           # Detailed transformation docs
```

## 📊 Output Format

### Column Specifications

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Howoldareyou` | float | Age in years | 29.0 |
| `MaritalStatus` | string | Marital status (capitalized) | "Married", "Single", "Divorced", "Windowed" |
| `Areyoumaleorfemale` | string | Gender (capitalized) | "Male", "Female" |
| `Yourbodyweight` | float | Weight in kilograms | 75.0 |
| `Yourheight` | float | Height in centimeters | 170.0 |
| `@_id` | integer | Unique 8-digit identifier | 95822412 |
| `@_index` | integer | Sequential index (1-based) | 1 |
| `BMI` | float | Calculated Body Mass Index | 25.95 |
| `weigthStatus` | string | BMI category | "Normal weight" |

### Sample Output

```csv
Howoldareyou,MaritalStatus,Areyoumaleorfemale,Yourbodyweight,Yourheight,@_id,@_index,BMI,weigthStatus
35.0,Windowed,Female,80.0,200.0,95822412,1,20.0,Normal weight
35.0,Single,Male,65.0,200.0,24942603,2,16.25,Underweight
28.0,Divorced,Male,73.0,200.0,13356886,3,18.25,Underweight
25.0,Divorced,Female,70.0,200.0,46913810,4,17.5,Underweight
29.0,Single,Male,100.0,190.0,42868828,5,27.70,Overweight
```

## 📖 Examples

### Example 1: Process Existing CSV
```bash
# Process the pre-cleaned CSV file
python3 2_transform_data.py

# Output:
# Mode: Processing from CSV file (default)
# ================================================================================
# BIOMEDICAL DATA TRANSFORMATION PIPELINE
# ================================================================================
# 
# ================================================================================
# STEP 1: LOADING CSV FILE
# ================================================================================
# Loading data from: .../2_data_clearance/input_cleaned.csv
#   - Loaded 132 records
# ...
# Final record count: 120
```

### Example 2: Process from SPSS File
```bash
# Process from the original SPSS file
python3 2_transform_data.py --sav

# Output:
# Mode: Processing from SPSS (.sav) file
# ================================================================================
# STEP 1: CONVERTING SPSS FILE TO CSV
# ================================================================================
# Loading SPSS file from: .../1_Source_data/Unclean data.sav
#   - Loaded 132 records from SPSS file
#   - Saved to CSV: .../2_data_clearance/input_cleaned.csv
# ...
```

### Example 3: View Height Conversion
```python
# Input heights (mixed units):
1.70    → 170.00 cm  (meters)
5.8     → 172.72 cm  (5 feet 8 inches)
170.0   → 170.00 cm  (already centimeters)
```

## 📦 Requirements

### Python Packages

```
pandas>=1.3.0
numpy>=1.20.0
pyreadstat>=1.1.0  # Optional: only for SPSS file processing
```

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.7 or higher
- **Memory**: Minimum 512 MB RAM
- **Disk Space**: Minimum 50 MB

## 🔍 Data Quality Report

### Processing Statistics (Example Run)

```
Input records:              132
Duplicates removed:         2
Invalid records removed:    10
Final valid records:        120

Weight Status Distribution:
- Overweight:    41 (31.5%)
- Obese:         41 (31.5%)
- Normal weight: 36 (27.7%)
- Underweight:    9 (6.9%)
```

### Data Validation Rules

1. **Required Fields**: Age, Gender, Weight, Height must not be null
2. **BMI Range**: Must be between 10 and 60 (filters out invalid values)
3. **Duplicates**: Exact duplicates are removed (keeps first occurrence)
4. **Type Validation**: All numeric fields converted to proper data types

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pyreadstat'`
```bash
Solution: pip install pyreadstat
```

**Issue**: `OSError: Cannot save file into a non-existent directory`
```bash
Solution: The script now automatically creates directories. 
Update to the latest version.
```

**Issue**: `TypeError: '>=' not supported between instances of 'str' and 'int'`
```bash
Solution: Ensure you're using the latest version with numeric type conversion.
```

## 📝 Notes

- The script uses a fixed random seed (42) for reproducible `@_id` generation
- Heights are sorted in descending order (tallest to shortest)
- The education column is excluded from the final output
- All categorical values are capitalized for consistency

## 👥 Author

Data Processing Pipeline  
Date: January 2026

## 📄 License

This project is part of biomedical research data processing initiatives.

## 🤝 Contributing

For improvements or bug reports, please document the issue with:
1. Input data sample
2. Expected output
3. Actual output
4. Error messages (if any)

---

**Last Updated**: January 29, 2026  
**Version**: 2.0  
**Status**: Production Ready ✅
