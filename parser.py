def _parse_value(val_str: str):
    """
    Convert a string value from the WHERE clause into a proper Python type.
    Supports:
      - integers: 30  ->  30
      - quoted strings: 'USA' -> "USA"
      - everything else stays as string
    """
    val_str = val_str.strip()

    # String literal in single quotes: 'USA'
    if val_str.startswith("'") and val_str.endswith("'") and len(val_str) >= 2:
        return val_str[1:-1]   # remove the quotes

    # Integer value
    if val_str.isdigit():
        return int(val_str)

    # Default: return as string
    return val_str


def parse_query(sql: str) -> dict:
    """
    Parse a simple SQL SELECT query into a dictionary structure.

    Supported forms:
      - SELECT * FROM table;
      - SELECT col1, col2 FROM table;
      - SELECT * FROM table WHERE col op value;
      - SELECT col1 FROM table WHERE col2 op value;
      - SELECT COUNT(*) FROM table;
      - SELECT COUNT(col) FROM table WHERE col2 op value;

    WHERE:
      - Single condition only
      - Operators: =, !=, >, <, >=, <=
      - Values: numbers or strings in single quotes
    """
    # Clean and normalize
    original = sql.strip()
    if not original:
        raise Exception("Empty query")

    # Remove trailing semicolon, if present
    if original.endswith(";"):
        original = original[:-1]

    upper = original.upper()

    # Must start with SELECT
    if not upper.startswith("SELECT "):
        raise Exception("Query must start with SELECT")

    # Find FROM keyword
    from_index = upper.find(" FROM ")
    if from_index == -1:
        raise Exception("Missing FROM clause")

    # --- Split around SELECT and FROM ---
    # Part between SELECT and FROM
    select_part = original[len("SELECT "):from_index].strip()

    # Part after FROM (may include WHERE)
    after_from = original[from_index + len(" FROM "):].strip()
    after_from_upper = upper[from_index + len(" FROM "):].strip()

    # ---------- WHERE handling ----------
    where_clause = None

    where_index = after_from_upper.find(" WHERE ")
    if where_index == -1:
        # No WHERE clause
        table_name = after_from.strip()
    else:
        # Split into table name and WHERE part
        table_name = after_from[:where_index].strip()
        where_part = after_from[where_index + len(" WHERE "):].strip()
        if not where_part:
            raise Exception("Empty WHERE condition")

        # Supported operators: <=, >=, !=, =, >, <
        ops = ["<=", ">=", "!=", "=", ">", "<"]
        op_found = None

        for op in ops:
            if op in where_part:
                op_found = op
                left, right = where_part.split(op, 1)
                col = left.strip()
                val = _parse_value(right)
                where_clause = {
                    "col": col,
                    "op": op_found,
                    "val": val,
                }
                break

        if op_found is None:
            raise Exception("Unsupported or missing operator in WHERE clause")

    # ---------- SELECT / COUNT handling ----------
    select_upper = select_part.upper()

    aggregation = None
    select_cols = None

    # Case 1: COUNT(...)
    if select_upper.startswith("COUNT(") and select_upper.endswith(")"):
        # content inside COUNT(...)
        inner = select_part[6:-1].strip()
        if inner == "*":
            aggregation = {"func": "COUNT", "arg": "*"}
        else:
            # COUNT(column_name)
            aggregation = {"func": "COUNT", "arg": inner}
        select_cols = []  # no normal columns in this mode

    # Case 2: Normal columns or *
    else:
        if select_part == "*":
            select_cols = ["*"]
        else:
            columns = [c.strip() for c in select_part.split(",")]
            select_cols = [c for c in columns if c]
            if not select_cols:
                raise Exception("No columns specified in SELECT")

    return {
        "select_cols": select_cols,
        "from_table": table_name,
        "aggregation": aggregation,
        "where_clause": where_clause,
    }
