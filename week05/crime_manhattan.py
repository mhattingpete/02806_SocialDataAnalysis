import pandas as pd
import numpy as np
import collections
import json

def count_crime(pathToFile,saveAs):
	# grap the columns with the borough and date info
	inF = pd.read_csv(pathToFile,usecols=['BORO_NM','RPT_DT','PD_DESC'])
	# convert boro to category to save space
	boro = inF.BORO_NM.astype('category')
	# insert into the dataframe
	inF = inF.assign(BORO_NM=boro)
	inF = inF[(inF.BORO_NM == 'MANHATTAN')]
	# extract the date
	date = inF.RPT_DT
	# grap the year from the date
	date = date.str.split('/').str[2]
	# convert the date into a dataframe
	date = date.to_frame()
	# convert int64 to uint16
	date = date.apply(pd.to_numeric,downcast='unsigned')
	# insert the concerted date into the original dataframe
	inF = inF.assign(year=date.values)
	# filter out rows, such that we only have samples from 2016
	inF = inF[(inF.year == 2016)]
	#print(inF.head(n=10))
	crime = inF.PD_DESC
	crime = crime.str.split(',').str[0]
	crime = crime.str.replace(' [0-9]','')
	crime = crime.str.replace('&$','')
	crime = crime.str.replace('\s$','').astype('category')
	inF = inF.assign(PD_DESC=crime)
	inF = inF.assign(counts=pd.Series(np.ones(inF.shape[0]),dtype=np.int8).values)
	df = inF.groupby('PD_DESC').sum()
	df = df.nlargest(5,'counts')
	labels = df.index.tolist()
	inF = inF[(inF.PD_DESC == labels[0]) | (inF.PD_DESC == labels[1]) | (inF.PD_DESC == labels[2]) | (inF.PD_DESC == labels[3]) | (inF.PD_DESC == labels[4])]
	date = inF.RPT_DT.astype('category')
	inF.RPT_DT = date
	month = inF.RPT_DT
	# grap the year from the date
	month = month.str.split('/').str[0]
	# convert the date into a dataframe
	month = month.to_frame()
	# convert int64 to uint16
	month = month.apply(pd.to_numeric,downcast='unsigned')
	# insert the concerted date into the original dataframe
	inF = inF.assign(month=month.values)
	inF = inF.groupby(['PD_DESC','month']).sum()
	inF = inF[inF.year.notnull()]
	inF = inF.reset_index(level=['PD_DESC','month'])
	data = {}
	for index, row in inF.iterrows():
		key = row['month']
		if key not in data:
			d = {'month':key,row['PD_DESC']:row['counts']}
			data[key] = d
		else:
			d = data[key]
			k = row['PD_DESC']
			if k in d:
				d[k] += row['counts']
			else:
				d[k] = row['counts']
	del inF
	od = collections.OrderedDict(sorted(data.items()))
	out = open(saveAs,'w')
	out.write('[\n')
	for k,v in od.items():
		json.dump(v,out)
		out.write(',\n')
	out.write(']')
	out.close()
	
	#print(inF.info(memory_usage='deep'))
	#inF.to_csv(saveAs,columns=['counts'])
	#print(inF.head(n=10))
	#print(inF.info(memory_usage='deep'))
	#print(inF.PD_DESC.unique()

if __name__ == '__main__':
	pathToFile = '/home/martin/Documents/02806-social-data-analysis/NYPD_Complaint_Data_Historic.csv'
	saveAs = 'crime_manhattan.json'
	count_crime(pathToFile,saveAs)