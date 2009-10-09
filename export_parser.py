#!/usr/bin/python

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import string
import os
import sys

if len(sys.argv) != 2:
	print "Incorrect arguments"
	exit(22)
else:
	base_dir_name = re.sub(' ','_',sys.argv[1])

wikipedia_base_url = "http://en.wikipedia.org/wiki/Special:Export/%s"
url = wikipedia_base_url % base_dir_name

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'lookingGlass/0.1')]
page = opener.open(url)
soup = BeautifulSoup(page)

if "REDIRECT" in soup.text.contents[0]:
	base_dir_name = re.sub(' ','_',re.sub(r'.*\[\[(.*)\]\]',r'\1',soup.text.contents[0]))
	url = wikipedia_base_url % base_dir_name
	page = opener.open(url)
	soup = BeautifulSoup(page)

page_list = []
page_list.append(base_dir_name)
broth = re.sub("\|[^\]]*?\]\]",']]',soup.text.contents[0])
regex = re.compile("\[\[([\w\s]*)\]\]")
for i in regex.findall(broth):
	page_list.append(re.sub(' ','_',i))

for dir_name in page_list:
	url = wikipedia_base_url % dir_name
	if dir_name != base_dir_name:
		page = opener.open(url)
		soup = BeautifulSoup(page)
		if "REDIRECT" in soup.text.contents[0]:
			dir_name = re.sub(' ','_',re.sub(r'.*\[\[(.*)\]\]',r'\1',soup.text.contents[0]))
			url = wikipedia_base_url % base_dir_name
			page = opener.open(url)
			soup = BeautifulSoup(page)
		dir_name = "./" + base_dir_name + "/" + dir_name + "/"
	else:
		dir_name = "./" + base_dir_name + "/"
	if not os.path.isdir(dir_name):
		os.mkdir(dir_name)
	contents = []
	para_list = []

	contents.append("Abstract")
	regex = re.compile("==[\w\s]*?==")
	jack = regex.findall(soup.text.contents[0])
	for i in jack:
		contents.append(i.strip("==").strip(' '))

	regex = re.compile('\{{2}.ite.*?\}{2}\n?',re.DOTALL | re.MULTILINE)
	broth = re.sub(regex,'',soup.text.contents[0])
	broth = re.sub("&.t.*?&.t;\n?",'',broth)
	regex = re.compile("\[\[Image.+?(\[\[[\w\s\.]*?\]\])?.*\]\]\n?")
	broth = re.sub(regex,'',broth)
	regex = re.compile("\[\[File.+?(\[\[[\w\s\.]*?\]\])?.*\]\]\n?")
	broth = re.sub(regex,'',broth)
	broth = re.sub('\[\[[a-z\-]{2,10}\:.*\]\]\n?','',broth)
	regex = re.compile('\{\|.*?\|\}\n?',re.DOTALL | re.MULTILINE)
	broth = re.sub(regex,'',broth)
	regex = re.compile('\{\{.*?\}\}\n?',re.DOTALL | re.MULTILINE)
	broth = re.sub(regex,'',broth)
	regex = re.compile('\{.*?\}\n?',re.DOTALL | re.MULTILINE)
	broth = re.sub(regex,'',broth)
	broth = re.sub("http\:[^\s|^\]]*",'',broth)
	pattern = re.compile('\[\[Category\:.*\]\]\n?',re.IGNORECASE)
	broth = re.sub(pattern,'',broth)
	broth = re.sub("\[\[[^\]]*?\|",'[[',broth)
	broth = re.sub("\* |\[ ?| ?\]|\'{2,3}|\&.{2,4}\;|\{|\}",'',broth)

	regex = re.compile("=?=?.*?==",re.DOTALL|re.MULTILINE)
	tag = iter(contents)
	filename = tag.next()
	search_tag = tag.next()
	text = regex.findall(broth)
	for i in text:
        	if search_tag in i.strip("="):
                	if filename:
                        	filename = re.sub(',','.2C',re.sub(' ','_',filename))
	                        f = open(dir_name + filename,'w')
        	                filename = search_tag
                	        try:
                        	        search_tag = tag.next()
	                        except: search_tag = ''
        	                f.write(string.join(para_list, '\n') + "\n")
                	        para_list = []
                        	f.close()
	        else:
        	        para_list.append(i.strip("=").encode("utf-8"))
