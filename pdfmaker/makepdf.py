import re
import html2text

import pdf.settings
import os

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
pdfmetrics.registerFont(TTFont('Akkurat-Reg','Akkurat_Reg.ttf'))
pdfmetrics.registerFont(TTFont('Akkurat-Light','Akkurat_Light.ttf'))
pdfmetrics.registerFont(TTFont('Akkurat-Bold','Akkurat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Akkurat-Italic','Akkurat-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Gridnik','Gridnik.ttf'))

registerFontFamily('Akkurat-Reg',normal='Akkurat-Reg',bold='Akkurat-Bold',italic='Akkurat-Italic')
registerFontFamily('Akkurat-Light',normal='Akkurat-Light',bold='Akkurat-Bold',italic='Akkurat-Italic')

# margin and padding definitions
sectionLeft = 0 
sectionRight = 24
sectionTop = 39
sectionBottom = 36

mainTextMargin = 190

# frames
frameLaterPagesSide = Frame(x1=0,y1=0,width=mainTextMargin,height=792,topPadding=39.4,bottomPadding=36,rightPadding=0)
frameLaterPagesMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=39.4,bottomPadding=36,rightPadding=24)
frameFirstPageSide = Frame(x1=0,y1=0,width=mainTextMargin,height=792,topPadding=0,leftPadding=0)
frameFirstPageMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=218,leftPadding=0)

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
	textobject.setFont('Akkurat-Light',9)
	textobject.textLines('''
	510 Victoria Ave
	Venice CA 90291
	www.leftfieldlabs.com
	''')
	canvas.drawText(textobject)

def contactleftLaterPages(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,57)
	textobject.setFont('Akkurat-Light',9)
	textobject.textLines('''
	510 Victoria Ave
	Venice CA 90291
	www.leftfieldlabs.com
	''')
	canvas.drawText(textobject)
	
def firstPage(canvas, doc):
	canvas.saveState()
	canvas.drawImage('http://some-antics.com/emma/appmedia/side.jpg',0,0,width=mainTextMargin-12,height=792)
	lfleft(canvas)
	contactleftFirstPage(canvas)
	canvas.restoreState()

def laterPages(canvas, doc):
	canvas.saveState()
	canvas.drawImage('http://some-antics.com/emma/appmedia/side.jpg',0,0,width=mainTextMargin-12,height=792)
	contactleftLaterPages(canvas)
	canvas.restoreState()

	
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
	project.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	date.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	author.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	phone.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
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
		section_print.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
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
							('TOPPADDING',(0,0),(1,0),30),
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
		i = i + 1


	
def prettyDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{} {}, {}".format(month, day, year)
	

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
	string = string.replace('<br />','[br]')
	string = string.replace('<b>','[b]')
	string = string.replace('</b>','[/b]')
	string = string.replace('<i>','[i]')
	string = string.replace('</i>','[/i]')
	string = string.replace('<u>','[u]')
	string = string.replace('</u>','[/u]')
	string = string.replace('<div style="margin-left: ','[indent')	
	string = string.replace('px; ">','indent]')
	string = string.replace('</div>','[/indent]')
	
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
	bracketre = re.compile('((.*?)<u>)')
	parsedbracketlist = bracketre.split(string)
	bracketmatch = re.search(bracketre,string)
	for text in parsedbracketlist:	
		if bracketmatch:
			p = Paragraph("brackets!",styles['Normal'])
			story.append(p)
		else:
			p = Paragraph(string,styles['Normal'])
			story.append(p)

def signatures(story):
	story.append(Spacer(width=612-mainTextMargin,height=100))
	client = tab("Client","Date",150)
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),9),
							('TEXTCOLOR',(0,0),(1,0),numgrey),
							('LINEABOVE',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),50),
							('RIGHTPADDING',(1,0),(1,0),20),
							('LEFTPADDING',(1,0),(1,0),20)]))

	client._argW[1] = 150
	
	agency = tab("Agency","Date",150)
	agency.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),9),
							('TEXTCOLOR',(0,0),(1,0),numgrey),
							('LINEABOVE',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),15),
							('RIGHTPADDING',(1,0),(1,0),20),
							('LEFTPADDING',(1,0),(1,0),20)]))
	agency._argW[1] = 150
	story.append(client)
	story.append(agency)
	
def maincontent(string,story):
	match = re.compile('(.*?<div style="margin-left: .*?px; ">.*?</div>)')
	match_obj = re.match(match,string)
	parsedlist = match.split(string)
	p = parsedlist[-1]
	if match_obj:
		for m in re.finditer('(.*?)<div style="margin-left: (.*?)px; ">(.*?)</div>',string):
			htext = m.group()
			pretext = m.group(1)
			#pretext = html2text.html2text(pretext)
			tabamt = m.group(2)
			text = m.group(3)
			#text = html2text.html2text(text)
			pre = Paragraph("<para spaceAfter=0 spaceBefore=10><font name='Akkurat-Light' size=9>{}</font></para>".format(pretext),styles['Normal'])
			t = tab('',text,int(tabamt)/2)
			t.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
									('SIZE',(0,0),(1,0),9),
									('TOPPADDING',(0,0),(1,0),0),
									('BOTTOMPADDING',(0,0),(1,0),0)]))
			
			story.append(pre)
			story.append(t)
		rest = p
		#rest = html2text.html2text(rest)
		rtext = Paragraph("<para spaceAfter=0 spaceBefore=10><font name='Akkurat-Light' size=9>{}</font></para>".format(rest),styles['Normal'])	
		story.append(rtext)
	else:
		#string = html2text.html2text(string)
		story.append(Paragraph("<para spaceAfter=40 spaceBefore=10><font name='Akkurat-Light' size=9>{}</font></para>".format(string),styles['Normal']))
	
def printpdf(sow,sectionset):
	filename = "{}.pdf".format(sow.project)
	pageOne = PageTemplate(id='FirstPage',frames=[frameFirstPageSide,frameFirstPageMain],onPage=firstPage)
	mainPages = PageTemplate(id='Sections',frames=[frameLaterPagesMain],onPage=laterPages)
	doc = BaseDocTemplate(filename.format(filename),pagesize=letter,pageTemplates=[pageOne,mainPages])
	Story = []
	c = canvas.Canvas(filename)
	style = styles['Normal']
	
	#firstpage client details and index
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

	



