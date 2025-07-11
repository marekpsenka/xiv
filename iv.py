from pylatex import Document, Table, Tabular, NoEscape, Package
from pylatex.utils import bold
import datetime as dt
import argparse
import os


def create_weekly_overview_pdf(start_date_str, out_dir: str):
    """
    Generates a four-week overview PDF table starting from the given date.
    """

    # Determine the start of the week (Monday) for the given date
    # Weekday 0 is Monday, 6 is Sunday
    start_of_first_week = start_date - dt.timedelta(days=start_date.weekday())

    doc = Document()
    doc.packages.append(Package("geometry", options=["margin=0.5cm"]))
    doc.packages.append(Package("fontenc", options=["T1"]))
    doc.packages.append(Package("tgbonum"))

    table = Table(position="h!")
    tabular = Tabular(r"|p{20cm}|")

    tabular.add_hline()
    for i in range(4):
        current_week_start = start_of_first_week + dt.timedelta(weeks=i)
        current_week_end = current_week_start + dt.timedelta(days=6)

        week_number = current_week_start.isocalendar()[1]  # ISO week number

        # Header row
        tabular.add_row(
            [
                bold(
                    f"Week {week_number}: {current_week_start.strftime('%d.%m')} - {current_week_end.strftime('%d.%m')}"
                ),
            ]
        )
        tabular.add_hline()

        # Empty, maximal size row
        # Use \rule{0pt}{<height>} to force row height
        tabular.add_row(
            [
                NoEscape(r"\rule[-" + "6cm" + "]{0pt}{" + "6cm" + "}"),
            ]
        )  # This will scale to max height
        tabular.add_hline()

    table.append(tabular)
    doc.append(table)

    filename = "iv_" + start_date.strftime("%y%m%d")
    os.makedirs(out_dir, exist_ok=True)
    doc.generate_pdf(os.path.join(out_dir, filename), clean_tex=False)
    print(f"Generated {filename} starting from week of {start_date_str}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a four-week overview PDF table."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--today",
        "-t",
        action="store_true",
        help="Generate table starting with this week",
    )
    group.add_argument(
        "--date",
        "-d",
        type=str,
        help="Generate table starting with a week containing a specific date (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="build",
        help="Directory to save the output PDF (default: build).",
    )

    args = parser.parse_args()

    if args.today:
        start_date = dt.date.today()
        create_weekly_overview_pdf(start_date, args.output_dir)
    elif args.date:
        try:
            start_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
            create_weekly_overview_pdf(start_date, args.output_dir)
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
    else:
        parser.print_help()
