## Summary of the video transcript (what it teaches)
you need to create a jupyter notebook and run for process the file :/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/data_clearance/output_cleaned.csv   using the guide : /Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/guide.md


* **“Garbage in, garbage out”**: if your dataset is messy, your analysis and decisions will be unreliable.
* **Data cleaning** = preparing data for analysis by removing/modifying data that is **incorrect, incomplete, irrelevant, duplicated, or improperly formatted**.
* The video walks through **7 common data quality issues** (shown in SPSS, but transferable to Python/Jupyter):

  1. **Irrelevant data** (unneeded columns or rows)
  2. **Incorrect data formats** (numbers stored as text, wrong decimals, etc.)
  3. **Duplicates** (same record repeated)
  4. **Structural issues** (typos, inconsistent capitalization, extra spaces)
  5. **Categorical strings not coded** (convert text categories into numeric codes for analysis)
  6. **Outliers** (extreme values; may be invalid or valid but influential)
  7. **Missing values** (no single best fix; depends on your goal)

---

## Jupyter Notebook guide (step-by-step) to process the data like in the video

Below is a clean notebook structure you can follow. It’s written as **student instructions**: create these sections in your notebook and implement each step.

---

### 0) Notebook setup and dataset load

**Goal:** import libraries, load the dataset, and inspect it.

**What to do:**

* Import: `pandas`, `numpy`, and plotting libs (`matplotlib`).
* Load your file (CSV/Excel).
* Print:

  * shape (rows, cols)
  * column names
  * `head()`
  * `info()` (types + missingness)

**Outputs you should include:**

* A short “Initial audit” cell showing: dataset dimensions, dtypes, and missing values per column.

---

### 1) Remove irrelevant variables (columns)

**Goal:** drop columns not needed for your analysis (like Kobo/metadata fields: start/end time, uuid, submission time, validation status, tags, etc.).

**What to do:**

* Decide which columns are metadata.
* Keep a unique identifier column if useful (the video kept an `index`-like field).

**Notebook actions:**

* Create a list: `irrelevant_cols = [...]`
* Drop them with `df.drop(columns=irrelevant_cols)`

**Outputs to include:**

* Before/after column count
* A printed list of removed columns

---

### 2) Remove irrelevant cases (rows)

**Goal:** filter dataset to only the population you want (video example: only people who completed tertiary education).

**What to do:**

* Filter rows using a condition on a column (e.g., `education_level == "Tertiary"`).
* Don’t delete blindly: keep a backup copy (or write to a new dataframe).

**Notebook actions:**

* `df_filtered = df[df["education_level"] == "Tertiary"].copy()`
* If a column becomes constant (only one unique value), drop it (video dropped education column after filtering).

**Outputs to include:**

* Rows before/after
* `value_counts()` for the filtering variable to prove the filter worked

---

### 3) Fix incorrect data formats

**Goal:** ensure numeric fields are numeric (age, weight, height), not text.

**What to do:**

* Identify columns that should be numeric.
* Convert them using `pd.to_numeric(..., errors="coerce")`.
* Set decimal expectations (e.g., weight may have 1 decimal).

**Notebook actions:**

* Convert: `age`, `weight`, `height`
* After conversion: check `df.dtypes` and count how many values became NaN due to coercion.

**Outputs to include:**

* `df[numeric_cols].describe()`
* counts of conversion failures per column

---

### 4) Detect and remove duplicates

**Goal:** find duplicated records using a unique ID (like the video’s `index`).

**What to do:**

* If you have a unique identifier column: check duplicates on it.
* If not, use a combination of columns that should uniquely identify a record.

**Notebook actions:**

* `dup_mask = df.duplicated(subset=["index"], keep="last")` (mirrors SPSS “keep last as primary”)
* Remove duplicates:

  * `df = df[~dup_mask].copy()`

**Outputs to include:**

* Number of duplicates found
* Rows before/after deduplication

---

### 5) Fix structural issues (typos, casing, extra spaces)

**Goal:** normalize string/categorical fields so categories are consistent (example: `Female` vs `female`).

**What to do:**

* For relevant categorical columns:

  * strip spaces
  * standardize case (often `.str.title()` or `.str.upper()` depending on preference)
* Use frequency tables (`value_counts`) to detect weird variants.

**Notebook actions:**

* Example:

  * `df["sex_raw"] = df["sex"].copy()` (optional audit)
  * `df["sex"] = df["sex"].str.strip()`
  * `df["sex"] = df["sex"].str.capitalize()` (so “female” → “Female”)

**Outputs to include:**

* `value_counts()` before and after cleaning for at least 1–2 categorical columns

---

### 6) Convert categorical strings into coded categories

**Goal:** convert text categories into numeric codes for modeling/analysis (SPSS “Automatic Recode”).

**What to do:**

* Create new coded columns (don’t overwrite original immediately).
* Use:

  * `astype("category").cat.codes` or
  * `pd.factorize()`

**Notebook actions:**

* Example:

  * `df["sex_code"], sex_map = pd.factorize(df["sex"])`
  * Store mapping table (code ↔ label) in the notebook.

**Outputs to include:**

* A small mapping table dataframe showing codes and labels
* Confirmation that coded columns are numeric

---

### 7) Detect and treat outliers

**Goal:** find extreme values (height mistakes like `172` instead of `1.72`, or real high earners/weights).

**What to do (two levels like the video):**

1. **Simple detection:** sort and inspect extremes
2. **Visual detection:** boxplot to identify outliers

**Notebook actions:**

* Sort:

  * `df.sort_values("height", ascending=False).head(20)`
* Fix obvious unit/decimal issues if domain knowledge confirms it:

  * Example rule: if height is in meters, values > 3 are invalid → maybe cm was entered.
* Make a boxplot for weight:

  * Identify outlier rows (e.g., using IQR rule) and decide treatment:

    * correct if data-entry error
    * remove value / remove row
    * keep but filter during analysis

**Outputs to include:**

* A boxplot for at least one numeric variable
* A table of detected outliers (top/bottom rows, and/or IQR-flagged rows)
* A short note in markdown: “Decision: corrected / removed / kept but flagged”

---

### 8) Handle missing values

**Goal:** decide how to deal with missingness without biasing results.

**What to do (match the video’s options):**

* Option A: drop rows with missing values in key variables (may lose data)
* Option B: impute (e.g., mean for numeric like weight)
* Option C: keep missing, but filter/handle them per analysis

**Notebook actions:**

* Create a “missingness report”:

  * `% missing` per column
* If you choose mean imputation for `weight`:

  * compute mean on non-missing
  * fill missing: `df["weight"] = df["weight"].fillna(weight_mean)`

**Outputs to include:**

* missingness table (counts + percentages)
* before/after missing counts for any imputed column
* a note explaining why you chose that method

---

### 9) Final validation + export cleaned dataset

**Goal:** prove the cleaned dataset is consistent and ready for analysis.

**What to do:**

* Re-run:

  * `info()`
  * duplicates check
  * `describe()`
  * `value_counts()` for key categories
* Save cleaned data:

  * CSV or parquet

**Outputs to include:**

* “Final audit” cell with the same metrics as the initial audit
* A saved file name like: `survey_cleaned.csv`

---

## Recommended notebook layout (copy this structure)

1. **Title + objective** (markdown)
2. **Load data + initial audit**
3. **Drop irrelevant columns**
4. **Filter irrelevant rows**
5. **Fix data types**
6. **Remove duplicates**
7. **Clean categorical text (structural issues)**
8. **Encode categories + mapping tables**
9. **Outlier detection + treatment**
10. **Missing values strategy + implementation**
11. **Final audit + export cleaned dataset**

If you paste a small sample of your real dataset columns (just the header row), I can adapt the checklist into an exact notebook template (with the exact column names and rules).
