import fitz
import easyocr
import sys

reader = easyocr.Reader(['en'], gpu=False, verbose=False)

def ocr_pdf(path, max_pages=None):
    doc = fitz.open(path)
    total = len(doc)
    if max_pages:
        total = min(total, max_pages)
    print(f"Total pages: {len(doc)}, processing: {total}")
    for i in range(total):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes('png')
        results = reader.readtext(img_bytes)
        if results:
            print(f"\n--- PAGE {i+1} ---")
            for bbox, text, conf in results:
                print(text)

if __name__ == "__main__":
    path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ocr_pdf(path, max_pages)
