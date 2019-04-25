# ouput directory (egs xvector)
# file extension has the same 
# extension the output directory 
# (egs dirname: xvector ext : file_name.xvector)
# label_phone or label_state (egs file_name.lab)
# list of file that we would like to process
# input.data
##	50000 100000 21.244 ... 10.40
# file_name.lab
##	0 50000 x=x-sil+ /A:.../F:
##	...
##	80000 90000 sil=a0-t /A	
##	90000 100000 21.244 ... 10.40
# file_name.xvector
##	50000 ... 21.244 ... 10.40
##	80000 90000  21.244 ... 10.40	
##	90000 100000 21.244 ... 10.40

import numpy
import sys
import glob
import argparse
import os
import re
#import TextGrid
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from intervaltree import IntervalTree,Interval
import pandas




def build_args():
	parser=argparse.ArgumentParser(description='')
	parser.add_argument('csvFilename',type=str, nargs=1,help='input corpus file')
	parser.add_argument('labFilename',type=str, nargs=1,help='input corpus file')
	parser.add_argument('outdirname',type=str, nargs=1,help='input corpus file')
	parser.add_argument('--ext',dest='ext',default='.word2vec',type=str,help='')
	return parser.parse_args()



def get_number_fames(lab_file_name):
	fid = open(lab_file_name)
	utt_labels = fid.readlines()
	fid.close()
	label_number = len(utt_labels)
	number_lab_frames=0

	for line in utt_labels:
		line = line.strip()
		temp_list = re.split('\s+', line)
		start_time = int(temp_list[0])
		end_time = int(temp_list[1])
		frame_number = int(end_time/50000) - int(start_time/50000)
		number_lab_frames+=frame_number
	return number_lab_frames




def generate_label_file(csvFilename,max_frame,outputFilename):
	dataFrame=pandas.read_csv(csvFilename)
	utt_number_word=0
	index=0
	nfeat=dataFrame.shape[1]-4
	features=numpy.zeros((max_frame,nfeat),dtype=numpy.float32)
	for word,beg,end in dataFrame.iloc[:,1:4].values:
		number_frame=int(end/50000) - int(beg/50000)
		data=numpy.array(dataFrame.iloc[index,4:].values,dtype=numpy.float32)
		for iframe,frame in enumerate(range(number_frame)):
			if utt_number_word<max_frame:
				features[iframe,:]=data
				utt_number_word+=1
		index+=1
	features.tofile(outputFilename)
	
def main():
	args=build_args()
	
	csvFilename=args.csvFilename[0]
	labFilename=args.labFilename[0]
	outdirname= args.outdirname[0]
	ext=args.ext
	
	if not os.path.exists(outdirname):
		os.mkdir(outdirname)

	
	outputFilename=os.path.join(outdirname,os.path.basename(os.path.splitext(labFilename)[0])+ext)
	max_frame=get_number_fames(labFilename)
	
	generate_label_file(csvFilename,max_frame,outputFilename)


if __name__ == '__main__':
	main()
