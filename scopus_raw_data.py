INPUT = 'data/mendeley_set.csv'
OUT = 'data/scopus_set.csv'

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
		scopus_list = raw_df['scopus']
		# Load configuration
		con_file = open("config.json")
		config = json.load(con_file)
		con_file.close()
		# Initialize client
		client = ElsClient(config['apikey'])

		author_id_list = []
		given_name_list = []
		sur_name_list = []
		affiliation_id_list = []
		affiliation_city_list = []
		affilname_list = []
		affiliation_country_list = []
		citedby_count_list = []

		for scopus_id in scopus_list:
			print(len(author_id_list))
			# Initialize document with Scopus ID.
			print(scopus_id)
			if type(scopus_id) is str:
				scopus_id = self.scopusID(scopus_id)
				# ['client', 'data', 'id', 'int_id', 'read', 'title', 'uri', 'write']
				scp_doc = AbsDoc(scp_id = scopus_id)
				if scp_doc.read(client):

					# dict_keys(['coredata'])
					# dict_keys(['srctype', 'prism:issueIdentifier', 'eid', 'prism:coverDate', 'prism:aggregationType', 'prism:url', 'subtypeDescription', 'dc:creator', 'link', 'prism:publicationName', 'source-id', 'citedby-count', 'prism:volume', 'subtype', 'prism:pageRange', 'dc:title', 'prism:endingPage', 'openaccess', 'openaccessFlag', 'prism:doi', 'prism:issn', 'prism:startingPage', 'dc:identifier'])
					# dict_keys(['ce:given-name', 'preferred-name', '@seq', 'ce:initials', '@_fa', 'affiliation', 'ce:surname', '@auid', 'author-url', 'ce:indexed-name'])
					if 'dc:creator' in scp_doc.data['coredata'].keys():					
						if 'ce:given-name' in scp_doc.data['coredata']['dc:creator']['author'][0].keys():
							given_name_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['ce:given-name'])
						else:
							given_name_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['preferred-name']['ce:given-name'])

						if 'affiliation' in scp_doc.data['coredata']['dc:creator']['author'][0].keys():
							# print(type(scp_doc.data['coredata']['dc:creator']['author'][0]['affiliation']))
							if type(scp_doc.data['coredata']['dc:creator']['author'][0]['affiliation']) is list:
								affiliation_id_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['affiliation'][0]['@id'])
							else:
								affiliation_id_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['affiliation']['@id'])
						else:
							affiliation_id_list.append('NA')
						author_id_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['@auid'])
						sur_name_list.append(scp_doc.data['coredata']['dc:creator']['author'][0]['ce:surname'])
					else:
						given_name_list.append('NA')
						sur_name_list.append('NA')
						author_id_list.append('NA')
						affiliation_id_list.append('NA')
					citedby_count_list.append(scp_doc.data['coredata']['citedby-count'])
				else: 
					given_name_list.append('NA')
					sur_name_list.append('NA')
					author_id_list.append('NA')
					affiliation_id_list.append('NA')
					citedby_count_list.append('NA')
			else:
				given_name_list.append('NA')
				sur_name_list.append('NA')
				author_id_list.append('NA')
				affiliation_id_list.append('NA')
				citedby_count_list.append('NA')

		raw_df['given-name'] = given_name_list
		raw_df['sur_name'] = sur_name_list
		raw_df['author_id'] = author_id_list
		raw_df['affiliation_id'] = affiliation_id_list
		raw_df['citedby_count'] = citedby_count_list

		return raw_df

	def scopusID(self, scopus):

		return scopus.split('-')[-1]

	def outPut(self, out_df):

		out_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	raw_data = scopusAPI().genData()
	scopusAPI().outPut(raw_data)

if __name__ == '__main__':

	main()