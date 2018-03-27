import re

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


with open('/home/cyan/Downloads/Barron-s-1100-Words-You-Need-table.pdf', 'rb') as pdf_doc:
    parser = PDFParser(pdf_doc)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = []
    
    for page in doc.get_pages():
        page_text = []
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox):
                page_text.append(lt_obj)
        extracted_text.append(page_text)

fig = plt.figure()
keys, values = [], []
pageno = 1
for page in extracted_text:
    ax1 = fig.add_subplot(4,4,pageno, aspect='equal')
    for box in page:
        ax1.add_patch(
            patches.Rectangle(
                (box.x0/1000, box.y0/1000),   # (x,y)
                (box.x1-box.x0)/1000,          # width
                (box.y1-box.y0)/1000,          # height
                facecolor = "red" if box.x0 < 80 else "orange" if 200 < box.x0 < 400 else "blue"
            )
        )
        keys.append(box) if (box.x0 < 80 or 200 < box.x0 < 400) else values.append(box)
    pageno += 1
fig.show()

words = []
prod = re.compile('[^a-z ]+', re.UNICODE | re.IGNORECASE)
for key in keys:
    for word in key.get_text().split('\n'):
        words.append(prod.sub('', word).strip())
filtered_words = list(filter(lambda x: len(x) and ' ' not in x, words))
print(list(enumerate(sorted(filtered_words))))
