INPUT = 'data/scopus_set_authors.csv'
OUT = 'data/scopus_set_authors.csv'

import scholarly
import pandas as pd

class scopusAPI(object):
	"""docstring for mendeleyAPI"""
	def __init__(self):

		self.raw_df = self.inPut()
		# self.scopus_raw_df = self.genName()

	def inPut(self): 

		return pd.read_csv(INPUT)

	# def genName(self):

	# 	raw_df = self.raw_df
	# 	given_name_list = raw_df['given-name']
	# 	sur_name_list = raw_df['sur_name']
	# 	authors_list = raw_df['authors']

	# 	first_name_list = []
	# 	last_name_list = []

	# 	for i in range(len(given_name_list)):
	# 		authors = authors_list[i]
	# 		g_name = given_name_list[i]
	# 		s_name = sur_name_list[i]
	# 		if (type(g_name) is not str or type(s_name) is not str) and (type(authors) is str):
	# 			full_name = []
	# 			for item in authors.split("'"):
	# 				if '(' not in item and ')' not in item and ',' not in item:
	# 					full_name.append(item)
	# 			first_name_list.append(full_name[0])
	# 			last_name_list.append(full_name[-1])
	# 		else:
	# 			first_name_list.append(g_name)
	# 			last_name_list.append(s_name)

	# 	raw_df['given-name'] = first_name_list
	# 	raw_df['sur_name'] = last_name_list

	# 	return raw_df

	# def scopusID(self, scopus):

	# 	return scopus.split('-')[-1]

	def genAuthors(self):

		raw_df = self.raw_df
		first_name_list = raw_df['given-name'].values.tolist()
		last_name_list = raw_df['sur_name'].values.tolist()

		affiliation_list = raw_df['author_affiliation'].values.tolist()
		author_citeby_list = raw_df['author_citeby'].values.tolist()
		email_list = raw_df['author_email'].values.tolist()

		full_name = '%s, %s' % (first_name_list[1], last_name_list[1])
		print(full_name)
		author_data = self.genScholars(full_name)
		search_query = scholarly.search_author(full_name)
		print(next(search_query))


		# for i in range(len(first_name_list)):
		# 	full_name = '%s, %s' % (first_name_list[i], last_name_list[i])
		# 	if affiliation_list[i] == 0:
		# 		# 'affiliation', 'citedby', 'email'
		# 		author_data = self.genScholars(full_name)
		# 		if author_data:
		# 			if hasattr(author_data, 'affiliation'):
		# 				affiliation_list[i] = author_data.affiliation
		# 			else:
		# 				affiliation_list[i] = ''
		# 			if hasattr(author_data, 'citedby'):
		# 				author_citeby_list[i] = author_data.citedby
		# 			else:
		# 				affiliation_list[i] = ''
		# 			if hasattr(author_data, 'email'):
		# 				email_list[i] = author_data.email
		# 			else:
		# 				email_list[i] = ''
		# 		else:
		# 			affiliation_list[i] = ''
		# 			author_citeby_list[i] = ''
		# 			email_list[i] = ''
		# 	else:
		# 		pass

		# 	raw_df['author_affiliation'] = affiliation_list
		# 	raw_df['author_citeby'] = author_citeby_list
		# 	raw_df['author_email'] = email_list

		# 	if i % 10 == 0:
		# 		scopusAPI().outPut(raw_df)
		# 	else:
		# 		pass

		# 	print(i)

		# scopusAPI().outPut(raw_df)

	def genScholars(self, full_name):

		search_query = scholarly.search_author(full_name)
		try:
			return next(search_query)
		except:
			return False

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8')

def main():

	scopusAPI().genAuthors()

if __name__ == '__main__':

	main()