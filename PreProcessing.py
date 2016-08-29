#!/usr/bin/python
# -*- coding: utf-8-*-
import re
import sys
import HTMLParser 
import string 
import itertools
import math
import pandas as pd
from nltk.corpus import stopwords 
import operator
from collections import OrderedDict
from itertools import groupby
import urlparse

class PreProcessing():
	def __init__(self, file_comments):
		self.file_comments = file_comments 

	def getMessage(self, arr_row):
	#returns the message in the given row
		return arr_row[1]

	def getCategory(self, arr_row):
	#return the category in the given row
		return arr_row[0]

	def removeURL(self, arr_row):
		str_message = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', self.getMessage(arr_row))
		return self.getCategory(arr_row), str_message

	def htmlParser(self, arr_row):
	# transform html special chars | &lt;3 -> <3 | &amp; -> &
		html_parser = HTMLParser.HTMLParser()
		str_message = html_parser.unescape(self.getMessage(arr_row))
		return self.getCategory(arr_row), str_message

	def removeTwitterUsersnames(self, arr_row):
		entity_prefixes = ['@','#']
		for separator in  string.punctuation:
			if separator not in entity_prefixes:
				text = self.getMessage(arr_row).replace(separator,' ')
		words = []
		for word in text.split():
			word = word.strip()
			if word:
				if word[0] not in entity_prefixes:
					words.append(word)
		str_message = ' '.join(words)
		return self.getCategory(arr_row), str_message

	def removeEmail(self, arr_row):
		str_message = re.sub(r'[\w\.-]+@[\w\.-]+', r'', self.getMessage(arr_row))
		return self.getCategory(arr_row), str_message

	def lowercaseMessage(self, arr_row):
		str_message = self.getMessage(arr_row).lower()
		return self.getCategory(arr_row), str_message

	def removeStopwords(self, arr_row):
		stop = set(stopwords.words('portuguese'))
		# words must have more than 2 chars and do not belong to the set stop
		list_message = [i for i in self.getMessage(arr_row).split() if i not in stop and len(i) >= 2]
		# Update list
		# list_message.update('word1','word2',...)
		str_message = ''
		for word in list_message:
			str_message += word + ' '
		return self.getCategory(arr_row), str_message[:-1]

	def removePunctuation(self,arr_row):
	# '''Strips punctuation from list of words'''
		list_punctuation = ['#', '"','£','$','€', '%', "'", '&', ')', '(', '+', '*', ',',\
		 '/', '.', ';', ':', '=', '<', '>', '@', '[', ']','-', '_', '\\', '^', '`',\
		  '{', '}', '|', '~']
		exclude = set(list_punctuation)
		str_message = ''.join(ch for ch in self.getMessage(arr_row) if ch not in exclude)
		return self.getCategory(arr_row), str_message

	def removeNumbers(self,arr_row):
		str_message = self.getMessage(arr_row)
		# this function below removes words that contain numbers
		str_message = ' '.join(s for s in str_message.split() if not any(c.isdigit() for c in s))
		# this function below removes all numbers in the text
		str_message = re.sub('^[0-9 ]+', '', str_message)
		# this function below removes all numbers that are not mixed with text
		#messageWithoutNumbers = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", getMessage(row))
		return self.getCategory(arr_row), str_message

	def standardizeWords(self,arr_row):
		str_message = ''.join(''.join(s)[:2] for _, s in itertools.groupby(self.getMessage(arr_row)))
		return self.getCategory(arr_row), str_message

	def separatePunctuation(self,arr_row):
		list_punctuation = '([.,!?()-])'
		messageWithSpaces = re.sub(list_punctuation, r' \1 ', self.getMessage(arr_row))
		str_message = re.sub('\s{2,}', ' ', messageWithSpaces)
		return self.getCategory(arr_row), str_message

	def standardizeEmojis(self,arr_row):
		# str_message = re.sub(' \:\) ', ' emoji_feliz ', self.getMessage(arr_row))
		str_message = self.getMessage(arr_row).replace(":)", "emojifeliz")
		str_message = str_message.replace(":-)", "emojifeliz")
		str_message = str_message.replace(":d", "emojifeliz")
		str_message = str_message.replace(":\'d", "emojifeliz")
		str_message = str_message.replace(":p", "emojifeliz")
		str_message = str_message.replace(";)", "emojifeliz")
		str_message = str_message.replace(":(", "emojitriste")
		str_message = str_message.replace(":/", "emojitriste")
		str_message = str_message.replace(";(", "emojitriste")
		str_message = str_message.replace(":\'(", "emojitriste")
		return self.getCategory(arr_row), str_message

	def clean(self):
		for arr_row in self.file_comments:
			arr_row = self.removeURL(arr_row)
			arr_row = self.htmlParser(arr_row)
			arr_row = self.lowercaseMessage(arr_row)
			arr_row = self.removeEmail(arr_row)
			arr_row = self.removeTwitterUsersnames(arr_row)
			arr_row = self.removeNumbers(arr_row)
			arr_row = self.standardizeEmojis(arr_row)
			arr_row = self.standardizeWords(arr_row)
			arr_row = self.removeStopwords(arr_row)
			arr_row = self.removePunctuation(arr_row)
			arr_row = self.separatePunctuation(arr_row)
			# print only string not empty
			if self.getMessage(arr_row):
				print self.getCategory(arr_row) + ',' + '\'' + self.getMessage(arr_row).strip() + '\''
		
