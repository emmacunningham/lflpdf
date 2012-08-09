import re
import html2text
import datetime
import time

import pdf.settings
import os

from django.core.files import File
from django.core.files.storage import FileSystemStorage, default_storage

from pdfmaker.models import Timeline

from xhtml2pdf import pisa, context, document
from xhtml2pdf.context import pisaContext
from xhtml2pdf.parser import pisaParser

from reportlab.pdfgen import canvas, textobject, pathobject
from reportlab.lib.pagesizes import letter, landscape


import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.colors import grey, CMYKColor, PCMYKColor
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Frame, FrameBreak, PageTemplate, BaseDocTemplate, NextPageTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

# define greys as cmyk=60%
linegrey = CMYKColor(0,0,0,0.3)
numgrey = CMYKColor(0,0,0,0.6)

# sets path for registerFont to find fonts in right place 
reportlab.rl_config.TTFSearchPath.append( os.path.join(pdf.settings.STATIC_ROOT,'fonts') )

# drawing definitions  
width = 792
height = 612
margin = 30

def fileDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{}_{}_{}".format(month, day, year)

def timelinerange(timeline):
	datestartall = timeline.timelinepoint_set.dates('datestart','day')
	dateendall = timeline.timelinepoint_set.dates('dateend','day',order='DESC')
	timelinefirst = datestartall[0]
	timelinelast = dateendall[0]
	s = fileDateTime(timelinelast)
	return s

def drawlines(canvas):
	canvas.setStrokeColorRGB(0.2,0.5,0.3)
	canvas.line(0,0,70,70)
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,749)
	textobject.textLines('''
	LEFT 
	FIELD 
	LABS
	''')
	canvas.drawText(textobject)

def printpdf(timeline,timelineset):
	filename = os.path.join(pdf.settings.MEDIA_ROOT,'pdf/timeline/{0}.pdf'.format(timeline.project))
	c = canvas.Canvas(filename,pagesize=letter)
	c.pagesize = landscape(letter)
	drawlines(c)
	c.save()