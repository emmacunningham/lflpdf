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
chartleft = 40 + margin
titley = height - 50 - margin
charttopy = titley - 50 
rightmargin = width - margin
useableverticalspace = charttopy - margin - 5
useablehorizspace = rightmargin - chartleft - 30


def prettyDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{} {}, {}".format(month, day, year)

def fileDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{}_{}_{}".format(month, day, year)

def timelinerange(canvas,timeline):
	datestartall = timeline.timelinepoint_set.dates('datestart','day')
	dateendall = timeline.timelinepoint_set.dates('dateend','day',order='DESC')
	datestartmonth = timeline.timelinepoint_set.dates('datestart','month')
	dateendmonth = timeline.timelinepoint_set.dates('dateend','month')
	timelinepoints = timeline.timelinepoint_set.order_by('datestart')
	
	timelinefirst = datestartall[0]
	timelinelast = dateendall[0]
	

	days = abs(timelinelast - timelinefirst)
	projectdays = days.days
	dayspace = useablehorizspace/projectdays
	
	firstmonth = timelinefirst.strftime('%B')
	c = chartleft + 30
	
	x = margin + 5
	
	for i in range(projectdays):
		if i%7 == 0:
			canvas.drawString(x,-c,str(timelinefirst.day))
			c = c + dayspace
		else: 
			c = c + dayspace
		

	

def timelinecategories(canvas,timeline):
	t = timeline.timelinepoint_set.all()
	timecatset = set( )
	for point in t:
		timecatset.add(point.timelinecategory.categoryname)
	tcount = len(timecatset)
	catvertspace = useableverticalspace/tcount
	canvas.rotate(90)
	lefty = margin + 20
	for timecat in timecatset:
		canvas.drawString(lefty,-chartleft,timecat)
		lefty = lefty + catvertspace

def drawlines(canvas,timeline):
	canvas.setStrokeColorRGB(0.0,0.0,0.0)
	canvas.line(margin,height-margin,width-margin,height-margin)
	canvas.drawString(chartleft,titley,'{0}'.format(timeline.project))
	canvas.line(margin,margin,width-margin,margin)
	canvas.drawString(margin,margin-10,'Timeline')
	canvas.drawString(width-80,margin-10,'{0}'.format(prettyDateTime(timeline.pub_date)))
	timelinecategories(canvas,timeline)
	timelinerange(canvas,timeline)
	

def printpdf(timeline,timelineset):
	filename = os.path.join(pdf.settings.MEDIA_ROOT,'pdf/timeline/{0}.pdf'.format(timeline.project))
	c = canvas.Canvas(filename,pagesize=landscape(letter))
	drawlines(c,timeline)
	c.save()