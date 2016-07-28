#!/usr/bin/python
# -*- coding: utf-8-*-

import csv
import sys
import re
import HTMLParser
import string 
import itertools

# files
comments_path = '/Users/tiagosimoes/Documents/TAP/Comentários Para Limpar/ComentariosMerged1.csv'
stopwordlist_path = '/Users/tiagosimoes/Documents/TAP/Portuguese-Stopwords-List-100.csv'


#program
def getMessage(row):
	#returns the message in the given row
	return row[1]

def getCategory(row):
	#return the category in the given row
	return row[0]

# def make_utf8(input):
#         input =  input.encode('utf-8')
#         return input

def removeEmail(row):
	# remove emails from strings
	# return a row  
	messageWithoutEmail = re.sub(r'[\w\.-]+@[\w\.-]+', r'', getMessage(row))
	return getCategory(row), messageWithoutEmail

def htmlParser(row):
	# transform html special chars | &lt;3 -> <3 | &amp; -> &
	# return a row
	html_parser = HTMLParser.HTMLParser()
	messageWithoutHtmlChars = html_parser.unescape(getMessage(row))
	return getCategory(row), messageWithoutHtmlChars

def splitAttachedWords(row):
	# useful in twitter | #DisplayIsAwesome -> Display Is Awesome
	# it only words when there are uppercases and lowercases
	# return a row
	messageNoAttachedWords = ' '.join(re.findall('[A-Z][^A-Z]*', getMessage(row)))
	return getCategory(row), messageNoAttachedWords

def getStopwordsList():
	stopwordlist_file = open(stopwordlist_path, 'r')
	try:
		reader_stopwordlist_file = csv.reader(stopwordlist_file)
		stopwordlist_list = []
		for row in reader_stopwordlist_file:
			stopwordlist_list.append(row[0])
			#stopwordlist_list.append(make_utf8(row[0]))
		return stopwordlist_list
	finally:
		stopwordlist_file.close()

def removeStopwords(row):
	stopwords = getStopwordsList()
	messageNoStopwords = ' '.join([word for word in getMessage(row).split()\
		if word not in stopwords])
	return getCategory(row), messageNoStopwords

def lowercaseMessage(row):
	return getCategory(row), getMessage(row).lower()

def removePunctuation(row):
	'''Strips punctuation from list of words'''
	punctuationList = ['#', '"', '%', "'", '&', ')', '(', '+', '*', ',',\
	 '/', '.', ';', ':', '=', '<', '>', '@', '[', ']', '\\', '^', '`',\
	  '{', '}', '|', '~']
	exclude = set(punctuationList)
	messageWithoutPunctuation = ''.join(ch for ch in getMessage(row)\
	 if ch not in exclude)
	return getCategory(row), messageWithoutPunctuation

def separatePunctuationFromString(row):
	punctuationList_string = '([.,!?()])'
	messageWithSpaces = re.sub(punctuationList_string, r' \1 ', getMessage(row))
	messageWithSpaces = re.sub('\s{2,}', ' ', messageWithSpaces)
	return getCategory(row), messageWithSpaces

def removeURLs(row):
	messageWithoutURLs = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', getMessage(row))
	return getCategory(row), messageWithoutURLs

def removeNumbers(row):
	messageWithoutNumbers = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", getMessage(row))
	return getCategory(row), messageWithoutNumbers


# main
# --Basic
# Escaping HTML characteres
# -Decoding data (if different from utf-8)
# -Apostrophe Lookup (if English)
# Removal of Stop-words
# Removal of Punctuations
# -Removal of Expressions
# -Split Attached Words
# -Slang lookups
# Standardizing words
# Removal of URLs
# --Advanced
# Grammar checking
# Spelling correction

#Para remover o utilizador de um Tweet podemos usar a API do twitter

comments_file = open(comments_path, 'r')
try:
    reader_comments_file = csv.reader(comments_file)
    
    for row in reader_comments_file: # row is a list: [category, message]
    	# print 'C: ' , removeEmail(row)[0]
    	# print 'M: ', removeEmail(row)[1]
    	# it is all in lower case, there is no use of this right now
    	#row = splitAttachedWords(row)
    	print 'a: ',row[1]
    	row = removeURLs(row)
    	row = htmlParser(row)
    	row = removeEmail(row)
    	row = lowercaseMessage(row)
    	row = removeStopwords(row)
    	row = removePunctuation(row)
    	row = removeNumbers(row)
    	row = standardizingWords(row)
    	row = separatePunctuationFromString(row)
    	print 'n: ',row[1]
    	#print row
finally:
    comments_file.close()




