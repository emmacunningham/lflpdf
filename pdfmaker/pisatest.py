from xhtml2pdf import pisa, context

def helloWorld():
	filename = __file__ + ".pdf"                
	p = "hello"

	pdf = pisa.CreatePDF(p,file(filename, "wb"))
	if not pdf.err:                             
		pisa.startViewer(filename)               

if __name__=="__main__":
	pisa.showLogging()                         
	
helloWorld()
