import csv
import os
def load_table(csv_filename: str):
    filepath=os.path.join("data",csv_filename)
    if not os.path.exists(filepath):
         raise Exception(f"CSV file '{csv_filename}' not found in /data folder")

    rows=[]
    with open(filepath,newline="") as f:
        reader=csv.DictReader(f)

        for row in reader:
            converted = {}
            for key, val in row.items():
                if val.isdigit():  
                    converted[key] = int(val)
                else:
                    converted[key] = val
            rows.append(converted)

    return rows
def execute_query(parsed: dict, table_name: str, rows: list[dict]) -> list[dict]:
    """Execute a SELECT query with optional WHERE and optional COUNT()."""

    # 1) Table check
    if parsed["from_table"] != table_name:
        raise Exception(f"Unknown table '{parsed['from_table']}'")

    # 2) WHERE filtering
    where = parsed["where_clause"]
    filtered_rows = rows
    if where is not None:
        filtered_rows = _apply_where(filtered_rows, where)

    # 3) Aggregation: COUNT()
    aggregation = parsed["aggregation"]
    if aggregation is not None:
        if aggregation["func"] == "COUNT":
            arg = aggregation["arg"]
            if arg == "*":
                count = len(filtered_rows)
            else:
                col = arg
                # COUNT(column) -> count non-null / non-empty values
                cnt = 0
                for r in filtered_rows:
                    if col not in r:
                        raise Exception(f"Unknown column '{col}' in COUNT()")
                    value = r[col]
                    if value not in (None, "", "NULL"):
                        cnt += 1
                count = cnt

            # Return as a single-row "table"
            return [{"COUNT": count}]
        else:
            raise Exception(f"Unsupported aggregation function '{aggregation['func']}'")

    # 4) No aggregation: normal SELECT
    select_cols = parsed["select_cols"]

    # SELECT * → return all columns
    if select_cols == ["*"]:
        return filtered_rows

    # SELECT specific columns
    result = []
    for row in filtered_rows:
        new_row = {}
        for col in select_cols:
            if col not in row:
                raise Exception(f"Unknown column '{col}' in SELECT list")
            new_row[col] = row[col]
        result.append(new_row)

    return result


def print_rows(rows: list[dict]):
    """Pretty-print rows in a table format."""
    if not rows:
        print("(no rows)")
        return

    # Get columns from first row
    cols = list(rows[0].keys())

    # Header
    header = " | ".join(cols)
    print(header)
    print("-" * len(header))

    # Rows
    for r in rows:
        line = " | ".join(str(r[c]) for c in cols)
        print(line)

def _compare(left, op, right):
    """Compare two values with a given operator."""
    if op == "=":
        return left == right
    if op == "!=":
        return left != right
    if op == ">":
        return left > right
    if op == "<":
        return left < right
    if op == ">=":
        return left >= right
    if op == "<=":
        return left <= right
    raise Exception(f"Unsupported operator '{op}'")


def _apply_where(rows: list[dict], where: dict) -> list[dict]:
    """Filter rows according to a WHERE clause."""
    col = where["col"]
    op = where["op"]
    val = where["val"]

    filtered = []
    for row in rows:
        if col not in row:
            raise Exception(f"Unknown column '{col}' in WHERE clause")
        row_val = row[col]
        if _compare(row_val, op, val):
            filtered.append(row)
    return filtered
