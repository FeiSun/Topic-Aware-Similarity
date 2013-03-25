# -*- coding:utf-8 -*-

import os
from preprocess import *

def get_coauthor_matrix(author_file_name, author_name, abstraction_file_name, title_file_name):

	in_put = open(author_file_name, 'rU')
	raw = in_put.readlines()

	#delete number and '\t' on each line
	raw = [w[w.find('\t')+1:-1] for w in raw]
	#以','分割author

	authors_lists = [w.split(', ') for w in raw]

	#实际paper的序列是与title文件对应的
	title_file = open(title_file_name, 'rU')

	title_idx_raw = title_file.readlines()

	#得到每篇paper对应的在pid文件中的位置
	title_idx = [int(w[w.find('\t')+1:-1]) for w in title_idx_raw]

	partial_paper_index = get_doc_index(abstraction_file_name)

	#得到每个实际的paper对应的pid中的位置序号
	partial_paper_index = [title_idx[w] for w in partial_paper_index]

	#只找有摘要的那些paper的author list
	authors_lists = [authors_lists[w] for w in partial_paper_index]

	#存在有些论文author name 形式不同，所以判断了下，但是如果多篇paper用相同的不同形式，则会有问题
	#如Ajay K. Gupta 之于 Ajay Gupta
	for w in authors_lists:
		if author_name in w:
			w.remove(author_name)

	#测试发现coauthor matrix有的全为1，发现是因为有些文件中的author name与文件名的author name并不对于
	#权宜之计，对于author list 找出公共的author name作为author name，将其去掉
	author_name_al =  list(set.intersection(*map(set,authors_lists)))

	if author_name_al:
		for x in author_name_al:
			for w in authors_lists:
				if x in w:
					w.remove(x)
		


	coauthor_matrix = [[0 for col in range(len(authors_lists))] for row in range(len(authors_lists))]

	for i in range(len(authors_lists)):
		for j in range(len(authors_lists)):
			if set(authors_lists[i]).intersection(set(authors_lists[j])) or i == j:
				coauthor_matrix[i][j] = 1

	return coauthor_matrix

	in_put.close()


			
def output_camatrix(author_file_name, abstraction_file_name, title_file_name, author_name, out_file_name):

	coauthor_matrix = get_coauthor_matrix(author_file_name, author_name, abstraction_file_name, title_file_name)

	
	out_put = open(out_file_name, 'w')
	
	for w in coauthor_matrix:
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
	coauthor_dir = 'E:\\Project\\Intent\\data\\coauthor\\'

	for (dirname, dirnames, filenames) in os.walk('E:\\DataSets\\Names Disambiguation\\abstract_data'):
		break

	#abstraction中文件和result文件中不对应，是子集
	authors = [w[:w.rfind('_')] for w in filenames]


	for w in authors:
		author_file_name = data_dir + w + '_authors.txt'
		abstraction_file_name = abstraction_dir + w + '_abstraction.txt'
		title_file_name = title_dir + w + '_title.txt'
		coauthor_file_name = coauthor_dir + w + '_coauthor.txt'
		output_camatrix(author_file_name, abstraction_file_name, title_file_name, w, coauthor_file_name)



if __name__ == '__main__':
	main()