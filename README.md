# python-growth-projects

## CSV Transformer
>A powerful CSV manipulation toolkit with a clean command-line interface

**Key Features**:
1. Multi-format Support: Read/write CSV, JSON, Excel, and Parquet files

2. Smart Auto-detection: Handle different delimiters, encodings, and quote styles automatically

3. Common Operations:

    - Filter rows (where price > 100)
    - Sort data (sort by date descending)
    - Select columns (select name,email)
    - Aggregate (group by department aggregate avg(salary))
    - Join files (join users.csv orders.csv on user_id)

4. Data Cleaning:

    - Fill missing values
    - Remove duplicates
    - Standardize formats
    - Regex find/replace

5. Output Options:

    - Pretty-printed tables
    - Markdown/HTML export
    - Direct database loading

6. Chaining: Pipe multiple operations together (`csvx clean data.csv | csvx filter 'status=="active"' | csvx sort by date`)

**Implementation Highlights**:
Use click or typer for CLI interface

pandas for data manipulation backbone

rich for beautiful console output

Add progress bars with tqdm for large files

Include comprehensive --help with examples

## Simple Web API (Django) For Project CMS

## Public Dataset Analysis (Undecided)