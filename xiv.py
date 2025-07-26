from pylatex import Document, Table, Tabular, Package, NewPage
from pylatex.utils import NoEscape
import os
import datetime
import argparse


def generate_xiv_table(start_date: datetime.date, doc: Document):
    with doc.create(Table(position="h!")) as table:
        with table.create(Tabular("|" + "p{3.38cm}|" * 7)) as tabular:
            tabular.add_hline()
            # First week
            headers = []
            for i in range(7):
                current_date = start_date + datetime.timedelta(days=i)
                date_str = current_date.strftime("%d.%m.")
                weekday_str = current_date.strftime("%a")
                headers.append(
                    NoEscape(f"\\textbf{{{date_str} {weekday_str}}}")
                )

            tabular.add_row(tuple(headers))
            tabular.add_hline()
            empty_row = [
                NoEscape(r"\rule[-" + "9.35cm" + "]{0pt}{" + "9.35cm" + "}")
            ] * 7
            tabular.add_row(empty_row)
            tabular.add_hline()

            # Second week
            next_week_start_date = start_date + datetime.timedelta(days=7)
            headers = []
            for i in range(7):
                current_date = next_week_start_date + datetime.timedelta(
                    days=i
                )
                date_str = current_date.strftime("%d.%m.")
                weekday_str = current_date.strftime("%a")
                headers.append(
                    NoEscape(f"\\textbf{{{date_str} {weekday_str}}}")
                )

            tabular.add_row(tuple(headers))
            tabular.add_hline()
            tabular.add_row(empty_row)
            tabular.add_hline()


def generate_xiv(start_date: datetime.date, out_dir: str, single_page: bool):
    doc = Document()
    doc.packages.append(
        Package("geometry", options=["landscape", "margin=0.5cm"])
    )
    doc.packages.append(Package("fontenc", options=["T1"]))
    doc.packages.append(Package("tgbonum"))

    generate_xiv_table(start_date, doc)

    if not single_page:
        doc.create(NewPage())
        generate_xiv_table(start_date + datetime.timedelta(days=14), doc)

    filename = "xiv_" + start_date.strftime("%y%m%d")
    os.makedirs(out_dir, exist_ok=True)
    doc.generate_pdf(os.path.join(out_dir, filename), clean_tex=False)
    print(f"LaTeX document '{filename}.pdf' generated successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a weekly notes table in LaTeX."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--today",
        "-t",
        action="store_true",
        help="Generate table starting with today's date.",
    )
    group.add_argument(
        "--date",
        "-d",
        type=str,
        help="Generate table starting with a specific date (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="build",
        help="Directory to save the output PDF (default: build).",
    )

    parser.add_argument(
        "--single-page",
        "-s",
        action="store_true",
        help="Generate only one XIV page instead of two (default: False)",
    )

    args = parser.parse_args()

    if args.today:
        start_date = datetime.date.today()
        generate_xiv(start_date, args.output_dir, args.single_page)
    elif args.date:
        try:
            start_date = datetime.datetime.strptime(
                args.date, "%Y-%m-%d"
            ).date()
            generate_xiv(start_date, args.output_dir, args.single_page)
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
    else:
        parser.print_help()
