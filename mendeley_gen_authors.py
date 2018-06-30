INPUT = 'data/mendeley_set.csv'
OUT = 'data/authors_set.csv'
KEY = 'config.yml'

from mendeley import Mendeley
import pandas as pd
import argparse
import yaml
import os

class mendeleyAPI(object):
	"""docstring for mendeleyAPI"""
	def __init__(self):

		self.raw_data = self.inPut()

	def inPut(self):

		in_pd = pd.read_csv(INPUT)
		return in_pd

	def genCatalog(self):

		config_file = KEY
		config = {}
		with open('config.yml') as f: config = yaml.load(f)
		mendeley = Mendeley(config['clientId'], config['clientSecret'])
		session = mendeley.start_client_credentials_flow().authenticate()

		catalog_df = pd.read_csv(INPUT)
		catalog_id_list = catalog_df['id'].tolist()
		c = 0
		authors_list = []
		for catalog_id in catalog_id_list:
			c+=1
			print(c)
			raw_catalog = session.catalog.get(catalog_id, view='all')
			if raw_catalog.authors:
				for author in raw_catalog.authors:
					first_name = author.first_name
					last_name = author.last_name
					name = (first_name, last_name)
					if name not in authors_list:
						authors_list.append(name)
					else:
						pass
			else:
				pass

		authors_df = pd.DataFrame()
		authors_df['author_name'] = authors_list
		return authors_df

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	authors_df = mendeleyAPI().genCatalog()
	mendeleyAPI().outPut(authors_df)

if __name__ == '__main__':

	main()