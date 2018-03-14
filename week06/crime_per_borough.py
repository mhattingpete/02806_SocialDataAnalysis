import pandas as pd
import numpy as np

def count_murder(pathToFile,saveAs):
	# grap the columns with the borough and date info
	inF = pd.read_csv(pathToFile,usecols=['BORO_NM','OFNS_DESC','CMPLNT_FR_DT','Latitude','Longitude','CMPLNT_FR_TM'])
	# convert boro to category to save space
	inF.BORO_NM = inF.BORO_NM.astype('category')
	# extract the date
	date = inF.CMPLNT_FR_DT
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
	time = inF.CMPLNT_FR_TM
	# grap the year from the date
	time = time.str.split(':').str[0]
	# convert the date into a dataframe
	time = time.to_frame()
	# convert int64 to uint16
	time = time.apply(pd.to_numeric,downcast='unsigned')
	# insert the concerted date into the original dataframe
	inF = inF.assign(CMPLNT_FR_TM=time.values)
	inF = inF[(inF.OFNS_DESC.str.contains('MURDER',na=False))]
	inF.to_csv(saveAs,columns=['Latitude','Longitude','CMPLNT_FR_TM','BORO_NM'])
	
if __name__ == '__main__':
	pathToFile = '/home/martin/Documents/02806-social-data-analysis/NYPD_Complaint_Data_Historic.csv'
	saveAs = 'murder_borough.csv'
	count_murder(pathToFile,saveAs)