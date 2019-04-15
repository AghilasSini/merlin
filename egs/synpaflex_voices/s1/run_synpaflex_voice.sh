#!/bin/bash

voice_name=${1}
qs_file_name=${2}
meta_inf=${3}
if test "$#" -ne 3; then
exit 1   
fi


current_working_dir=$(pwd)
voice_dataset_dir=${current_working_dir}/database/${voice_name}

if [ -d ${voice_dataset_dir} ]; then

#./01_setup.sh ${voice_name} ${qs_file_name} ${meta_inf}
experiments_dir=${current_working_dir}/experiments
voice_dir=${experiments_dir}/${voice_name}
acoustic_dir=${voice_dir}/acoustic_model
duration_dir=${voice_dir}/duration_model
synthesis_dir=${voice_dir}/test_synthesis

#./04_prepare_conf_files.sh ./conf/global_settings.cfg
cp -rf ${voice_dataset_dir}/label_phone_align ${voice_dataset_dir}/file_id_list.scp ${acoustic_dir}/data
cp -rf ${voice_dataset_dir}/label_phone_align ${voice_dataset_dir}/file_id_list.scp ${duration_dir}/data

#if [ -d ${voice_dataset_dir}/prompt-lab ] ; then
#cp -rf ${voice_dataset_dir}/prompt-lab ${voice_dataset_dir}/test_id_list.scp ${synthesis_dir}

#fi

if [ ! -d ${acoustic_dir}/data/bap ] && [ ! -d ${acoustic_dir}/data/lf0 ] && [ ! -d ${acoustic_dir}/data/mgc ] ;then
./03_prepare_acoustic_features.sh ${voice_dataset_dir}/wav  ${acoustic_dir}/data
fi

./05_train_duration_model.sh conf/duration_${voice_name}.conf
./06_train_acoustic_model.sh conf/acoustic_${voice_name}.conf
#./07_run_merlin.sh conf/test_dur_synth_${voice_name}.conf conf/test_synth_${voice_name}.conf




fi



