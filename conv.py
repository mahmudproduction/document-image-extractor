import os 
os.system('clear')
from PyPDF2 import PdfFileReader
from pypdf import PdfReader


# pdf = PdfFileReader

reader = PdfReader('D:\\py\\pdf\\work_permit_checlist_revize.pdf')
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
with open('1.txt', 'w', encoding='utf-8') as file:
    # Записываем текст в файл
    file.write(text)