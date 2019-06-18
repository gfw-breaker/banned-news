#!/usr/bin/python
# coding: utf-8

import macros
import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
channel_url = sys.argv[2]

index_page = '' + macros.head
links = macros.tail


def get_content(url):
	response = requests.get(url)
	text = response.text.encode('ISO-8859-1')
	parser = BeautifulSoup(text, 'html.parser').find('div', id= 'article-content')
	for script in parser.find_all('script'):
		script.decompose()
	for iframe in parser.find_all('iframe'):
		iframe.decompose()
	for img in parser.find_all('img'):
		del img['width']
		del img['height']
		del img['sizes']
	post_title = parser.find('div', attrs = {'class': 'zhidingtu'})
	if post_title is None:
		post_title = ''
	else:
		post_title = post_title.prettify().encode('utf-8') \
			.replace('//img.soundofhope.org', 'http://img.soundofhope.org')
	post_content = parser.find('div', attrs = {'class': 'content'})
	if post_content is None:
		post_cotent =  '-'
	else:
		post_content = post_content.prettify().encode('utf-8') \
			.replace('//img.soundofhope.org', 'http://img.soundofhope.org') \
			.replace('<h1>', '<h3>').replace('<h1 ', '<h3 ').replace('</h1>', '</h3>') \
			.replace('<h2>', '<h4>').replace('<h2 ', '<h4 ').replace('</h2>', '</h4>')
	return post_title + '<hr/>\n' + post_content


def get_name(link):
	fname = link.split('/')[-1]
	aid  = fname.split('.')[0]
	return aid


def write_page(name, path, title, link, content):
	new_link = macros.git_base_url + '/' + channel + '/' + name 
	body = '### ' + title
	body += "\n------------------------\n\n" + macros.menu + "\n\n" + content
	body += "\n<hr/>\n手机上长按并复制下列链接或二维码分享本文章：<br/>"
	body += "\n" + new_link + " <br/>"
	body += "\n<a href='" + new_link + "'><img src='" + new_link + ".png'/></a> <br/>"
	body += "\n原文地址（需翻墙访问）：" + link + "\n"
	body += "\n\n------------------------\n" + links
	fh = open(path, 'w')
	fh.write(body)
	fh.close()


index_text = requests.get(channel_url).text.encode('utf-8')
index_html = BeautifulSoup(index_text, 'html.parser')
articles = index_html.find('div', attrs = {'class':'list-ref-2'}).find_all('a')
for article in articles:
	a_url = 'http:' + article.get('href').encode('utf-8')
	#print a_url
	a_title = article.find('div', attrs = {'class':'title'})
	for span in a_title.find_all('span'):
		span.decompose()
	a_title = a_title.text.encode('utf-8').strip()
	#print a_title
	name = get_name(a_url) + '.md'
	file_path = '../pages/' + channel + '/' + name 
	#content = get_content(a_url)

	if not os.path.exists(file_path):
		print file_path
		content = get_content(a_url)
		write_page(name, file_path, a_title, a_url, content)
	index_page += '#### [' + a_title + '](' + file_path + ') \n\n'


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()



