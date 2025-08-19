# Bloom Filter Email Checker

A Python implementation of a **Bloom filter** to test whether emails from one CSV file are probably present in another. Built for an **Algorithms & Design** course.

---

## How it works
- Reads a CSV of emails (the “database”).
- Builds a Bloom filter with optimal size (`m`) and number of hash functions (`k`) based on a target false-positive probability.
- Reads another CSV of emails to test.
- Prints whether each email is **“Probably in the DB”** or **“Not in the DB.”**

---

## Requirements
- Python 3.8+
- Two CSV files:
  - **emails.csv** → build the filter  
  - **queries.csv** → emails to check  

The first row (header) is skipped.

---

## Usage
```bash
python bloom_emails.py emails.csv queries.csv
```

## Example output
```bash
bob@example.org,Probably in the DB
dave@example.com,Not in the DB
