import os
import sys
import glob
import roots
import string
import numpy
import argparse

from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from intervaltree import IntervalTree,Interval
from collections import namedtuple
import pandas
from collections import OrderedDict 

WordEmb=namedtuple('WordEmb','begSeg endSeg EmbVect')

spkear_id_mapping={'0007':'slt','0001':'awb'}




def build_args():
	parser=argparse.ArgumentParser(description='')
	parser.add_argument('corpus',type=str, nargs=1,help='input corpus file')
	parser.add_argument('w2v_model_name', type=str, nargs=1, help='output')
	parser.add_argument('outdirname', type=str, nargs=1, help='output directory')
	parser.add_argument('--seq_name',dest="seqname",default="Word",type=str,help="")
	return parser.parse_args()

def get_embedding_wordvect(word,w2vmodel,word_dict={}):
	word_trans=word.to_string()
	word_dict['word']=word_trans
	
	segs=word.get_related_items('Time Segment')
	begSeg=segs[0].as_acoustic_TimeSegment().get_segment_start()
	word_dict['begSeg']=int(begSeg/1e-7)
	
	endSeg=segs[-1].as_acoustic_TimeSegment().get_segment_end()
	word_dict['endSeg']=int(endSeg/1e-7)
	

	wordEmbVect=numpy.zeros(50)
	
	if word_trans in w2vmodel:
		wordEmbVect=w2vmodel[word_trans]
	for ival,embVal in enumerate(wordEmbVect):
		word_dict['emb_'+str(ival).zfill(3)]= embVal

def add_silence(start,end,word_dict,label='silence',word_emb=numpy.zeros(50)):
	word_dict['word']=label
	word_dict['begSeg']=start
	word_dict['endSeg']=end
	for ival,embVal in enumerate(word_emb):
		word_dict['emb_'+str(ival).zfill(3)]= embVal

def main():
	args=build_args()
	rootsFilename=args.corpus[0]
	corpus=roots.Corpus()
	corpus.load(rootsFilename)
	w2vmodel=Word2Vec.load(args.w2v_model_name[0])
	seq_name=args.seqname
	if not os.path.exists(args.outdirname[0]):
		os.mkdir(args.outdirname[0])

	nbutts=corpus.count_utterances()
	utts=corpus.get_utterances(0,nbutts)



	for iutt,utt in enumerate(utts):
		words=utt.get_sequence(seq_name).as_word_sequence().get_all_items()
		words=[word for word in words if len(word.get_related_items('Phone'))>0]
		sig_item=utt.get_sequence('Signal').get_item(0).as_acoustic_SignalSegment()
		uttFilename=sig_item.get_file_name()
		baseFilename=os.path.splitext(os.path.basename(uttFilename))[0]
		speaker_id=baseFilename.split('-')[0]
		if speaker_id in spkear_id_mapping.keys():
			speaker_name=spkear_id_mapping[speaker_id]
		uttFilename=baseFilename.replace(speaker_id+'-0001-',speaker_name+'_arctic_a')
		print(uttFilename)
		words_list=[]
		prev_seg_end=0
		for word in words:
			word_dict=OrderedDict()
			get_embedding_wordvect(word,w2vmodel,word_dict)
			if int(word_dict['begSeg'])!=prev_seg_end:
				silence_dict=OrderedDict()
				add_silence(prev_seg_end,word_dict['begSeg'],silence_dict)
				words_list.append(silence_dict)

			print(word_dict['begSeg'],word_dict['endSeg'],word_dict['word'])
			prev_seg_end=word_dict['endSeg']
			words_list.append(word_dict)
		end_utt=int(sig_item.get_segment_duration()/1e-7)
		if end_utt>prev_seg_end:
			silence_dict=OrderedDict()
			add_silence(prev_seg_end,end_utt,silence_dict)
			words_list.append(silence_dict)
		outFilename=os.path.join(args.outdirname[0],uttFilename)
		pandas.DataFrame(words_list).to_csv(outFilename+'.csv')
					
if __name__ == '__main__':
	main()
