#!/usr/bin/python
# -*- coding: utf-8-*-
import csv
from PreProcessing import PreProcessing

# main
# --Basic
# 
# Removal of URLs
# Escaping HTML characteres
# Removal of emails
# Lowercase 
# Removal of Stop-words
# Removal of Punctuations
# Removal of numbers in the middle of the text
# Standardizing words
# Separate Punctuation from words
#
# -Removal of Expressions
# -Split Attached Words
# -Slang lookups
# -Decoding data (if different from utf-8)
# -Apostrophe Lookup (if English)
#
# --Advanced
# Grammar checking
# Spelling correction

#Para remover o utilizador de um Tweet podemos usar a API do twitter

# 	>>>>>>>L E R<<<<<<<<
# from nltk.stem.porter import PorterStemmer
# porter = PorterStemmer()
#
def main():
	comments_path = '/Users/tiagosimoes/Documents/TAP/Dados-Categorizados/comentarios-treino.csv'
	comments_file = open(comments_path, 'r')
	reader_comments_file = csv.reader(comments_file)
	newDoc = PreProcessing(reader_comments_file)
	newDoc.clean()
if __name__ == '__main__':
    main()