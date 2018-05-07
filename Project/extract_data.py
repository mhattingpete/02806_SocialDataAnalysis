import pandas as pd

if __name__ == '__main__':
	saveAs = "processed_data.csv"
	d = pd.read_csv("samlede_socio_data_kbh.csv")
	columns = ["v_id","rode_nr","aar",
	"alder_pct_0_5","alder_pct_6_17","alder_pct_18_29","alder_pct_30_39","alder_pct_40_49","alder_pct_50_64","alder_pct_over_65",
	"pct_tilkn_arb_markedet",
	"pct_gymnasial_udd","pct_erh_faglig_udd","pct_kort_viderg_udd","pct_mellemlang_viderg_udd","pct_lang_viderg_udd","pct_ingen_udd","pct_under_udd",
	"pct__ivaerksaettere","pct__lonmodtagere",
	"pct_lav_indkomst","pct_middel_indkomst","pct_hoj_indkomst",
	"pct_enlige_u_born","pct_enlige_m_born","pct_par_u_born","pct_par_m_born"]
	df = d[columns]
	del d
	df.to_csv(saveAs,columns=columns)