import argparse
from configparser import ConfigParser
from api_client import APIClient
from data_transformer import DataTransformer
from mysql_handler import MySQLHandler


def fetch_data_flow(db, client, transformer, country, start_date, end_date):
    print(f"Fetching data for {country} from {start_date} to {end_date} ...")
    raw_cases, raw_vacc = client.fetch_both(country)
    cases = transformer.clean_cases(raw_cases, start_date, end_date)
    vaccs = transformer.clean_vaccinations(raw_vacc, start_date, end_date)
    db.insert_data("daily_cases", cases)
    db.insert_data("vaccination_data", vaccs)
    print(f"Loaded {len(cases)} daily_cases & {len(vaccs)} vaccination records.")


def main():
    config = ConfigParser()
    config.read("config.ini")

    db_handler = MySQLHandler(dict(config["mysql"]))
    db_handler.create_tables()

    api_client = APIClient(config["api"]["base_url"])
    transformer = DataTransformer()

    parser = argparse.ArgumentParser(description="Healthcare ETL CLI")
    subparsers = parser.add_subparsers(dest="command")

    # fetch_data with freeform args
    f = subparsers.add_parser("fetch_data")
    f.add_argument("params", nargs=6)

    q = subparsers.add_parser("query_data")
    q.add_argument("query_type", choices=["total_cases", "daily_trends", "top_n_countries_by_metric"])
    q.add_argument("arg1")
    q.add_argument("arg2", nargs="?", default=None)

    subparsers.add_parser("list_tables")
    subparsers.add_parser("drop_tables")

    args = parser.parse_args()

    if args.command == "fetch_data":
        # Parse custom keyword-style params
        if args.params[0] == "country" and args.params[2] == "start_date" and args.params[4] == "end_date":
            country = args.params[1]
            start_date = args.params[3]
            end_date = args.params[5]
            fetch_data_flow(db_handler, api_client, transformer, country, start_date, end_date)
        else:
            print("❌ Invalid fetch_data syntax. Use:\n  python main.py fetch_data country \"India\" start_date \"YYYY-MM-DD\" end_date \"YYYY-MM-DD\"")

    elif args.command == "query_data":
        if args.query_type == "total_cases":
            sql = f"SELECT SUM(total_cases) FROM daily_cases WHERE country_name='{args.arg1}'"
            rows = db_handler.query(sql)
            total = rows[0][0] or 0
            print(f"Total COVID-19 Cases in {args.arg1}: {int(total):,}")

        elif args.query_type == "daily_trends":
            sql = f"SELECT report_date, {args.arg2} FROM daily_cases WHERE country_name='{args.arg1}'"
            rows = db_handler.query(sql)
            print("Date        |", args.arg2.replace("_", " ").title())
            print("-----------------------------")
            for r in rows:
                date_str = r[0].strftime("%Y-%m-%d")
                print(f"{date_str} | {int(r[1]):,}")

        elif args.query_type == "top_n_countries_by_metric":
            sql = f"""
                SELECT country_name, SUM({args.arg2}) AS total
                FROM vaccination_data
                GROUP BY country_name
                ORDER BY total DESC
                LIMIT {args.arg1}
            """
            rows = db_handler.query(sql)
            print("Country         | Total")
            print("----------------------------")
            for r in rows:
                print(f"{r[0]:15} | {int(r[1]):,}")

    elif args.command == "list_tables":
        for t in db_handler.query("SHOW TABLES;"):
            print(t[0])

    elif args.command == "drop_tables":
        db_handler.query("DROP TABLE IF EXISTS daily_cases")
        db_handler.query("DROP TABLE IF EXISTS vaccination_data")
        db_handler.conn.commit()
        print("Tables dropped.")

    else:
        parser.print_help()

    db_handler.close()


if __name__ == "__main__":
    main()
