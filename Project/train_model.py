import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def getColumns(file_name,save_as=None):
	dateparse = lambda dates: pd.datetime.strptime(dates,"%Y")
	d = pd.read_csv(file_name,parse_dates=['aar'],date_parser=dateparse)
	d = d.sort_values(["aar","rode_nr"])
	d = d.set_index("aar")
	columns = ["v_id","rode_nr",
	"alder_pct_0_5","alder_pct_6_17","alder_pct_18_29","alder_pct_30_39","alder_pct_40_49","alder_pct_50_64","alder_pct_over_65",
	"pct_gymnasial_udd","pct_erh_faglig_udd","pct_kort_viderg_udd","pct_mellemlang_viderg_udd","pct_lang_viderg_udd","pct_ingen_udd","pct_under_udd",
	"pct_lav_indkomst","pct_middel_indkomst","pct_hoj_indkomst"]
	df = d[columns]
	del d
	if save_as:
		df.to_csv(save_as,columns=columns)
	return df

def prepareData(df):
	dfTrain = df[:"2013-01-01"]
	dfPred = df.loc["2014-01-01"]
	dfTrain.dropna(inplace=True)
	columns=["rode_nr",
		"alder_pct_0_5","alder_pct_6_17","alder_pct_18_29","alder_pct_30_39","alder_pct_40_49","alder_pct_50_64","alder_pct_over_65",
		"pct_gymnasial_udd","pct_erh_faglig_udd","pct_kort_viderg_udd","pct_mellemlang_viderg_udd","pct_lang_viderg_udd","pct_ingen_udd","pct_under_udd"]
	y = dfTrain.as_matrix(columns=["avg_income_level"]).ravel()
	X = dfTrain.as_matrix(columns=columns)
	y_test = dfPred.as_matrix(columns=["avg_income_level"]).ravel()
	X_test = dfPred.as_matrix(columns=columns)
	X_train, X_eval, y_train, y_eval = train_test_split(X,y,train_size=0.6)
	return X_train,y_train,X_eval,y_eval,X_test,y_test

def trainModel(X_train,y_train,X_eval,y_eval):
	model = RandomForestRegressor(n_estimators=5)
	model.fit(X_train,y_train)
	print("Train Score {}".format(model.score(X_train,y_train)))
	print("Eval Score {}".format(model.score(X_eval,y_eval)))
	return model

def predict(model,X_test):
	return model.predict(X_test)