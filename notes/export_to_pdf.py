import os
import markdown
import pdfkit

# Konfiguracja programu do konwersji md na pdf

PATH_TO_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

try:
    config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
except OSError as e:
    print(f"Error! Cannot fint path to: {PATH_TO_WKHTMLTOPDF}")
    exit(1)

NOTES_DIR = '.'

print("Converting to PDF...\n")

if not os.path.exists(NOTES_DIR):
    print(f"Folder '{NOTES_DIR}' not exist.")
    exit()

for filename in os.listdir(NOTES_DIR):
    if filename.endswith(".md"):
        # Przygotuj dwie sciezki: wejsciowa dla starej i wyjsciowa dla nowego PDFa
        md_file_path = os.path.join(NOTES_DIR, filename)
        pdf_file_path = os.path.join(NOTES_DIR, "pdfs", filename.replace('.md', '.pdf'))

        if os.path.exists(pdf_file_path):
            print(f"Skipping - {pdf_file_path} - already exists.")
            continue
        
        print(f"🔎 Converting {filename} to PDF...")
        
        # Otwieramy notatke z kodowaniem na Polskie znaczki
        with open(md_file_path, 'r', encoding='utf-8') as f:
            text_from_note = f.read()
            html_code = markdown.markdown(text_from_note, extensions=['tables', 'fenced_code'])
            # Definiujemy prosty styl CSS z bezszeryfową czcionką dla ładniejszego wyglądu
            custom_css = """
            <style>
                body {
                    font-family: Arial, Helvetica, sans-serif;
                    color: #333;
                    line-height: 1.6;
                }
                code {
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-family: Consolas, monospace;
                }
                pre code {
                    display: block;
                    padding: 10px;
                    background-color: #f4f4f4;
                    border-radius: 4px;
                    overflow-x: auto;
                }
            </style>
            """
            
            # Odczytywanie pl jako UTF-8 oraz dodanie stylów CSS
            print_html = f'<meta charset="UTF-8">\n{custom_css}\n{html_code}'
            # Zleć druk
            pdfkit.from_string(print_html, pdf_file_path, configuration=config)

print("\nSuccess! ✨")
