from pathlib import Path
from PyPDF2 import PdfReader

PDF_FILE = Path("support-policy.pdf")
OUTPUT_FILE = Path("output/support_policy_text.txt")

reader = PdfReader(PDF_FILE)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        f.write(
            f"\n\n===== PAGE {page_number} =====\n\n"
        )

        f.write(text)

print(
    f"Extracted {len(reader.pages)} pages."
)

print(
    f"Saved to: {OUTPUT_FILE}"
)