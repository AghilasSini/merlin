import pandas
import numpy
import argparse
import codecs
import warnings


import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def build_args():
    parser=argparse.ArgumentParser(description='Significance Differance')
    parser.add_argument('dataFn',type=str,nargs=1,help='data filename ')
    return parser.parse_args()




def main():
    dataFilename=build_args().dataFn[0]
    dataFrame=pandas.read_csv(dataFilename)
    dataFrame=dataFrame.fillna(0)
    utts_epoch_id=[ str(utt).replace('_arctic','') for utt in dataFrame.iloc[:,0]]
    max_size=dataFrame.shape[0]
    utt2v = dataFrame.iloc[:,1:].values
    #pretty_plot(utt2v,utts_epoch_id,out_plot_name='file_name')
    use_tensorflow_tensorboard4project('tensorboard',utt2v,utts_epoch_id,max_size)


def pretty_plot(data_set,data_set_labels,out_plot_name):
    # PCA
    pca = PCA(n_components=4)
    data = pca.fit_transform(data_set)
    print(type(data))
    labels=data_set_labels

    plt.subplots_adjust(bottom = 0.5)
    plt.scatter(data[:, 0], data[:, 1], marker='o', c=data[:, 2], s=data[:, 3] * 100,cmap=plt.get_cmap('Spectral'))
    for label, x, y in zip(labels, data[:, 0], data[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-30, 30),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    plt.show()

def use_tensorflow_tensorboard4project(log_dir_name,data_set,data_set_labels,max_size):
    path=log_dir_name
    with codecs.open(path+"/metadata.tsv",'w+','utf-8') as fmeta:
        fmeta.write('utt_name\tspeaker_name\n')
        for utt in data_set_labels:
            speaker_name=utt.split('_')[0]
            fmeta.write('{}\t{}\n'.format(utt,speaker_name))
    sess = tf.InteractiveSession()
    with tf.device('/cpu:0'):
         embedding = tf.Variable(data_set,trainable=False, name='embedding')
    tf.global_variables_initializer().run()
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
