INPUT = 'data/sample_set.csv'
OUT = 'data/mendeley_set.csv'
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

		id_list = []
		# issn_list = []
		# isbn_list = []
		# pui_list = []
		# sgr_list = []
		scopus_list = []
		doi_list = []
		# pmid_list = []
		title_list = []
		type_list = []
		year_list = []
		authors_list = []
		source_list = []
		pages_list = []
		volume_list = []
		reader_count_list = []
		link_list = []

		dois = pd.read_csv(INPUT)['doi'].tolist()
		for doi in dois:
			print(len(doi_list))
			# ['abstract', 'authors', 'chapter', 'city', 'content_type', 'day', 'edition', 'editors', 'file_attached', 'files', 'id', 'identifiers', 'institution', 'issue', 'keywords', 'link', 'month', 'pages', 'publisher', 'reader_count', 'reader_count_by_academic_status', 'reader_count_by_country', 'reader_count_by_subdiscipline', 'revision', 'series', 'source', 'title', 'type', 'volume', 'websites', 'year']
			try:
				raw_catalog = session.catalog.by_identifier(doi=doi, view='all')
			except:
				pass

			catalog_id = raw_catalog.id
			# catalog_issn = raw_catalog.identifiers['issn']
			# catalog_isbn = raw_catalog.identifiers['isbn']
			# catalog_pui = raw_catalog.identifiers['pui']
			# catalog_sgr = raw_catalog.identifiers['sgr']
			if 'scopus' in raw_catalog.identifiers.keys():
				catalog_scopus = raw_catalog.identifiers['scopus']
			else:
				catalog_scopus = 'NA'
			catalog_doi = raw_catalog.identifiers['doi']
			# catalog_pmid = raw_catalog.identifiers['pmid']
			catalog_title = raw_catalog.title
			catalog_type = raw_catalog.type
			catalog_year = raw_catalog.year
			if raw_catalog.authors:
				author = raw_catalog.authors[0]
				catalog_authors = (author.first_name, author.last_name)
			else:
				catalog_authors = 'NA'
			catalog_source = raw_catalog.source
			catalog_pages = raw_catalog.pages
			catalog_volume = raw_catalog.volume
			catalog_reader_count = raw_catalog.reader_count
			catalog_link = raw_catalog.link

			if catalog_title not in title_list:
				id_list.append(catalog_id)
				# issn_list.append(catalog_issn)
				# isbn_list.append(catalog_isbn)
				# pui_list.append(catalog_pui)
				# sgr_list.append(catalog_sgr)
				scopus_list.append(catalog_scopus)
				doi_list.append(catalog_doi)
				# pmid_list.append(catalog_pmid)
				title_list.append(catalog_title)
				type_list.append(catalog_type)
				year_list.append(catalog_year)
				authors_list.append(catalog_authors)
				source_list.append(catalog_source)
				pages_list.append(catalog_pages)
				volume_list.append(catalog_volume)
				reader_count_list.append(catalog_reader_count)
				link_list.append(catalog_link)
			else:
				pass

		catalog_df = pd.DataFrame()
		catalog_df['id'] = id_list
		# catalog_df['issn'] = issn_list
		# catalog_df['isbn'] = isbn_list
		# catalog_df['pui'] = pui_list
		# catalog_df['sgr'] = sgr_list
		catalog_df['scopus'] = scopus_list
		catalog_df['doi'] = doi_list
		# catalog_df['pmid'] = pmid_list
		catalog_df['title'] = title_list
		catalog_df['type'] = type_list
		catalog_df['year'] = year_list
		catalog_df['authors'] = authors_list
		catalog_df['source'] = source_list
		catalog_df['pages'] = pages_list
		catalog_df['volume'] = volume_list
		catalog_df['reader_count'] = reader_count_list
		catalog_df['link'] = link_list

		return catalog_df

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	catalog_df = mendeleyAPI().genCatalog()
	mendeleyAPI().outPut(catalog_df)

if __name__ == '__main__':

	main()