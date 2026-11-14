# Historical Bug Datasets

## 1. Mozilla Bug Reports

**Source:** Mozilla Bugzilla REST API

**API:** https://bugzilla.mozilla.org/rest/bug

**Project:** Firefox

**Collection size:** 10 bug reports

**Format:** JSON

**Access:** Public, read-only API

## 2. Collected Fields

- Bug ID
- Summary
- Status
- Resolution
- Product
- Component
- Creation Time

## 3. Storage Location

The original downloaded dataset is stored at:

`datasets/raw/mozilla_sample.json`

## 4. Collection Method

The dataset was collected using a Python script named `download_mozilla.py`.

Python's built-in libraries were used to retrieve the public JSON response and save it locally.

## 5. Data Processing Status

- Collection: Completed
- Raw data storage: Completed
- Data cleaning: Pending
- Standardization: Pending
- Chunking: Pending
- Embedding generation: Pending
- Vector database indexing: Pending

## 6. Security and Data Handling

Only publicly accessible bug-report information is collected. Dataset processing will preserve technical information needed for defect analysis and avoid collecting unnecessary personal information.
