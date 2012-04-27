import re
import html2text
import datetime
import time

import pdf.settings
import os

from django.core.files import File

from xhtml2pdf import pisa, context, document
from xhtml2pdf.context import pisaContext
from xhtml2pdf.parser import pisaParser

from reportlab.pdfgen import canvas, textobject, pathobject
from reportlab.lib.pagesizes import letter


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

# building fonts
pdfmetrics.registerFont(TTFont('Akkurat-Reg','Akkurat-Reg.ttf'))
pdfmetrics.registerFont(TTFont('Akkurat','Akkurat-Light.ttf'))
pdfmetrics.registerFont(TTFont('AkkuratBd','Akkurat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('AkkuratIt','Akkurat-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Gridnik','Gridnik.ttf'))

registerFontFamily('Akkurat-Reg',normal='Akkurat-Reg',bold='Akkurat-Bold',italic='Akkurat-Italic')
registerFontFamily('Akkurat',normal='Akkurat',bold='AkkuratBd',italic='AkkuratIt')

# margin and padding definitions
sectionLeft = 0 
sectionRight = 24
sectionTop = 39
sectionBottom = 36

mainTextMargin = 190

# frames

frameLaterPagesMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=39.4,bottomPadding=36,rightPadding=24,leftPadding=20)
frameFirstPageSide = Frame(x1=0,y1=0,width=mainTextMargin,height=792,topPadding=0,leftPadding=0)
frameFirstPageMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=218,leftPadding=20)




def lfleft(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,749)
	textobject.setFont('Gridnik',25)
	textobject.textLines('''
	LEFT 
	FIELD 
	LABS
	''')
	canvas.drawText(textobject)
	
def contactleftFirstPage(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,57)
	textobject.setFont('Akkurat',9)
	textobject.textLines('''
	510 Victoria Ave
	Venice CA 90291
	www.leftfieldlabs.com
	''')
	canvas.drawText(textobject)

def contactleftLaterPages(canvas):
	textobject = canvas.beginText()
	lflwidth = canvas.stringWidth('LEFT FIELD LABS','Gridnik',12)
	addrwidth = canvas.stringWidth('510 Victoria Ave, Venice CA 90291','Akkurat',9)
	emailwidth = canvas.stringWidth('www.leftfieldlabs.com','Akkurat',9)
	lflx = addrwidth - lflwidth + 30
	emailx = addrwidth - emailwidth + 30
	textobject.setTextOrigin(lflx,57)
	textobject.setFont('Gridnik',12)
	textobject.textLine('LEFT FIELD LABS')
	y = textobject.getY()
	textobject.setTextOrigin(30,y)
	
	textobject.setFont('Akkurat',9)
	textobject.textLine('510 Victoria Ave, Venice CA 90291')
	yy = textobject.getY()
	textobject.setTextOrigin(emailx,yy)
	textobject.textLine('www.leftfieldlabs.com')
	canvas.drawText(textobject)

def ffirstPage(sow):
	img = sow.assets.img.name
	def firstPage(canvas, doc):
		canvas.saveState()
		canvas.drawImage('media/{}'.format(img),0,0,width=mainTextMargin-12,height=792)
		lfleft(canvas)
		contactleftFirstPage(canvas)
		canvas.restoreState()
	return firstPage
		
def llaterPages(sow):
	img = sow.assets.img.name
	def laterPages(canvas, doc):
		canvas.saveState()
		canvas.drawImage('media/{}'.format(img),0,0,width=mainTextMargin-12,height=792)
		contactleftLaterPages(canvas)
		canvas.restoreState()
	return laterPages
	
# hacked tabbing
def tab(left,right,tabamt):
	data = [['{}'.format(left),'{}'.format(right)]]
	t = Table(data)
	t.hAlign = 'LEFT'
	t.setStyle(TableStyle([('LEFTPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('TOPPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('BOTTOMPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('ALIGN',(0,0),(1,0),'LEFT')]))
	t._argW[0]=tabamt
	return t
	
def projectInfo(sow,story):
	authorname = '{} {}'.format(sow.author.user.first_name,sow.author.user.last_name)
	authorphone = sow.author.phone
	statementofwork = Paragraph("<para spaceAfter=20><font name='Akkurat-Reg' size=16>// STATEMENT OF WORK<br/></font></para>",styles['Normal'])
	project = tab('PROJECT:',sow.project,83)
	client = tab('CLIENT:',sow.client,83)
	date = tab('DATE:',prettyDateTime(sow.pub_date),83)
	author = tab('CONTACT:',authorname,83)
	phone = tab('',authorphone,83)
	project.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	date.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	author.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	phone.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	story.append(statementofwork)
	story.append(project)
	story.append(client)
	story.append(date)
	story.append(author)
	story.append(phone)
	
def buildIndex(sow,story):
	index = tab('//','INDEX',22)
	index.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),10),
							('TOPPADDING',(0,0),(1,0),20)]))
	sectionset = sow.content_set.order_by('order')
	story.append(index)
	i = 1
	for content in sectionset:
		sectionid = addZero(i)
		sectiontitle = content.sectiontitle
		section_print = tab('{}'.format(sectionid),'{}'.format(sectiontitle),22)	
		section_print.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
								('SIZE',(0,0),(1,0),10),
								('TEXTCOLOR',(0,0),(0,0),numgrey)]))
		story.append(section_print)
		i = i + 1
	
def sectionHeaders(sectionid,sectiontitle):
	sectionhead = tab(sectionid,sectiontitle.upper(),22)
	sectionhead.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),14),
							('TEXTCOLOR',(0,0),(0,0),numgrey),
							('LINEBELOW',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),15),
							('TOPPADDING',(0,0),(1,0),0),
							('RIGHTPADDING',(0,0),(0,0),0)]))
	sectionhead._argW[1] = 500
	return sectionhead

def sectionContent(Story,sectionset):
	Story.append(FrameBreak())
	i = 1
	for content in sectionset:
		sectionid = addZero(i)
		sectiontitle = content.sectiontitle
		sectioncontent = content.sectioncontent
		
		Story.append(sectionHeaders(sectionid,sectiontitle))
		#maincontent(sectioncontent,Story)
		junk(sectioncontent,Story)
		Story.append(Spacer(width=612-mainTextMargin,height=30))
		i = i + 1


	
def prettyDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{} {}, {}".format(month, day, year)

def fileDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{}{}{}".format(month, day, year)


def addZero(num):
	if num < 10:
		sectionid = '0'
		sectionid += str(num)
		return sectionid
	else:
		sectionid = num	
		return sectionid
		
def junk(string,story):
	# temp replace html styling to non-html tags
	string = string.replace('</li>','</li>[br]')
	string = string.replace('<br />','[br]')
	string = string.replace('<b>','[b]')
	string = string.replace('</b>','[/b]')
	string = string.replace('<i>','[i]')
	string = string.replace('</i>','[/i]')
	string = string.replace('<u>','[u]')
	string = string.replace('</u>','[/u]')
	string = string.replace('<div style="margin-left:','[indent')	
	string = string.replace('px; ">','indent]')
	string = string.replace('</div>','[/indent]')
	#string = string.replace('<ol>','[indent 40indent]<ol>')
	#string = string.replace('</ol>','</ol>[/indent]')

	
	# strip away all html
	string = html2text.html2text(string)
	
	# convert non-html tags to reportlab-friendly inline tags
	string = string.replace('[br]','<br/>')
	string = string.replace('[b]','<b>')
	string = string.replace('[/b]','</b>')
	string = string.replace('[i]','<i>')
	string = string.replace('[/i]','</i>')
	string = string.replace('[u]','<u>')
	string = string.replace('[/u]','</u>')

	
	# general non-html tag regex
	bracketre = re.compile('(\[indent .*?indent\].*?\[/indent\])',re.S)
	parsedbracketlist = bracketre.split(string)
	story.append(Spacer(width=612-mainTextMargin,height=10))
	for text in parsedbracketlist:
		indentmatch = re.search('\[indent (.*?)indent\](.*?)\[/indent\]',text,re.S)
		if indentmatch:
			indentamt = indentmatch.group(1)
			indenttext = indentmatch.group(2)
			para = '<para leftIndent={} fontName="Akkurat" fontSize=9>{}</para>'.format(indentamt,indenttext)
			p = Paragraph(para,styles['Normal'])
			story.append(p)			
		else:
			text = text.replace('[/indent]','')
			styles = getSampleStyleSheet()
			styles.add(ParagraphStyle(name='Akkuratfonts',fontName='Akkurat',fontSize=9))
			p = Paragraph(text,styles['Akkuratfonts'])
			story.append(p)

def signatures(story):
	story.append(Spacer(width=612-mainTextMargin,height=100))
	client = tab("Client","Date",150)
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),9),
							('TEXTCOLOR',(0,0),(1,0),numgrey),
							('LINEABOVE',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),50),
							('RIGHTPADDING',(1,0),(1,0),20),
							('LEFTPADDING',(1,0),(1,0),20)]))

	client._argW[1] = 150
	
	agency = tab("Agency","Date",150)
	agency.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),9),
							('TEXTCOLOR',(0,0),(1,0),numgrey),
							('LINEABOVE',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),15),
							('RIGHTPADDING',(1,0),(1,0),20),
							('LEFTPADDING',(1,0),(1,0),20)]))
	agency._argW[1] = 150
	story.append(client)
	story.append(agency)


def printpdf(sow,sectionset):
	versiondate = fileDateTime(datetime.datetime.today())
	filename = "media/pdf/{}{}.pdf".format(sow.project,versiondate)
	pageOne = PageTemplate(id='FirstPage',frames=[frameFirstPageSide,frameFirstPageMain],onPage=ffirstPage(sow))
	mainPages = PageTemplate(id='Sections',frames=[frameLaterPagesMain],onPage=llaterPages(sow))
	doc = BaseDocTemplate(filename.format(filename),pagesize=letter,pageTemplates=[pageOne,mainPages])
	Story = []
	c = canvas.Canvas(filename)
	style = styles['Normal']
	#firstpage client details and index
	c.drawImage("http://some-antics.com/emma/appmedia/side.jpg",0,0,width=mainTextMargin-12,height=792)
	Story.append(FrameBreak())
	projectInfo(sow,Story)
	buildIndex(sow,Story)	
	
	#rest of pages
	Story.append(NextPageTemplate('Sections'))
		
	#main text content
	sectionContent(Story,sectionset)
	
	#signatures
	signatures(Story)
	
	doc.build(Story)

	f = open(filename)
	pdf = File(f)
	sow.pdf = pdf
	sow.pdf.filename = filename
	sow.save()
	
	
	
		