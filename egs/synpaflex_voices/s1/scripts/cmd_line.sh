
data_dir=/vrac/asini/workspace/merlin_install/merlin/egs/synpaflex_voices/s1/experiments/synpaflex_mulit_spk_v0/acoustic_model/data

#1
python add_extra_feat.py ${data_dir}/ffr0001_mmebovary.txt ${data_dir}/label_phone_align ${data_dir}/FFR0001_LVPG_0001_0049_0093_extra.txt ${data_dir}/profile

# 2
python add_extra_feat.py ${data_dir}/ffr0009_boule.txt ${data_dir}/label_phone_align ${data_dir}/FFR0009_LVGP_XXXX_YYYY_ZZZZ_syl.txt ${data_dir}/profile
 
# 3
python add_extra_feat.py ${data_dir}/ffr0011_comtesse.txt ${data_dir}/label_phone_align ${data_dir}/FFR0011_LAWS_XXXX_YYYY_ZZZ.txt ${data_dir}/profile
 
# 4
python add_extra_feat.py ${data_dir}/ffr0012_boule.txt ${data_dir}/label_phone_align ${data_dir}/FFR0012_LAWS_0001_0049_0093_ext.txt ${data_dir}/profile

#5
python add_extra_feat.py ${data_dir}/ffr0012_mmebovary.txt ${data_dir}/label_phone_align ${data_dir}/FFR0012_LAWS_XXXX_YYYY_ZZZZ_syl.txt ${data_dir}/profile
 

#6
python add_extra_feat.py ${data_dir}/mfr0002_caglio.txt ${data_dir}/label_phone_align ${data_dir}/MFR0002_LAWS_0001_0016_0022_ext.txt ${data_dir}/profile

#7
python add_extra_feat.py ${data_dir}/mfr0008_notaire.txt ${data_dir}/label_phone_align ${data_dir}/MFR0008_LVPG_0001_0046_0087.txt ${data_dir}/profile

#8 
python add_extra_feat.py ${data_dir}/mfr0013_caglio.txt ${data_dir}/label_phone_align ${data_dir}/MFR0013_LAWS_0001_0016_0022_ext.txt ${data_dir}/profile

#9 
python add_extra_feat.py ${data_dir}/mfr0013_comtesse.txt ${data_dir}/label_phone_align ${data_dir}/MFR0013_LAWS_XXXX_YYYY_ZZZ.txt ${data_dir}/profile

#10
python add_extra_feat.py ${data_dir}/mfr0014_comtesse.txt ${data_dir}/label_phone_align ${data_dir}/MFR0014_LAWS_0001_0046_0087.txt ${data_dir}/profile

#11
python add_extra_feat.py ${data_dir}/mfr0014_notaire.txt ${data_dir}/label_phone_align ${data_dir}/MFR0014_LAWS_XXXX_YYYY_ZZZ.txt ${data_dir}/profile

#12
python add_extra_feat.py ${data_dir}/mfr0015_boule.txt ${data_dir}/label_phone_align ${data_dir}/MFR0015_LAWS_XXXX_YYYY_ZZZZ_syl.txt ${data_dir}/profile
 
















