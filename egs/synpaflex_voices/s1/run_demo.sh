#!/bin/bash -e

if test "$#" -ne 0; then
    echo "Usage: ./run_demo.sh"
    exit 1
fi

### Step 1: setup directories and the training data files ###
#./01_setup.sh nadine

### Step 2: prepare config files for acoustic, duration models and for synthesis ###
./04_prepare_conf_files.sh conf/global_settings.cfg

### Step 3: train duration model ###
./05_train_duration_model.sh conf/duration_nadine.conf

### Step 4: train acoustic model ###
./06_train_acoustic_model.sh conf/acoustic_nadine.conf

### Step 5: synthesize speech ###
./07_run_merlin.sh conf/test_dur_synth_nadine.conf conf/test_synth_nadine.conf 


