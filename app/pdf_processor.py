import os
import fitz  # PyMuPDF

def extract_section_title(page):
    """Try to extract a section title from page text using font size heuristics"""
    blocks = page.get_text("dict")["blocks"]
    max_font_size = 0
    title_text = None

    for block in blocks:
        if block['type'] != 0:  # Text block only
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                font_size = span["size"]
                y0 = span["origin"][1]  # vertical position
                # Consider text near top half of page only
                if y0 > page.rect.height / 2:
                    continue
                if font_size > max_font_size and span["text"].strip():
                    max_font_size = font_size
                    title_text = span["text"].strip()
    return title_text if title_text else None

def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text().strip()
        if not text:
            continue
        section_title = extract_section_title(page)
        if not section_title:
            section_title = f"Page {page_num + 1}"

        sections.append({
            "document": os.path.basename(pdf_path),
            "page": page_num + 1,
            "section_title": section_title,
            "text": text
        })
    return sections

def extract_sections_from_folder(folder_path):
    all_sections = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            sections = extract_sections_from_pdf(full_path)
            all_sections.extend(sections)
    return all_sections
