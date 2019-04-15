import os
import random
import pandas as pd
import argparse 
import numpy as np

def build_arg_parser():
    parser=argparse.ArgumentParser(description='parse')
    parser.add_argument('file_list_inf',type=str,nargs=1,help='list of the file info')
    parser.add_argument('meta_config',type=str,nargs=1,help='config file')
    return parser



def main():
	args = build_arg_parser().parse_args()
	input_file_list = args.file_list_inf[0]
	meta_config = args.meta_config[0]
	input_data = pd.read_csv(input_file_list,sep=';') 
	data_size=np.floor(np.sum(input_data.iloc[:,1].values)*1000)/1000.0
	train_size = 0.8*data_size
	sum_train = 0.0
	train_file_list=[]
	test_file_list=[]
	for idx,file_name in enumerate(input_data.iloc[:,0]):
		if sum_train>=train_size:
			test_file_list.append(file_name)
		else:
			sum_train+=input_data.iloc[idx,1]
			train_file_list.append(file_name)

	ntrain_set= len(train_file_list)
	if len(test_file_list)%2!=0:
		nval_set =(len(test_file_list)//2)+1
		ntest_set =len(test_file_list)//2
	else:
		nval_set =len(test_file_list)//2
		ntest_set =len(test_file_list)//2
	with open(meta_config,'w') as fn:
		fn.write('{};{};{}\n'.format(ntrain_set+1,nval_set,ntest_set))


if __name__ == '__main__':
	main()



