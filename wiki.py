#!/usr/bin/python

import urllib2
from BeautifulSoup import BeautifulSoup
import xml.dom.minidom
from xml.dom import minidom
import re
import string

wikipedia_base_url = "http://en.wikipedia.org/w/index.php?title=%s&printable=yes"
url = wikipedia_base_url % 'Boca_Raton'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'lookingGlass/0.1')]
page = opener.open(url)
soup = BeautifulSoup(page)

pringle = []
pringle.append("Abstract")
chip = soup.find(summary="Contents").findAll("span","toctext")
for i in chip:
	 pringle.append(re.sub('<.*?>','',str(i)))
#print pringle
tag = iter(pringle)
gringo = soup.findAll('p')
para_list = []
filename = tag.next()
search_tag = re.sub(',','.2C',re.sub(' ','_',tag.next()))
#print gringo[2].find(id=str(pringle[1]))

for i in gringo:
#	if "name" in str(i.a): 
	if search_tag in str(i.a):
		if filename:
			print "\n",re.sub('.2C',',',re.sub('_',' ',filename)),"\n"
			filename = search_tag
			try:
				search_tag = tag.next()
				search_tag = re.sub(',','.2C',re.sub(' ','_',search_tag))
			except: search_tag = ""
		print string.join(para_list, '\n')
		para_list = []
	else:
		para_list.append(re.sub('<.*?>','',str(i)))
#print filename
#print string.join(para_list, '\n')


#	print re.sub('<.*?>','',str(i))
#print re.sub('<.*?>','',str(gringo))
#	while gringo.nextSibling
#print gringo.replace(<?>,'')
#yam = str(gringo.a)
#print yam[yam.find("\"")+1:yam.find("\"",yam.find("\"")+1)]

#print soup.prettify()
