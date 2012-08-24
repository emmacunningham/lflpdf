import re
import html2text
import datetime
import time

import pdf.settings as pdfsettings
import os

from django.core.files import File
from django.core.files.storage import FileSystemStorage, default_storage


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
reportlab.rl_config.TTFSearchPath.append( os.path.join(pdfsettings.STATIC_ROOT,'fonts') )

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
	textobject.setFont('Gridnik',27)
	textobject.textLines('''
	LEFT 
	FIELD 
	LABS
	''')
	canvas.drawText(textobject)
	
def contactleftFirstPage(canvas):
	textobject = canvas.beginText()
	addrwidth = canvas.stringWidth('510 Victoria Ave, Venice CA 90291','Akkurat',10)
	urlwidth = canvas.stringWidth('www.leftfieldlabs.com','Akkurat',10)
	urlx = addrwidth - urlwidth + 18
	phonewidth = canvas.stringWidth('424-500-2045','Akkurat',10)	
	phonex = addrwidth - phonewidth + 18	
	textobject.setTextOrigin(18,75)	
	textobject.setFont('Akkurat',10)
	textobject.textLine('510 Victoria Ave, Venice CA 90291')
	yy = textobject.getY()
	textobject.setTextOrigin(urlx,yy)
	textobject.textLine('www.leftfieldlabs.com')
	yyy = textobject.getY()
	textobject.setTextOrigin(phonex,yyy)
	textobject.textLine('424-500-2045')
	canvas.drawText(textobject)


def contactleftLaterPages(canvas):
	textobject = canvas.beginText()
	lflwidth = canvas.stringWidth('LEFT FIELD LABS','Gridnik',12)
	addrwidth = canvas.stringWidth('510 Victoria Ave, Venice CA 90291','Akkurat',10)
	urlwidth = canvas.stringWidth('www.leftfieldlabs.com','Akkurat',10)
	phonewidth = canvas.stringWidth('424-500-2045','Akkurat',10)	
	phonex = addrwidth - phonewidth + 18
	lflx = addrwidth - lflwidth + 18
	urlx = addrwidth - urlwidth + 18
	textobject.setTextOrigin(lflx,75)
	textobject.setFont('Gridnik',12)
	textobject.textLine('LEFT FIELD LABS')
	y = textobject.getY()
	textobject.setTextOrigin(18,y)
	textobject.setFont('Akkurat',10)
	textobject.textLine('510 Victoria Ave, Venice CA 90291')
	yy = textobject.getY()
	textobject.setTextOrigin(urlx,yy)
	textobject.textLine('www.leftfieldlabs.com')
	yyy = textobject.getY()
	textobject.setTextOrigin(phonex,yyy)
	textobject.textLine('424-500-2045')
	canvas.drawText(textobject)

def ffirstPage(sow):
	img = sow.img
	def firstPage(canvas, doc):
		canvas.saveState()
		if img:
			path = os.path.join(pdfsettings.MEDIA_ROOT, 'img/{0}'.format(img.name))
			canvas.drawImage(path,0,0,width=mainTextMargin-12,height=792)
		else:
			path = os.path.join(pdfsettings.MEDIA_ROOT, 'img/default.jpg')
			canvas.drawImage(path,0,0,width=mainTextMargin-12,height=792)
			
		lfleft(canvas)
		contactleftFirstPage(canvas)
		canvas.restoreState()
	return firstPage
		
def llaterPages(sow):
	img = sow.img
	def laterPages(canvas, doc):
		canvas.saveState()
		if img:
			path = os.path.join(pdfsettings.MEDIA_ROOT, 'img/{0}'.format(img.name))
			canvas.drawImage(path,0,0,width=mainTextMargin-12,height=792)
		else:
			path = os.path.join(pdfsettings.MEDIA_ROOT, 'img/default.jpg')
			canvas.drawImage(path,0,0,width=mainTextMargin-12,height=792)
		contactleftLaterPages(canvas)
		canvas.restoreState()
	return laterPages
	
# hacked tabbing
def tab(left,right,tabamt):
	data = [['{0}'.format(left),'{0}'.format(right)]]
	t = Table(data)
	t.hAlign = 'LEFT'
	t.setStyle(TableStyle([('LEFTPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('TOPPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('BOTTOMPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('ALIGN',(0,0),(1,0),'LEFT')]))
	t._argW[0]=tabamt
	return t
	
def partab(left,right,tabamt):
	data = [[left,right]]
	t = Table(data)
	t.hAlign = 'LEFT'
	t.setStyle(TableStyle([('LEFTPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('TOPPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('BOTTOMPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('ALIGN',(0,0),(1,0),'LEFT')]))
	t._argW[0]=tabamt
	return t	
	
def projectInfo(sow,story):
	authorname = '{0} {1}'.format(sow.author.user.first_name,sow.author.user.last_name)
	authoremail = sow.author.user.email
	statementofwork = Paragraph("<para spaceAfter=20><font name='Akkurat-Reg' size=16>// STATEMENT OF WORK<br/></font></para>",styles['Normal'])
	project = tab('PROJECT:',sow.project,83)
	client = tab('CLIENT:',sow.client,83)
	date = tab('DATE:',prettyDateTime(sow.pub_date),83)
	author = tab('CONTACT:',authorname,83)
	email = tab('',authoremail,83)
	project.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),5),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),5),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	date.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),5),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	author.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),5),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	email.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),5),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	story.append(statementofwork)
	story.append(project)
	story.append(client)
	story.append(date)
	story.append(author)
	story.append(email)
	
def buildIndex(sow,story):
	index = tab('//','INDEX',22)
	index.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),12),
							('TOPPADDING',(0,0),(1,0),20)]))
	sectionset = sow.content_set.order_by('order')
	story.append(index)
	i = 1
	for content in sectionset:
		sectionid = addZero(i)
		sectiontitle = content.sectiontitle
		section_print = tab('{0}'.format(sectionid),'{0}'.format(sectiontitle),22)	
		section_print.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
								('SIZE',(0,0),(1,0),12),
								('TOPPADDING',(0,0),(1,0),5),
								('TEXTCOLOR',(0,0),(0,0),numgrey)]))
		story.append(section_print)
		i = i + 1
	
def sectionHeaders(sectionid,sectiontitle):
	sectionhead = tab(sectionid,sectiontitle.upper(),22)
	sectionhead.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),16),
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
		formatsectioncontent(sectioncontent,Story)
		Story.append(Spacer(width=612-mainTextMargin,height=30))
		i = i + 1
	#agreement
	Story.append(sectionHeaders(addZero(i),"Agreement"))


	
def prettyDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{0} {1}, {2}".format(month, day, year)

def fileDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{0}_{1}_{2}".format(month, day, year)


def addZero(num):
	if num < 10:
		sectionid = '0'
		sectionid += str(num)
		return sectionid
	else:
		sectionid = num	
		return sectionid


def formatsectioncontent(string,story):
	string = string.replace('&nbsp;','')
	string = string.replace('<br>','[br]')

	def dumbb(matchobj):
		s = matchobj.group(1)
		return s

	string = re.sub('<b .*?>(.*?)</b>',dumbb,string)


	def dumbp(matchobj):
		p = re.search('padding-left: (.*?)px;',matchobj.group(1))
		if p:
			s = '[indent {0}indent]'.format(p.group(1))
			s += matchobj.group(2)
			s += '[/indent]'
			return s
		else:
			s = matchobj.group(2)
			s += '[br]'
			return s
				
	string = re.sub('<p (.*?)>(.*?)</p>',dumbp,string)

	def dumbspan(matchobj):
		s = ''
		s += matchobj.group(1)
		return s

	string = re.sub('<span .*?>(.*?)</span>',dumbspan,string)

	# temp replace html styling to non-html tags
	string = string.replace('<br />','[br]')
	string = string.replace('<b>','[b]')
	string = string.replace('</b>','[/b]')
	string = string.replace('<i>','[i]')
	string = string.replace('</i>','[/i]')
	string = string.replace('<u>','[u]')
	string = string.replace('</u>','[/u]')

	def dumbul(matchobj):
		s = ''
		s += matchobj.group(1)
		return s

	string = re.sub('<ul .*?>(.*?)</ul>',dumbul,string)



	string = string.replace('<ul>','[ul]')
	string = string.replace('</ul>','[/ul]')

	def lidash(matchobj):
		s = matchobj.group()
		s = s.replace('<li>','-')
		s = s.replace('</li>','[br]')
		return s

	#string = re.sub('\[ul\].*?(<li>)(.*?)</li>.*?\[/ul\]',lidash,string)
	
	string = string.replace('<li>','- ')
	string = string.replace('</li>','[br]')	

	string = string.replace('[ul]','[br]')
	string = string.replace('[/ul]','')

	string = string.replace('<div style="margin-left:','[indent')	
	string = string.replace('px; ">','indent]')
	string = string.replace('</div>','[/indent]')

	def dumba(matchobj):
		if len(matchobj.group(2)) > 80:
			s =  matchobj.group(1)
			s += 'link'
			s += '</a>'
		else:
			s =  matchobj.group(1)
			s += matchobj.group(2)
			s += '</a>'
		return s

	string = re.sub('(<a .*?>)(.*?)</a>',dumba,string)
	
	def dumbol(matchobj):
		s = matchobj.group(1)
		c = 1
		listitems = ''
		for i in re.finditer('<li .*?>(.*?)</li>',s):
			listitems += str(c)
			listitems += '.'
			listitems += ' '
			listitems += i.group(1)
			c = c + 1
		return listitems

	string = re.sub('<ol .*?>(.*?)</ol>',dumbol,string)
	
	def dumbli(matchobj):
		s = '-'
		s += matchobj.group(1)
		return s


	
	def dumbtable(matchobj):
	  s = '[table]'+matchobj.group(1)+'[/table]'
	  return s

	string = re.sub('<table .*?>(.*?)</table>',dumbtable,string,flags=re.M|re.S)            
	# strip away all html
	#string = html2text.html2text(string)

	# convert pseudo-html tags to reportlab-friendly inline tags
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
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Akkuratfonts11',fontName='Akkurat',fontSize=11))
	for text in parsedbracketlist:	  
		indentmatch = re.search('\[indent (.*?)indent\](.*?)\[/indent\]',text,re.S)
		tablematch = re.search('\[table\]',text,re.S|re.M)		  					
		if indentmatch:
			indentamt = indentmatch.group(1)
			indenttext = indentmatch.group(2)
			para = '<para leftIndent={0} fontName="Akkurat" fontSize=11>{1}</para>'.format(indentamt,indenttext)
			p = Paragraph(para,styles['Normal'])
			story.append(p)
		elif tablematch:
		  tablere = re.compile('(\[table\].*?\[/table\])',re.S)
		  parsedtablelist = tablere.split(text)
		  for ttext in parsedtablelist:
		    if re.search(tablere,ttext):
		      rowre = re.compile('<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>',re.S|re.M)
		      rowsearch = re.search(rowre,ttext)
		      #parsedrowlist = rowre.split(ttext)
		      for match in rowre.finditer(ttext):
		        col1 = Paragraph(match.group(1),styles['Akkuratfonts11'])
		        col2 = Paragraph(match.group(2),styles['Akkuratfonts11'])
		        row = partab(col1,col2,120)

		        story.append(row)
		    else:
		      nontable = Paragraph(ttext,styles['Akkuratfonts11'])
		      story.append(nontable)
		else:
		  text = text.replace('[/indent]','')
		  p = Paragraph(text,styles['Akkuratfonts11'])
		  story.append(p)
			

def signatures(sow,story):
	story.append(Spacer(width=612-mainTextMargin,height=100))
	client_agency = sow.client
	if sow.client_contact:
		client_signature = sow.client_contact + '\n' + client_agency
	else:
	  client_signature = client_agency + '\n'
	client = tab(client_signature,"Date\n",150)
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),11),
							('TEXTCOLOR',(0,0),(1,0),numgrey),
							('LINEABOVE',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),50),
							('RIGHTPADDING',(1,0),(1,0),20),
							('LEFTPADDING',(1,0),(1,0),20)]))
	client._argW[1] = 150
	agency_signature_rep = sow.agency_signature
	agency_signature = '{0} - Partner\nLeft Field Labs, LLC'.format(agency_signature_rep)
	
	agency = tab(agency_signature,"Date\n",150)
	agency.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat'),
							('SIZE',(0,0),(1,0),11),
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
	s = '{0}'.format(sow.project)
	s = s.replace(' ','')

	s = s.replace('/','_')
	filename = os.path.join(pdfsettings.MEDIA_ROOT,"pdf/sow/{0}_{1}.pdf".format(s,versiondate))


	pageOne = PageTemplate(id='FirstPage',frames=[frameFirstPageSide,frameFirstPageMain],onPage=ffirstPage(sow))
	mainPages = PageTemplate(id='Sections',frames=[frameLaterPagesMain],onPage=llaterPages(sow))
	doc = BaseDocTemplate(filename,pagesize=letter,pageTemplates=[pageOne,mainPages])
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
	signatures(sow,Story)

	doc.build(Story)

	f = open(filename)
	pdf = File(f)
	sow.pdf.filename = filename
	sow.pdf = pdf
	sow.save()
		