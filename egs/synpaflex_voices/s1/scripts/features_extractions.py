from scipy import interpolate
import numpy
import sys
import glob
import argparse
import os
import roots
# 1 do interpolation  using spline ibterpolation algorithm
# 2 extraction
# 3 save
# Id;F0mean; F0range; F010% F030% F050% F070% F090%;LogEnergyAverage
#;LogEnergyRange;LogEnergy10% ;LogEnergy30% ;LogEnergy50% ;LogEnergy70%
#;LogEnergy90%;MeanArticulationRate;DeviationArticulationRate;BreathGroupDuration;
#PreviousPauseDuration;NextPauseDuration
FEATURES=["Id","Start","End","F0mean","F0range", "F010%", 
		"F030%", "F050%","F070%","F090%",
		"LogEnergyAverage","LogEnergyRange","LogEnergy10%",
		"LogEnergy30%" ,"LogEnergy50%" ,"LogEnergy70%","LogEnergy90%",
		"MeanArticulationRate","DeviationArticulationRate",
		"BreathGroupDuration","PreviousPauseDuration","NextPauseDuration"]






def interpotation(value,vowel_time_steps,vowel_values):
   tck = interpolate.splrep(vowel_time_steps, vowel_values)
   return interpolate.splev(value, tck)

def build_args():
	parser=argparse.ArgumentParser(description='')
	parser.add_argument('datadir', type=str, nargs=1, help='data directory')
	parser.add_argument('filelist', type=str, nargs=1, help='file list')
	return parser.parse_args()

def get_file_list(datadir,filelist,ext='_syl.json'):
	with open(filelist,'r') as fl:
		return [ os.path.join(datadir,fn+ext)for fn in fl.readlines()]



def main():
	args=build_args()
	datadir=args.datadir[0]
	filelist=args.filelist[0]
	corpusFileList=get_file_list(datadir,filelist)
	for rootsFilename in corpusFileList:
		corpus=roots.Corpus()
		corpus.load(rootsFilename)
		nutts=corpus.utterance_count()
		=corpus.get_utterances(0,nutts)

if __name__ == '__main__':
	main()


print(f(1.25))