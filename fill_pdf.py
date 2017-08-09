from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
from itertools import product


fname = 'SirotaLab-DefensiveBehaviorAgainstImplantSheet.pdf'

daterange = pd.date_range(pd.datetime(year=2017, month=4, day=21), freq='3D', periods=37)
dates = daterange.format(formatter=lambda dt: dt.strftime('%d.%m.%Y'))


packet = io.BytesIO()

# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
for date, (x, y) in zip(dates, product([80, 320], reversed(range(100, 650, 14)))):
    can.drawString(x, y, date)
can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(fname, "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page2 = new_pdf.getPage(0)
page.mergePage(page2)
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("newpdf.pdf", "wb")
output.write(outputStream)
outputStream.close()