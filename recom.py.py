
import cv2
import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import pickle
from utils import display_img

data = pd.read_pickle('pickles/clean data')

stop_words = set(nltk.corpus.stopwords.words('english'))
def nlp_preprocessing(total_text, index, column):
    if type(total_text) is not int:
        string = ""
        for words in total_text.split():
            # remove the special chars in review like '"#$@!%^&*()_+-~?>< etc.
            word = ("".join(e for e in words if e.isalnum()))
            # Conver all letters to lower-case
            word = word.lower()
            # stop-word removal
            if not word in stop_words:
                string += word + " "
        data[column][index] = string

for index, row in data.iterrows():
    nlp_preprocessing(row['title'], index, 'title')   

tfidf_title_vectorizer = TfidfVectorizer(min_df = 0)
tfidf_title_features = tfidf_title_vectorizer.fit_transform(data['title'])     

#getting word2vec for our data
with open('pickles/word2vec_model','rb') as handle:
    model=pickle.load(handle)    
 
vocab=list(model.keys())    
def build_avg_vec(sentence, num_features, doc_id):
    # sentace: its title of the apparel
    # num_features: the lenght of word2vec vector, its values = 300
    # m_name: model information it will take two values
        # if  m_name == 'avg', we will append the model[i], w2v representation of word i
        # if m_name == 'weighted', we will multiply each w2v[word] with the idf(word)

    featureVec = np.zeros((num_features,), dtype="float32")
    # we will intialize a vector of size 300 with all zeros
    # we add each word2vec(wordi) to this fetureVec
    nwords = 0
    
    for word in sentence.split():
        nwords += 1
    if  word in  tfidf_title_vectorizer.vocabulary_:
                featureVec = np.add(featureVec, tfidf_title_features[doc_id, tfidf_title_vectorizer.vocabulary_[word]] * model[word])

    if(nwords>0):
        featureVec = np.divide(featureVec, nwords)
    # returns the avg vector of given sentance, its of shape (1, 300)
    return featureVec    


w2v_title,doc_id = [],0
# for every title we build a avg vector representation
for i in data['title']:
    w2v_title.append(build_avg_vec(i, 300, doc_id))
    doc_id += 1

# w2v_title = np.array(# number of doc in courpus * 300), each row corresponds to a doc 
w2v_title = np.array(w2v_title)


def recomend(doc_id,num_result):
    pairwise_dist = pairwise_distances(w2v_title, w2v_title[doc_id].reshape(1,-1))
    #argsort will give indices of smallest dist
    indices = np.argsort(pairwise_dist.flatten())[0:num_result]
    #smallest distances
    pdists  = np.sort(pairwise_dist.flatten())[0:num_result]
    #data frame indices of the 9 smallest distace's
    df_indices = list(data.index[indices])
    for i in range(0, len(indices)):
        display_img(data['medium_image_url'].loc[df_indices[i]])
        print('ASIN :',data['asin'].loc[df_indices[i]])
        cv2.waitKey(300)
        print('BRAND :',data['brand'].loc[df_indices[i]])
        print ('euclidean distance from given input image :', pdists[i])
        print('='*125)
recomend(12566, 20)

