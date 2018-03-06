import pandas as pd
import numpy as np

def count_crime(pathToFile,saveAs):
	# grap the columns with the borough and date info
	inF = pd.read_csv(pathToFile,usecols=['BORO_NM','RPT_DT'])
	# convert boro to category to save space
	boro = inF.BORO_NM.astype('category')
	# insert into the dataframe
	inF = inF.assign(BORO_NM=boro)
	# extract the date
	date = inF.RPT_DT
	# grap the year from the date
	date = date.str.split('/').str[2]
	# convert the date into a dataframe
	date = date.to_frame()
	# convert int64 to uint16
	date = date.apply(pd.to_numeric,downcast='unsigned')
	# insert the concerted date into the original dataframe
	inF = inF.assign(RPT_DT=date.values)
	# filter out rows, such that we only have samples from 2016
	inF = inF[(inF.RPT_DT == 2016)]
	inF = inF.assign(counts=pd.Series(np.ones(inF.shape[0]),dtype=np.int8).values)
	outF = inF.groupby('BORO_NM').sum()/inF.shape[0]
	outF.to_csv(saveAs,columns=['counts'])

if __name__ == '__main__':
	pathToFile = '/home/martin/Documents/02806-social-data-analysis/NYPD_Complaint_Data_Historic.csv'
	saveAs = 'crime_borough.csv'
	count_crime(pathToFile,saveAs)