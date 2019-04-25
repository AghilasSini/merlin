
# -*- coding: utf-8 -*-
"""
Extract features 
"""


import sys;
import os;
import argparse;
import matplotlib;
#matplotlib.style.use('ggplot')
import pandas as pd;
import re;
import distutils.dir_util;
import shutil;

#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../lib")

import roots

import math 
import codecs
import numpy as np

from collections import OrderedDict
from scipy import interpolate


class DialProp(object):
	def __init__(self,brg,seq_name_dict):
		self.brg=brg
		self.seq_name_dict=seq_name_dict
		self.energy_values={}
		self.f0_values={}
		self.get_vowel_time_position()

	# breath group properties
	def get_breath_group_id(self):
		position='0'
		if self.brg.is_first_in_sequence () and self.brg.is_last_in_sequence ():
				#only of breath group
				position= '-1'
		elif self.brg.is_first_in_sequence ():
				#the first breath group
				position= '0'
		elif self.brg.is_last_in_sequence ():
				# the last breath group
				position= '1'
		else:
				# in the midle
				position= '2'
		return position


	def get_vowel_time_position(self):
		phonemes = self.brg.get_related_items(self.seq_name_dict['pho'])
		pos_vowels_values=[]
		f0_vowels_values=[]
		energy_vowels_values=[]
		
		offset_brg=self.get_breath_group_start()
		dur_brg=self.get_breath_group_duration()
		for phone in phonemes:
			phoneIpa=phone.as_phonology_Phoneme().get_ipa()
			if phoneIpa.is_vowel():
				phone_seg=phone.get_related_items(self.seq_name_dict['seg'])
				phone_duration=sum([seg.as_acoustic_TimeSegment().get_segment_duration() for seg in phone_seg])
				pos_vowels_values.append(phone_seg[0].as_acoustic_TimeSegment().get_segment_start()+(phone_duration/2))
				energy_vowels_values.append(phone.get_related_items(self.seq_name_dict['pho_energy'])[0].to_string())
				f0_vowels_values.append(np.mean([ float(val) for val in phone.get_related_items(self.seq_name_dict['f0_seq'])]))

		for per in [.1,.3,.5,.7,.9]:
	    	value=offset_brg+per*dur_brg
	    	self.energy_values[per]=interpoteur(pos_vowels_values,energy_vowels_values,value)
	    	self.f0_values[per]=interpoteur(pos_vowels_values,f0_vowels_values,value)


	def get_breath_group_f010():
		return self.f0_values[.1]

	def get_breath_group_f030():
		return self.f0_values[.3]
		
	def get_breath_group_f050():
		return self.f0_values[.5]

	def get_breath_group_f070():
		return self.f0_values[.7]

	def get_breath_group_f090():
		return self.f0_values[.9]	


	def get_breath_group_ene10():
		return self.energy_values[.1]

	def get_breath_group_ene30():
		return self.energy_values[.3]

	
	def get_breath_group_ene50():
		return self.energy_values[.5]


	def get_breath_group_ene70():
		return self.energy_values[.7]


	def get_breath_group_ene90():
		return self.energy_values[.9]
	





	def get_breath_group_start(self):
		return self.brg.get_related_items(self.seq_name_dict['seg'])[0].as_acoustic_TimeSegment().get_segment_start()

	def get_breath_group_end(self):
		return self.brg.get_related_items(self.seq_name_dict['seg'])[-1].as_acoustic_TimeSegment().get_segment_end()

	def interpoteur(vowel_time_steps,vowel_values,value):
		tck=interpolate.splrep(vowel_time_steps, vowel_values)
		return interpolate.splev(value, tck)



	def get_breath_group_type(self):
		disc_items=self.brg.get_related_items(self.seq_name_dict['disc'])
		if len(disc_items)>0:
			
			return 'direct'#disc_items[0].to_string(-1).split('/')[0]
		else:
			return 'narr'

	def get_breath_group_nbr_word(self):
		return str(len(self.brg.get_related_items(self.seq_name_dict['wrd'])))


	def get_breath_group_nbr_syllable(self):
		return str(len(self.brg.get_related_items(self.seq_name_dict['syl'])))

	#def get_breath_group_average_duration(self):
		

	def get_breath_group_nbr_vowel(self):
		phonemes = self.brg.get_related_items(self.seq_name_dict['pho'])
		nbr_vowel = 0
		for phone in phonemes:
			phoneIpa=phone.as_phonology_Phoneme().get_ipa()
			if phoneIpa.is_vowel():
				nbr_vowel+=1
		return str(nbr_vowel)

	def get_breath_group_duration(self):
		segs = self.brg.get_related_items(self.seq_name_dict['seg'])
		duration=0.0
		for seg in segs:
			duration+=seg.as_acoustic_TimeSegment().get_segment_duration()
		return str(math.floor(duration*1000)/1000)

	def get_breath_group_f0range(self):
		f0_range_items=self.brg.get_related_items(self.seq_name_dict['bgr_f0'])
		if len(f0_range_items)>0:
			return str(math.floor(float(f0_range_items[0].to_string(-1))*1000)/1000)
		else:
			return 'x'

	def get_breath_group_rate(self):
		rate_items=self.brg.get_related_items(self.seq_name_dict['bgr_rate'])
		if len(rate_items)>0:
			return str(math.floor(float(rate_items[0].to_string(-1))*1000)/1000)
		else:
			return 'x'

	def get_breath_group_dur_lab(self):
		phones=self.brg.get_related_items(self.seq_name_dict['pho'])
		vowels=[0.0]
		for phone in phones:
			phone_dur_label=phone.get_related_items(self.seq_name_dict['pho_dur'])
			phoneme_ipa = phone.as_phonology_Phoneme().get_ipa()
			if phoneme_ipa.is_vowel() and len(phone_dur_label)>0:
				vowels.append(int(phone_dur_label[0].to_string()))   #np.median(get_f0(phone)))

		return str(np.median(vowels))

	def get_breath_group_energy(self):
		phones=self.brg.get_related_items(self.seq_name_dict['pho'])
		vowels=[0.0]
		for phone in phones:
			phone_dur_label=phone.get_related_items(self.seq_name_dict['pho_energy'])
			phoneme_ipa = phone.as_phonology_Phoneme().get_ipa()
			if phoneme_ipa.is_vowel() and len(phone_dur_label)>0:
				vowels.append(float(phone_dur_label[0].to_string()))   #np.median(get_f0(phone)))

		return str(np.median(vowels))


class BreathGroupProp(object):
	def __init__(self):
		self.features =OrderedDict([
		('id',"get_breath_group_id"),
		('beg',"get_breath_group_start"),
		('end',"get_breath_group_end"),	
		('range', "get_breath_group_f0range"),
		('f010%', "get_breath_group_f010"),
		('f030%', "get_breath_group_f030"),
		('f050%', "get_breath_group_f050"),
		('f070%', "get_breath_group_f070"),
		('f090%', "get_breath_group_f090"),
		('energy', "get_breath_group_energy"),
		('ene10%', "get_breath_group_ene10"),
		('ene30%', "get_breath_group_ene50"),
		('ene50%', "get_breath_group_ene70"),
		('ene70%', "get_breath_group_ene90"),
		('ene90%', "get_breath_group_ene90"),
		('rate' , "get_breath_group_rate"),
		('dur',"get_breath_group_duration")
		
		])
		self.data=OrderedDict()

	def extract_features(self, dp):
		#very use full tric
		for key in self.features.keys():
			method = self.features[key]
			self.data[key] = getattr(dp, method)()

	def get_feature(self, feature_name):
		return self.data[feature_name]

	def get_features_keys(self):
		return self.features.keys()


def is_all_seq_valid(utt,seq_name_dict):
	for nseq in seq_name_dict.values():
		if not utt.is_valid_sequence(nseq):
			print('{} doesnt exists '.format(nseq))
			sys.exit(-1)


def get_number_vowels(brg,phone_seq)
		phonemes = brg.get_related_items(phone_seq)
		nbr_vowel = 0
		for phone in phonemes:
			phoneIpa=phone.as_phonology_Phoneme().get_ipa()
			if phoneIpa.is_vowel():
				nbr_vowel+=1
		return str(nbr_vowel)



def get_properties(utt,speaker_name,seq_name_dict):
	phrases = utt.get_sequence(seq_name_dict['bgr']).as_symbol_sequence().get_all_items()
	#is_all_seq_valid(utt,seq_name_dict)
	segs= utt.get_sequence(seq_name_dict['seg'])
	brgs=[]
	forward_pause=[]
	backward_pause=[]
	for phrase in phrases:
		is_long_sil=False
		long_enough=False
		isegs=phrase.get_related_indices(seq_name_dict['seg'])
		words=phrase.get_related_items(seq_name_dict['wrd'])
		numVowel=get_number_vowels(phrase,seq_name_dict['pho'])
		if len(isegs)>0 and len(words)>0 and numVowel>2:

			first_seg=segs.get_item(isegs[0]-1).as_acoustic_TimeSegment()
			last_seg=segs.get_item(isegs[-1]+1).as_acoustic_TimeSegment()
			# is it pause or not
			is_first_nss=len(first_seg.get_related_items('NSS JTrans'))
			is_last_nss=len(last_seg.get_related_items('NSS JTrans'))

			if is_first_nss>0 and is_last_nss>0:
				is_long_sil=True

			if first_seg.get_segment_duration()>0.1 and last_seg.get_segment_duration() >0.1 :
				long_enough=True

			if long_enough and is_long_sil:
				brgs.append(phrase)
				forward_pause.append(last_seg.get_segment_duration())
				backward_pause.append(first_seg.get_segment_duration())
				#ibrgs.append(last_seg.get_segment_duration())
			else:
				pass
			
	
	for bbg,fbg,bgr in zip(backward_pause,forward_pause,brgs):
		breath_group_dict=OrderedDict()
		dp = DialProp(bgr,seq_name_dict)
		bgr_prop=BreathGroupProp()
		bgr_prop.extract_features(dp)
		[breath_group_dict[feat]=bgr_prop.get_feature(feat) for feat in bgr_prop.get_features_keys()]
		breath_group_dict['PreviousPauseDuration']=bbg
		breath_group_dict['NextPauseDuration']=fbg
		yield breath_group_dict
	












def build_arg_parser():
	parser=argparse.ArgumentParser(description='parse')
	parser.add_argument('in_corpus',type=str,nargs=1,help='roots corpus input file name')
	parser.add_argument('out_data',type=str,nargs=1,help='dialogue freatures  filename csv')
	parser.add_argument('--seg-seq',dest='seg_seq',default='Time Segment JTrans', help='time segment sequence')
	parser.add_argument('--nss-seq',dest='nss_seq',default='NSS JTrans', help='phonemes sequence')
	parser.add_argument('--pho-seq',dest='pho_seq',default='Phone JTrans', help='phonemes sequence')
	parser.add_argument('--pho-dur-seq',dest='pho_dur_seq',default='Phone Dur Normd', help='phonemes sequence')
	parser.add_argument('--pho-energy-seq',dest='pho_energy_seq',default='Phone Energy Mean', help='phonemes sequence')
	parser.add_argument('--syl-seq',dest='syl_seq',default='Syllable', help='syllables sequence')
	parser.add_argument('--wrd-seq',dest='wrd_seq',default='Word JTrans', help='words sequence')
	parser.add_argument('--wrd-raw-seq',dest='wrd_raw_seq',default='Word Raw', help='words raw sequence')

	parser.add_argument('--pos-seq',dest='pos_seq',default='POS Stanford', help='part of speech sequence')
	parser.add_argument('--phr-seq',dest='phr_seq',default='Breath Group', help='breath group sequence')
	parser.add_argument('--phr-f0-seq',dest='phr_f0_seq',default='Breath Group F0 Range', help='breath group sequence')
	parser.add_argument('--phr-rate-seq',dest='phr_rate_seq',default='Breath Group Artic. Rate', help='breath group sequence')
	parser.add_argument('--disc-seq',dest='disc_seq',default='Character Label', help='discourse')
	
	parser.add_argument('--sig-seq', 	dest="sign_seq", type=str, default="Signal",help='Name of the signal sequence')	
	parser.add_argument('--f0-seq', 		dest="f0_seq", 			type=str, default="F0", help='Name of the F0 sequence')
	parser.add_argument('--alphabet-name', 	dest="alphabet_name", type=str, default="sampa", help='Name of the alphabet to use')									

   # parser.add_argument('copy_dest_dir',type=str,nargs=1,help='phone label output file name (merlin)')

	return parser









def main():
	# Build the feature extractor
	args=build_arg_parser().parse_args()

	
	rootsFilename=args.in_corpus[0]


	print("Loading corpus {}...".format(args.in_corpus[0]))

	corpus = roots.Corpus()
	corpus.load(args.in_corpus[0])
	nbutts = corpus.count_utterances()
	utts = corpus.get_utterances(0, nbutts)
	print("Generate data...")
	out_dir_name=args.out_data[0]
	seq_name_dict={
	'disc':args.disc_seq,
	'bgr':args.phr_seq,
	'bgr_f0':args.phr_f0_seq,
	'bgr_rate':args.phr_rate_seq,
	'wrd':args.wrd_seq,
	'pos':args.pos_seq,
	'syl':args.syl_seq,
	'pho':args.pho_seq,
	'seg':args.seg_seq,
	'pho_dur':args.pho_dur_seq,
	'pho_energy':args.pho_energy_seq,
	'f0_seq':args.f0_seq
	}

	baseFilename=os.path.basename(rootsFilename).split('.')[0]
	outFilename=os.path.join(out_dir_name,'{}.csv'.format(baseFilename))
	brg_data_list=[]
	for iutt,utt in enumerate(utts):
		if utt.is_valid_sequence(args.sign_seq):
			# audioFn=utt.get_sequence(args.sign_seq).get_item(0).as_acoustic_SignalSegment().get_file_name()
			# speaker_name=os.path.basename(audioFn).split('_')[0]
			for bg in get_properties(utt,speaker_name,seq_name_dict):
				brg_data_list.append(bg)
	pd.DataFrame(brg_data_list).to_csv(outFilename)

	
	


if __name__ == '__main__':
	main()
