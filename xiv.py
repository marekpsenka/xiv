from pylatex import Document, Table, Tabular, Package
from pylatex.utils import NoEscape
import os
import datetime


def generate_weekly_notes_table(start_date_str):
    doc = Document()
    doc.packages.append(
        Package("geometry", options=["landscape", "margin=0.5cm"])
    )

    with doc.create(Table(position="h!")) as table:
        with table.create(Tabular("|" + "p{3.38cm}|" * 7)) as tabular:
            tabular.add_hline()
            # First week
            start_date = datetime.datetime.strptime(
                start_date_str, "%Y-%m-%d"
            ).date()
            headers = []
            for i in range(7):
                current_date = start_date + datetime.timedelta(days=i)
                date_str = current_date.strftime("%d.%m.")
                weekday_str = current_date.strftime("%a")
                headers.append(
                    NoEscape(f"\\textbf{{{date_str} {weekday_str}}}")
                )

            tabular.add_row(tuple(headers))
            tabular.add_row([""] * 7)
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
            tabular.add_row([""] * 7)
            tabular.add_hline()

    filename = "weekly_notes"
    out_dir = "build"
    doc.generate_pdf(os.path.join(out_dir, filename), clean_tex=False)
    print(f"LaTeX document '{filename}.pdf' generated successfully.")


if __name__ == "__main__":
    # Example usage: Start the table with the week of April 6th, 2025 (Sunday)
    generate_weekly_notes_table("2025-04-06")
