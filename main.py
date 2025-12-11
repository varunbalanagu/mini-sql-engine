from engine import load_table, execute_query, print_rows
from parser import parse_query

def main():
    print("Mini SQL Engine")
    print("Type 'exit' or 'quit' to stop.")
    print("----------------------------------")

    # Ask for CSV filename (without .csv)
    table_name = input("Enter CSV filename (without .csv): ").strip()
    csv_file = table_name + ".csv"

    # Load table data
    try:
        rows = load_table(csv_file)
        print(f"Loaded table '{table_name}' with {len(rows)} rows.")
    except Exception as e:
        print("ERROR:", e)
        return

    # REPL loop
    while True:
        query = input("sql> ").strip()

        # Exit commands
        if query.lower() in ("exit", "quit"):
            print("Exiting SQL engine...")
            break

        if not query:
            continue  # ignore empty lines

        try:
            # 1) Parse the SQL string
            parsed = parse_query(query)

            # 2) Execute the parsed query
            result = execute_query(parsed, table_name, rows)

            # 3) Print the result
            print_rows(result)

        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    main()
