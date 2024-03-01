import pdfplumber

file_path = "./report05.pdf"

with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[1]
        text = page.extract_text()
        array = text.split()
        try:
            delimiter_index = array.index("Source")
            newarray = array[:delimiter_index]
            print(newarray[-1])
        except ValueError:
            try:
                delimiter_index = array.index("Disclaimer")
                newarray = array[:delimiter_index]
                print(newarray[-1])
            except ValueError:
                print("Source and Disclaimer not found.")
