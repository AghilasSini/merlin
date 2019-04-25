#
import os 
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import codecs
import pandas as pd
import argparse


def build_args():
	parser=argparse.ArgumentParser(description='')
	parser.add_argument('infile', type=str, nargs=1, help='input')
	parser.add_argument('outfile', type=str, nargs=1, help='input')
	return parser.parse_args()





def load_data(data_filename,size_emb=512):
	data={}
	with codecs.open(data_filename,'r') as df:
		for iline,line in enumerate(df.readlines()):
			spk_id=line.strip().split(' ')[0].strip()
			data[iline]=[float(value) for value in line.strip().split(' ')[3:-1]]+[spk_id]
	return pd.DataFrame.from_dict(data,orient='index',columns=['emb_{}'.format(emb_) for emb_ in range(size_emb)]+['target'])

size_emb=512

fid=build_args().infile[0]
df=load_data(fid)

# features
features = ['emb_{}'.format(emb_) for emb_ in range(size_emb)]

# Separating out the features
x = df.loc[:, features].values

# Separating out the target
y = df.loc[:,['target']].values

# Standardizing the features
scaler = StandardScaler()

# Fit on training set only.
scaler.fit(x)


# Apply transform to both the training set and the test set.
xs = scaler.transform(x)

pca = PCA(.90)
pca.fit(xs)
xs = pca.transform(xs)
print(xs.shape)


with open(build_args().infil[e0],'w') as fl:
	for sp,v in zip(y,xs):
		fl.write('{}|{}\n'.format(sp[0],';'.join([ str(x) for x in v])))
