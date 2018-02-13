import numpy as np
import json

def processData(filename):
	data = dict()
	labels = dict()
	with open(filename,'r') as f:
		for i,l in enumerate(f):
			if i == 0:
				l = l[:-1]
				s = l.split(',')
				for i,k in enumerate(s):
					data[k] = []
					labels[i] = k
			else:
				l = l[:-1]
				s = l.split(',')
				for i in labels:
					if 'nr' == labels[i] or 'months' == labels[i]:
						data[labels[i]].append(int(s[i]))
					else:
						data[labels[i]].append(s[i])
	hist,bin_edges = np.histogram(data['months'],bins=20)
	result = {'counts':hist.tolist(),'edges':bin_edges[1:].tolist()}
	with open('hist_president.csv','w') as out:
		s = ','.join(result.keys())+'\n'
		out.write(s)
		for i in range(len(result['counts'])):
			s = ','.join([str(result['counts'][i]),str(result['edges'][i])])+'\n'
			out.write(s)

if __name__ == '__main__':
	processData('president.csv')