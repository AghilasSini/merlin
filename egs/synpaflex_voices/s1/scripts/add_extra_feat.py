import numpy
import sys
import glob
import argparse
import os
import re
#import TextGrid
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
# author: asini
# date : 04/03/2019
# first example is related to speaker embedding
# a new version is comming
# just for fun
def build_args():
	parser=argparse.ArgumentParser(description='')
	parser.add_argument('file_id_list', type=str, nargs=1, help='input')
	parser.add_argument('lab_dir_path', type=str, nargs=1, help='input')
	parser.add_argument('feat_file_name', type=str, nargs=1, help='input')
        parser.add_argument('outdirname', type=str, nargs=1, help='output')
	# parser.add_argument('w2v_model_name', type=str, nargs=1, help='output')
	return parser.parse_args()

def add_extract_feat(nframes, nfeat,feat_file_name,lab_file_name,out_dir,sep=' '):
	print(lab_file_name)
	filename=os.path.basename(os.path.splitext(lab_file_name)[0])+'.profile'
	print(filename)
	full_file_name=os.path.join(out_dir,filename)
	print(full_file_name)
	features=numpy.zeros((nframes,nfeat),dtype=numpy.float32)
	with open(feat_file_name,'r') as featfn:
		data=numpy.array(featfn.readline().strip().split(sep),dtype=numpy.float32)
		for iframe in range(nframes):
			features[iframe,:]=data
		outfilename=open(full_file_name,'wb')
		features.tofile(outfilename)
		outfilename.close()

def extract_melody_feat(tier_name,tg,outfilename):
	nbrframes=0
	with open(outfilename,'w') as outf:
		for interval in tg[tier_name]:
			start_time=int(interval.xmin()*10^-7)
			end_time=int(interval.xmax()*10^-7)
			nbrframes += int(end_time/50000) - int(start_time/50000)
			for iframe in range(frame_number):
				outf.write(interval.mark()+'\n')
	return nbrframes,

def add_w2v_feat(word_tier_name,tg,outfilename,w2v_model):
	with open(outfilename,'w') as outf:
		for interval in tg[word_tier_name]:
			start_time=int(interval.xmin()/1e-7)
			end_time=int(interval.xmax()/1e-7)
			frame_number = int(end_time/50000) - int(start_time/50000)
			if interval.mark() != '#':
				for iframe in range(frame_number):
					word_emb=[]
					if interval.mark() in w2v_model:
						word_emb=w2v_model[interval.mark()]
					print('{} {} {}'.format(start_time,end_time, ' '.join(word_emb.split(','))))





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
	print(' label file:  {} has {} frames'.format(lab_file_name,number_lab_frames))

	return number_lab_frames

def main():
	args=build_args()
	file_id_list=args.file_id_list[0]
	lab_dir_path=args.lab_dir_path[0]	
	feat_file_name=args.feat_file_name[0]
	outdirname=args.outdirname[0]
	# w2v_model_name=args.w2v_model_name[0]
	nfeat=32
	# default one for now
	# w2v_model={}
	# with open(w2v_model_name,'r') as w2v:
	# 	lines=w2v.readlines()
	# 	for line in lines:
	# 		word,emb=line.strip().split('|')
	# 		w2v_model[word]=emb

	file_list_name=[os.path.join(lab_dir_path,fname.strip()) for fname in  open(file_id_list,'r').readlines() ]
	print(file_list_name)
	for lab_file_name in file_list_name:
		lab_file_name=lab_file_name+'.lab'
		nframes=get_number_fames(lab_file_name)
	# 	#tg=TextGrid.TextGrid()
	# 	#tg.read(textgridFilename)
	# 	#outfilename=os.path.join(outdirname,os.path.basename(textgridFilename).split('.')[0]+'.lab')
		add_extract_feat(nframes,nfeat,feat_file_name,lab_file_name,outdirname,sep=";")
		#add_w2v_feat("word",tg,outfilename,w2v_model)



if __name__ == '__main__':
	main()
