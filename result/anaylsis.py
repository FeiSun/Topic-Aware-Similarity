# -*- coding:utf-8 -*-

import string as str
import numpy as np


#doc topic matrix
def get_dzmatrix(file_name):

	dz_file = open(file_name,'rU')
	dz_raw = dz_file.readlines()

	dz_raw = [w.rstrip('\n') for w in dz_raw]

	dz_matrix = [w.split('\t') for w in dz_raw]

	#需要判断是否存在NaN，程序可能中间有错，输出的并非全是数字
	for i in range(len(dz_matrix)):
		dz_matrix[i] = [str.atof(w) for w in dz_matrix[i]]

	dz_index = [np.argsort(np.array(w)) for w in dz_matrix]
	#逆序，从大到小排序
	dz_topicindex = [w[::-1] for w in dz_index]

	return dz_topicindex


#topic word matrix
def get_zwmatrix(file_name):

	zw_file = open(file_name,'rU')
	zw_raw = zw_file.readlines()

	zw_raw = [w.rstrip('\n') for w in zw_raw]

	zw_matrix = [w.split('\t') for w in zw_raw]

	#需要判断是否存在NaN，程序可能中间有错，输出的并非全是数字
	for i in range(len(zw_matrix)):
		zw_matrix[i] = [str.atof(w) for w in zw_matrix[i]]

	zw_index = [np.argsort(np.array(w)) for w in zw_matrix]
	#逆序，从大到小排序
	zw_wordindex = [w[::-1] for w in zw_index]

	return zw_wordindex


def test(file_name):

	#读取每个doc topic文件，输出每个doc的topic代表词

	vocab_dir = 'E:\\Project\\Intent\\data\\vocab\\'

	#读取vocab
	vocab_file = open('vocab.txt','rU')
	vocab_raw = vocab_file.readlines()

	vocab = [w.rstrip('\n') for w in vocab_raw]

	dz_topicindex = get_dzmatrix(file_name)
	zw_wordindex = get_zwmatrix(file_name)


	dz_maxtopic = [w[:3] for w in dz_topicindex]
	zw_maxword = [w[:10] for w in zw_wordindex]

	doc_topic_word = []

	for i in range(len(dz_maxtopic)):
		temp = []
		for w in dz_maxtopic[i]:
			temp.extend(zw_maxword[w])
		doc_topic_word.extend([temp])


	#输出文档对应的topic词
	for i in range(len(doc_topic_word)):
		doc_topic_word[i] = [vocab[w] for w in doc_topic_word[i]]



def main():
	pass

if __name__ == '__main__':
	main()