# -*- coding:utf-8 -*-

import os
import math
import nltk
import re
from nltk.probability import FreqDist
#from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize


pattern = r'''(?x)    # set flag to allow verbose regexps
		([A-Z]\.)+        # abbreviations, e.g. U.S.A.
		| \w+(-\w+)*        # words with optional internal hyphens
		| \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
		| \.\.\.            # ellipsis
		| [][.,;"'?():-_`]  # these are separate tokens
		'''

stop_word = nltk.corpus.stopwords.words('english')


def is_word(string):
	i = 0
	for s in string:
		if s.isalpha():
			return True
		else:
			i = i +1
	if i == len(string):
		return False



def get_doc_index(file_name):
	in_put = open(file_name, 'rU')
	raw = in_put.readlines()

	#保留有摘要的paper 序号
	paper_id = [raw.index(w) for w in raw if w != 'null\n']

	return paper_id


def get_docs(file_name):
	in_put = open(file_name, 'rU')
	raw = in_put.readlines()

	#保留有摘要的paper 序号
	paper_id = [raw.index(w) for w in raw if w != 'null\n']
	raw = [w.lower() for w in raw if w != 'null\n']

	docs = [nltk.regexp_tokenize(w, pattern) for w in raw]

	#只保留英文单词,有-的会被删掉,删除停用词
	for i in range(len(docs)):
		docs[i] = [w for w in docs[i] if is_word(w) and not w in stop_word]

	wnl = nltk.WordNetLemmatizer()

	#词形还原
	for i in range(len(docs)):
		docs[i] = [wnl.lemmatize(t) for t in docs[i]]

	in_put.close()

	return docs

def output_vocab(in_file_name, out_file_name):
	docs = get_docs(in_file_name)

	out_put = open(out_file_name, 'w')

	#统计所有文档词汇
	words = []
	for w in docs:
		words += w

	vocab = list(set(words))

	for w in vocab:
		out_put.write(w + "\n")

	out_put.close()


def get_dwmatrix(abstraction_file_name, vocab_file_name):
	docs = get_docs(abstraction_file_name)

	#统计所有文档词汇
	words = []
	for w in docs:
		words += w

	vocab = list(set(words))

	out_put = open(vocab_file_name, 'w')

	for w in vocab:
		out_put.write(w + "\n")

	out_put.close()

	#统计词频
	freq_list = [FreqDist(doc) for doc in docs]

	#建文档 单词矩阵
	matrix = [[] for i in range(len(vocab))]

	for i in range(len(vocab)):
		matrix[i] = [w[vocab[i]] for w in freq_list]

	return matrix


def TF_IDF(matrix):
	vocab_number = len(matrix)
	doc_number = len(matrix[0])

	for i in range(vocab_number):
		num = doc_number - matrix[i].count(0) + 1
		matrix[i] = [w * math.log((doc_number + 1 ) * 1.0 / num ) for w in matrix[i]]

	return matrix



def output_dwmatrix(abstraction_file_name, wdmatrix_file_name, vocab_file_name):
	dw_matrix = get_dwmatrix(abstraction_file_name, vocab_file_name)

	#dw_matrix = TF_IDF(dw_matrix)

	out_put = open(wdmatrix_file_name, 'w')
	
	for w in dw_matrix:
		for i in range(len(w)):
			if i != len(w) - 1:
				out_put.write(str(w[i]) + "\t")
			else:
				out_put.write(str(w[i]) + "\n")
		#out_put.write("\n")

	out_put.close()





def main():

	abstraction_dir = 'E:\\DataSets\\Names Disambiguation\\abstract_data\\'
	data_dir = 'E:\\DataSets\\Names Disambiguation\\data\\result\\'
	title_dir = 'E:\\DataSets\\Names Disambiguation\\title_data\\'
	wdmatrix_dir = 'E:\\Project\\Intent\\data\\wdmatrix\\'
	vocab_dir = 'E:\\Project\\Intent\\data\\vocab\\'

	for (dirname, dirnames, filenames) in os.walk('E:\\DataSets\\Names Disambiguation\\abstract_data'):
		break

	#abstraction中文件和result文件中不对应，是子集
	authors = [w[:w.rfind('_')] for w in filenames]

	for w in authors:
		abstraction_file_name = abstraction_dir + w + '_abstraction.txt'
		wdmatrix_file_name = wdmatrix_dir + w + '_wdmatrix.txt'
		vocab_file_name = vocab_dir + w + '_vocab.txt'
		output_dwmatrix(abstraction_file_name, wdmatrix_file_name, vocab_file_name)


	

if __name__ == '__main__':
	main()

#porter = nltk.PorterStemmer()
#[porter.stem(t) for t in tokens]

#[wnl.lemmatize(t) for t in docs[0]]

### Local Variables: ###
### mode:python      ###
### coding:utf-8     ###
### End:             ###
