# -*- coding:utf-8 -*-

import os
from preprocess import *

def get_ground_truth(truth_file_name, paper_id_file_name, title_file_name, abstraction_file_name, classify_file_name):

	truth_file = open(truth_file_name, 'rU')

	truth_raw = truth_file.readlines()[1:]

	#数据中存在多余空格
	#ground truth文件最后一个没有回车
	for i in range(len(truth_raw)):
		if i != len(truth_raw) - 1:
			truth_raw[i] = " ".join(truth_raw[i][truth_raw[i].find(":")+1:-1].split())
		else:
			truth_raw[i] = " ".join(truth_raw[i][truth_raw[i].find(":")+1:].split())
		

	
	truth = [w.split(' ') for w in truth_raw]


	paper_id_file = open(paper_id_file_name, 'rU')
	paper_id_raw = paper_id_file.readlines()

	paper_id = [w[:-1].split('\t') for w in paper_id_raw]

	#每篇paper id对应的文件中的行数位置
	paper_id_index = {}

	for i in range(len(paper_id)):
		paper_id_index[paper_id[i][0]] = i

	
	#实际paper的序列是与title文件对应的
	title_file = open(title_file_name, 'rU')

	title_idx_raw = title_file.readlines()

	#得到每篇paper对应的在pid文件中的位置
	title_idx = [int(w[w.find('\t')+1:-1]) for w in title_idx_raw]

	#truth中存的是每个pid中paper的位置序号
	#truth中与pid中文件也不是完全对应的，Barry Wilkinson中pid就比classify中的少
	for i in range(len(truth)):
		truth[i] = [paper_id_index[w] for w in truth[i] if paper_id_index.has_key(w)]



	partial_paper_index = get_doc_index(abstraction_file_name)

	#得到每个实际的paper对应的pid中的位置序号
	partial_paper_index = [title_idx[w] for w in partial_paper_index]

	for i in range(len(truth)):
		truth[i] = [partial_paper_index.index(w) for w in truth[i] if w in partial_paper_index]


	out_put = open(classify_file_name, 'w')

	for w in truth:
		for i in range(len(w)):
			if i != len(w) - 1:
				out_put.write(str(w[i]) + "\t")
			else:
				out_put.write(str(w[i]) + "\n")

	out_put.close()




def main():

	abstraction_dir = 'E:\\DataSets\\Names Disambiguation\\abstract_data\\'
	data_dir = 'E:\\DataSets\\Names Disambiguation\\data\\result\\'
	title_dir = 'E:\\DataSets\\Names Disambiguation\\title_data\\'
	truth_dir = 'E:\\DataSets\\Names Disambiguation\\data\\AllAnswer\\'

	classify_dir = 'E:\\Project\\Intent\\data\\classify\\'


	for (dirname, dirnames, filenames) in os.walk('E:\\DataSets\\Names Disambiguation\\abstract_data'):
		break

	#abstraction中文件和result文件中不对应，是子集
	authors = [w[:w.rfind('_')] for w in filenames]

	for w in authors:
		truth_file_name = truth_dir + w + '(classify).txt'
		abstraction_file_name = abstraction_dir + w + '_abstraction.txt'
		paper_id_file_name = data_dir + w + '_pid.txt'
		title_file_name = title_dir + w + '_title.txt'
		classify_file_name = classify_dir + w + '_classify.txt'

		get_ground_truth(truth_file_name, paper_id_file_name, title_file_name, abstraction_file_name, classify_file_name)


	

if __name__ == '__main__':
	main()
