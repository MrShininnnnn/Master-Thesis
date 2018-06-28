INPUT = 'data/scopus_set.csv'
OUT = ''

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import pandas as pd
import json


class scopusAPI(object):
	"""docstring for mendeleyAPI"""
	def __init__(self):

		self.raw_df = self.inPut()

	def inPut(self): 

		return pd.read_csv(INPUT)

	def genData(self):

		raw_df = self.raw_df
		given_name_list = raw_df['given-name']
		sur_name_list = raw_df['sur_name']
		authors_list = raw_df['authors']
		for i in range(len(given_name_list)):
			authors = authors_list[i]
			g_name = given_name_list[i]
			if type(g_name) is not str:
				for item in authors.split("'"):
					if '(' not in item and ')' not in item and ',' not in item:
						print(item)
				break





		return raw_df

	def scopusID(self, scopus):

		return scopus.split('-')[-1]

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8')

def main():

	raw_data = scopusAPI().genData()
	# scopusAPI().outPut(raw_data)

if __name__ == '__main__':

	main()