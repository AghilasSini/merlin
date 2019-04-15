import random
import argparse

def build_arg_parser():
	parser=argparse.ArgumentParser(description='parse')
	parser.add_argument('orginal_file_name',type=str,nargs=1,help='list of the file info')
	parser.add_argument('shuffled_file_name',type=str,nargs=1,help='config file')
	return parser



def main():
	args = build_arg_parser().parse_args()
	org_file_name = args.orginal_file_name[0]
	shuffled_file_name = args.shuffled_file_name[0]
	new_list=[]
	with open(org_file_name,'r') as oldfile:
		old_list=[ fl.strip() for fl in oldfile.readlines() ]
		new_list=random.sample(old_list,len(old_list))
	with open(shuffled_file_name,'w') as shuffledFile:
		[ shuffledFile.write(fl+'\n')  for fl in new_list]



if __name__=='__main__':
	main()
