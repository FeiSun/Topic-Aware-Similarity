# -*- coding:utf-8 -*-


def purity(doc_topic_file_name, classify_file_name):
	in_put = open(doc_topic_file_name, 'rU')

	raw = in_put.readlines()

	doc_topic = raw[0][:-1].split('\t')

	doc_topic = [int(w) for w in doc_topic]

	topic = list(set(doc_topic))


	topic_doc = []

	for w in topic:
		temp = [i for i, x in enumerate(doc_topic) if x == w]
		topic_doc.extend([temp])



	in_put1 = open(classify_file_name, 'rU')

	truth_raw = in_put1.readlines()

	truth_author_doc = [w[:-1] for w in truth_raw]

	truth_author_doc = [w.split('\t') for w in truth_author_doc]

	for i in range(len(truth_author_doc)):
		truth_author_doc[i] = [int(w) for w in truth_author_doc[i]]


	topic_doc_intersection = []

	for w in topic_doc:
		temp = [len(set.intersection(set(w),set(x))) for x in truth_author_doc]
		topic_doc_intersection.extend([temp])

	sum = 0
	for w in topic_doc_intersection:
		sum = sum + max(w)

	purity = 1.0 * sum / len(doc_topic)

	return purity



def main():

	purity_dir = './purity/'
	PLSA_purity_dir = './PLSA purity/'
	classify_dir = '../data/classify/'

	author_file = open('../data/authors.txt', 'rU')
	authors = author_file.readlines()

	authors = [w[:-1] for w in authors]

	result = []

	for x in authors:
		#PLSA_purity_file_name = PLSA_purity_dir + x + '_maxtopic.txt'
		purity_file_name = purity_dir + x + '_maxtopic.txt'
		classify_file_name = classify_dir + x + '_classify.txt'

		result.append(purity(purity_file_name, classify_file_name))


	out_put = open('./purity.txt', 'w')

	for x in result:
		out_put.write(str(x) + "\n")


	author_file.close()
	out_put.close()




if __name__ == '__main__':
        main()
