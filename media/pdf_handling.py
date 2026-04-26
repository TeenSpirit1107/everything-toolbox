import os
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2 import PageObject

# 始终使用本文件所在目录下的 input/ 与 output/，不随运行时的 cwd 变化
_PDF_HANDLING_DIR = os.path.dirname(os.path.abspath(__file__))


def merge_pdfs_to_one_page():
    input_path = os.path.join(_PDF_HANDLING_DIR, "input")
    if not os.path.exists(input_path):
        os.mkdir(input_path)
        print(f"Directory '{input_path}' does not exist. Automatically created. Please place your PDF files in it.")
        input("When finished, press any key to continue.")

    # Find all PDF files in the input directory (alphabetical order = recommended merge order)
    pdf_files = sorted(
        f for f in os.listdir(input_path) if f.lower().endswith(".pdf")
    )
    if not pdf_files:
        print("No PDF files found in the 'input' directory.")
        return

    print("\nRecommended merge order (alphabetical A→Z, first to last):")
    for i, name in enumerate(pdf_files, start=1):
        print(f"  {i}. {name}")

    used_files = set()
    writer = PdfWriter()

    def append_pdf_pages(filename: str) -> None:
        selected_path = os.path.join(input_path, filename)
        reader = PdfReader(selected_path)
        for page in reader.pages:
            new_page = PageObject.create_blank_page(
                width=page.mediabox.width, height=page.mediabox.height
            )
            new_page.merge_page(page)
            writer.add_page(new_page)

    while True:
        # List available PDF files excluding already used ones (same order as pdf_files)
        available_files = [f for f in pdf_files if f not in used_files]
        if not available_files:
            print("No more available PDF files to insert.")
            break

        print("\nAvailable PDF files (alphabetical):")
        for idx, file in enumerate(available_files, start=1):
            print(f"{idx}. {file}")

        raw = input(
            "Select number to insert one PDF, 0 to finish, "
            "r = Recommended (merge ALL remaining in A→Z order): "
        ).strip().lower()

        if raw == "0":
            break
        if raw in ("r", "rec", "recommended", "-1"):
            for fname in available_files:
                used_files.add(fname)
                append_pdf_pages(fname)
            print("Merged all remaining files in recommended (alphabetical) order.")
            break

        try:
            choice = int(raw)
            if choice == 0:
                break
            selected_file = available_files[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
            continue

        used_files.add(selected_file)
        append_pdf_pages(selected_file)

    # Save the merged PDF
    output_path = input("Enter the output file name (without extension): ")
    if not output_path:
        print("Output file name cannot be empty. Automatically using 'merged_output.pdf'.")
        output_path = "merged_output"
    if not output_path.endswith('.pdf'):
        output_path += '.pdf'
    output_dir = os.path.join(_PDF_HANDLING_DIR, "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory 'output' did not exist and was created.")
    output_path = os.path.join(output_dir, output_path)
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Merged PDF saved as '{output_path}'")


if __name__ == "__main__":
    print("Welcome to pdf_tools by Rosalind!")
    
    while True:
        choice = input("Select an option:\n1. Merge PDFs to one page\nx. Exit\n")
        if choice.lower() == 'x':
            break
        if choice == '1':
            merge_pdfs_to_one_page()
        else:
            print("Invalid choice.")
            continue
