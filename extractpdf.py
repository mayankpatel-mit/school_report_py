import tabula

file_path = "./schoolreport01.pdf"

tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

for i, table in enumerate(tables):
    print(f"Table {i}:")
    print(table)
    print("\n")
