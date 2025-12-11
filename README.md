# Mini In-Memory SQL Engine (Python)

A small educational SQL engine that loads a CSV as an in-memory table and runs a minimal subset of SQL queries.

**Author:** Varun  
**Project:** Mini SQL Engine  
**Status:** Completed — core features (SELECT, WHERE, COUNT) implemented

---

## Features

This engine supports the following:

- Load CSV files into memory (list of dicts)
- Interactive REPL to type SQL queries
- `SELECT` projection:
  - `SELECT * FROM table;`
  - `SELECT col1, col2 FROM table;`
- `WHERE` filtering with a single condition:
  - Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`
  - Values: integers (e.g. `30`) or single-quoted strings (e.g. `'USA'`)
- Aggregation: `COUNT()`:
  - `COUNT(*)` and `COUNT(column_name)`
  - Works with optional `WHERE` filter
- Basic error handling for unknown columns, missing clauses, and invalid syntax

---

## Requirements

- Python 3.8+  
(No external libraries required — uses built-in `csv` and `os` modules.)

---

## Project Structure

