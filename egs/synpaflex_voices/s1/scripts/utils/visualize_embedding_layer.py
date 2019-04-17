import pandas
import numpy
import argparse
import codecs
import warnings


import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector




def build_args():
    parser=argparse.ArgumentParser(description='Significance Differance')
    parser.add_argument('dataFn',type=str,nargs=1,help='data filename ')
    return parser.parse_args()




def main():
    dataFilename=build_args().dataFn[0]
    dataFrame=pandas.read_csv(dataFilename)
    dataFrame=dataFrame.fillna(0)
    utts_epoch_id=[ str(utt) for utt in dataFrame.iloc[:,0]]
    max_size=dataFrame.shape[0]
    print(max_size)
    utt2v = dataFrame.iloc[:,1:512].values
    with codecs.open("./tensorboard/metadata.tsv",'w+','utf-8') as fmeta:
        for utt in utts_epoch_id:
            fmeta.write(utt+'\n')
    print(type(utt2v))
    sess = tf.InteractiveSession()
    with tf.device('/cpu:0'):
         embedding = tf.Variable(utt2v,trainable=False, name='embedding')
    print(max_size)
    tf.global_variables_initializer().run()
    path='tensorboard'
    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(path,sess.graph)
    config = projector.ProjectorConfig()
    embed =config.embeddings.add()
    embed.tensor_name='embedding'
    embed.metadata_path ='metadata.tsv'
    projector.visualize_embeddings(writer,config)
    saver.save(sess,path+'/model.ckpt',global_step=max_size)

if __name__=='__main__':
    main()
