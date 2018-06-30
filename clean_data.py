INPUT = 'data/raw_scopus_set_authors.csv'
OUT = 'data/cleaned_sample_set_authors.csv'

import pandas as pd

class dataClean(object):
	"""docstring for dataClean"""
	def __init__(self):
		
		self.raw_data = self.inPut()

	def inPut(self):

		return pd.read_csv(INPUT, index_col = 'id')

	def preProcess(self):

		raw_data = self.raw_data
		
		sample_size = len(raw_data.index.tolist())
		hindex_del = self.hindexCount(raw_data)
		hindex_del_index = [raw_data.index[i] for i in hindex_del]
		print(len(hindex_del_index))
		for index in hindex_del_index:
			raw_data = raw_data.drop(index)

		cit_by_doc_del = self.docCount(raw_data)
		cit_by_doc_index = [raw_data.index[i] for i in cit_by_doc_del]
		print(len(cit_by_doc_del))
		for index in cit_by_doc_index:
			raw_data = raw_data.drop(index)

		co_authors_total_del = self.coauthorsCount(raw_data)
		co_authors_total_del_index = [raw_data.index[i] for i in co_authors_total_del]
		print(len(co_authors_total_del))
		for index in co_authors_total_del_index:
			raw_data = raw_data.drop(index)		

		citedby_count_del = self.citedbyCount(raw_data)
		citedby_count_del_index = [raw_data.index[i] for i in citedby_count_del]
		print(len(citedby_count_del))
		for index in citedby_count_del_index:
			raw_data = raw_data.drop(index)

		self.outPut(raw_data)


	def hindexCount(self, df):

		return [i for i in range(len(df.index)) if str(df.h_index[i]) == '0']

	def docCount(self, df):

		return [i for i in range(len(df.index)) if str(df.cit_by_doc[i]) == '0' or int(df.cit_by_doc[i]) == 0]

	def coauthorsCount(self, df):

		return [i for i in range(len(df.index)) if str(df.co_authors_total[i]) == '0' or int(df.co_authors_total[i]) == 0]
	
	def citedbyCount(self, df):

		return [i for i in range(len(df.index)) if str(df.citedby_count[i]) == '0' or int(df.citedby_count[i]) == 0]

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	dataClean().preProcess()

if __name__ == '__main__':

	main()