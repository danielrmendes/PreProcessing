#!/usr/bin/python
# -*- coding: utf-8-*-
import csv
from PreProcessing import PreProcessing

def main():
	comments_path = '/Users/tiagosimoes/Documents/Thesis/PreProcessing/comentariosdev.csv'
	comments_file = open(comments_path, 'r')
	reader_comments_file = csv.reader(comments_file)
	newDoc = PreProcessing(reader_comments_file)
	newDoc.clean('csv')
	
if __name__ == '__main__':
    main()