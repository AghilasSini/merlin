#generate csv
outdir=${1}
file_id_list=${2}
indir_lab=${3}
csv=1
emb=0

if [ $csv -ne "0" ];then
	for fl in `cat $file_id_list`;do
		echo $fl
	done
fi

