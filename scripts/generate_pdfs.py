"""Generate 10 PDF files with random content using Faker and PyMuPDF."""
import os
import argparse
from pathlib import Path
import pymupdf  # PyMuPDF
from faker import Faker

DEFAULT_OUTPUT_DIR = ".data/generated_pdfs"
NUM_FILES = 10

fake = Faker()


def create_pdf(filepath: str) -> None:
    doc = pymupdf.open()

    for _ in range(fake.random_int(min=1, max=3)):
        page = doc.new_page()
        y = 72  # top margin

        # Title
        title = fake.catch_phrase()
        page.insert_text((72, y), title, fontsize=18, fontname="helv")
        y += 30

        # Author and date
        meta_line = f"By {fake.name()}  |  {fake.date()}"
        page.insert_text((72, y), meta_line, fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 25

        # Body paragraphs
        for _ in range(fake.random_int(min=3, max=6)):
            paragraph = fake.paragraph(nb_sentences=fake.random_int(min=3, max=8))
            # Wrap text manually (~90 chars per line at fontsize 11)
            words = paragraph.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 > 90:
                    page.insert_text((72, y), line, fontsize=11, fontname="helv")
                    y += 16
                    line = word
                    if y > 750:
                        break
                else:
                    line = f"{line} {word}".strip()
            if line and y <= 750:
                page.insert_text((72, y), line, fontsize=11, fontname="helv")
                y += 24
            if y > 750:
                break

    doc.save(filepath)
    doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PDF files with random content.")
    parser.add_argument(
        "-o", "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save generated PDFs (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "-n", "--num-files",
        type=int,
        default=NUM_FILES,
        help=f"Number of PDF files to generate (default: {NUM_FILES})",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    num_files = args.num_files
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, num_files + 1):
        filename = f"document_{i:02d}.pdf"
        filepath = os.path.join(output_dir, filename)
        create_pdf(filepath)
        print(f"Created {filepath}")

    print(f"\nDone. {num_files} PDFs saved to {output_dir}")


if __name__ == "__main__":
    main()
