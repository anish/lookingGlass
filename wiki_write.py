#!/usr/bin/python

import urllib2
from BeautifulSoup import BeautifulSoup
import xml.dom.minidom
from xml.dom import minidom
import re
import string
import os
import sys

if len(sys.argv) != 2:
	print "Incorrect arguments"
	exit(22)
else:
	dir_name = re.sub(' ','_',sys.argv[1])

wikipedia_base_url = "http://en.wikipedia.org/w/index.php?title=%s&printable=yes"
url = wikipedia_base_url % dir_name

dir_name = "./" + dir_name + "/"
if not os.path.isdir(dir_name):
	os.mkdir(dir_name)

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'lookingGlass/0.1')]
page = opener.open(url)
soup = BeautifulSoup(page)

contents = []
para_list = []
contents.append("Abstract")
contents_soup = soup.find(summary="Contents").findAll("span","toctext")
for i in contents_soup:
	 contents.append(re.sub('<.*?>','',str(i)))

tag = iter(contents)
para_soup = soup.findAll('p')
filename = tag.next()
search_tag = re.sub(',','.2C',re.sub(' ','_',tag.next()))

for i in para_soup:
	if search_tag in str(i.a):
		if filename:
			f = open(dir_name + filename,'w')
			#print "\n",re.sub('.2C',',',re.sub('_',' ',filename)),"\n"
			filename = search_tag
			try:
				search_tag = tag.next()
				search_tag = re.sub(',','.2C',re.sub(' ','_',search_tag))
			except: search_tag = ""
			f.write(re.sub('\[.*\]','',string.join(para_list, '\n')) + "\n")
			para_list =[]
			f.close()
		#print re.sub('\[.*\]','',string.join(para_list, '\n'))
	else:
		para_list.append(re.sub('<.*?>','',str(i)))
