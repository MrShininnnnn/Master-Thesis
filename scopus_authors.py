INPUT = 'data/cleaned_sample_set_authors.csv'
OUT = 'data/cleaned_sample_set_aff.csv'

import pandas as pd
import requests, json, time
from bs4 import BeautifulSoup as bs

class scopusAPI(object):
	"""docstring for mendeleyAPI"""
	def __init__(self):

		self.raw_df = self.inPut()
		# self.scopus_raw_df = self.genName()

	def inPut(self): 

		return pd.read_csv(INPUT)

	def nanCheck(self, num):

		try:
			return str(int(num))
		except:
			return False

	def textMining(self, resp):

		affiliation = False
		doc_total = False
		cit_by_doc = False
		co_authors_total = False

		soup = bs(resp.text, 'html5lib')
		for script in soup(['script', 'style']):
			script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		
		text_join = ' '.join(chunk for chunk in chunks if chunk)
		h_index = text_join.split('View h-graph ')[-1].split(' ')[0]
		print('h_index:', h_index)
		affiliation = text_join.split('affiliation Location ')[-1].split(',')[0]
		print('affiliation:', affiliation)

		for line in text.split('\n'):
			if 'Documents' in line and 'author' not in line and 'Review' not in line and not doc_total:
				doc_total = line.split(' ')[0]
				print('doc_total: ', doc_total)
			elif 'documents' in line and 'Cited by' in line and not cit_by_doc:
				cit_by_doc = line.split(' ')[2]
				print('cit_by_doc: ', cit_by_doc)
			elif 'co-authors' in line and not co_authors_total:
				co_authors_total = line.split(' ')[0]
				print('co_authors_total: ', co_authors_total)
			else:
				pass

		if not doc_total:
			doc_total = '0'
		if not cit_by_doc:
			cit_by_doc = '0'
		if not co_authors_total:
			co_authors_total = '0'
		if not affiliation:
			affiliation = ''

		return h_index, doc_total, cit_by_doc, co_authors_total, affiliation

	def genAuthors(self):

		raw_df = self.raw_df
		author_id_list = self.raw_df['author_id'].values.tolist()

		# Load configuration
		con_file = open("config.json")
		config = json.load(con_file)
		con_file.close()

		headers = {"X-ELS-APIKey": config['apikey'], "Accept": 'application/json'}

		index = len(author_id_list)

		h_index_list = ['0'] * index
		doc_total_list = ['0'] * index
		cit_by_doc_list = ['0'] * index
		co_authors_total_list = ['0'] * index
		affiliation_list = [''] * index

		for i in range(index):
			print(i)
			author_id = self.nanCheck(author_id_list[i])
			if author_id:
				print('author_id: ', author_id)
				resp = requests.get("https://www.scopus.com/authid/detail.uri?authorId=%s" % (author_id), headers= headers)
				h_index, doc_total, cit_by_doc, co_authors_total, affiliation = self.textMining(resp)
				h_index_list[i] = h_index
				doc_total_list[i] = doc_total
				cit_by_doc_list[i] = cit_by_doc
				co_authors_total_list[i] = co_authors_total
				affiliation_list[i] = affiliation
			else:
				pass
			print('\n')

			if i % 25 == 0:
				raw_df['h_index'] = h_index_list
				raw_df['doc_total'] = doc_total_list
				raw_df['cit_by_doc'] = cit_by_doc_list
				raw_df['co_authors_total'] = co_authors_total_list
				raw_df['affiliation'] = affiliation_list
				self.outPut(raw_df)

		raw_df['h_index'] = h_index_list
		raw_df['doc_total'] = doc_total_list
		raw_df['cit_by_doc'] = cit_by_doc_list
		raw_df['co_authors_total'] = co_authors_total_list
		raw_df['affiliation'] = affiliation_list
		self.outPut(raw_df)

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	scopusAPI().genAuthors()

if __name__ == '__main__':

	main()