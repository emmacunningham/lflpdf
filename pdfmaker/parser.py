#not actually being used

import re



def marginparseold(string):
	match_re=re.compile('<div style="margin-left: (.*?)px;">(.*?)</(div)>')
	match_obj=match_re.match(string)
	tabamt = match_obj.group(1)
	text = match_obj.group(2)
	match_sub=re.sub('<div style="margin-left: (.*?)px;">(.*?)</(div)>',"{}".format(text),string,flags=0)
	print tabamt
	
def boldparse(string):
	match_re=re.compile("<(b)>(.*?)</(b)>")
	match_obj=match_re.match(string)
	text = match_obj.group(2)
	match_sub=re.sub("<(b)>(.*?)</(b)>","{}".format(text),string,flags=0)
	print match_sub

def italicparse(string):
	match_re=re.compile("<(i)>(.*?)</(i)>")
	match_obj=match_re.match("<i>{}</i>".format(string))
	text = match_obj.group(2)


def marginparse(string):
	for m in re.finditer('<div style="margin-left: (.*?)px;">(.*?)</div>',string):
		tabamt = m.group(1)
		text = m.group(2)
		print text

marginparse('<div style="margin-left: 40px;">hello</div>')


#marginparse('<div style="margin-left: 40px;">indented stuff</div>and then other stuff')

