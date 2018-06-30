DATA = 'data/raw_data.txt'
OUT = 'data/sample_set.csv'
KEY = 'DOI: '
INDEX = 'doi'

import pandas as pd

class dataGeneration():

	def __init__(self):
		self.doi_list = self.doiList()

	def doiList(self):
		doi_list = []

		with open(DATA) as f:
			for line in f:
				if KEY in line:
					line = line.split(KEY)[-1]
					doi_num = line[0:-2]
					doi_list.append(doi_num)

		return doi_list

	def outPut(self):
		
		doi_list = list(set(self.doi_list))
		raw_data = {INDEX: doi_list}
		raw_data_df = pd.DataFrame(raw_data, columns=[INDEX])
		raw_data_df.to_csv(OUT, encoding = 'utf-8', index = False)

def main():

	dataGeneration().outPut()

if __name__ == '__main__':
	main()